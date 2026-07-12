import os
import re
import json

builder_dir = 'scripts/builders'
template_file = os.path.join(builder_dir, 'update_app_m2_03.py')

with open(template_file, 'r', encoding='utf-8') as f:
    template_content = f.read()

def parse_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    title_match = re.search(r'# 에피소드 \d+\.\s*(.+)', text)
    title = title_match.group(1).strip() if title_match else "방탈출 게임"
    
    qs = []
    q_pattern = re.compile(r'- \*\*Q(\d+)\.\*\*(.*?)(?=- \*\*Q|\Z|##)', re.DOTALL)
    q_matches = q_pattern.findall(text)
    
    ans_section = re.search(r'## 5\. \[정답 및 해설\].*', text, re.DOTALL)
    ans_text = ans_section.group(0) if ans_section else ""
    
    for match in q_matches:
        qnum = int(match[0])
        qtext_raw = match[1].strip()
        ans_match = re.search(rf'- Q{qnum}:\s*(.*?)(?=- Q|\Z|##)', ans_text, re.DOTALL)
        ans_raw = ans_match.group(1).strip() if ans_match else ""
        ans_clean = ans_raw.split('(')[0].strip() if '(' in ans_raw and not ans_raw.startswith('(') else ans_raw.split(' ')[0]
        
        # Remove special characters from ans_clean
        ans_clean = re.sub(r'[^0-9a-zA-Z가-힣\-\./]', '', ans_clean)
        
        ans_check = f"ans === '{ans_clean}'"
        
        qs.append({
            "qnum": qnum,
            "title": f"스테이지 {qnum}",
            "story": "단서를 찾아 문제를 해결하세요.",
            "qtext": f"<strong>Q{qnum}.</strong> {qtext_raw}",
            "placeholder": "정답 입력",
            "error": "틀렸습니다. 다시 시도해보세요.",
            "ans_check": ans_check
        })
    return title, qs

units = [
    ('04', 'm2_04_equations', '연립일차방정식'),
    ('05', 'm2_05_functions', '일차함수'),
    ('06', 'm2_06_geometry1', '도형의성질1'),
    ('07', 'm2_07_geometry2', '도형의성질2'),
    ('08', 'm2_08_probability', '확률')
]

for unit_id, fname, kor_title in units:
    txt_path = f'stories/중2/{fname}.txt'
    if not os.path.exists(txt_path):
        continue
    title, qs = parse_txt(txt_path)
    
    content = template_content.replace('app_m2_03_escape_room.html', f'app_m2_{unit_id}_escape_room.html')
    content = content.replace('요정 숲의 불균형', title)
    content = content.replace('m2_03_inequalities', fname)
    
    # regex sub qs array
    qs_str = "qs = " + json.dumps(qs, ensure_ascii=False, indent=4)
    content = re.sub(r'qs\s*=\s*\[.*?\](?=\s*(?:#|for|with))', qs_str, content, flags=re.DOTALL)
    
    with open(os.path.join(builder_dir, f'update_app_m2_{unit_id}.py'), 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Generated update_app_m2_{unit_id}.py")

