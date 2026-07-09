import re

html_file = 'app_m1_04_escape_room.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

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

img_map = {
    'q1': 'img1_radar.png',
    'q2': 'img1_radar.png',
    'q3': 'img1_radar.png',
    'q4': 'img1_radar.png',
    'q5': 'img2_pillars.png',
    'q6': 'img3_atlantis.png',
    'q7': 'img3_atlantis.png',
    'q8': 'img3_atlantis.png',
    'q9': 'img4_mirror.png',
    'q10': 'img4_mirror.png',
    'q11': 'img5_descend.png',
    'q12': 'img5_descend.png',
    'q13': 'img6_oxygen.png',
    'q14': 'img6_oxygen.png',
    'q15': 'img6_oxygen.png',
    'q16': 'img7_gears.png',
    'q17': 'img7_gears.png',
    'q18': 'img8_buoyancy.png',
    'q19': 'img8_buoyancy.png',
    'q20': 'img9_laser.png',
    'outro': 'img10_escape.png',
    'intro': 'img1_radar.png'
}

for q_id, img_name in img_map.items():
    div_id = f'id="panel_{q_id}"' if q_id not in ['outro', 'intro'] else f'id="{q_id}"'
    pattern = rf'(<div {div_id} class="glass-panel(?: active)?">)(\s*<h[12]>)'
    replacement = rf'\1\n            <img src="assets/m1_04/{img_name}" alt="Background" class="panel-image">\2'
    content = re.sub(pattern, replacement, content, count=1)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added images successfully.")
