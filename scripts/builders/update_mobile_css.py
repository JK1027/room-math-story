import re

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_04_escape_room.html")
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the @media (max-width: 600px) block
media_pattern = r'@media\s*\(max-width:\s*600px\)\s*\{[\s\S]*?\}'
new_media = '''
        @media (max-width: 600px) {
            body {
                height: 100vh;
                height: 100dvh;
                overflow: hidden;
            }
            .container {
                height: 100%;
                padding: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-sizing: border-box;
            }
            .glass-panel {
                width: 100%;
                height: 96vh;
                height: 96dvh;
                padding: 1rem;
                border-radius: 16px;
                box-sizing: border-box;
                display: none;
                flex-direction: column;
                justify-content: space-between;
                overflow: hidden;
            }
            .glass-panel.active {
                display: flex;
            }
            h1 { font-size: 1.8rem; letter-spacing: 1px; margin-bottom: 0.5rem; }
            h2 { font-size: 1.2rem; margin-bottom: 0.5rem; padding-bottom: 5px; }
            .panel-image {
                height: auto;
                max-height: 38vh; /* Scale down image on mobile to fit screen */
                flex: 1 1 auto;
                object-fit: cover;
                margin-bottom: 0.5rem;
            }
            .story-box {
                cursor: pointer;
                font-size: 0.9rem;
                padding: 0.8rem;
                margin-bottom: 0.5rem;
                max-height: 85px;
                overflow-y: auto;
                flex: 0 0 auto;
            }
            .question-box {
                padding: 0.8rem;
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
                flex: 0 0 auto;
            }
            .question-box::before { font-size: 3rem; top: -5px; right: -5px; }
            .input-group { margin-top: 0.5rem; }
            input[type="text"] { font-size: 1rem; padding: 0.8rem; }
            .btn { font-size: 1rem; padding: 0.8rem; letter-spacing: 1px; }
            .btn-group { flex-direction: row; gap: 0.5rem; margin-top: 0.5rem; flex: 0 0 auto; }
            .sound-toggle { top: 5px; right: 5px; font-size: 0.7rem; padding: 4px 8px; }
            .graph-container { padding: 0.8rem; margin: 0.5rem 0; flex: 1 1 auto; max-height: 25vh; }
        }
'''
content = re.sub(media_pattern, new_media.strip(), content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Mobile CSS updated successfully.")
