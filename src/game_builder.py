import os
import json
import sys
from src.models import Chapter
from src.base import Builder
from src.game_serializer import GameSerializer
from scripts.config import paths

class GameBuilder(Builder):
    """
    [Game TemplateRenderer] chapterXX.md 도메인을 직렬화하여
    templates/game.html 공통 템플릿에 GAME_DATA JSON을 바인딩 렌더링하는 
    프로젝트 유일 게임 컴파일러입니다.
    """
    
    def build(self, chapter: Chapter, grade_str: str, unit_code: str) -> bool:
        output_dir = paths.ROOT_DIR / "build" / "webapps"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 단일 공통 템플릿 로드
        template_path = paths.TEMPLATES_DIR / "game.html"
        if not template_path.exists():
            print(f"  [Error] Generic game template not found: {template_path}", file=sys.stderr)
            return False
            
        with open(template_path, 'r', encoding='utf-8') as tf:
            html_template = tf.read()
            
        # 2. GameSerializer를 활용한 도메인 객체 -> GAME_DATA JSON 직렬화
        game_data = GameSerializer.serialize(chapter, grade_str, unit_code)
        
        # 단원별 테마명 및 제한 시간 등 환경설정 보정
        theme_map = {
            "m1_04": "atlantis",
            "m1_05": "da_vinci",
            "m2_05": "da_vinci"
        }
        game_data["theme"] = theme_map.get(unit_code, "atlantis")
        
        # JSON 직렬화 수행
        game_data_json = json.dumps(game_data, ensure_ascii=False, indent=2)
        
        import base64
        # UTF-8 데이터를 안전하게 Base64로 인코딩
        game_data_base64 = base64.b64encode(game_data_json.encode('utf-8')).decode('utf-8')
        
        # 2000자씩 쪼개서 JS 결합 코드로 변환 (GAS의 단일 라인 길이 한계 우회)
        chunk_size = 2000
        chunks = [game_data_base64[i:i+chunk_size] for i in range(0, len(game_data_base64), chunk_size)]
        js_chunks = " +\n        ".join([f'"{chunk}"' for chunk in chunks])
        
        # 3. 공통 템플릿에 GAME_DATA 직렬화본 바인딩 주입 (Runtime Contract 시동)
        injection_block = f"""
    <!-- ─── GAME_DATA_INJECTION ─── -->
    <script>
        const GAME_DATA_BASE64 = {js_chunks};
        (function() {{
            if (typeof GameRuntime !== 'undefined' && typeof GAME_DATA_BASE64 !== 'undefined') {{
                // UTF-8 안전 복원용 Base64 디코딩
                const gameData = JSON.parse(decodeURIComponent(escape(atob(GAME_DATA_BASE64))));
                GameRuntime.start(gameData);
            }}
        }})();
    </script>
"""
        # </body> 직전에 인젝션 스크립트 삽입
        new_html_content = html_template.replace("</body>", f"{injection_block}\n</body>")
        
        # 4. 최종 컴파일 결과물 파일 출력
        output_file_name = f"app_{unit_code}_escape_room.html"
        output_file_path = output_dir / output_file_name
        
        try:
            with open(output_file_path, 'w', encoding='utf-8-sig') as f:
                f.write(new_html_content)
                
            # 동시에 gas/ 폴더 밑 및 서브 프로젝트 폴더 밑의 Index_{unit_code}.html 배포 복사 동조
            gas_target_dir = paths.ROOT_DIR / "gas"
            if gas_target_dir.exists():
                gas_file_name = f"Index_{unit_code}.html"
                # root gas folder
                with open(gas_target_dir / gas_file_name, 'w', encoding='utf-8-sig') as gf:
                    gf.write(new_html_content)
                
                # sub project folders (m1_project, m2_project, m3_project)
                sub_proj = f"m1_project" if "m1_" in unit_code else ("m2_project" if "m2_" in unit_code else "m3_project")
                sub_target_dir = gas_target_dir / sub_proj
                if sub_target_dir.exists():
                    with open(sub_target_dir / gas_file_name, 'w', encoding='utf-8-sig') as gsf:
                        gsf.write(new_html_content)
                    print(f"  [OK] Apps Script sub-project game deployment copied: {sub_proj}/{gas_file_name}")
                print(f"  [OK] Apps Script game deployment copied: {gas_file_name}")
                
            print(f"  [OK] Game compiled successfully: {output_file_path.name}")
            return True
        except Exception as e:
            print(f"  [Error] Failed to write game HTML: {e}", file=sys.stderr)
            return False
