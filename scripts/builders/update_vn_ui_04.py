import re

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_04_escape_room.html")
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS for .log-modal and .log-content
# We'll replace the existing CSS block
old_css_pattern = r'\.log-modal\s*\{[\s\S]*?\.close-log\s*\{[\s\S]*?\}'
new_css = '''
        .log-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; max-height: 50vh;
            background: rgba(40, 40, 40, 0.95);
            z-index: 2000;
            justify-content: center;
            align-items: flex-start;
            border-bottom: 2px solid var(--accent-blue);
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .log-modal.active {
            display: flex;
            animation: slideDown 0.3s ease-out forwards;
        }
        @keyframes slideDown {
            from { transform: translateY(-100%); }
            to { transform: translateY(0); }
        }
        .log-content {
            background: transparent;
            border: none;
            padding: 2rem;
            width: 100%;
            max-width: 800px;
            max-height: 50vh;
            overflow-y: auto;
            color: rgba(255, 255, 255, 0.9);
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
content = re.sub(old_css_pattern, new_css.strip(), content)

# 2. Update typeWriterHTML for visual novel style chunks
old_typewriter_pattern = r'let typeWriterTimeout;[\s\S]*?typeWriterTimeout = setTimeout\(type, speed\);\s*\}\s*else\s*\{\s*element\.innerHTML = textStr;\s*triggerComplete\(\);\s*\}\s*\}\s*type\(\);\s*\}'
new_typewriter = '''
        let typeWriterTimeout;
        function typeWriterHTML(element, speed = 25, onComplete = null) {
            let isComplete = false;
            let currentChunkIndex = 0;
            let chunks = [];
            
            function triggerComplete() {
                if(!isComplete) {
                    isComplete = true;
                    element.style.cursor = 'default';
                    if(onComplete) onComplete();
                }
            }
            if (typeWriterTimeout) clearTimeout(typeWriterTimeout);
            
            const htmlContent = element.getAttribute('data-raw-html') || element.innerHTML;
            if (!element.hasAttribute('data-raw-html')) {
                element.setAttribute('data-raw-html', htmlContent);
            }
            
            // Split by <br><br> to create chunks
            chunks = htmlContent.split(/<br\\s*\\/?>\\s*<br\\s*\\/?>/i).filter(c => c.trim() !== '');
            if(chunks.length === 0) {
                triggerComplete();
                return;
            }
            
            let i = 0;
            let textStr = '';
            let typingFinished = false;
            element.style.cursor = 'pointer';
            
            function renderChunk() {
                if (typeWriterTimeout) clearTimeout(typeWriterTimeout);
                i = 0;
                textStr = '';
                typingFinished = false;
                
                let chunkText = chunks[currentChunkIndex].trim();
                if(currentChunkIndex < chunks.length - 1) {
                    chunkText += '<br><br><span style="font-size:0.8rem; color:var(--accent-blue);">(클릭하여 다음 대사 보기 ▼)</span>';
                }
                
                element.innerHTML = '';
                
                function type() {
                    if (i < chunkText.length) {
                        if (chunkText.charAt(i) === '<') {
                            const endTag = chunkText.indexOf('>', i);
                            if (endTag !== -1) {
                                textStr += chunkText.substring(i, endTag + 1);
                                i = endTag + 1;
                            } else {
                                textStr += chunkText.charAt(i);
                                i++;
                            }
                        } else {
                            textStr += chunkText.charAt(i);
                            i++;
                        }
                        element.innerHTML = textStr + (i % 2 === 0 ? '█' : '');
                        typeWriterTimeout = setTimeout(type, speed);
                    } else {
                        element.innerHTML = textStr;
                        typingFinished = true;
                        if(currentChunkIndex === chunks.length - 1) {
                            triggerComplete();
                        }
                    }
                }
                type();
            }
            
            element.onclick = () => {
                if (!typingFinished) {
                    // Skip typing
                    clearTimeout(typeWriterTimeout);
                    let chunkText = chunks[currentChunkIndex].trim();
                    if(currentChunkIndex < chunks.length - 1) {
                        chunkText += '<br><br><span style="font-size:0.8rem; color:var(--accent-blue);">(클릭하여 다음 대사 보기 ▼)</span>';
                    }
                    element.innerHTML = chunkText;
                    typingFinished = true;
                    if(currentChunkIndex === chunks.length - 1) {
                        triggerComplete();
                    }
                } else {
                    if (currentChunkIndex < chunks.length - 1) {
                        currentChunkIndex++;
                        renderChunk();
                    }
                }
            };
            
            renderChunk();
        }
'''
content = re.sub(old_typewriter_pattern, lambda m: new_typewriter.strip(), content)

# 3. Ensure `.story-box` CSS implies it's clickable
if 'cursor: pointer;' not in content.split('.story-box {')[1].split('}')[0]:
    content = content.replace('.story-box {', '.story-box {\n            cursor: pointer; /* Click to advance text */')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Visual Novel UI update completed.")
