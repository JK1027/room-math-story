import re

html_file = 'app_m1_04_escape_room.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. intro 패널 이미지 변경
content = re.sub(
    r'(<div id="intro" class="glass-panel active">)\s*<img src="[^"]+" alt="Background" class="panel-image">',
    r'\1\n            <img src="assets/m1_04/intro.png" alt="Background" class="panel-image">',
    content
)

# 2. q1 ~ q20 패널 이미지 변경
for i in range(1, 21):
    content = re.sub(
        rf'(<div id="panel_q{i}" class="glass-panel">)\s*<img src="[^"]+" alt="Background" class="panel-image">',
        rf'\1\n            <img src="assets/m1_04/q{i}.png" alt="Background" class="panel-image">',
        content
    )

# 3. outro 패널 이미지 변경
content = re.sub(
    r'(<div id="outro" class="glass-panel">)\s*<img src="[^"]+" alt="Background" class="panel-image">',
    r'\1\n            <img src="assets/m1_04/outro.png" alt="Background" class="panel-image">',
    content
)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML images updated successfully for Unit 04.")
