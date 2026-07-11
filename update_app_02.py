import re
import os

html_file = 'app_m1_02_escape_room.html'
base_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>마법 학교 아르카나의 입학 시험: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0B0E14;
            --glass-bg: rgba(13, 20, 30, 0.75);
            --glass-border: rgba(168, 85, 247, 0.25);
            --accent: #A855F7;
            --accent-hover: #C084FC;
            --text-main: #E9D5FF;
            --text-muted: #A78BFA;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Noto Sans KR', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: hidden;
            position: relative;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: 
                radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(88, 28, 135, 0.15) 0%, transparent 40%);
            z-index: -2;
        }

        .container {
            width: 100%;
            max-width: 800px;
            padding: 2rem;
            position: relative;
            z-index: 10;
        }

        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-top: 1px solid rgba(168, 85, 247, 0.4);
            border-left: 1px solid rgba(168, 85, 247, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(168, 85, 247, 0.05);
            display: none; 
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .glass-panel.active {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }

        h1 {
            font-family: 'Orbit', sans-serif;
            font-size: 2.5rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #FFF 30%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(168, 85, 247, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 500;
            letter-spacing: 1px;
        }

        .panel-image {
            width: 100%;
            max-height: 250px;
            object-fit: cover;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 16px rgba(0,0,0,0.5);
            border: 1px solid rgba(168, 85, 247, 0.2);
        }

        .story-box {
            position: relative;
            background: linear-gradient(90deg, rgba(30, 15, 45, 0.5) 0%, rgba(0,0,0,0.3) 100%);
            border-left: 4px solid var(--accent);
            padding: 0.8rem 1.2rem;
            margin-bottom: 1.5rem;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            height: 90px;
            max-height: 90px;
            overflow: hidden;
            box-sizing: border-box;
        }

        .story-text {
            width: 100%;
            height: 100%;
            overflow: hidden;
            line-height: 1.6;
            font-size: 1.02rem;
            color: var(--text-main);
            text-align: justify;
        }

        .story-log-trigger {
            position: absolute;
            bottom: 4px;
            right: 8px;
            background: rgba(16, 185, 129, 0.25);
            border: 1px solid rgba(16, 185, 129, 0.5);
            color: #34D399;
            padding: 2px 6px;
            font-size: 0.7rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: bold;
            z-index: 10;
        }
        .story-log-trigger:hover {
            background: rgba(16, 185, 129, 0.5);
            color: white;
        }

        .question-box {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            position: relative;
            box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.02);
        }

        .question-box::before {
            content: 'Q';
            position: absolute;
            font-family: 'Share Tech Mono', monospace;
            font-size: 4rem;
            color: rgba(168, 85, 247, 0.05);
            top: -10px;
            right: 10px;
            font-weight: bold;
            pointer-events: none;
        }

        .question-content {
            font-size: 1.15rem;
            line-height: 1.8;
            margin-bottom: 1rem;
        }

        .input-group {
            margin-top: 1rem;
        }

        input[type="text"] {
            width: 100%;
            padding: 1rem 1.2rem;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 12px;
            color: white;
            font-size: 1.1rem;
            font-family: 'Share Tech Mono', monospace, 'Noto Sans KR';
            transition: all 0.3s;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
        }

        input[type="text"]:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.4), inset 0 2px 4px rgba(0,0,0,0.5);
        }

        .error-msg {
            color: #EF4444;
            font-size: 0.95rem;
            margin-top: 0.5rem;
            display: none;
            text-align: center;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
            animation: shake 0.5s ease;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-5px); }
            40%, 80% { transform: translateX(5px); }
        }

        .progress-container {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
            margin-bottom: 2rem;
            overflow: hidden;
            display: none;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }

        .progress-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #7C3AED, var(--accent));
            border-radius: 3px;
            box-shadow: 0 0 10px var(--accent);
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn-group {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }

        .btn {
            background: linear-gradient(135deg, #6B21A8, #4C1D95);
            color: white;
            border: 1px solid #8B5CF6;
            padding: 0.6rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 900;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 3px;
            width: 100%;
            box-shadow: 0 10px 25px rgba(76, 29, 149, 0.5), inset 0 2px 5px rgba(255,255,255,0.3);
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }

        .btn::after {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: all 0.6s;
        }

        .btn:hover::after {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(168, 85, 247, 0.5), inset 0 2px 5px rgba(255,255,255,0.5);
            border-color: #A78BFA;
        }

        .btn:active {
            transform: translateY(1px);
        }

        .sound-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--glass-border);
            padding: 8px 16px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            z-index: 100;
            backdrop-filter: blur(10px);
            font-size: 0.9rem;
            transition: all 0.3s;
            font-weight: bold;
        }

        .sound-toggle:hover {
            background: var(--accent);
            border-color: white;
            box-shadow: 0 0 15px var(--accent);
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        /* Mobile Responsive Viewport */
        @media (max-width: 600px) {
            body {
                overflow-y: auto;
            }
            .container {
                padding: 10px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-sizing: border-box;
                min-height: 100vh;
            }
            .glass-panel {
                width: 100%;
                max-height: 94vh;
                max-height: 94dvh;
                height: auto;
                padding: 1.2rem;
                border-radius: 16px;
                box-sizing: border-box;
                display: none;
                flex-direction: column;
                justify-content: flex-start;
                overflow-y: auto;
            }
            .glass-panel.active {
                display: flex;
            }
            .story-box {
                padding: 0.6rem 1rem;
                margin-bottom: 0.5rem;
                height: 80px;
                max-height: 80px;
                overflow: hidden;
                flex: 0 0 auto;
            }
            .story-text {
                font-size: 0.85rem;
                line-height: 1.5;
            }
            h1 { font-size: 1.6rem; letter-spacing: 1px; }
            h2 { font-size: 1rem; margin-bottom: 1rem; }
            .panel-image { max-height: 180px; margin-bottom: 1rem; }
            .question-box { padding: 0.8rem; margin-bottom: 1rem; }
            .question-box::before { font-size: 3rem; top: -5px; right: -5px; }
            input[type="text"] { font-size: 1rem; padding: 0.8rem; }
            .btn { font-size: 0.9rem; padding: 0.5rem; letter-spacing: 1px;  border-radius: 6px;}
            .btn-group { flex-direction: column; gap: 0.6rem; }
            .sound-toggle { top: 10px; right: 10px; font-size: 0.8rem; padding: 6px 12px; }
        }

        /* Visual Novel Log Modal Styles */
        .log-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(10px);
        }
        .log-content {
            background: #11091C;
            border: 2px solid var(--accent);
            border-radius: 20px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            padding: 2rem;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        .log-content h2 {
            font-family: 'Orbit', sans-serif;
            color: var(--accent);
            margin-bottom: 1rem;
            text-align: left;
        }
        #logContainer {
            overflow-y: auto;
            flex-grow: 1;
            margin-bottom: 1.5rem;
            padding-right: 10px;
            font-size: 0.95rem;
            line-height: 1.8;
            color: #cbd5e1;
        }
        #logContainer strong {
            color: var(--accent);
        }
        .close-log {
            position: absolute;
            top: 15px;
            right: 15px;
            background: transparent;
            border: none;
            color: #ef4444;
            font-size: 1.5rem;
            cursor: pointer;
            transition: scale 0.2s;
        }
        .close-log:hover {
            scale: 1.2;
        }
    </style>
