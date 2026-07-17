import os
import re
from pathlib import Path
from src.models import Chapter
from src.base import Builder
from scripts.config import paths

def format_markdown_to_html(text: str) -> str:
    """마크다운의 볼드, 백틱, 리스트 문법을 인게임 사이버 네온 태그로 안전하게 치환합니다."""
    if not text:
        return ""
    
    # 1. 줄바꿈 규격화
    text = text.replace('\r\n', '\n')
    
    # 2. 마크다운 볼드 치환: **텍스트** -> 강조 네온
    text = re.sub(
        r'\*\*(.*?)\*\*', 
        r'<strong style="color: var(--primary-neon); text-shadow: var(--text-glow);">\1</strong>', 
        text
    )
    
    # 3. 마크다운 백틱 치환: `텍스트` -> 모달 인코드형 뱃지
    text = re.sub(
        r'`(.*?)`', 
        r'<code style="background: rgba(255, 255, 255, 0.08); color: var(--primary-neon); border: 1px solid var(--border-glass); padding: 2px 6px; border-radius: 4px; font-family: monospace;">\1</code>', 
        text
    )
    
    # 4. 불릿 리스트 치환: - 텍스트 -> 인게임 상태 블록 라인
    text = re.sub(
        r'^\s*-\s+(.*?)$', 
        r'<div style="margin-left: 15px; margin-bottom: 6px; color: var(--accent-neon); font-family: \'Share Tech Mono\', monospace;">▪ \1</div>', 
        text, 
        flags=re.MULTILINE
    )
    
    # 5. 인게임 캐릭터 대사 말머리 [화자]: 강조 색상 이식
    text = re.sub(
        r'\[(.*?)(?:_dyn)?\]:', 
        r'<span style="color: var(--primary-neon); font-weight: bold; text-shadow: var(--text-glow)">[\1]:</span>', 
        text
    )
    
    # 6. 줄바꿈 -> <br> 변환
    text = text.replace('\n', '<br>')
    return text

