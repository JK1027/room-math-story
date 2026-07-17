import os
from pathlib import Path
from src.models import Chapter
from src.base import Builder
from scripts.config import paths

class StorybookBuilder(Builder):
    """
    [Storybook Viewer 빌더] chapterXX.md 모델을 읽어 
    Kindle / Apple Books 리더기 스타일의 독서 친화적인(Reader-Friendly) 1컬럼 HTML 문서를 생성합니다.
    """
    
    def build(self, chapter: Chapter, grade_str: str, unit_code: str) -> bool:
        output_dir = paths.ROOT_DIR / "build" / "storybooks"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 파일명 dynamic resolver 연동
        source_path = paths.story_path(grade_str, unit_code)
        output_file = output_dir / f"{source_path.stem}_storybook.html"
        
        # 리소스 URI/경로 매핑 (일원화된 assets/units/ 경로를 추종)
        assets_relative_path = f"../../assets/units/{unit_code}"
        
        html_content = []
        
        # HTML Header & Kindle-like Styling
        html_content.append(f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스토리북 검토: {chapter.title}</title>
    <!-- 구글 하이브리드 서체 로드 (Sans-serif 헤더 + Serif 본문) -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700&family=Noto+Serif+KR:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f8f5ef;      /* 미색 종이 질감 배경 */
            --card-bg: #fcfbfa;       /* 한층 더 밝은 크림색 본문지 */
            --text-main: #2c2a29;     /* 짙은 차콜 먹색 */
            --text-muted: #78736d;    /* 브라운 그레이 */
            --primary: #85754e;       /* 앤틱 브라운 */
            --border-color: #e6dfcf;  /* 연한 베이지 크림 보더 */
        }}
        
        body {{
            font-family: 'Noto Serif KR', serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.75;
            -webkit-font-smoothing: antialiased;
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
            border-bottom: 1px double var(--border-color);
        }}
        
        .grade-tag {{
            display: inline-block;
            font-family: 'Noto Sans KR', sans-serif;
            color: var(--primary);
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        
        h1 {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 2.1rem;
            margin: 0;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.02em;
        }}
        
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }}
        
        .meta-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 2px;
            padding: 14px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }}
        
        .meta-label {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 700;
            margin-bottom: 4px;
        }}
        
        .meta-val {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 1.05rem;
            font-weight: 500;
            color: var(--text-main);
        }}
        
        .section-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 16px rgba(44, 42, 41, 0.03);
            border-radius: 4px;
            padding: 45px;
            margin-bottom: 40px;
            box-sizing: border-box;
        }}
        
        h2 {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 1.45rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 25px;
            color: var(--text-main);
            border-left: 3px solid var(--primary);
            padding-left: 12px;
        }}
        
        .story-p {{
            font-size: 1.05rem;
            color: var(--text-main);
            text-indent: 1.2em;
            margin-bottom: 1.1em;
            text-align: justify;
        }}
        
        /* 테이블 세련되게 단순화 */
        .quiz-details {{
            border-collapse: collapse;
            width: 100%;
            font-size: 0.95rem;
            margin-bottom: 24px;
            border-top: 1px solid var(--text-main);
            border-bottom: 1px solid var(--text-main);
        }}
        
        .quiz-details td {{
            padding: 12px 14px;
            border-bottom: 1px solid var(--border-color);
            vertical-align: top;
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
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 10px rgba(0,0,0,0.04);
            border-radius: 2px;
        }}
        
        .img-caption {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 8px;
            font-weight: 500;
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
            border-radius: 2px;
            font-size: 0.75rem;
            font-weight: 700;
            font-family: 'Noto Sans KR', sans-serif;
        }}
        
        .badge-accent {{
            background-color: #f5eedc;
            color: #705f30;
            border: 1px solid #ebdcb8;
        }}
        
        /* 반응형 뷰포트 조율 */
        @media (max-width: 768px) {{
            .container {{
                padding: 20px 10px;
            }}
            .section-card {{
                padding: 25px 15px;
            }}
            h1 {{
                font-size: 1.7rem;
            }}
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
            <div class="img-frame">
                <img class="img-preview" src="{assets_relative_path}/{chapter.intro_image}" alt="Intro Image">
                <div class="img-caption">[삽화 0] 인트로 전경 일러스트</div>
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
                    <td style="color:#b45309">💡 {q.hint}</td>
                </tr>
            </table>
            
            <div class="img-frame">
                <img class="img-preview" src="{assets_relative_path}/{q.image}" alt="Q{q.qnum} Image">
                <div class="img-caption">[삽화 {q.qnum}] 제 {q.qnum}구역 기하 수수께끼 상세 도판</div>
            </div>
            
            <h4 style="margin-bottom: 8px; font-family:'Noto Sans KR', sans-serif; color: var(--text-muted)">📖 본문 시나리오</h4>
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
                <div class="img-caption">[돌발 삽화 {ev.evnum}] 돌발 상황 이벤트 배경</div>
            </div>
            
            <h4 style="margin-bottom: 8px; font-family:'Noto Sans KR', sans-serif; color: var(--text-muted)">📖 돌발 시나리오</h4>
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
                <div class="img-caption">[삽화 21] 미션 성공 탈출 좌표 오프닝 및 엔딩 아웃트로</div>
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
