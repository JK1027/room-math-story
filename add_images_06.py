import re

html_file = 'app_m1_06_escape_room.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 스타일 확인 및 주입
css = """
        .panel-image {
            width: 100%;
            max-height: 250px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
"""
if '.panel-image {' not in content:
    content = content.replace('</style>', css + '</style>')

# intro, q1 ~ q20, outro에 대한 매핑
img_map = {
    'intro': 'intro.png',
    'outro': 'outro.png'
}
for i in range(1, 21):
    img_map[f'q{i}'] = f'q{i}.png'

for q_id, img_name in img_map.items():
    div_id = f'id="panel_{q_id}"' if q_id not in ['outro', 'intro'] else f'id="{q_id}"'
    pattern = rf'(<div {div_id} class="glass-panel(?: active)?">)(\s*<h[12]>)'
    replacement = rf'\1\n            <img src="assets/m1_06/{img_name}" alt="Background" class="panel-image">\2'
    content = re.sub(pattern, replacement, content, count=1)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added images successfully for Unit 06.")