class StorybookBuilder(Builder):
    """
    [Storyboard Slider 빌더] chapterXX.md 모델을 읽어 
    좌우 2단 와이드 그리드(좌측 이미지 확대 500px) 및 Page Up/Down 키보드 기반 슬라이더 전환식
    스토리보드 뷰어 HTML을 생성합니다.
    """
    
    def build(self, chapter: Chapter, grade_str: str, unit_code: str) -> bool:
        output_dir = paths.ROOT_DIR / "build" / "storybooks"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 파일명 dynamic resolver 연동
        source_path = paths.story_path(grade_str, unit_code)
        output_file = output_dir / f"{source_path.stem}_storybook.html"
        
        # 리소스 URI/경로 매핑 (일원화된 assets/units/ 경로를 추종)
        assets_relative_path = f"../../assets/units/{unit_code}"
        
        # 단원별 테마명 보정
        theme_map = {
            "m1_04": "atlantis",
            "m1_05": "da_vinci",
            "m2_05": "da_vinci"
        }
        theme_name = theme_map.get(unit_code, "atlantis")
        
        html_content = []
        
        # HTML Header & WebApp Matching Slider CSS
        html_content.append(f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스토리보드(슬라이더): {chapter.title}</title>
    <!-- 웹앱 동일 구글 폰트 로드 -->
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700&family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --primary-neon: #00f2fe;
            --accent-neon: #4facfe;
            --danger-neon: #ef4444;
            --bg-glass: rgba(10, 25, 47, 0.7);
            --border-glass: rgba(0, 242, 254, 0.18);
            --text-glow: 0 0 10px rgba(0, 242, 254, 0.4);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
        }}

        /* ─── 단원별 웹앱 동일 테마 확장 ─── */
        body.theme-atlantis {{
            background: radial-gradient(circle at center, #0a2540 0%, #001020 100%);
            --primary-neon: #60a5fa;
            --accent-neon: #3b82f6;
            --text-glow: 0 0 10px rgba(96, 165, 250, 0.4);
        }}
        body.theme-da_vinci {{
            background: radial-gradient(circle at center, #3e2723 0%, #1a0c00 100%);
            --primary-neon: #d97706;
            --accent-neon: #f59e0b;
            --text-glow: 0 0 10px rgba(217, 119, 6, 0.4);
        }}
        body.theme-space {{
            background: radial-gradient(circle at center, #1e1b4b 0%, #030712 100%);
            --primary-neon: #a855f7;
            --accent-neon: #c084fc;
            --text-glow: 0 0 10px rgba(168, 85, 247, 0.4);
        }}

        body {{
            font-family: 'Noto Sans KR', sans-serif;
            background: #030712;
            color: var(--text-main);
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden; /* 스크롤바 감추고 씬단위 통제 */
            display: flex;
            flex-direction: column;
        }}
        
        .container {{
            max-width: 1550px;
            width: 100%;
            margin: 0 auto;
            padding: 20px;
            box-sizing: border-box;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            border-radius: 6px;
            padding: 12px 24px;
            margin-bottom: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }}
        
        .grade-tag {{
            font-family: 'Orbitron', sans-serif;
            color: var(--primary-neon);
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 0.15em;
            text-shadow: var(--text-glow);
        }}
        
        h1 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.4rem;
            margin: 0;
            font-weight: 700;
            color: #ffffff;
            text-shadow: var(--text-glow);
        }}

        /* ─── 슬라이드 카드 래퍼 및 카드 정의 ─── */
        .storyboard-viewport {{
            flex: 1;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .storyboard-card {{
            display: none; /* JS에 의해 active 상태만 block */
            grid-template-columns: 650px 1fr; /* 왼쪽 이미지 영역 대폭 확대 */
            gap: 40px;
            background: var(--bg-glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-glass);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            border-radius: 8px;
            padding: 35px;
            box-sizing: border-box;
            width: 100%;
            max-height: 80vh;
            overflow-y: auto; /* 내용이 너무 길어지면 카드 내 스크롤 */
        }}
        
        .storyboard-card.active {{
            display: grid;
        }}
        
        /* 좌측: 대형 비주얼 영역 */
        .storyboard-left {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-right: 1px dashed var(--border-glass);
            padding-right: 25px;
        }}
        
        /* 우측: 상세 내용 영역 */
        .storyboard-right {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        
        h2 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 15px;
            color: var(--primary-neon);
            text-shadow: var(--text-glow);
            border-bottom: 1px solid var(--border-glass);
            padding-bottom: 8px;
        }}
        
        .story-p {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid var(--border-glass);
            border-radius: 6px;
            padding: 16px 20px;
            font-size: 0.98rem;
            color: #e5e7eb;
            white-space: pre-line;
            line-height: 1.7;
            margin-top: 15px;
        }}
        
        /* 테이블 양식 */
        .quiz-details {{
            border-collapse: collapse;
            width: 100%;
            font-size: 0.88rem;
            margin-bottom: 15px;
            border-top: 1px solid var(--border-glass);
            border-bottom: 1px solid var(--border-glass);
        }}
        
        .quiz-details td {{
            padding: 9px 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            vertical-align: top;
            color: #e5e7eb;
        }}
        
        .quiz-details tr:last-child td {{
            border-bottom: none;
        }}
        
        .field-name {{
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 700;
            color: var(--text-muted);
            width: 110px;
        }}
        
        /* 대형 삽화 디자인 */
        .img-frame {{
            width: 100%;
            text-align: center;
        }}
        
        .img-preview {{
            width: 100%;
            height: auto;
            max-height: 520px; /* 고화질 웅장한 이미지 높이 설정 */
            object-fit: contain;
            border: 1px solid var(--border-glass);
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
            border-radius: 6px;
            background: #020617;
        }}
        
        .img-caption {{
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.82rem;
            color: var(--text-muted);
            margin-top: 12px;
            line-height: 1.4;
        }}
        
        .choices-list {{
            margin: 0;
            padding-left: 18px;
        }}
        
        .choices-list li {{
            margin-bottom: 4px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.7rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
        }}
        
        .badge-accent {{
            background-color: rgba(239, 68, 68, 0.15);
            color: var(--danger-neon);
            border: 1px solid rgba(239, 68, 68, 0.25);
            text-shadow: 0 0 5px rgba(239, 68, 68, 0.3);
        }}

        /* ─── 하단 컨트롤러 패널 ─── */
        .control-bar {{
            background: var(--bg-glass);
            border-top: 1px solid var(--border-glass);
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.4);
        }}
        
        .nav-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glass);
            color: #ffffff;
            padding: 8px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}
        
        .nav-btn:hover {{
            background: var(--primary-neon);
            color: #000000;
            box-shadow: var(--text-glow);
        }}
        
        .indicator {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--primary-neon);
            text-shadow: var(--text-glow);
        }}
        
        .jump-select {{
            background: #020617;
            border: 1px solid var(--border-glass);
            color: #ffffff;
            padding: 8px 12px;
            border-radius: 4px;
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.88rem;
            outline: none;
            cursor: pointer;
        }}

        /* 모바일 대응 */
        @media (max-width: 950px) {{
            .storyboard-card {{
                grid-template-columns: 1fr !important;
                max-height: 70vh;
            }}
            .storyboard-left {{
                border-right: none;
                border-bottom: 1px dashed var(--border-glass);
                padding-right: 0;
                padding-bottom: 20px;
            }}
            body {{
                overflow: auto;
                height: auto;
            }}
            .control-bar {{
                position: sticky;
                bottom: 0;
            }}
        }}
    </style>
