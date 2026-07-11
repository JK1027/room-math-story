import re

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_04_escape_room.html")
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS for .panel-image
content = re.sub(r'\.panel-image\s*\{[^\}]*\}', '''
        .panel-image {
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
'''.strip(), content)

# 2. Update CSS for .story-box
if 'max-height: 150px;' not in content:
    content = re.sub(r'(\.story-box\s*\{[^}]*)(})', r'\1\n            max-height: 150px;\n            overflow-y: auto;\n        \2', content)

# 3. Add CSS for Log Modal and Button
modal_css = '''
        /* Story Log Modal CSS */
        .log-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(16, 185, 129, 0.9);
            color: white;
            padding: 10px 20px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            z-index: 1000;
            transition: all 0.3s;
        }
        .log-btn:hover {
            background: rgba(16, 185, 129, 1);
            transform: scale(1.05);
        }
        .log-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }
        .log-modal.active {
            display: flex;
        }
        .log-content {
            background: rgba(30, 41, 59, 0.95);
            border: 1px solid rgba(148, 163, 184, 0.3);
            border-radius: 12px;
            padding: 2rem;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            color: var(--text-main);
        }
        .log-content h2 { margin-top: 0; color: var(--accent-blue); }
        .log-content hr { border-color: rgba(255,255,255,0.1); margin: 15px 0; }
        .close-log {
            float: right;
            background: var(--error-red);
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }
'''
if '.log-btn {' not in content:
    content = content.replace('</style>', modal_css + '</style>')

# 4. Add HTML for Log Button and Modal at the end of body
html_elements = '''
    <!-- Story Log UI -->
    <button class="log-btn" onclick="openLog()">📜 이전 대사 보기</button>
    <div id="storyLogModal" class="log-modal">
        <div class="log-content">
            <button class="close-log" onclick="closeLog()">닫기 ✕</button>
            <h2>📜 지나온 해저 탐사 기록</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>
'''
if 'id="storyLogModal"' not in content:
    content = content.replace('</body>', html_elements + '\n</body>')

# 5. Add JS for Log tracking
js_code = '''
        let storyHistory = [];
        function openLog() {
            document.getElementById('storyLogModal').classList.add('active');
            const container = document.getElementById('logContainer');
            if (storyHistory.length === 0) {
                container.innerHTML = '기록이 없습니다.';
            } else {
                container.innerHTML = storyHistory.join('<hr>');
            }
        }
        function closeLog() {
            document.getElementById('storyLogModal').classList.remove('active');
        }

        // Add current intro to history on load
        window.addEventListener('DOMContentLoaded', () => {
            const introPanel = document.getElementById('intro');
            const introTitle = introPanel.querySelector('h1') ? introPanel.querySelector('h1').innerText : '도입부';
            const introStory = introPanel.querySelector('.story-box') ? introPanel.querySelector('.story-box').innerHTML : '';
            if (introStory) {
                storyHistory.push(`<strong>[${introTitle}]</strong><br>${introStory}`);
            }
        });
'''
if 'let storyHistory = [];' not in content:
    content = content.replace('// Q1', js_code + '\n        // Q1')

# 6. Update nextStage function to record history
if 'storyHistory.push' not in content.split('function nextStage')[1].split('function showError')[0]:
    content = re.sub(
        r'(function nextStage\(currentId, nextId, progress\) \{[\s\S]*?)(document\.getElementById\(nextId\)\.classList\.add\(\'active\'\);)',
        r'\1\n            // 기록 추가\n            const nextPanel = document.getElementById(nextId);\n            const title = nextPanel.querySelector("h2") ? nextPanel.querySelector("h2").innerText : "";\n            const storyBox = nextPanel.querySelector(".story-box");\n            if (storyBox) {\n                storyHistory.push(`<strong>[${title}]</strong><br>${storyBox.innerHTML}`);\n            }\n            \n            \2',
        content
    )

# 7. Update Image paths
img_map = {
    'q1': 'img1_radar.png',
    'q2': 'img1_radar.png',
    'q3': 'img1_radar.png',
    'q4': 'img11_deep_cave.png',
    'q5': 'img2_pillars.png',
    'q6': 'img3_atlantis.png',
    'q7': 'img12_compass.png',
    'q8': 'img3_atlantis.png',
    'q9': 'img4_mirror.png',
    'q10': 'img4_mirror.png',
    'q11': 'img5_descend.png',
    'q12': 'img13_graph_speed.png',
    'q13': 'img6_oxygen.png',
    'q14': 'img6_oxygen.png',
    'q15': 'img14_oxygen_leak.png',
    'q16': 'img7_gears.png',
    'q17': 'img7_gears.png',
    'q18': 'img8_buoyancy.png',
    'q19': 'img15_golden_door.png',
    'q20': 'img9_laser.png',
    'outro': 'img10_escape.png',
    'intro': 'img1_radar.png'
}

for q_id, img_name in img_map.items():
    div_id = f'id="{q_id}"' if q_id in ['outro', 'intro'] else f'id="panel_{q_id}"'
    # We find the image tag inside this panel and replace its src
    # Pattern to match the specific panel and its image tag
    pattern = rf'(<div {div_id}[^>]*>[\s\S]*?<img src="assets/m1_04_coordinates/)img[^"]*\.png(")'
    replacement = rf'\g<1>{img_name}\g<2>'
    content = re.sub(pattern, replacement, content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Update completed.")