</head>
<body>

    <button id="soundToggle" class="sound-toggle" onclick="toggleSound()">🔊 소리 켜짐</button>

    <div class="container">
        
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <!-- 0. 인트로 -->
        <div id="intro" class="glass-panel active">
            <img src="assets/m1_02_rational_numbers/intro.png" alt="Background" class="panel-image">
            <h1>마법 학교 아르카나</h1>
            <h2>20관문 최종 입학 시험</h2>
            <div class="story-box">
                <div class="story-text">
                    세계 최고의 마법 학교 '아르카나'의 최종 입학 시험장에 오신 것을 환영합니다.<br><br>
                    이곳의 마법은 단순한 주문이 아니라 '정수와 유리수'의 수학적 원리를 통해 발동합니다.<br><br>
                    제한 시간 45분 내에 20개의 수식 결계를 완벽하게 풀어내어 아르카나 수석 입학의 영광을 쟁취하십시오!
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group" style="margin-top: 2rem; width:100%;">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 5)">입학 시험 시작</button>
            </div>
        </div>

        <!-- Q1 -->

    </div>

    <!-- Audio Elements -->
    <audio id="bgm" loop>
        <source src="https://assets.mixkit.co/music/preview/mixkit-space-ambient-tension-905.mp3" type="audio/mp3">
    </audio>
    <audio id="sndClick">
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-mechanical-switch-key-2980.wav" type="audio/wav">
    </audio>
    <audio id="sndTick">
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-key-press-computer-2253.wav" type="audio/wav">
    </audio>
    <audio id="sndSuccess">
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-digital-quick-bypass-2255.wav" type="audio/wav">
    </audio>
    <audio id="sndError">
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-ambient-dark-error-sound-2985.wav" type="audio/wav">
    </audio>
    <audio id="sndVictory">
        <source src="https://assets.mixkit.co/music/preview/mixkit-uplifting-creative-technology-groove-911.mp3" type="audio/mp3">
    </audio>

    <script>
        let isMuted = false;
        const bgm = document.getElementById('bgm');
        const sndClick = document.getElementById('sndClick');
        const sndTick = document.getElementById('sndTick');
        const sndSuccess = document.getElementById('sndSuccess');
        const sndError = document.getElementById('sndError');
        const sndVictory = document.getElementById('sndVictory');

        function toggleSound() {
            isMuted = !isMuted;
            const btn = document.getElementById('soundToggle');
            if (isMuted) {
                btn.innerText = '🔇 소리 꺼짐';
                try { bgm.pause(); } catch(e) {}
            } else {
                btn.innerText = '🔊 소리 켜짐';
                try { bgm.play(); } catch(e) {}
            }
        }

        function startBGM() {
            if (!isMuted) {
                bgm.volume = 0.3;
                try {
                    bgm.play().catch(e => console.log("BGM Autoplay blocked"));
                } catch(e) {}
            }
        }

        function playClick() {
            if (!isMuted) {
                try {
                    sndClick.currentTime = 0;
                    sndClick.play().catch(e => {});
                } catch(e) {}
            }
        }

        function playTick() {
            if (!isMuted) {
                try {
                    sndTick.currentTime = 0;
                    sndTick.volume = 0.5;
                    sndTick.play().catch(e => {});
                } catch(e) {}
            }
        }

        function playSuccess() {
            if (!isMuted) {
                try {
                    sndSuccess.currentTime = 0;
                    sndSuccess.play().catch(e => {});
                } catch(e) {}
            }
        }

        function playError() {
            if (!isMuted) {
                try {
                    sndError.currentTime = 0;
                    sndError.play().catch(e => {});
                } catch(e) {}
            }
        }

        function playVictory() {
            if (!isMuted) {
                try {
                    bgm.pause();
                    sndVictory.volume = 0.5;
                    sndVictory.play().catch(e => {});
                } catch(e) {}
            }
        }

        function cleanString(str) {
            return str.replace(/\\s+/g, '').toLowerCase();
        }

        function showError(panelId, errorId) {
            try { playError(); } catch(e) {}
            const panel = document.getElementById(panelId);
            const err = document.getElementById(errorId);
            err.style.display = 'block';
            err.classList.remove('shake');
            void err.offsetWidth;
            err.classList.add('shake');
            setTimeout(() => {
                err.style.display = 'none';
            }, 3000);
        }

        let storyHistory = [];
        function openLog() {
            try { playClick(); } catch(e) {}
            const modal = document.getElementById('storyLogModal');
            const container = document.getElementById('logContainer');
            if (storyHistory.length === 0) {
                container.innerHTML = "기록이 존재하지 않습니다.";
            } else {
                container.innerHTML = storyHistory.join("<br><br>");
            }
            modal.style.display = 'flex';
        }
        function closeLog() {
            try { playClick(); } catch(e) {}
            document.getElementById('storyLogModal').style.display = 'none';
        }

        let typeWriterTimeout;
        
        function splitSentences(text) {
            let result = [];
            let start = 0;
            for (let i = 0; i < text.length; i++) {
                const char = text.charAt(i);
                if (char === '.' || char === '!' || char === '?') {
                    const nextChar = text.charAt(i + 1);
                    if (!nextChar || nextChar === ' ' || nextChar === '\\n' || nextChar === '<') {
                        result.push(text.substring(start, i + 1).trim());
                        start = i + 1;
                    }
                }
            }
            const finalChunk = text.substring(start).trim();
            if (finalChunk) {
                result.push(finalChunk);
            }
            return result;
        }

        function typeWriterHTML(element, speed = 25, onComplete = null) {
            let isComplete = false;
            let currentChunkIndex = 0;
            let chunks = [];
            const textEl = element.querySelector('.story-text');
            if(!textEl) {
                if(onComplete) onComplete();
                return;
            }

            function triggerComplete() {
                if(!isComplete) {
                    isComplete = true;
                    element.style.cursor = 'default';
                    if(onComplete) onComplete();
                }
            }
            if (typeWriterTimeout) clearTimeout(typeWriterTimeout);
            const htmlContent = textEl.getAttribute('data-raw-html') || textEl.innerHTML;
            if (!textEl.hasAttribute('data-raw-html')) {
                textEl.setAttribute('data-raw-html', htmlContent);
            }
            let rawLines = htmlContent.split(/<br\\s*\\/?>/i);
            for(let line of rawLines) {
                let sentences = splitSentences(line);
                for(let s of sentences) {
                    if(s.trim()) chunks.push(s.trim());
                }
            }
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
                let chunkText = chunks[currentChunkIndex];
                const currentPanel = element.closest('.glass-panel');
                const panelTitle = currentPanel.querySelector('h2') ? currentPanel.querySelector('h2').innerText : '단서';
                const logEntry = `<strong>[${panelTitle}]</strong> ${chunkText}`;
                if (!storyHistory.includes(logEntry)) {
                    storyHistory.push(logEntry);
                }
                if(currentChunkIndex < chunks.length - 1) {
                    chunkText += ' <span style="font-size:0.75rem; color:var(--accent); font-weight:bold; animation: blink 1s infinite;">(클릭 ▼)</span>';
                }
                textEl.innerHTML = '';
                
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
                        textEl.innerHTML = textStr;
                        if (chunkText.charAt(i-1) !== ' ' && chunkText.charAt(i-1) !== '\\n') {
                            try { playTick(); } catch(e) {}
                        }
                        typeWriterTimeout = setTimeout(type, speed);
                    } else {
                        textEl.innerHTML = chunkText;
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
                    clearTimeout(typeWriterTimeout);
                    let chunkText = chunks[currentChunkIndex];
                    if(currentChunkIndex < chunks.length - 1) {
                        chunkText += ' <span style="font-size:0.75rem; color:var(--accent); font-weight:bold; animation: blink 1s infinite;">(클릭 ▼)</span>';
                    }
                    textEl.innerHTML = chunkText;
                    typingFinished = true;
                    if(currentChunkIndex === chunks.length - 1) triggerComplete();
                } else {
                    if (currentChunkIndex < chunks.length - 1) {
                        currentChunkIndex++;
                        renderChunk();
                    }
                }
            };
            renderChunk();
        }

        function nextStage(currentId, nextId, progressPercent) {
            try { playClick(); } catch(e) {}
            if(currentId === 'intro') {
                try { startBGM(); } catch(e) {}
            }
            const currentEl = document.getElementById(currentId);
            const nextEl = document.getElementById(nextId);
            const progContainer = document.getElementById('progressContainer');
            const progBar = document.getElementById('progressBar');
            currentEl.classList.remove('active');
            setTimeout(() => {
                if(nextId !== 'intro') progContainer.style.display = 'block';
                progBar.style.width = progressPercent + '%';
                nextEl.classList.add('active');
                const storyBox = nextEl.querySelector('.story-box');
                if(storyBox) typeWriterHTML(storyBox, 25);
            }, 300);
        }

        window.onload = () => {
            const introPanel = document.getElementById('intro');
            const introStoryBox = introPanel.querySelector('.story-box');
            if (introStoryBox) typeWriterHTML(introStoryBox, 25);
        };
    </script>

    <div id="storyLogModal" class="log-modal">
        <div class="log-content">
            <button class="close-log" onclick="closeLog()">닫기 ✕</button>
            <h2>📜 지나온 시험 기록</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>

