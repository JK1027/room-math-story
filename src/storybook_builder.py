import os
from pathlib import Path
from src.models import Chapter
from src.base import Builder
from scripts.config import paths

class StorybookBuilder(Builder):
    """
    [Storybook Viewer 빌더] chapterXX.md 모델을 읽어 
    실제 방탈출 게임 웹앱과 100% 동일한 비주얼 테마(네온 컬러, 다크 네이비 블루, 글래스모피즘, 동일 폰트)
    를 갖춘 검토용 스토리북 HTML을 생성합니다. (타이핑 효과 제외)
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
        
        # HTML Header & WebApp Matching Neon CSS
        html_content.append(f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스토리북 검토: {chapter.title}</title>
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
            line-height: 1.7;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 50px 20px;
            box-sizing: border-box;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 2px solid var(--border-glass);
            background: var(--bg-glass);
            backdrop-filter: blur(8px);
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }}
        
        .grade-tag {{
            display: inline-block;
            font-family: 'Orbitron', sans-serif;
            color: var(--primary-neon);
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 0.15em;
            margin-bottom: 8px;
            text-shadow: var(--text-glow);
        }}
        
        h1 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            margin: 0;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.01em;
            text-shadow: var(--text-glow);
        }}
        
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-top: 25px;
        }}
        
        .meta-card {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-glass);
            border-radius: 6px;
            padding: 14px;
            text-align: center;
        }}
        
        .meta-label {{
            font-family: 'Orbitron', sans-serif;
            font-size: 0.8rem;
            color: var(--text-muted);
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}
        
        .meta-val {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #ffffff;
        }}
        
        /* 웹앱 동일 반투명 글래스 패널 */
        .section-card {{
            background: var(--bg-glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-glass);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            border-radius: 12px;
            padding: 40px;
            margin-bottom: 40px;
            box-sizing: border-box;
        }}
        
        h2 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 25px;
            color: var(--primary-neon);
            text-shadow: var(--text-glow);
            border-bottom: 1px solid var(--border-glass);
            padding-bottom: 12px;
        }}
        
        .story-p {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid var(--border-glass);
            border-radius: 6px;
            padding: 16px 20px;
            font-size: 1rem;
            color: #e5e7eb;
            white-space: pre-line;
            line-height: 1.75;
        }}
        
        /* 웹앱 뼈대 테이블 정합 */
        .quiz-details {{
            border-collapse: collapse;
            width: 100%;
            font-size: 0.95rem;
            margin-bottom: 25px;
            border-top: 1px solid var(--border-glass);
            border-bottom: 1px solid var(--border-glass);
        }}
        
        .quiz-details td {{
            padding: 12px 14px;
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
            width: 120px;
        }}
        
        /* 삽화 프레임 정의 */
        .img-frame {{
            text-align: center;
            margin: 25px 0;
        }}
        
        .img-preview {{
            max-width: 100%;
            max-height: 380px;
            border: 1px solid var(--border-glass);
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.4);
            border-radius: 6px;
        }}
        
        .img-caption {{
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 8px;
            letter-spacing: 0.05em;
        }}
        
        .choices-list {{
            margin: 0;
            padding-left: 20px;
        }}
        
        .choices-list li {{
            margin-bottom: 5px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
        }}
        
        .badge-accent {{
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--danger-neon);
            border: 1px solid rgba(239, 68, 68, 0.2);
            text-shadow: 0 0 5px rgba(239, 68, 68, 0.3);
        }}
        
        /* 반응형 */
        @media (max-width: 768px) {{
            .container {{
                padding: 20px 10px;
            }}
            .section-card {{
                padding: 25px 15px;
            }}
            h1 {{
                font-size: 1.6rem;
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
        <div class="section-card">
            <h2>🎬 [오프닝 & 인트로]</h2>
            <div class="img-frame">
                <img class="img-preview" src="{assets_relative_path}/{chapter.intro_image}" alt="Intro Image">
                <div class="img-caption">[ILLUSTRATION 00] INTRO STORY ILLUSTRATION</div>
            </div>
            <div class="story-p">{chapter.intro_story}</div>
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
        <div class="section-card">
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
            
            <div class="img-frame">
                <img class="img-preview" src="{assets_relative_path}/{q.image}" alt="Q{q.qnum} Image">
                <div class="img-caption">[ILLUSTRATION {q.qnum:02d}] ZONE {q.qnum} PUZZLE ILLUSTRATION</div>
            </div>
            
            <h4 style="margin-bottom: 8px; font-family:'Orbitron', sans-serif; color: var(--text-muted)">📖 SCENARIO DIALOGUE</h4>
            <div class="story-p">{q.story}</div>
        </div>
""")

        # EVENTS 1 ~ 4
        for idx, ev in enumerate(chapter.events, 1):
            html_content.append(f"""
        <!-- EVENT{ev.evnum} -->
        <div class="section-card">
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
            
            <div class="img-frame">
                <img class="img-preview" src="{assets_relative_path}/{ev.image}" alt="Event{ev.evnum} Image">
                <div class="img-caption">[ILLUSTRATION EVENT {ev.evnum:02d}] SUDDEN SITUATION SCENE</div>
            </div>
            
            <h4 style="margin-bottom: 8px; font-family:'Orbitron', sans-serif; color: var(--text-muted)">📖 EVENT SCENARIO</h4>
            <div class="story-p">{ev.story}</div>
        </div>
""")

        # OUTRO
        html_content.append(f"""
        <!-- OUTRO -->
        <div class="section-card">
            <h2>🎬 [엔딩 & 아웃트로]</h2>
            <div class="img-frame">
                <img class="img-preview" src="{assets_relative_path}/{chapter.outro_image}" alt="Outro Image">
                <div class="img-caption">[ILLUSTRATION 21] OUTRO SUCCESS ENDING SCENE</div>
            </div>
            <div class="story-p">{chapter.outro_story}</div>
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
