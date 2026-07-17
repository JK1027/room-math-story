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
    [Storyboard PDF-like Grid 빌더] chapterXX.md 모델을 읽어 
    전통적인 2단 스토리보드(좌측: 이미지/일러스트 지시, 우측: 대사/명세 표) 격자 레이아웃을 생성합니다.
    인쇄(PDF 저장) 시 최적의 페이지 나눔(Page Break)을 지원합니다.
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
        
        # HTML Header & WebApp Matching Grid CSS
        html_content.append(f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스토리보드 검토(PDF형): {chapter.title}</title>
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
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            box-sizing: border-box;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 40px;
            background: var(--bg-glass);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-glass);
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }}
        
        .grade-tag {{
            display: inline-block;
            font-family: 'Orbitron', sans-serif;
            color: var(--primary-neon);
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 0.15em;
            margin-bottom: 6px;
            text-shadow: var(--text-glow);
        }}
        
        h1 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.85rem;
            margin: 0;
            font-weight: 700;
            color: #ffffff;
            text-shadow: var(--text-glow);
        }}
        
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            margin-top: 20px;
        }}
        
        .meta-card {{
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border-glass);
            border-radius: 4px;
            padding: 10px;
            text-align: center;
        }}
        
        .meta-label {{
            font-family: 'Orbitron', sans-serif;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 2px;
        }}
        
        .meta-val {{
            font-size: 1rem;
            font-weight: 700;
            color: #ffffff;
        }}
        
        /* ─── 2단 스토리보드 그리드 카드 ─── */
        .storyboard-card {{
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 30px;
            background: var(--bg-glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-glass);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
            box-sizing: border-box;
            page-break-inside: avoid; /* PDF 출력 시 페이지 끊김 방지 */
        }}
        
        /* 좌측: 비주얼/이미지 영역 */
        .storyboard-left {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        /* 우측: 명세/지문 영역 */
        .storyboard-right {{
            display: flex;
            flex-direction: column;
        }}
        
        h2 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 20px;
            color: var(--primary-neon);
            text-shadow: var(--text-glow);
            border-bottom: 1px solid var(--border-glass);
            padding-bottom: 10px;
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
            margin-top: auto; /* 대사는 카드 아래쪽에 배치하여 흐름 고정 */
        }}
        
        /* 테이블 명세 스타일 */
        .quiz-details {{
            border-collapse: collapse;
            width: 100%;
            font-size: 0.9rem;
            margin-bottom: 20px;
            border-top: 1px solid var(--border-glass);
            border-bottom: 1px solid var(--border-glass);
        }}
        
        .quiz-details td {{
            padding: 10px 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
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
        
        /* 이미지 프리뷰 양식 */
        .img-frame {{
            width: 100%;
            text-align: center;
        }}
        
        .img-preview {{
            width: 100%;
            height: auto;
            max-height: 250px;
            object-fit: contain;
            border: 1px solid var(--border-glass);
            box-shadow: 0 0 12px rgba(0, 0, 0, 0.4);
            border-radius: 4px;
            background: #020617;
        }}
        
        .img-caption {{
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 8px;
            letter-spacing: 0.03em;
            line-height: 1.3;
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
        
        /* ─── PDF 인쇄 최적화 규칙 ─── */
        @media print {{
            body {{
                background: #ffffff !important;
                color: #000000 !important;
            }}
            .container {{
                max-width: 100% !important;
                padding: 10px !important;
            }}
            header {{
                background: #ffffff !important;
                color: #000000 !important;
                border: 1px solid #cccccc !important;
                box-shadow: none !important;
                page-break-after: avoid;
            }}
            .meta-card {{
                background: #ffffff !important;
                border: 1px solid #cccccc !important;
            }}
            .meta-val, h1, h2, .grade-tag {{
                color: #000000 !important;
                text-shadow: none !important;
            }}
            .storyboard-card {{
                grid-template-columns: 280px 1fr !important;
                background: #ffffff !important;
                border: 1px solid #999999 !important;
                box-shadow: none !important;
                color: #000000 !important;
                page-break-inside: avoid !important;
                margin-bottom: 25px !important;
                padding: 20px !important;
            }}
            .story-p {{
                background: #f9f9f9 !important;
                border: 1px solid #cccccc !important;
                color: #111111 !important;
            }}
            .quiz-details td {{
                color: #111111 !important;
                border-bottom: 1px solid #dddddd !important;
            }}
            .img-preview {{
                border: 1px solid #cccccc !important;
            }}
        }}

        /* 모바일 대응 */
        @media (max-width: 900px) {{
            .storyboard-card {{
                grid-template-columns: 1fr !important;
                gap: 20px;
                padding: 20px;
            }}
            .img-preview {{
                max-height: 300px;
            }}
        }}
    </style>
</head>
<body class="theme-{theme_name}">
    <div class="container">
        <header>
            <span class="grade-tag">{grade_str.upper()} / {unit_code.upper()}</span>
            <h1>{chapter.title}</h1>
            <div class="meta-grid">
                <div class="meta-card">
                    <div class="meta-label">TEMPLATE</div>
                    <div class="meta-val">{chapter.template}</div>
                </div>
                <div class="meta-card">
                    <div class="meta-label">HERO</div>
                    <div class="meta-val">{chapter.hero}</div>
                </div>
                <div class="meta-card">
                    <div class="meta-label">HELPER</div>
                    <div class="meta-val">{chapter.helper}</div>
                </div>
                <div class="meta-card">
                    <div class="meta-label">VILLAIN</div>
                    <div class="meta-val">{chapter.villain}</div>
                </div>
            </div>
        </header>

        <!-- INTRO -->
        <div class="storyboard-card">
            <div class="storyboard-left">
                <div class="img-frame">
                    <img class="img-preview" src="{assets_relative_path}/{chapter.intro_image}" alt="Intro Image">
                    <div class="img-caption">
                        <strong>[ILLUSTRATION 00] INTRO SCENE</strong><br>
                        지시: {chapter.title}에 안착한 인트로 배경 화면
                    </div>
                </div>
            </div>
            <div class="storyboard-right">
                <h2>🎬 [오프닝 & 인트로]</h2>
                <div class="story-p">{format_markdown_to_html(chapter.intro_story)}</div>
            </div>
        </div>
""")

        # QUESTIONS 1 ~ 20
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
        <!-- Q{q.qnum} -->
        <div class="storyboard-card">
            <div class="storyboard-left">
                <div class="img-frame">
                    <img class="img-preview" src="{assets_relative_path}/{q.image}" alt="Q{q.qnum} Image">
                    <div class="img-caption">
                        <strong>[ILLUSTRATION {q.qnum:02d}] ZONE {q.qnum}</strong><br>
                        지시: {q.title} 관련 퍼즐 삽화 도판
                    </div>
                </div>
            </div>
            <div class="storyboard-right">
                <h2>🧩 Q{q.qnum}: {q.title} {extra_class_badge}</h2>
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
                        <td class="field-name">에러 메시지</td>
                        <td>{q.error_message}</td>
                    </tr>
                    <tr>
                        <td class="field-name">힌트</td>
                        <td style="color:var(--accent-neon)">💡 {q.hint}</td>
                    </tr>
                </table>
                <div class="story-p">{format_markdown_to_html(q.story)}</div>
            </div>
        </div>
""")

        # EVENTS 1 ~ 4
        for idx, ev in enumerate(chapter.events, 1):
            html_content.append(f"""
        <!-- EVENT{ev.evnum} -->
        <div class="storyboard-card">
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
                <div class="story-p">{format_markdown_to_html(ev.story)}</div>
            </div>
        </div>
""")

        # OUTRO
        html_content.append(f"""
        <!-- OUTRO -->
        <div class="storyboard-card">
            <div class="storyboard-left">
                <div class="img-frame">
                    <img class="img-preview" src="{assets_relative_path}/{chapter.outro_image}" alt="Outro Image">
                    <div class="img-caption">
                        <strong>[ILLUSTRATION 21] OUTRO SCENE</strong><br>
                        지시: 미션 성공 후 아웃트로 엔딩 연출
                    </div>
                </div>
            </div>
            <div class="storyboard-right">
                <h2>🎬 [엔딩 & 아웃트로]</h2>
                <div class="story-p">{format_markdown_to_html(chapter.outro_story)}</div>
            </div>
        </div>
    </div>
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
