import os
import re

builder_dir = 'scripts/builders'
src_file = os.path.join(builder_dir, 'update_app_m2_03.py')
dest_file = os.path.join(builder_dir, 'update_app_m2_04.py')

with open(src_file, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('app_m2_03_escape_room.html', 'app_m2_04_escape_room.html')
content = content.replace('요정 숲의 불균형', '괴도 X의 암호 편지')
content = content.replace('m2_03_inequalities', 'm2_04_equations')

content = re.sub(r'--bg-main: #[0-9a-fA-F]+;', '--bg-main: #0c101b;', content)
content = re.sub(r'--glass-bg: rgba\([^)]+\);', '--glass-bg: rgba(15, 23, 42, 0.75);', content)
content = re.sub(r'--glass-border: rgba\([^)]+\);', '--glass-border: rgba(224, 180, 76, 0.25);', content)
content = re.sub(r'--accent: #[0-9a-fA-F]+;', '--accent: #e0b44c;', content)
content = re.sub(r'--accent-hover: #[0-9a-fA-F]+;', '--accent-hover: #f5d06e;', content)
content = re.sub(r'--text-main: #[0-9a-fA-F]+;', '--text-main: #f1f5f9;', content)

bg_old = r'radial-gradient\(circle at 10% 20%, rgba[^)]+\) 0%, transparent 40%\), radial-gradient\(circle at 90% 80%, rgba[^)]+\) 0%, transparent 40%\)'
bg_new = r'radial-gradient(circle at 10% 20%, rgba(224, 180, 76, 0.08) 0%, transparent 40%), radial-gradient(circle at 90% 80%, rgba(15, 23, 42, 0.3) 0%, transparent 40%)'
content = re.sub(r'radial-gradient\(circle at 10% 20%, rgba\(0, 255, 128.*?transparent 40%\)', bg_new, content, flags=re.DOTALL)

qs_code = '''qs = [
    {"qnum": 1, "title": "제 1구역: 미지수가 2개인 단서", "story": "세계적인 미술관에서 전설의 다이아몬드 '별의 눈물'이 도난당했습니다! 현장에는 오직 괴도 X가 남긴 연립방정식 암호 편지뿐입니다.", "qtext": "<strong>Q1.</strong> 방정식 \\\\(2x + y - 5 = 0\\\\) 은 미지수가 몇 개인 일차방정식인가?", "placeholder": "예: 2", "error": "다시 세어보세요! 미지수의 개수가 다릅니다.", "ans_check": "ans === '2' || ans === '2개'"},
    {"qnum": 2, "title": "미지수가 2개인 일차방정식 찾기", "story": "수많은 방정식들 속에 진짜 암호가 섞여 있습니다. 어떤 것이 우리가 찾는 형태인지 식별해야 합니다.", "qtext": "<strong>Q2.</strong> 다음 중 미지수가 2개인 일차방정식은?<br>(1) \\\\(x + 2 = 3\\\\) <br>(2) \\\\(x + y = 5\\\\) <br>(3) \\\\(x^2 + y = 1\\\\)", "placeholder": "번호 입력 (예: 2)", "error": "틀렸습니다. 미지수가 두 개이고 차수가 1인 식을 찾아야 합니다.", "ans_check": "ans === '2' || ans === '(2)'"},
    {"qnum": 3, "title": "순서쌍 암호 1", "story": "진짜 암호식을 찾았습니다! 이제 암호의 해를 모두 찾아 입력해야 잠금장치가 해제됩니다.", "qtext": "<strong>Q3.</strong> \\\\(x, y\\\\)가 자연수일 때, \\\\(x + y = 3\\\\) 을 만족하는 순서쌍 \\\\((x, y)\\\\)를 모두 구하시오.", "placeholder": "예: (1,2),(2,1)", "error": "자연수 조합이 틀렸습니다.", "ans_check": "ans.replace(/\\\\s+/g, '') === '(1,2),(2,1)' || ans.replace(/\\\\s+/g, '') === '(2,1),(1,2)' || ans.replace(/\\\\s+/g, '') === '1,2,2,1' || ans.includes('1,2') && ans.includes('2,1')"},
    {"qnum": 4, "title": "순서쌍 암호 2", "story": "다음 암호식도 해가 정해져 있습니다. 몇 개의 해가 존재하는지 개수를 파악하세요.", "qtext": "<strong>Q4.</strong> \\\\(x, y\\\\)가 자연수일 때, \\\\(2x + y = 5\\\\) 를 만족하는 순서쌍 \\\\((x, y)\\\\)의 개수는 몇 개인가?", "placeholder": "숫자만 입력", "error": "개수가 틀렸습니다. (1,3)과 (2,1)을 확인해보세요.", "ans_check": "ans === '2' || ans === '2개'"},
    {"qnum": 5, "title": "손상된 암호 복원", "story": "편지의 한 부분이 찢겨져 상수 a의 값이 보이지 않습니다. 이미 알고 있는 해를 이용해 복원하세요.", "qtext": "<strong>Q5.</strong> \\\\(x=1, y=2\\\\) 가 방정식 \\\\(3x - ay = -1\\\\) 의 해일 때, 상수 \\\\(a\\\\)의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "계산이 틀렸습니다. 대입하여 풀어보세요.", "ans_check": "ans === '2'"},
    
    {"qnum": 6, "title": "제 2구역: 얽힌 실타래", "story": "첫 번째 단서를 돌파하자 수많은 붉은 실들이 얽힌 방이 나타납니다. 두 식이 어떻게 연결되는지 파악해야 합니다.", "qtext": "<strong>Q6.</strong> 두 일차방정식을 한 쌍으로 묶어 놓은 것을 무엇이라 하는가?", "placeholder": "여섯 글자 입력", "error": "용어가 틀렸습니다. 연립...?", "ans_check": "ans.includes('연립') && (ans.includes('일차방정식') || ans.includes('방정식'))"},
    {"qnum": 7, "title": "연립방정식의 해 확인", "story": "두 개의 방정식이 만나는 지점이 정확한지 확인하려면, 미지수 a를 알아내야 합니다.", "qtext": "<strong>Q7.</strong> \\\\(x=2, y=1\\\\) 이 연립방정식 \\\\(\\\\begin{cases} x+y=3 \\\\\\\\ ax-y=3 \\\\end{cases}\\\\) 의 해일 때, \\\\(a\\\\)의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "틀렸습니다. 두 번째 식에 대입해보세요.", "ans_check": "ans === '2'"},
    {"qnum": 8, "title": "직관적 해독", "story": "단순한 암호는 직관적으로 풀 수도 있습니다. 머릿속으로 두 식을 더해보세요.", "qtext": "<strong>Q8.</strong> \\\\(\\\\begin{cases} x+y=5 \\\\\\\\ x-y=1 \\\\end{cases}\\\\) 의 해를 구하시오.", "placeholder": "예: (3,2) 또는 x=3,y=2", "error": "합이 5이고 차가 1인 두 수를 다시 찾아보세요.", "ans_check": "ans.replace(/\\\\s+/g, '') === '(3,2)' || (ans.includes('3') && ans.includes('2'))"},
    {"qnum": 9, "title": "그래프와 해", "story": "방에는 두 개의 레이저 선이 교차하고 있습니다. 연립방정식의 해는 기하학적으로 무엇을 의미할까요?", "qtext": "<strong>Q9.</strong> 연립방정식의 해는 두 일차방정식의 그래프가 만나는 ( ? )의 좌표와 같다.", "placeholder": "두 글자 입력", "error": "만나는 점을 뜻하는 단어입니다.", "ans_check": "ans === '교점'"},
    {"qnum": 10, "title": "해독 방식 선택", "story": "이제 본격적인 해독 다이얼을 돌려야 합니다. 한 식을 다른 식에 밀어넣는 방법의 이름은?", "qtext": "<strong>Q10.</strong> 연립방정식을 풀 때 한 방정식을 다른 방정식에 대입하여 미지수를 없애는 방법을 무엇이라 하는가?", "placeholder": "세 글자 입력", "error": "틀렸습니다. '~입법' 입니다.", "ans_check": "ans.includes('대입')"},

    {"qnum": 11, "title": "제 3구역: 암호 해독", "story": "복잡한 기계식 다이얼 장치 앞입니다. 두 식을 합치거나 빼서 미지수를 없애는 또 다른 기술이 필요합니다.", "qtext": "<strong>Q11.</strong> 연립방정식을 풀 때 두 방정식을 더하거나 빼서 미지수를 없애는 방법을 무엇이라 하는가?", "placeholder": "세 글자 입력", "error": "틀렸습니다. 더하고 빼는 방법입니다.", "ans_check": "ans.includes('가감')"},
    {"qnum": 12, "title": "대입의 마술", "story": "첫 번째 다이얼에 대입법을 적용합니다. y 대신 2x를 쏙 넣어보세요.", "qtext": "<strong>Q12.</strong> \\\\(\\\\begin{cases} y = 2x \\\\\\\\ x + y = 6 \\\\end{cases}\\\\) 을 대입법으로 풀 때, \\\\(x\\\\)의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "틀렸습니다. x + 2x = 6 을 풀어보세요.", "ans_check": "ans === '2' || ans.includes('x=2')"},
    {"qnum": 13, "title": "가감의 선택", "story": "두 번째 다이얼입니다. 두 식의 y 부호가 다릅니다. 없애려면 어떻게 해야 할까요?", "qtext": "<strong>Q13.</strong> \\\\(\\\\begin{cases} 2x + y = 7 \\\\\\\\ 2x - y = 1 \\\\end{cases}\\\\) 을 가감법으로 풀기 위해 두 식을 ( 더해야 / 빼야 ) y가 없어진다.", "placeholder": "더해야 또는 빼야", "error": "+y 와 -y 입니다. 부호를 생각하세요.", "ans_check": "ans.includes('더해') || ans.includes('더하')"},
    {"qnum": 14, "title": "해독 완료 1", "story": "좋습니다! 다이얼을 더해서 해를 완전히 구해봅시다.", "qtext": "<strong>Q14.</strong> Q13의 연립방정식을 풀어 해 \\\\((x, y)\\\\)를 구하시오.", "placeholder": "예: (2,3)", "error": "틀렸습니다. 4x=8에서 x를 구하고 대입하세요.", "ans_check": "ans.replace(/\\\\s+/g, '') === '(2,3)' || (ans.includes('2') && ans.includes('3'))"},
    {"qnum": 15, "title": "해독 완료 2", "story": "마지막 다이얼입니다! 이번엔 x의 계수가 다르고 y의 계수가 같습니다. 빼서 해를 구하세요.", "qtext": "<strong>Q15.</strong> \\\\(\\\\begin{cases} x + 2y = 4 \\\\\\\\ 3x + 2y = 8 \\\\end{cases}\\\\) 의 해 \\\\((x, y)\\\\)를 구하시오.", "placeholder": "예: (2,1)", "error": "틀렸습니다. 식을 빼면 -2x = -4 가 됩니다.", "ans_check": "ans.replace(/\\\\s+/g, '') === '(2,1)' || (ans.includes('2') && ans.includes('1'))"},

    {"qnum": 16, "title": "제 4구역: 괴도 X의 은신처", "story": "드디어 은신처의 금고 앞입니다. 짐승 형상의 조각상들이 있고, 다리 개수로 암호가 설정되어 있습니다.", "qtext": "<strong>Q16.</strong> 토끼와 닭이 섞여 있는 우리에 머리가 모두 10개, 다리가 모두 28개이다. 토끼를 x마리, 닭을 y마리라 할 때, <b>다리 수에 대한 방정식</b>을 세우시오.", "placeholder": "예: 4x+2y=28", "error": "토끼 다리는 4개, 닭 다리는 2개입니다.", "ans_check": "ans.replace(/\\\\s+/g, '') === '4x+2y=28' || ans.replace(/\\\\s+/g, '') === '2x+4y=28' || ans.replace(/\\\\s+/g, '') === '2y+4x=28' || ans.replace(/\\\\s+/g, '') === '28=4x+2y'"},
    {"qnum": 17, "title": "조각상의 비밀", "story": "식을 세웠으니 풀어야 합니다. 토끼 조각상은 몇 개일까요?", "qtext": "<strong>Q17.</strong> Q16의 연립방정식을 풀어 토끼(x)는 몇 마리인지 구하시오.", "placeholder": "숫자만 입력", "error": "틀렸습니다. x+y=10 과 연립하세요.", "ans_check": "ans === '4' || ans === '4마리'"},
    {"qnum": 18, "title": "동전 금고", "story": "다음은 동전 금고입니다. 개수와 금액 정보로 두 번째 식을 세워야 합니다.", "qtext": "<strong>Q18.</strong> 100원짜리 동전 x개와 500원짜리 동전 y개를 합하여 10개, 금액이 2600원일 때, <b>동전 개수에 대한 방정식</b>을 세우시오.", "placeholder": "예: x+y=10", "error": "개수에 대한 식입니다.", "ans_check": "ans.replace(/\\\\s+/g, '') === 'x+y=10' || ans.replace(/\\\\s+/g, '') === 'y+x=10' || ans.replace(/\\\\s+/g, '') === '10=x+y'"},
    {"qnum": 19, "title": "동전 개수 확인", "story": "동전 금고를 열기 위해 100원짜리 동전의 개수를 알아야 합니다.", "qtext": "<strong>Q19.</strong> Q18의 정보(100x+500y=2600)와 연립방정식을 풀어 100원짜리 동전(x)은 몇 개인지 구하시오.", "placeholder": "숫자만 입력", "error": "틀렸습니다. 가감법이나 대입법을 적용하세요.", "ans_check": "ans === '6' || ans === '6개'"},
    {"qnum": 20, "title": "마지막 암호: 시간의 나이", "story": "마지막 다이아몬드 보호 장막입니다! 시간과 나이에 대한 연립방정식을 풀어 장막을 걷어내세요!", "qtext": "<strong>Q20.</strong> 현재 아버지와 아들의 나이의 합은 50세이고, 5년 후에는 아버지의 나이가 아들의 나이의 3배가 된다. 현재 아들의 나이를 구하시오.", "placeholder": "숫자만 입력", "error": "틀렸습니다. x+y=50, x+5 = 3(y+5) 를 풀어보세요.", "ans_check": "ans === '10' || ans === '10세' || ans === '10살'"}
]'''

parts = content.split("qs = [")
content = parts[0] + qs_code + "\n\nbase_html = " + parts[1].split("base_html = ", 1)[1]

with open(dest_file, 'w', encoding='utf-8') as f:
    f.write(content)

print('Generated update_app_m2_04.py')
