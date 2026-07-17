import os
from pathlib import Path
from src.models import Chapter
from src.base import Builder
from scripts.config import paths

class StorybookBuilder(Builder):
    """
    [Storybook Viewer 빌더] chapterXX.md 모델을 읽어 
    인간 친화적이고 긴 글을 검토하기 편리한 모바일/데스크톱 대응형 HTML 뷰어 문서를 생성합니다.
    """
    
    def build(self, chapter: Chapter, grade_str: str, unit_code: str) -> bool:
        output_dir = paths.ROOT_DIR / "build" / "storybooks"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        chapter_num = unit_code[3:5]
        output_file = output_dir / f"chapter{chapter_num}_storybook.html"
        
        # 리소스 URI/경로 매핑 (일원화된 assets/units/ 경로를 추종)
        assets_relative_path = f"../../assets/units/{unit_code}"
        
        html_content = []
        
        # HTML Header
        html_content.append(f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Storybook 검토: {chapter.title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --primary: #2563eb;
            --primary-light: #eff6ff;
            --accent: #f59e0b;
            --border-color: #e2e8f0;
        }}
        
        body {{
            font-family: 'Inter', 'Noto Sans KR', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.7;
        }}
        
        .container {{
            max-width: 960px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid var(--border-color);
        }}
        
        .grade-tag {{
            display: inline-block;
            background-color: var(--primary-light);
            color: var(--primary);
            font-weight: 600;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-bottom: 12px;
        }}
        
        h1 {{
            font-size: 2.2rem;
            margin: 0;
            font-weight: 700;
            color: #0f172a;
        }}
        
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 24px;
        }}
        
        .meta-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }}
        
        .meta-label {{
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        
        .meta-val {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-main);
        }}
        
        .section-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
        }}
        
        h2 {{
            font-size: 1.6rem;
            border-left: 4px solid var(--primary);
            padding-left: 14px;
            margin-top: 0;
            margin-bottom: 20px;
            color: #0f172a;
        }}
        
        .story-p {{
            white-space: pre-line;
            font-size: 1.05rem;
            color: #334155;
            background: #f1f5f9;
            padding: 20px;
            border-radius: 10px;
            border-left: 3px solid var(--text-muted);
        }}
        
        .content-split {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
            margin-top: 20px;
        }}
        
        @media(min-width: 768px) {{
            .content-split {{
                grid-template-columns: 1.2fr 1fr;
            }}
        }}
        
        .img-preview {{
            width: 100%;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            object-fit: cover;
            max-height: 320px;
        }}
        
        .quiz-details {{
            border-collapse: collapse;
            width: 100%;
            font-size: 0.95rem;
        }}
        
        .quiz-details td {{
            padding: 10px 12px;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .quiz-details tr:last-child td {{
            border-bottom: none;
        }}
        
        .field-name {{
            font-weight: 600;
            color: var(--text-muted);
            width: 110px;
        }}
        
        .choices-list {{
            margin: 0;
            padding-left: 20px;
        }}
        
        .choices-list li {{
            margin-bottom: 4px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        
        .badge-accent {{
            background-color: #fffbeb;
            color: var(--accent);
            border: 1px solid #fef3c7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <span class="grade-tag">{grade_str.upper()} / {unit_code.upper()}</span>
            <h1>{chapter.title}</h1>
            <div class="meta-grid">
                <div class="meta-card">
                    <div class="meta-label">템플릿</div>
                    <div class="meta-val">{chapter.template}</div>
                </div>
                <div class="meta-card">
                    <div class="meta-label">주인공 (Hero)</div>
                    <div class="meta-val">{chapter.hero}</div>
                </div>
                <div class="meta-card">
                    <div class="meta-label">조력자 (Helper)</div>
                    <div class="meta-val">{chapter.helper}</div>
                </div>
                <div class="meta-card">
                    <div class="meta-label">빌런 (Villain)</div>
                    <div class="meta-val">{chapter.villain}</div>
                </div>
            </div>
        </header>

        <!-- INTRO -->
        <div class="section-card">
            <h2>🎬 [오프닝 & 인트로]</h2>
            <div style="text-align: center; margin-bottom: 20px;">
                <img class="img-preview" src="{assets_relative_path}/{chapter.intro_image}" alt="Intro Image">
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
                choices_html = '<span style="color:var(--text-muted)">주관식</span>'
                
            extra_class_badge = f'<span class="badge badge-accent">{q.extra_class}</span>' if q.extra_class else ""
            
            # 구조화된 정답 포맷팅 출력
            ans_spec = q.answer
            ans_display = f"Type: {ans_spec.get('type')}<br>Values: {ans_spec.get('values', [])}"
            
            html_content.append(f"""
        <!-- Q{q.qnum} -->
        <div class="section-card">
            <h2>🧩 Q{q.qnum}: {q.title} {extra_class_badge}</h2>
            <div class="content-split">
                <div>
                    <table class="quiz-details">
                        <tr>
                            <td class="field-name">퀴즈 질문</td>
                            <td>{q.qtext}</td>
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
                            <td style="color:#d97706">{q.hint}</td>
                        </tr>
                    </table>
                </div>
                <div style="text-align: center;">
                    <img class="img-preview" src="{assets_relative_path}/{q.image}" alt="Q{q.qnum} Image">
                </div>
            </div>
            <h4 style="margin-bottom: 8px; color: var(--text-muted)">📖 지문 스토리</h4>
            <div class="story-p">{q.story}</div>
        </div>
""")

        # EVENTS 1 ~ 4
        for idx, ev in enumerate(chapter.events, 1):
            html_content.append(f"""
        <!-- EVENT{ev.evnum} -->
        <div class="section-card">
            <h2>🎬 EVENT {ev.evnum}: {ev.title}</h2>
            <div class="content-split">
                <div>
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
                <div style="text-align: center;">
                    <img class="img-preview" src="{assets_relative_path}/{ev.image}" alt="Event{ev.evnum} Image">
                </div>
            </div>
            <h4 style="margin-bottom: 8px; color: var(--text-muted)">📖 이벤트 시나리오</h4>
            <div class="story-p">{ev.story}</div>
        </div>
""")

        # OUTRO
        html_content.append(f"""
        <!-- OUTRO -->
        <div class="section-card">
            <h2>🎬 [엔딩 & 아웃트로]</h2>
            <div style="text-align: center; margin-bottom: 20px;">
                <img class="img-preview" src="{assets_relative_path}/{chapter.outro_image}" alt="Outro Image">
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