</head>
<body class="theme-{theme_name}">
    <div class="container">
        <header>
            <span class="grade-tag">{grade_str.upper()} / {unit_code.upper()}</span>
            <h1>{chapter.title} (Storyboard)</h1>
            <div class="indicator" id="top-indicator">SCENE 1 / 26</div>
        </header>

        <div class="storyboard-viewport">
            <!-- INTRO (Index 0) -->
            <div class="storyboard-card active" data-index="0" data-title="오프닝 & 인트로">
                <div class="storyboard-left">
                    <div class="img-frame">
                        <img class="img-preview" src="{assets_relative_path}/{chapter.intro_image}" alt="Intro Image">
                        <div class="img-caption">
                            <strong>[ILLUSTRATION 00] INTRO SCENE</strong><br>
                            지시: {chapter.title}에 안착한 오프닝 인트로 배경 일러스트
                        </div>
                    </div>
                </div>
                <div class="storyboard-right">
                    <h2>🎬 [오프닝 & 인트로]</h2>
                    <div class="story-p">{format_markdown_to_html(chapter.intro_story)}</div>
                </div>
            </div>
""")

        # QUESTIONS 1 ~ 20 (Index 1 ~ 20)
        scene_count = 1
        for idx, q in enumerate(chapter.questions, 1):
            choices_html = ""
            if q.choices:
                choices_li = "".join([f"<li>{opt}</li>" for opt in q.choices])
                choices_html = f'<ol class="choices-list">{choices_li}</ol>'
            else:
                choices_html = '<span style="color:var(--text-muted)">주관식 (INPUT)</span>'
                
            extra_class_badge = f'<span class="badge badge-accent">{q.extra_class}</span>' if q.extra_class else ""
            
            # 구조화된 정답 포맷팅
            ans_spec = q.answer
            ans_display = f"Type: {ans_spec.get('type')} / Values: {ans_spec.get('values', [])}"
            
            html_content.append(f"""
            <!-- Q{q.qnum} (Index {scene_count}) -->
            <div class="storyboard-card" data-index="{scene_count}" data-title="Q{q.qnum}: {q.title}">
                <div class="storyboard-left">
                    <div class="img-frame">
                        <img class="img-preview" src="{assets_relative_path}/{q.image}" alt="Q{q.qnum} Image">
                        <div class="img-caption">
                            <strong>[ILLUSTRATION {q.qnum:02d}] ZONE {q.qnum}</strong><br>
                            지시: {q.title} 관련 수수께끼 도판 이미지
                        </div>
                    </div>
                </div>
                <div class="storyboard-right">
                    <h2>🧩 Q{q.qnum}: {q.title} {extra_class_badge}</h2>
                    <div class="story-p">{format_markdown_to_html(q.story)}</div>
                    <table class="quiz-details">
                        <tr>
                            <td class="field-name">퀴즈 질문</td>
                            <td><strong>{q.qtext}</strong></td>
                        </tr>
                        <tr>
                            <td class="field-name">선택지</td>
                            <td>{choices_html}</td>
                        </tr>
                        <tr>
                            <td class="field-name">정답 조건</td>
                            <td><code>{ans_display}</code></td>
                        </tr>
                        <tr>
                            <td class="field-name">플레이스홀더</td>
                            <td>{q.placeholder}</td>
                        </tr>
                        <tr>
                            <td class="field-name">힌트</td>
                            <td style="color:var(--accent-neon)">💡 {q.hint}</td>
                        </tr>
                    </table>
                </div>
            </div>
