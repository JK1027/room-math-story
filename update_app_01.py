import re
import os

html_file = 'app_m1_01_escape_room.html'
base_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>장영실의 공방과 멈춰버린 조선: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #18120F;
            --glass-bg: rgba(30, 20, 15, 0.75);
            --glass-border: rgba(229, 169, 60, 0.25);
            --accent: #E5A93C;
            --accent-hover: #F2C063;
            --text-main: #F4EBE1;
            --text-muted: #A89F91;
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
                radial-gradient(circle at 20% 30%, rgba(229, 169, 60, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(139, 92, 26, 0.15) 0%, transparent 40%);
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
            border-top: 1px solid rgba(229, 169, 60, 0.4);
            border-left: 1px solid rgba(229, 169, 60, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(229, 169, 60, 0.05);
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
            text-shadow: 0 0 30px rgba(229, 169, 60, 0.3);
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
            border: 1px solid rgba(229, 169, 60, 0.2);
        }

        .story-box {
            position: relative;
            background: linear-gradient(90deg, rgba(55, 40, 30, 0.5) 0%, rgba(0,0,0,0.3) 100%);
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
            color: rgba(229, 169, 60, 0.05);
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
            border: 1px solid rgba(229, 169, 60, 0.3);
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
            box-shadow: 0 0 15px rgba(229, 169, 60, 0.4), inset 0 2px 4px rgba(0,0,0,0.5);
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
            background: linear-gradient(90deg, #B95C1A, var(--accent));
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
            background: linear-gradient(135deg, #A16207, #78350F);
            color: white;
            border: 1px solid #D97706;
            padding: 0.6rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 900;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 3px;
            width: 100%;
            box-shadow: 0 10px 25px rgba(120, 53, 15, 0.5), inset 0 2px 5px rgba(255,255,255,0.3);
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
            box-shadow: 0 15px 30px rgba(229, 169, 60, 0.5), inset 0 2px 5px rgba(255,255,255,0.5);
            border-color: #F59E0B;
        }

        .btn:active {
            transform: translateY(1px);
        }

        .sound-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(30, 20, 15, 0.6);
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
            background: #1e140f;
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
            <img src="assets/m1_01_prime_factorization/intro.png" alt="Background" class="panel-image">
            <h1>앙부일구와 자격루</h1>
            <h2>멈춰버린 조선의 시간을 돌려라</h2>
            <div class="story-box">
                <div class="story-text">
                    여러분은 국립중앙박물관에서 낡은 해시계를 만졌다가 1434년 조선 시대 장영실의 공방으로 타임슬립했습니다.<br><br>
                    장영실은 일식 예측을 실패해 참형에 처해질 위기입니다!<br><br>
                    공방 곳곳에 숨겨진 수학 단서를 20개 해결해 앙부일구와 자격루를 복구하고 일식의 정확한 시각을 계산하여 역사를 되돌리세요!
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group" style="margin-top: 2rem; width:100%;">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 5)">시스템 복구 가동</button>
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

        // 엔터키 정답 제출 바인딩
        document.addEventListener('keydown', function(e) {
            if (e.target && e.target.id.startsWith('ans') && e.key === 'Enter') {
                const qnum = e.target.id.replace('ans', '');
                const activePanel = e.target.closest('.glass-panel');
                if (activePanel) {
                    const btn = activePanel.querySelector('.btn-group .btn');
                    if (btn) btn.click();
                }
            }
        });

        // 오디오 로드 에러 복구/예외 방어선
        window.addEventListener('DOMContentLoaded', () => {
            const audios = [
                document.getElementById('bgm'),
                document.getElementById('sndClick'),
                document.getElementById('sndTick'),
                document.getElementById('sndSuccess'),
                document.getElementById('sndError'),
                document.getElementById('sndVictory')
            ];
            audios.forEach(audio => {
                if (audio) {
                    audio.addEventListener('error', (e) => {
                        console.warn(`사운드 리소스 로드 실패: ${audio.id}`);
                    });
                }
            });
        });

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

        // Q1

        window.onload = () => {
            const introPanel = document.getElementById('intro');
            const introStoryBox = introPanel.querySelector('.story-box');
            if (introStoryBox) typeWriterHTML(introStoryBox, 25);
        };
    </script>

    <div id="storyLogModal" class="log-modal">
        <div class="log-content">
            <button class="close-log" onclick="closeLog()">닫기 ✕</button>
            <h2>📜 지나온 역사 기록</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>

</body>
</html>
"""

qs = [
    {"qnum": 1, "title": "공방 서랍 열기", "story": "🕰️ <strong>[공방 비밀 서랍]</strong><br><br>장영실의 공방 서랍장에 낡은 놋쇠 자물쇠가 걸려 있습니다. 10 이하의 소수 개수를 입력해야만 열릴 것 같습니다.", "qtext": "<strong>Q1. [소수와 합성수]</strong><br>10 이하의 자연수 중 소수는 모두 몇 개인가?", "placeholder": "숫자 또는 개수 입력", "error": "자물쇠가 굳게 닫혀 있습니다! 숫자를 다시 세어 보십시오.", "ans_check": "ans === '4' || ans === '4개'"},
    {"qnum": 2, "title": "비밀 금고 수색", "story": "🕰️ <strong>[두 번째 상자]</strong><br><br>서랍을 열자 상패 형태의 나무 금고가 보입니다. 15 이하의 소수들을 모두 합한 값을 맞춰야만 덮개가 열립니다.", "qtext": "<strong>Q2. [소수의 합]</strong><br>15 이하의 소수의 합을 구하시오.", "placeholder": "숫자만 입력", "error": "금고에서 불길한 경고음이 납니다!", "ans_check": "ans === '41'"},
    {"qnum": 3, "title": "벽면 문양 해독", "story": "🕰️ <strong>[벽면의 한지 조각]</strong><br><br>벽에 비스듬히 붙어 있는 한지에 네 개의 수가 적혀 있습니다. 합성수가 아닌 수를 골라 아래 받침대를 누르십시오.", "qtext": "<strong>Q3. [합성수 판별]</strong><br>다음 중 합성수가 아닌 것은?<br>(1) 9 &nbsp;&nbsp;(2) 15 &nbsp;&nbsp;(3) 17 &nbsp;&nbsp;(4) 21", "placeholder": "보기 번호 또는 숫자 입력", "error": "벽에서 먼지가 떨어집니다! 잘못 선택했습니다.", "ans_check": "ans === '3' || ans === '17' || ans === '(3)'"},
    {"qnum": 4, "title": "비밀 통로 개방", "story": "🕰️ <strong>[지하 계단]</strong><br><br>벽면이 회전하며 지하 보관소로 가는 돌계단이 나타납니다. 가장 작은 소수와 가장 작은 합성수의 합을 디딤돌에 새겨야 안전합니다.", "qtext": "<strong>Q4. [소수와 합성수의 성질]</strong><br>가장 작은 소수와 가장 작은 합성수의 합을 구하시오.", "placeholder": "숫자만 입력", "error": "계단이 흔들립니다! 함정이 작동하기 전 정답을 입력하세요.", "ans_check": "ans === '6'"},
    {"qnum": 5, "title": "수은 장치 활성화", "story": "🕰️ <strong>[수은 흘려보내기]</strong><br><br>지하 첫 방에 도달하니 수은 운반로가 있습니다. 20 이상 30 이하의 소수 개수만큼 조절 밸브를 돌려야 수은이 정상 흐릅니다.", "qtext": "<strong>Q5. [소수 찾기]</strong><br>20 이상 30 이하의 소수는 모두 몇 개인가?", "placeholder": "숫자 또는 개수 입력", "error": "수은이 역류하려고 합니다! 신속하게 개수를 맞추십시오.", "ans_check": "ans === '2' || ans === '2개'"},
    {"qnum": 6, "title": "앙부일구 암호판", "story": "🔐 <strong>[영침 정렬]</strong><br><br>암실 중앙에 빛나는 앙부일구(해시계) 영침 제어판이 드러납니다. 60의 소인수분해 값에서 2의 지수만큼 영침을 틀어야 조준이 맞습니다.", "qtext": "<strong>Q6. [지수 구하기]</strong><br>60을 소인수분해할 때, 2의 지수는 얼마인가?", "placeholder": "숫자만 입력", "error": "조준 실패! 그림자가 어긋납니다.", "ans_check": "ans === '2'"},
    {"qnum": 7, "title": "앙부일구 암호판", "story": "🔐 <strong>[빛의 굴절 판독]</strong><br><br>영침 끝에서 레이저처럼 반사된 빛이 천장을 비춥니다. 식의 거듭제곱 계산값을 구해야 다음 거울을 회전시킵니다.", "qtext": "<strong>Q7. [거듭제곱의 계산]</strong><br>$2^3 \\times 3^2$ 의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "거울 각도가 틀렸습니다! 빛이 소멸합니다.", "ans_check": "ans === '72'"},
    {"qnum": 8, "title": "앙부일구 암호판", "story": "🔐 <strong>[소인수 정렬]</strong><br><br>두 번째 광선이 황동 암호판으로 유도됩니다. 180의 소인수들의 합을 입력하여 록(Lock)을 푸십시오.", "qtext": "<strong>Q8. [소인수의 합]</strong><br>180의 소인수를 모두 더한 값을 구하시오.", "placeholder": "숫자만 입력", "error": "암호판이 잠겨 움직이지 않습니다!", "ans_check": "ans === '10'"},
    {"qnum": 9, "title": "앙부일구 암호판", "story": "🔐 <strong>[약수 기어 작동]</strong><br><br>암호판의 톱니들이 돌아가기 시작합니다. 72의 약수의 개수를 구하여 톱니 조절판에 입력해야 정상 동기화됩니다.", "qtext": "<strong>Q9. [약수의 개수 1]</strong><br>72의 약수의 개수를 구하시오.", "placeholder": "숫자만 입력", "error": "기어 맞물림 이상! 톱니 개수가 맞지 않습니다.", "ans_check": "ans === '12'"},
    {"qnum": 10, "title": "앙부일구 암호판", "story": "🔐 <strong>[최종 시각 조절]</strong><br><br>해시계 마지막 암호판입니다. 약수의 개수 15개가 될 수 있도록 미지수 a의 값을 구하십시오.", "qtext": "<strong>Q10. [약수의 개수 2]</strong><br>$3^4 \\times 5^a$ 의 약수의 개수가 15개일 때, a의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "동기화 실패! 시간이 어긋납니다.", "ans_check": "ans === '2'"},
    {"qnum": 11, "title": "자격루 동력 복구", "story": "⚙️ <strong>[물통 수압 동기]</strong><br><br>쿵- 하는 소리와 함께 지하 거대 물시계(자격루)의 실린더가 노출됩니다. 24와 36의 최대공약수를 구해 수압 밸브를 개방하십시오.", "qtext": "<strong>Q11. [최대공약수]</strong><br>24와 36의 최대공약수를 구하시오.", "placeholder": "숫자만 입력", "error": "수압 이상! 물통이 파열될 위험이 있습니다!", "ans_check": "ans === '12'"},
    {"qnum": 12, "title": "자격루 동력 복구", "story": "⚙️ <strong>[동력 톱니 동기]</strong><br><br>물이 흘러가며 물레바퀴가 돌기 시작합니다. 두 동력 톱니바퀴 15와 25의 최소공배수를 구하여 속도를 매칭하십시오.", "qtext": "<strong>Q12. [최소공배수]</strong><br>15와 25의 최소공배수를 구하시오.", "placeholder": "숫자만 입력", "error": "속도 불일치! 기어가 헛돕니다.", "ans_check": "ans === '75'"},
    {"qnum": 13, "title": "자격루 동력 복구", "story": "⚙️ <strong>[압축 실린더 평형]</strong><br><br>피스톤 압축기가 상하 운동을 개시합니다. 두 거듭제곱 수의 최대공약수를 구하여 피스톤 높이를 통제하십시오.", "qtext": "<strong>Q13. [거듭제곱의 최대공약수]</strong><br>두 수 $2^2 \\times 3$, $2 \\times 3^2 \\times 5$ 의 최대공약수를 구하시오. (숫자로 환산)", "placeholder": "숫자만 입력", "error": "압축 피스톤 불균형! 진동이 커집니다.", "ans_check": "ans === '6'"},
    {"qnum": 14, "title": "자격루 동력 복구", "story": "⚙️ <strong>[배수 구멍 청소]</strong><br><br>자격루 배수 배관에 슬러지가 꼈습니다. 12와 18의 공약수 개수만큼 메인 밸브를 순간 방출하여 배수관을 청소하십시오.", "qtext": "<strong>Q14. [공약수의 개수]</strong><br>두 수 12, 18의 공약수의 개수는 모두 몇 개인가?", "placeholder": "숫자 또는 개수 입력", "error": "배수가 막혔습니다! 수조가 넘치려 합니다.", "ans_check": "ans === '4' || ans === '4개'"},
    {"qnum": 15, "title": "자격루 동력 복구", "story": "⚙️ <strong>[최종 부력 동조]</strong><br><br>부력 띄우개 장치가 마침내 수면에 뜹니다. 두 수의 최소공배수를 유도하여 마지막 동조 코드를 완성하세요.", "qtext": "<strong>Q15. [최소공배수의 성질]</strong><br>두 수의 곱이 300이고 최대공약수가 5일 때, 이 두 수의 최소공배수를 구하시오.", "placeholder": "숫자만 입력", "error": "부력 균형 붕괴! 부표가 가라앉습니다.", "ans_check": "ans === '60'"},
    {"qnum": 16, "title": "일식 관측과 시간 톱니", "story": "⏱️ <strong>[정사각형 황동판 타일]</strong><br><br>천장을 바라볼 수 있는 망원경(일식 관측 의기) 관측 대를 복구합니다. 벽면 가로 18, 세로 24를 가장 큰 정사각형 타일로 빈틈없이 채우기 위해 타일 한 변의 길이를 결정하세요.", "qtext": "<strong>Q16. [최대공약수 활용]</strong><br>가로 18cm, 세로 24cm인 직사각형 벽을 가능한 큰 정사각형 타일로 빈틈없이 채우려 한다. 타일 한 변의 길이를 구하시오. (단위 생략)", "placeholder": "숫자 또는 cm 입력", "error": "타일 배치 실패! 벽면이 무너집니다.", "ans_check": "ans === '6' || ans === '6cm'"},
    {"qnum": 17, "title": "일식 관측과 시간 톱니", "story": "⏱️ <strong>[톱니바퀴 맞물림]</strong><br><br>관측 회전 기어를 조절합니다. 톱니수 12개와 18개인 A, B 기어가 처음으로 다시 만날 때까지 기어 A가 몇 바퀴를 돌아야 합니까?", "qtext": "<strong>Q17. [최소공배수 활용 1]</strong><br>톱니수가 각각 12개, 18개인 두 톱니바퀴 A, B가 맞물려 돌 때, 처음으로 다시 같은 톱니에서 맞물리려면 A는 몇 바퀴를 돌아야 하는가?", "placeholder": "숫자 또는 바퀴 수 입력", "error": "기어 스펙이 안 맞습니다! 회전이 멈춥니다.", "ans_check": "ans === '3' || ans === '3바퀴'"},
    {"qnum": 18, "title": "일식 관측과 시간 톱니", "story": "⏱️ <strong>[관측 거울 간격]</strong><br><br>햇빛을 적절히 차단할 렌즈 간격을 연산해야 합니다. 나눗셈의 나머지를 역이용하여 최고 간격 수치를 구하세요.", "qtext": "<strong>Q18. [최대공약수 활용 2]</strong><br>어떤 수로 37을 나누면 1이 남고, 46을 나누면 2가 남는다. 이러한 수 중 가장 큰 수를 구하시오.", "placeholder": "숫자만 입력", "error": "렌즈 초점이 맞지 않아 일식이 보이지 않습니다!", "ans_check": "ans === '4'"},
    {"qnum": 19, "title": "일식 관측과 시간 톱니", "story": "⏱️ <strong>[신호용 북 타이머]</strong><br><br>일식의 시작을 전 궁궐에 알릴 두 대고의 북 연타 타이머를 맞춥니다. 10분, 15분 간격으로 치는 북이 오전 9시 이후 처음 동시 작동하는 시간을 구하세요.", "qtext": "<strong>Q19. [최소공배수 활용 2]</strong><br>버스 A는 10분, 버스 B는 15분 간격으로 출발한다. 오전 9시에 동시에 출발했다면, 다음으로 처음 동시에 출발하는 시각은 9시 몇 분인가? (분만 입력)", "placeholder": "숫자 또는 분 입력", "error": "북 신호가 어긋나 백성들이 혼란에 빠집니다!", "ans_check": "ans === '30' || ans === '30분'"},
    {"qnum": 20, "title": "일식 관측과 시간 톱니", "story": "⏱️ <strong>[최종 일식 시작 시각]</strong><br><br>일식이 진행될 최종 일시 정합 비밀코드를 계산하세요! 3, 4, 5 어느 수로 나누어도 2가 남는 가장 작은 세 자리 자연수입니다.", "qtext": "<strong>Q20. [최소공배수 활용 3]</strong><br>3, 4, 5 어느 수로 나누어도 2가 남는 가장 작은 세 자리 자연수를 구하시오.", "placeholder": "숫자만 입력", "error": "암호 실패! 일식 예측 보고가 불가능합니다!", "ans_check": "ans === '122'"}
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
            <img src="assets/m1_01_prime_factorization/q{qnum}.png" alt="Background" class="panel-image">
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
                <button class="btn" onclick="checkQ{qnum}()">{'시스템 복구 시작' if qnum==1 else '다음으로'}</button>
            </div>
        </div>
'''
    panels_html += panel

outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>앙부일구와 자격루 복구 완료</h2>
            <img src="assets/m1_01_prime_factorization/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">정답 122를 입력하자 멈춰있던 자격루가 장엄한 종소리와 함께 힘차게 돌아가며 일식의 정확한 시각을 조명판에 투사합니다! 
                동시에 저 멀리서 장영실의 일식 예측 성공을 축하하는 전령의 외침이 들려오고 참형 집행이 즉시 중단됩니다. 
                그 순간 찬란한 광채가 여러분을 감싸더니 다시 국립중앙박물관의 한 전시실로 소환됩니다. 소인수분해와 공배수의 비밀로 역사를 멋지게 구했습니다!</div>
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

print("app_m1_01_escape_room.html created successfully.")
