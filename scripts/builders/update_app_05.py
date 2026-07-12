import re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_05_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>다빈치의 비밀 작업실: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #201A15;
            --glass-bg: rgba(35, 28, 22, 0.75);
            --glass-border: rgba(205, 133, 63, 0.25);
            --accent: #CD853F;
            --accent-hover: #D2B48C;
            --text-main: #FDF5E6;
            --text-muted: #D3C2B0;
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
                radial-gradient(circle at 20% 30%, rgba(205, 133, 63, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(139, 92, 26, 0.12) 0%, transparent 40%);
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
            border-top: 1px solid rgba(205, 133, 63, 0.4);
            border-left: 1px solid rgba(205, 133, 63, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(205, 133, 63, 0.05);
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
            text-shadow: 0 0 30px rgba(205, 133, 63, 0.3);
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
            height: auto;
            max-height: 250px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
        }

        .story-box {
            position: relative;
            background: linear-gradient(90deg, rgba(60, 45, 30, 0.5) 0%, rgba(0,0,0,0.3) 100%);
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
            color: rgba(205, 133, 63, 0.05);
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
            border: 1px solid rgba(205, 133, 63, 0.3);
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
            box-shadow: 0 0 15px rgba(205, 133, 63, 0.4), inset 0 2px 4px rgba(0,0,0,0.5);
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
            background: linear-gradient(90deg, #B45309, var(--accent));
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
            background: linear-gradient(135deg, #B45309, #78350F);
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
            box-shadow: 0 15px 30px rgba(205, 133, 63, 0.5), inset 0 2px 5px rgba(255,255,255,0.5);
            border-color: #F59E0B;
        }

        .btn-hint {
            display: inline-block;
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid rgba(16, 185, 129, 0.5);
            color: #34D399;
            padding: 4px 10px;
            font-size: 0.85rem;
            font-weight: 700;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            vertical-align: middle;
            margin-left: 10px;
            letter-spacing: 0.5px;
            text-transform: none;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        .btn-hint:hover {
            background: rgba(16, 185, 129, 0.4);
            color: #fff;
            box-shadow: 0 0 10px rgba(52, 211, 153, 0.4);
        }


        .btn:active {
            transform: translateY(1px);
        }

        .sound-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(35, 28, 22, 0.6);
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
            background: #231B15;
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
            <img src="assets/m1_05_basic_geometry/intro.png" alt="Background" class="panel-image">
            <h1>다빈치의 비밀 작업실</h1>
            <h2>르네상스 기하학의 수수께끼</h2>
            <div class="story-box">
                <div class="story-text">
                    르네상스 시대의 천재, 레오나르도 다빈치의 숨겨진 비밀 작업실에 도달했습니다.<br><br>
                    하지만 이 작업실은 침입자를 막기 위해 복잡한 기하학적 장치들로 굳게 봉인되어 있습니다.<br><br>
                    설계도의 점, 선, 각도, 그리고 삼각형의 비밀을 풀어 20개의 수수께끼 결계를 해결하고 걸작을 공개하세요!
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group" style="margin-top: 2rem; width:100%;">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 5)">수수께끼 해독 가동</button>
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

        let timeLeft = 40 * 60;
        let timerId = null;

        function updateTimerDisplay() {
            let m = Math.floor(timeLeft / 60);
            let s = timeLeft % 60;
            let timeStr = (m < 10 ? '0'+m : m) + ':' + (s < 10 ? '0'+s : s);
            document.querySelectorAll('.game-timer').forEach(el => el.innerText = timeStr);
        }

        function startTimer() {
            if (timerId) return;
            updateTimerDisplay();
            timerId = setInterval(() => {
                timeLeft--;
                if (timeLeft <= 0) {
                    clearInterval(timerId);
                    updateTimerDisplay();
                    alert("⏰ 제한 시간 40분이 초과되었습니다! 미궁에 영원히 갇혔습니다...");
                    location.reload();
                } else {
                    updateTimerDisplay();
                }
            }, 1000);
        }

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

        let wrongCount = 0;
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
            if (currentId === 'intro') startTimer();
            if (nextId === 'outro') clearInterval(timerId);
            try { playClick(); } catch(e) {}
            if(currentId === 'intro') {
                try { startBGM(); } catch(e) {}
            }

            const currentEl = document.getElementById(currentId);
            const nextEl = document.getElementById(nextId);
            const progContainer = document.getElementById('progressContainer');
            const progBar = document.getElementById('progressBar');

            if (currentEl) currentEl.classList.remove('active');
    
            setTimeout(() => {
                if(nextId !== 'intro' && progContainer) progContainer.style.display = 'block';
                if(progBar) progBar.style.width = progressPercent + '%';
                if(nextEl) {
                    nextEl.classList.add('active');
            
                    const toHide = nextEl.querySelectorAll('.question-box, .btn-group');
                    toHide.forEach(el => {
                        el.style.opacity = '0';
                        el.style.transform = 'translateY(10px)';
                        el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
                        el.style.pointerEvents = 'none';
                    });
            
                    const storyBox = nextEl.querySelector('.story-box');
                    if(storyBox) {
                        typeWriterHTML(storyBox, 25, () => {
                            toHide.forEach(el => {
                                el.style.opacity = '1';
                                el.style.transform = 'translateY(0)';
                                el.style.pointerEvents = 'auto';
                            });
                        });
                    } else {
                        toHide.forEach(el => {
                            el.style.opacity = '1';
                            el.style.transform = 'translateY(0)';
                            el.style.pointerEvents = 'auto';
                        });
                    }
                }
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
            <h2>📜 지나온 기하학 기록</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>

</body>
</html>
"""

qs = [
    {"qnum": 1, "title": "도형의 3요소", "story": "📐 <strong>[양피지 도면 스케치]</strong><br><br>다빈치의 책상에 기하학의 시작을 알리는 스케치북이 펼쳐져 있습니다. 도형을 만드는 기본 3요소를 완성하십시오.", "qtext": "<strong>Q1. [도형의 기본 요소]</strong><br>도형을 구성하는 가장 기본이 되는 요소 세 가지는 점, 선, 그리고 무엇인가?", "placeholder": "한글 단어 입력", "error": "도형이 입체적으로 구성되지 않습니다! 3요소를 다시 쓰십시오.", "ans_check": "ans === '면'", "hint": "도형을 구성하는 가장 기본 요소인 점, 선, 면 중 마지막 요소를 생각해 봅니다."},
    {"qnum": 2, "title": "두 점을 잇는 직선", "story": "📐 <strong>[직선 스케일러]</strong><br><br>나무 제어반 위에 두 금속 핀 A, B가 고정되어 있습니다. 이 두 점을 완전히 통과할 수 있는 단 하나의 직선 개수를 도출하십시오.", "qtext": "<strong>Q2. [직선의 결정]</strong><br>서로 다른 두 점 A, B를 지나는 직선은 모두 몇 개인가?", "placeholder": "숫자 또는 개수 입력", "error": "직선이 어긋납니다! 개수를 확인하세요.", "ans_check": "ans === '1' || ans === '1개'", "hint": "한 점에서 다른 한 점을 향해 자를 대고 그을 수 있는 직선은 오직 하나뿐입니다."},
    {"qnum": 3, "title": "뻗어가는 광선", "story": "📐 <strong>[렌즈 광선 방출]</strong><br><br>시작점 A에서 나와 조절 반사경 B를 지나 끝없이 뻗어 나가는 성질의 기하학적 도형 명칭을 쓰시오.", "qtext": "<strong>Q3. [선분과 반직선]</strong><br>점 A에서 시작하여 점 B 방향으로 끝없이 뻗어 나가는 선분을 기호로 나타낼 때, 이를 무엇이라 부르는가?", "placeholder": "한글 단어 입력", "error": "광선의 방향이나 명칭이 잘못되었습니다!", "ans_check": "ans === '반직선' || ans === '반직선ab'", "hint": "한 점에서 시작하여 다른 점 방향으로 끝없이 뻗어 나가는 선의 명칭을 구합니다."},
    {"qnum": 4, "title": "수평의 각도", "story": "📐 <strong>[수평 평형추]</strong><br><br>작업대 기울기가 한쪽으로 쏠려 있습니다. 완벽하게 평평한 수평 상태의 각도 명칭을 입력해 수평추를 고정시키세요.", "qtext": "<strong>Q4. [평각]</strong><br>180도인 각을 무엇이라 부르는가?", "placeholder": "한글 단어 입력", "error": "추가 수평을 유지하지 못하고 떨어집니다!", "ans_check": "ans === '평각'", "hint": "평평한 일직선이 이루는 각으로, 한자 '평평할 평'을 사용하는 각의 명칭입니다."},
    {"qnum": 5, "title": "다빈치의 벽시계", "story": "📐 <strong>[기계식 추시계]</strong><br><br>벽면에 나뭇가지 기어로 된 추시계 바늘이 4시 정각에 걸려 멈췄습니다. 시침과 분침 사이의 좁은 쪽 각도를 입력해 시계를 다시 작동시키세요.", "qtext": "<strong>Q5. [시계 각도]</strong><br>시계가 4시 정각을 가리킬 때, 시침과 분침이 이루는 작은 쪽의 각의 크기를 구하시오. (단위 생략)", "placeholder": "숫자 또는 각도 입력", "error": "톱니가 제대로 돌지 못합니다! 각도를 확인하십시오.", "ans_check": "ans === '120' || ans === '120도'", "hint": "시계의 한 시간 간격(한 칸)은 30도를 이룹니다. 4시 정각일 때 두 바늘 사이의 칸수를 세어 30도에 곱합니다."},
    {"qnum": 6, "title": "교차하는 빛줄기", "story": "✂️ <strong>[교차 거울 방호벽]</strong><br><br>지하 복도 양쪽에서 나온 두 빛줄기가 한 점에서 교차해 사각 문양이 나타납니다. 서로 마주 보며 대칭을 이루는 두 각의 이름을 대십시오.", "qtext": "<strong>Q6. [교각과 맞꼭지각]</strong><br>두 직선이 교차할 때 생기는 교각 중, 마주 보는 두 각을 무엇이라 하는가?", "placeholder": "한글 단어 입력", "error": "문양의 중심이 어긋납니다!", "ans_check": "ans === '맞꼭지각'", "hint": "두 직선이 교차하여 만날 때 서로 마주 보는 쌍으로 존재하는 두 각을 의미합니다."},
    {"qnum": 7, "title": "맞꼭지각의 성질", "story": "✂️ <strong>[반사 평형]</strong><br><br>마주 보는 거울의 크기 비율을 묻습니다. 맞꼭지각의 크기 성질을 한마디로 적으십시오.", "qtext": "<strong>Q7. [맞꼭지각의 크기]</strong><br>맞꼭지각의 크기는 서로 어떠한가? (같다 / 다르다)", "placeholder": "예: 같다", "error": "반사 평형이 성립하지 않습니다!", "ans_check": "ans === '같다'", "hint": "서로 마주 보는 맞꼭지각의 크기는 항상 서로 같은 성질을 가집니다."},
    {"qnum": 8, "title": "평행선의 법칙 1", "story": "✂️ <strong>[평행 빔 통로]</strong><br><br>평행하게 달리는 두 철 레일 l과 m 위에 직각 대각선 n이 놓였습니다. 같은 위치에 대응하는 두 동위각의 크기 관계는 어떠합니까?", "qtext": "<strong>Q8. [동위각]</strong><br>직선 l과 m이 평행하고 한 직선 n과 만날 때, 동위각의 크기는 서로 어떠한가? (같다 / 다르다)", "placeholder": "예: 같다", "error": "평행 빔이 엇갈려 차단 장벽이 다시 활성화됩니다!", "ans_check": "ans === '같다'", "hint": "두 직선이 평행할 때, 같은 위치에 있는 동위각의 크기는 항상 서로 같습니다."},
    {"qnum": 9, "title": "평행선의 법칙 2", "story": "✂️ <strong>[엇각 센서 조율]</strong><br><br>철 레일 교차점 반대편의 어긋난 엇각 센서 각도를 정렬해야 합니다. 엇각의 크기 성질은 서로 어떠합니까?", "qtext": "<strong>Q9. [엇각]</strong><br>평행한 두 직선 사이를 가로지르는 선이 있을 때, 엇각의 크기는 서로 어떠한가? (같다 / 다르다)", "placeholder": "예: 같다", "error": "센서 각도 매칭 실패!", "ans_check": "ans === '같다'", "hint": "두 직선이 평행할 때, 엇갈린 위치에 있는 엇각의 크기는 서로 같습니다."},
    {"qnum": 10, "title": "최종 평행 조건", "story": "✂️ <strong>[평행 잠금 링]</strong><br><br>문 고리 톱니를 잠급니다. 두 직선이 평행할 최종 조건 중 하나는 동위각이 같거나 무엇이 같은 경우입니까?", "qtext": "<strong>Q10. [평행선 조건]</strong><br>두 직선이 평행할 조건 중 하나는 동위각의 크기가 같거나 무엇의 크기가 같은 경우인가?", "placeholder": "한글 단어 입력", "error": "문 고리가 고정되지 않고 헛돕니다!", "ans_check": "ans === '엇각'", "hint": "두 직선이 평행할 조건 중 하나는 동위각 또는 엇각의 크기가 서로 같은 경우입니다."},
    {"qnum": 11, "title": "도구 없는 수작업", "story": "📏 <strong>[설계판 도구함]</strong><br><br>3구역 작도의 방입니다. 오직 눈금 없는 황동 자와 회전 컴퍼스만으로 선을 그리는 기하학적 행위를 무엇이라 부릅니까?", "qtext": "<strong>Q11. [작도의 정의]</strong><br>눈금 없는 자와 컴퍼스만을 사용하여 도형을 그리는 것을 무엇이라 하는가?", "placeholder": "한글 단어 입력", "error": "도구 선택법이 기하학 원칙에 어긋납니다!", "ans_check": "ans === '작도'", "hint": "눈금 없는 자와 컴퍼스 단 두 도구만 사용하여 도형을 그리는 수학적 작도법을 뜻합니다."},
    {"qnum": 12, "title": "길이의 복사", "story": "📏 <strong>[황동 컴퍼스 보정]</strong><br><br>특정 선분의 길이를 그대로 복사해 가로축 목재 보드판 위에 표시하기 위해 사용해야 할 필수 작도 기구를 적으십시오.", "qtext": "<strong>Q12. [작도 도구]</strong><br>길이가 주어진 선분을 다른 직선 위로 옮길 때 주로 사용하는 도구는 무엇인가?", "placeholder": "한글 단어 입력", "error": "길이가 왜곡되었습니다! 엉뚱한 도구를 썼습니다.", "ans_check": "ans === '컴퍼스'", "hint": "주어진 선분의 길이를 그대로 재어서 다른 곳으로 복사해 옮길 때 벌려서 사용하는 도구를 떠올려 봅니다."},
    {"qnum": 13, "title": "삼각형 조립 조건", "story": "📏 <strong>[삼각형 목재 프레임]</strong><br><br>가장 긴 기둥 c가 나머지 두 기둥 a, b의 합보다 어떠해야 삼각형 구조가 견고하게 지탱됩니까?", "qtext": "<strong>Q13. [삼각형의 결정 조건]</strong><br>삼각형의 세 변의 길이가 a, b, c (c가 가장 긴 변)일 때, c는 a+b보다 ( 커야 / 작아야 ) 하는가?", "placeholder": "커야 또는 작아야 입력", "error": "프레임이 연결되지 않고 무너집니다!", "ans_check": "ans === '작아야'", "hint": "가장 긴 변의 길이는 나머지 두 짧은 변의 길이를 더한 값보다 항상 작아야 삼각형이 만들어집니다."},
    {"qnum": 14, "title": "기둥 조립 테스트", "story": "📏 <strong>[세 개의 나무 쐐기]</strong><br><br>준비된 세 쐐기 (3cm, 4cm, 7cm)로 결합 장치 삼각형 지지대를 만들 수 있는지 판별하십시오.", "qtext": "<strong>Q14. [삼각형 조립 판별]</strong><br>다음 세 선분의 길이로 삼각형을 만들 수 있는가? (3cm, 4cm, 7cm) (있다 / 없다)", "placeholder": "있다 또는 없다 입력", "error": "쐐기 길이가 맞물리지 않고 어긋납니다!", "ans_check": "ans === '없다'", "hint": "가장 긴 변인 7cm와 나머지 두 변의 합인 3+4=7cm를 비교하여 삼각형 성립 조건을 따져봅니다."},
    {"qnum": 15, "title": "각도와 변의 작도", "story": "📏 <strong>[마지막 작도 완성]</strong><br><br>두 변의 길이와 그 사이의 각(끼인각)이 주어지면, 단 하나의 고유한 삼각형을 작도할 수 있습니까?", "qtext": "<strong>Q15. [삼각형의 작도 조건]</strong><br>두 변의 길이와 그 끼인각의 크기가 주어졌을 때, 삼각형을 작도할 수 있는가? (있다 / 없다)", "placeholder": "있다 또는 없다 입력", "error": "작도식 오류! 모형이 일그러집니다.", "ans_check": "ans === '있다'", "hint": "두 변의 길이와 그 사이에 낀 각이 주어지면 삼각형은 오직 하나로 결정되므로 작도가 가능합니다."},
    {"qnum": 16, "title": "완벽한 포갬", "story": "🖼️ <strong>[거울 대칭 무늬]</strong><br><br>4구역 미술실입니다. 좌우 모양과 크기가 완벽히 같아 겹쳤을 때 하나로 포개어지는 두 도형의 수학적 관계를 무어라 합니까?", "qtext": "<strong>Q16. [합동의 정의]</strong><br>모양과 크기가 완전히 같아서 포개었을 때 완전히 겹쳐지는 두 도형을 서로 무엇이라 하는가?", "placeholder": "한글 단어 입력", "error": "포개어지지 않고 테두리가 남습니다!", "ans_check": "ans === '합동'", "hint": "두 도형이 크기와 모양이 완벽히 같아서 포개었을 때 완전히 겹쳐지는 관계를 뜻합니다."},
    {"qnum": 17, "title": "세 변의 합동", "story": "🖼️ <strong>[세 쇠사슬의 균형]</strong><br><br>세 변의 길이가 각각 같은 두 삼각형 액자의 합동 조건을 기호 세 글자로 써넣으십시오.", "qtext": "<strong>Q17. [SSS 합동]</strong><br>삼각형의 합동 조건 중 세 변의 길이가 각각 같을 때의 합동을 무엇이라 하는가?", "placeholder": "예: SSS", "error": "합동 매칭 기호가 틀렸습니다!", "ans_check": "ans === 'sss' || ans === 'sss합동'", "hint": "세 변의 길이가 각각 같을 때의 합동 조건으로, 변을 뜻하는 Side의 첫 글자를 딴 기호입니다."},
    {"qnum": 18, "title": "양 변과 사이 각", "story": "🖼️ <strong>[톱니 조작 밸런스]</strong><br><br>두 변의 길이와 그 사이에 끼인각이 같은 기하학적 합동 조건을 기호 세 글자로 써넣으십시오.", "qtext": "<strong>Q18. [SAS 합동]</strong><br>삼각형의 두 변의 길이와 그 끼인각의 크기가 각각 같을 때의 합동 조건을 무엇이라 하는가?", "placeholder": "예: SAS", "error": "기어가 헛돌며 맞물리지 않습니다!", "ans_check": "ans === 'sas' || ans === 'sas합동'", "hint": "두 변(Side)과 그 끼인각(Angle)의 크기가 각각 같을 때의 합동 기호를 떠올려 봅니다."},
    {"qnum": 19, "title": "한 변과 두 각", "story": "🖼️ <strong>[양 날개 조율]</strong><br><br>한 변의 길이와 양 끝각이 같은 날개 양면의 기하학 합동 조건을 기호 세 글자로 써넣으십시오.", "qtext": "<strong>Q19. [ASA 합동]</strong><br>삼각형의 한 변의 길이와 그 양 끝각의 크기가 각각 같을 때의 합동 조건을 무엇이라 하는가?", "placeholder": "예: ASA", "error": "좌우 날개의 조화가 깨져 문이 다시 잠깁니다!", "ans_check": "ans === 'asa' || ans === 'asa합동'", "hint": "한 변(Side)과 그 양 끝각(Angle)의 크기가 각각 같을 때의 합동 기호를 떠올려 봅니다."},
    {"qnum": 20, "title": "최종 마스터 합동 키", "story": "🖼️ <strong>[걸작의 봉인 해제]</strong><br><br>직각삼각형 빗변과 한 예각의 특수 기하학 조건이 완성되었습니다. 두 기하학 파트는 서로 '합동이다 / 아니다' 중 무엇입니까?", "qtext": "<strong>Q20. [합동 판별]</strong><br>직각삼각형에서 빗변의 길이와 한 예각의 크기가 같을 때, 두 삼각형은 합동인 양상을 나타내는가? (합동이다 / 아니다)", "placeholder": "합동이다 또는 아니다 입력", "error": "걸작 모나리자 스크린의 잠금이 해제되지 않습니다!", "ans_check": "ans === '합동이다' || ans === '합동'", "hint": "두 직각삼각형이 완전히 포개어져 크기와 모양이 일치하는지 직관적으로 판단해 봅니다."}
]


import re
def generate_hint(qtext, ans_check):
    qtext_clean = qtext.lower()
    
    if '소인수분해' in qtext_clean: return "주어진 수를 가장 작은 소수부터 차례대로 나누어 소수들의 곱으로 나타내보세요. (거듭제곱 기호 ^ 사용)"
    elif '최대공약수' in qtext_clean: return "공통된 소인수 중 지수가 같거나 가장 작은 것을 선택하여 모두 곱합니다."
    elif '최소공배수' in qtext_clean: return "모든 소인수를 선택하고, 공통된 소인수는 지수가 같거나 가장 큰 것을 선택하여 곱합니다."
    elif '정수' in qtext_clean and '유리수' in qtext_clean: return "양의 부호(+)나 음의 부호(-)를 주의해서 계산하세요. (음수×음수=양수)"
    elif '절댓값' in qtext_clean: return "절댓값은 수직선에서 원점으로부터의 거리이므로 항상 0보다 크거나 같습니다."
    elif '일차방정식' in qtext_clean and '해' in qtext_clean: return "미지수 x를 포함한 항은 좌변으로, 상수는 우변으로 이항하여 x = (숫자) 형태로 만드세요."
    elif '일차함수' in qtext_clean and '기울기' in qtext_clean: return "일차함수 y = ax + b 에서 x의 계수 a가 기울기를 의미합니다."
    elif '일차함수' in qtext_clean and ('y절편' in qtext_clean or 'x절편' in qtext_clean): return "y절편은 x=0일 때의 y값(b), x절편은 y=0일 때의 x값(-b/a)입니다."
    elif '연립방정식' in qtext_clean: return "가감법(두 식을 적절히 곱해 더하거나 빼기)이나 대입법을 사용하여 한 미지수를 먼저 없애보세요."
    elif '부등식' in qtext_clean: return "부등식의 양변에 음수를 곱하거나 나누면 부등호의 방향이 반대로 바뀐다는 점을 잊지 마세요."
    elif '경우의 수' in qtext_clean: return "동시에(연달아) 일어나는 사건은 곱의 법칙(×), 따로 일어나는 사건은 합의 법칙(+)을 적용하세요."
    elif '확률' in qtext_clean: return "(특정 사건이 일어날 경우의 수) / (모든 경우의 수) 로 계산한 분수 형태를 구하세요."
    elif '부피' in qtext_clean and '구' in qtext_clean: return "구의 부피 공식은 4/3 × 파이 × r³ 입니다."
    elif '겉넓이' in qtext_clean and '구' in qtext_clean: return "구의 겉넓이 공식은 4 × 파이 × r² 입니다."
    elif '부피' in qtext_clean and '기둥' in qtext_clean: return "기둥의 부피는 (밑넓이 × 높이) 입니다."
    elif '부피' in qtext_clean and '뿔' in qtext_clean: return "뿔의 부피는 1/3 × (밑넓이 × 높이) 입니다."
    elif '겉넓이' in qtext_clean: return "겉넓이는 전개도를 그렸을 때 모든 면의 넓이의 합입니다."
    elif '다각형' in qtext_clean and '내각' in qtext_clean: return "n각형의 내각의 크기의 합은 180° × (n - 2) 입니다."
    elif '다각형' in qtext_clean and '대각선' in qtext_clean: return "n각형의 대각선의 총 개수는 n(n - 3) / 2 입니다."
    elif '외각' in qtext_clean: return "다각형의 모든 외각의 크기의 합은 항상 360° 입니다."
    elif '닮음비' in qtext_clean: return "닮음비가 m:n 이면, 넓이비는 m²:n², 부피비는 m³:n³ 입니다."
    elif '피타고라스' in qtext_clean or '직각삼각형' in qtext_clean: return "직각삼각형에서 빗변의 길이의 제곱은 나머지 두 변의 길이의 제곱의 합과 같습니다. (a² + b² = c²)"
    elif '소수' in qtext_clean and '합' in qtext_clean: return "1과 자기 자신만을 약수로 가지는 수를 소수라고 합니다. (예: 2, 3, 5, 7...)"
    elif '좌표' in qtext_clean: return "x축의 좌표를 먼저, y축의 좌표를 나중에 (x, y) 형태로 생각해보세요."

    if '파이' in ans_check or 'pi' in ans_check: return "계산된 원주율은 기호 대신 한글 '파이'라고 적어주세요. (예: 36파이)"
    if '(' in ans_check and ',' in ans_check: return "순서쌍은 괄호나 띄어쓰기 없이 숫자와 쉼표로만 입력하거나 (x,y) 형태로 정확히 입력해보세요."
    
    ans_list = []
    if '||' in ans_check:
        ans_list = [a.strip().strip("'\"") for a in ans_check.split('||')]
        valid_ans = [a for a in ans_list if 'ans ===' in a]
        if valid_ans:
            first_ans = valid_ans[0].replace('ans === ', '').strip("'\"")
            return f"단위가 있다면 제외해보고, 기호 유무를 확인하세요. (정답 길이: 약 {len(first_ans)}글자)"
    else:
        match = re.search(r"ans === '([^']+)'", ans_check)
        if match:
            ans = match.group(1)
            if ans.isdigit(): return f"계산 실수가 없는지 다시 확인해보세요. 정답은 {len(ans)}자리 숫자입니다."
            else: return f"정답은 기호나 문자를 포함해 총 {len(ans)}글자입니다."
            
    return "단위(cm, 개 등)를 생략하거나 기호가 정확히 일치하는지 확인해 보세요."

for q in qs:
    q['hint'] = q.get('hint') or generate_hint(q['qtext'], q.get('ans_check', ''))

for q in qs:
    if 'hint' in q and '<button class="btn-hint"' not in q['qtext']:
        hint_text = q['hint'].replace("'", "\\'")
        q['qtext'] = q['qtext'].replace('</strong>', f'</strong> <button class="btn-hint" onclick="alert(\'💡 힌트: {hint_text}\')">💡 힌트</button>', 1)

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
            <h2>제 {qnum}구역: {title} <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="assets/m1_05_basic_geometry/q{qnum}.png" alt="Background" class="panel-image">
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
                <button class="btn" onclick="checkQ{qnum}()">{'작도 활성화 시작' if qnum==1 else '다음으로'}</button>

            </div>
        </div>
'''
    panels_html += panel

outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>봉인 해제!</h1>
            <h2>다빈치의 잃어버린 걸작 복원</h2>
            <img src="assets/m1_05_basic_geometry/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">마지막 패스코드 '합동이다'를 누르고 수수께끼판을 맞추자, 요란하게 회전하는 기계 톱니소리와 함께 다빈치의 작업실 숨겨진 벽면이 서서히 열립니다! 
                그 안에는 현대의 헬리콥터와 낙하산 원형이 담긴 다빈치의 실제 설계 스케치와 걸작 유화 판넬이 화려한 금빛 조명 속에서 웅장하게 서 있습니다. 
                눈금 없는 자와 컴퍼스, 그리고 기하학의 완전한 합동 조건을 이해해 르네상스의 가장 깊은 비밀을 파헤친 요원들, 탈출 완벽 성공입니다!</div>
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
                wrongCount = 0;
                {victory_call} 
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                wrongCount++;
                if (wrongCount >= 3) {{
                    alert("🚨 3회 오답 패널티! 1구역으로 강제 이동됩니다.");
                    wrongCount = 0;
                    document.getElementById('ans1').value = '';
                    nextStage('panel_q{qnum}', 'panel_q1', 0);
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}');
                }}
            }}
        }}
'''
    js_checks += js

# Compile
new_content = re.sub(r'<!-- Q1.*?-->', lambda m: '<!-- Q1 -->\n' + panels_html + '\n    ', base_html, flags=re.DOTALL)
new_content = re.sub(r'// Q1[\s\S]*?(?=window\.onload = \(\) => \{)', lambda m: '// Q1\n' + js_checks + '\n        ', new_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("app_m1_05_escape_room.html created successfully.")