""")
            scene_count += 1

        # EVENTS 1 ~ 4 (Index 21 ~ 24)
        for idx, ev in enumerate(chapter.events, 1):
            html_content.append(f"""
            <!-- EVENT{ev.evnum} (Index {scene_count}) -->
            <div class="storyboard-card" data-index="{scene_count}" data-title="EVENT {ev.evnum}: {ev.title}">
                <div class="storyboard-left">
                    <div class="img-frame">
                        <img class="img-preview" src="{assets_relative_path}/{ev.image}" alt="Event{ev.evnum} Image">
                        <div class="img-caption">
                            <strong>[ILLUSTRATION EVENT {ev.evnum:02d}]</strong><br>
                            지시: {ev.title} 돌발 상황 이벤트 배경
                        </div>
                    </div>
                </div>
                <div class="storyboard-right">
                    <h2>🎬 EVENT {ev.evnum}: {ev.title}</h2>
                    <div class="story-p">{format_markdown_to_html(ev.story)}</div>
                    <table class="quiz-details">
                        <tr>
                            <td class="field-name">버튼 텍스트</td>
                            <td>{ev.btn_text}</td>
                        </tr>
                        <tr>
                            <td class="field-name">다음 스테이지</td>
                            <td><code>{ev.next_stage}</code></td>
                        </tr>
                        <tr>
                            <td class="field-name">진행도</td>
                            <td>{ev.progress}%</td>
                        </tr>
                    </table>
                </div>
            </div>
""")
            scene_count += 1

        # OUTRO (Index 25)
        html_content.append(f"""
            <!-- OUTRO (Index {scene_count}) -->
            <div class="storyboard-card" data-index="{scene_count}" data-title="엔딩 & 아웃트로">
                <div class="storyboard-left">
                    <div class="img-frame">
                        <img class="img-preview" src="{assets_relative_path}/{chapter.outro_image}" alt="Outro Image">
                        <div class="img-caption">
                            <strong>[ILLUSTRATION 21] OUTRO SCENE</strong><br>
                            지시: 미션 성공 후 아웃트로 엔딩 연출 일러스트
                        </div>
                    </div>
                </div>
                <div class="storyboard-right">
                    <h2>🎬 [엔딩 & 아웃트로]</h2>
                    <div class="story-p">{format_markdown_to_html(chapter.outro_story)}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 하단 컨트롤러 패널 -->
    <div class="control-bar">
        <button class="nav-btn" id="prev-btn">◀ PREV</button>
        
        <div>
            <select class="jump-select" id="jump-select">
                <!-- JS로 동적 생성 -->
            </select>
        </div>
        
        <button class="nav-btn" id="next-btn">NEXT ▶</button>
    </div>

    <!-- ─── 슬라이드 넘김 제어 스크립트 ─── -->
    <script>
        const cards = document.querySelectorAll('.storyboard-card');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const topIndicator = document.getElementById('top-indicator');
        const jumpSelect = document.getElementById('jump-select');
        
        let currentIndex = 0;
        const total = cards.length;
        
        // 1. 드롭다운 씬 목록 채우기
        cards.forEach((card, idx) => {{
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = `[${{idx + 1}}/${{total}}] ${{card.getAttribute('data-title')}}`;
            jumpSelect.appendChild(opt);
        }});
        
        // 2. 씬 전환 함수
        function showScene(index) {{
            if (index < 0 || index >= total) return;
            
            cards.forEach(card => card.classList.remove('active'));
            cards[index].classList.add('active');
            
            currentIndex = index;
            topIndicator.textContent = `SCENE ${{currentIndex + 1}} / ${{total}}`;
            jumpSelect.value = currentIndex;
            
            // 포커스 해제 (키보드 버블링 방지)
            jumpSelect.blur();
        }}
        
        // 3. 버튼 클릭 이벤트
        prevBtn.addEventListener('click', () => {{
            if (currentIndex > 0) showScene(currentIndex - 1);
        }});
        
        nextBtn.addEventListener('click', () => {{
            if (currentIndex < total - 1) showScene(currentIndex + 1);
        }});
        
        jumpSelect.addEventListener('change', (e) => {{
            showScene(parseInt(e.target.value, 10));
        }});
        
        // 4. ⌨️ 키보드 단축키 연동 (Page Up / Page Down / 방향키)
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'PageUp' || e.key === 'ArrowUp' || e.key === 'ArrowLeft') {{
                e.preventDefault();
                if (currentIndex > 0) showScene(currentIndex - 1);
            }} else if (e.key === 'PageDown' || e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ') {{
                e.preventDefault();
                if (currentIndex < total - 1) showScene(currentIndex + 1);
            }}
        }});
    </script>
</body>
</html>
""")

        # 파일 쓰기
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("".join(html_content))
            print(f"  [OK] Storybook Viewer compiled successfully: {output_file.name}")
            return True
        except Exception as e:
            print(f"  [Error] Failed to write storybook HTML: {e}")
            return False