</body>
</html>
"""

qs = [
    {"qnum": 1, "title": "빛과 어둠의 대비", "story": "🔮 <strong>[속성 기호 표시]</strong><br><br>마법 아카데미의 첫 시험관이 양수와 음수의 부호를 사용한 표시법을 묻습니다. 해저의 수치를 기호로 바르게 나타내십시오.", "qtext": "<strong>Q1. [양수와 음수]</strong><br>해발 1000m를 +1000m로 나타낼 때, 해저 500m는 어떻게 나타내는가?", "placeholder": "예: -300m", "error": "마력이 충돌합니다! 방향과 부호를 다시 확인하십시오.", "ans_check": "ans === '-500m' || ans === '-500'"},
    {"qnum": 2, "title": "정수의 조건", "story": "🔮 <strong>[마법 스크롤 선별]</strong><br><br>다양한 수가 적힌 종이 중 정수가 아닌 속성을 골라내어 마법진에서 소거해야 문이 열립니다.", "qtext": "<strong>Q2. [정수의 판별]</strong><br>다음 중 정수가 아닌 것의 번호를 쓰시오.<br>(1) -3 &nbsp;&nbsp;(2) 0 &nbsp;&nbsp;(3) 1.5 &nbsp;&nbsp;(4) 7", "placeholder": "보기 번호 입력", "error": "스파크가 튑니다! 정수가 아닌 수를 다시 골라 보십시오.", "ans_check": "ans === '3' || ans === '1.5' || ans === '(3)'"},
    {"qnum": 3, "title": "수직선의 기점", "story": "🔮 <strong>[마력 수직선의 기점]</strong><br><br>공중에 투사된 마력선 위의 눈금 0을 가리키는 한글 단어를 묻는 단어 퀴즈 자물쇠입니다.", "qtext": "<strong>Q3. [원점]</strong><br>수직선에서 0을 나타내는 점을 무엇이라 하는가?", "placeholder": "한글 단어 입력", "error": "수직선 기점이 정렬되지 않습니다!", "ans_check": "ans === '원점'"},
    {"qnum": 4, "title": "정수의 개수", "story": "🔮 <strong>[차원의 문 양단]</strong><br><br>-5 차원과 3 차원 사이에 떠다니는 순수한 정수 결정들의 총 개수를 연산하십시오.", "qtext": "<strong>Q4. [두 수 사이의 정수]</strong><br>-5와 3 사이에 있는 정수는 모두 몇 개인가?", "placeholder": "숫자 또는 개수 입력", "error": "수치가 맞지 않아 문이 닫힙니다!", "ans_check": "ans === '7' || ans === '7개'"},
    {"qnum": 5, "title": "속성 에너지 융합", "story": "🔮 <strong>[마력의 좌표 합성]</strong><br><br>원점으로부터의 거리 조건과 상대적 크기 정보를 조합하여 최종 합성된 에너지값 a+b를 도출해 내십시오.", "qtext": "<strong>Q5. [수직선 위의 점]</strong><br>두 정수 a, b에 대하여 a는 원점으로부터의 거리가 4이고, b는 -2보다 3만큼 큰 수이다. a가 양수일 때 a+b의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "융합 실패! 에너지 폭발 조짐이 보입니다.", "ans_check": "ans === '5'"},
    {"qnum": 6, "title": "마법 절댓값 장벽", "story": "📜 <strong>[절댓값 연산 장벽]</strong><br><br>두 수의 절댓값 합을 맞춰야만 계단을 막고 있는 마법 보라색 장벽이 걷힙니다.", "qtext": "<strong>Q6. [절댓값 계산]</strong><br>|-7| + |3| 의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "장벽의 절댓값이 꿈쩍도 하지 않습니다!", "ans_check": "ans === '10'"},
    {"qnum": 7, "title": "상반되는 속성의 거리", "story": "📜 <strong>[최대 거리 추출]</strong><br><br>절댓값이 4인 두 상반된 지점 사이의 실제 물리적 거리를 계산하여 동력선에 입력하십시오.", "qtext": "<strong>Q7. [절댓값의 성질]</strong><br>절댓값이 4인 두 수의 차를 구하시오. (큰 수에서 작은 수를 뺌)", "placeholder": "숫자만 입력", "error": "수치 동조 실패! 축의 거리가 맞지 않습니다.", "ans_check": "ans === '8'"},
    {"qnum": 8, "title": "최강의 절댓값 보석", "story": "📜 <strong>[크기 비교 홀로그램]</strong><br><br>나열된 다섯 개의 오라클 마력석 중 절댓값 힘이 가장 거대한 원석을 제단에 올리십시오.", "qtext": "<strong>Q8. [절댓값의 대소]</strong><br>다음 수 중 절댓값이 가장 큰 수를 쓰시오.<br>[-2.5, 3, -4, 0, 1.5]", "placeholder": "해당 수 입력 (부호 포함)", "error": "제단이 보석을 밀어냅니다!", "ans_check": "ans === '-4'"},
    {"qnum": 9, "title": "부등식과 영역", "story": "📜 <strong>[영역 격리 밸브]</strong><br><br>조건식 -3 < x <= 2 에 속하는 모든 정수 마나 노드의 개수를 찾아 밸브 압력을 맞추세요.", "qtext": "<strong>Q9. [부등호의 이해]</strong><br>-3 < x <= 2 를 만족하는 정수 x의 개수를 구하시오.", "placeholder": "숫자 또는 개수 입력", "error": "압력이 새어나갑니다! 다시 계산하십시오.", "ans_check": "ans === '5' || ans === '5개'"},
    {"qnum": 10, "title": "균형의 추", "story": "📜 <strong>[중심좌표 조율]</strong><br><br>수직선의 양단 -4 지점과 8 지점의 정확한 물리적 중심 위치(한가운데 정수)를 찾아 조율을 매칭하십시오.", "qtext": "<strong>Q10. [한가운데 있는 수]</strong><br>수직선에서 -4와 8의 한가운데 있는 점이 나타내는 수를 구하시오.", "placeholder": "숫자만 입력", "error": "조율 실패! 추가 비대칭으로 기울어집니다.", "ans_check": "ans === '2'"},
    {"qnum": 11, "title": "기초 마법진 덧셈", "story": "🪄 <strong>[덧셈 진법]</strong><br><br>제 3구역에 진입했습니다. 기초 연산 마법진에 덧셈 수식을 입력해 전력을 공급하십시오.", "qtext": "<strong>Q11. [정수의 덧셈]</strong><br>(-5) + (+8) 의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "마법진에 스파크가 튑니다! 연산이 틀렸습니다.", "ans_check": "ans === '3'"},
    {"qnum": 12, "title": "기초 마법진 뺄셈", "story": "🪄 <strong>[뺄셈 에너지 반전]</strong><br><br>음수를 빼는 반전 수식 에너지를 통제해 회로를 통과시키십시오.", "qtext": "<strong>Q12. [정수의 뺄셈]</strong><br>(+3) - (-7) 의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "반전 에너지가 제어되지 않습니다!", "ans_check": "ans === '10'"},
    {"qnum": 13, "title": "소수점 마나 정렬", "story": "🪄 <strong>[유리수의 덧셈]</strong><br><br>소수점으로 조각난 음의 유리수 마나들의 합을 정밀 튜닝하십시오.", "qtext": "<strong>Q13. [유리수의 덧셈]</strong><br>(-2.5) + (-1.5) 의 값을 구하시오.", "placeholder": "숫자만 입력 (부호 포함)", "error": "마나 강도 어긋남! 폭주 위험!", "ans_check": "ans === '-4'"},
    {"qnum": 14, "title": "3중 혼합 마나", "story": "🪄 <strong>[혼합 연산]</strong><br><br>연속해서 연결된 3중 수식 노드를 계산해 과전류를 상쇄해야 안전하게 나아갈 수 있습니다.", "qtext": "<strong>Q14. [정수의 덧뺄셈 혼합]</strong><br>5 - 9 + 3 의 값을 구하시오.", "placeholder": "숫자만 입력 (부호 포함)", "error": "과전류 차단 실패! 회로 차단 경고!", "ans_check": "ans === '-1'"},
    {"qnum": 15, "title": "기억의 왜곡 복원", "story": "🪄 <strong>[기억 복구 주문]</strong><br><br>테러로 왜곡되어 잘못 덧셈 처리된 어떤 마법 값을 뺄셈으로 다시 바르게 계산해 내십시오.", "qtext": "<strong>Q15. [식의 바른 계산]</strong><br>어떤 수에서 -3을 빼야 할 것을 잘못하여 더했더니 5가 되었다. 바르게 계산한 답을 구하시오.", "placeholder": "숫자만 입력", "error": "왜곡 복원 실패! 기억 마법이 정지됩니다.", "ans_check": "ans === '11'"},
    {"qnum": 16, "title": "대마법 곱셈 시전", "story": "🎇 <strong>[어둠의 곱셈]</strong><br><br>마지막 4구역입니다. 음양 속성이 혼재된 곱셈 결계를 차례대로 무력화하십시오.", "qtext": "<strong>Q16. [정수의 곱셈]</strong><br>(-4) × (+6) 의 값을 구하시오.", "placeholder": "숫자만 입력 (부호 포함)", "error": "곱셈 역류 발생! 차단막이 두꺼워집니다.", "ans_check": "ans === '-24'"},
    {"qnum": 17, "title": "대마법 나눗셈 시전", "story": "🎇 <strong>[음수의 분열]</strong><br><br>음수를 음수로 나누어 마나를 안정적으로 분열시키는 몫을 구하십시오.", "qtext": "<strong>Q17. [정수의 나눗셈]</strong><br>(-15) ÷ (-3) 의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "마나가 불균일하게 분열됩니다!", "ans_check": "ans === '5'"},
    {"qnum": 18, "title": "거듭제곱 마법", "story": "🎇 <strong>[거듭제곱 메아리]</strong><br><br>음수 -2를 3중으로 중첩해 외치는 거듭제곱의 메아리 마법 수치를 해독하십시오.", "qtext": "<strong>Q18. [거듭제곱]</strong><br>$(-2)^3$ 의 값을 구하시오.", "placeholder": "숫자만 입력 (부호 포함)", "error": "메아리가 너무 큽니다! 귀를 막고 다시 입력하세요.", "ans_check": "ans === '-8'"},
    {"qnum": 19, "title": "사칙 혼합 제어", "story": "🎇 <strong>[연산 제어 스크린]</strong><br><br>곱셈과 나눗셈이 혼재된 복합 스크린의 중앙 해답을 계산해 방화벽을 해킹하십시오.", "qtext": "<strong>Q19. [유리수의 사칙혼합 1]</strong><br>$(-2) \\times (-3) - (+10) \\div (-2)$ 의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "해킹 방어 프로토콜 작동! 수치 리셋 경고!", "ans_check": "ans === '11'"},
    {"qnum": 20, "title": "최종 마법진의 해", "story": "🎇 <strong>[마법 코어 잠금 해제]</strong><br><br>최종 아르카나 시험의 마지막 복합 다중 중괄호 수식을 완전하게 풀어 마법 학교 입학 증서를 획득하십시오!", "qtext": "<strong>Q20. [유리수의 사칙혼합 2]</strong><br>$12 - [ 5 - \\{ (-2) \\times 3 - 4 \\} ]$ 의 값을 구하시오.", "placeholder": "숫자만 입력 (부호 포함)", "error": "시험 통과 실패! 최종 마나 코어가 작동하지 않습니다.", "ans_check": "ans === '-3'"}
]

panels_html = ""
for q in qs:
    qnum = q['qnum']
    title = q['title']
    story = q['story']
    qtext = q['qtext']
    placeholder = q['placeholder']
    error = q['error']
    
    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel">
            <h2>제 {qnum}구역: {title}</h2>
            <img src="assets/m1_02_rational_numbers/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="question-box">
                <div class="question-content">
                    {qtext}
                    <div class="input-group">
                        <input type="text" id="ans{qnum}" placeholder="{placeholder}">
                    </div>
                </div>
            </div>
            <div class="error-msg" id="error{qnum}">{error}</div>
            <div class="btn-group">
                <button class="btn" onclick="checkQ{qnum}()">{'마법 시전 시작' if qnum==1 else '다음으로'}</button>
            </div>
        </div>
'''
    panels_html += panel

outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>시험 합격!</h1>
            <h2>아르카나 마법 학교 입학 허가</h2>
            <img src="assets/m1_02_rational_numbers/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">마지막 패스코드 '-3'을 입력하고 주문을 외우자, 거대한 연산 마법진이 황금빛 오라를 뿜어내며 하늘 높이 솟아오릅니다! 
                이마에 찬란한 입학 허가 인장이 새겨지고 시험장의 철문이 천천히 열리며 환호하는 아카데미 선배들이 나타납니다. 
                정수와 유리수의 완벽한 사칙연산 제어로 험난한 마력 결계를 돌파해 낸 신입 마법사, 아르카나 수석 입학을 대성공으로 축하합니다!</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

js_checks = ""
for q in qs:
    qnum = q['qnum']
    ans_check = q['ans_check']
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    victory_call = 'try { playVictory(); } catch(e) {}' if qnum == 20 else 'try { playSuccess(); } catch(e) {}'
    
    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace('(','').replace(')','');
            if ({ans_check}) {{
                {victory_call} 
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                showError('panel_q{qnum}', 'error{qnum}');
            }}
        }}
'''
    js_checks += js

# Compile
new_content = re.sub(r'<!-- Q1.*?-->', lambda m: '<!-- Q1 -->\n' + panels_html + '\n    ', base_html, flags=re.DOTALL)
new_content = re.sub(r'// Q1[\s\S]*?(?=window\.onload = \(\) => \{)', lambda m: '// Q1\n' + js_checks + '\n        ', new_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("app_m1_02_escape_room.html created successfully.")
