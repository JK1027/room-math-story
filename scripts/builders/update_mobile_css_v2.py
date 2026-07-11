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
                padding: 5px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-sizing: border-box;
            }
            .glass-panel {
                width: 100%;
                height: 98vh;
                height: 98dvh;
                padding: 0.8rem;
                border-radius: 16px;
                box-sizing: border-box;
                display: none;
                flex-direction: column;
                justify-content: flex-start;
                overflow: hidden;
            }
            .glass-panel.active {
                display: flex;
            }
            h1 { font-size: 1.5rem; letter-spacing: 1px; margin-top: 0; margin-bottom: 0.3rem; }
            h2 { font-size: 1.1rem; margin-top: 0; margin-bottom: 0.3rem; padding-bottom: 3px; }
            .panel-image {
                height: 0;
                flex: 1 1 25vh; /* Lower the basis slightly to ensure everything fits */
                min-height: 0;
                object-fit: cover;
                margin-bottom: 0.4rem;
                width: 100%;
            }
            .story-box {
                cursor: pointer;
                font-size: 0.85rem;
                padding: 0.6rem 0.8rem;
                margin-bottom: 0.4rem;
                max-height: 80px;
                overflow-y: auto;
                flex: 0 0 auto;
            }
            .question-box {
                padding: 0.6rem 0.8rem;
                margin-bottom: 0.4rem;
                font-size: 0.85rem;
                flex: 0 0 auto;
            }
            .question-box::before { font-size: 2.5rem; top: -5px; right: -5px; }
            .input-group { margin-top: 0.4rem; }
            input[type="text"] { font-size: 0.95rem; padding: 0.6rem; }
            .btn { font-size: 0.95rem; padding: 0.6rem; letter-spacing: 1px; }
            .btn-group { flex-direction: row; gap: 0.4rem; margin-top: 0.4rem; flex: 0 0 auto; }
            .sound-toggle { top: 3px; right: 3px; font-size: 0.65rem; padding: 3px 6px; }
            .graph-container { padding: 0.6rem; margin: 0.4rem 0; flex: 1 1 auto; max-height: 20vh; }
        }
'''
content = re.sub(media_pattern, new_media.strip(), content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Mobile CSS V2 updated successfully.")
