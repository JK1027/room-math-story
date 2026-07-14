import re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m2_01_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>무한을 달리는 사이버 스피드웨이: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #09090e;
            --glass-bg: rgba(13, 15, 30, 0.75);
            --glass-border: rgba(0, 240, 255, 0.2);
            --accent: #00f0ff;
            --accent-hover: #39f5ff;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
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
                radial-gradient(circle at 10% 20%, rgba(0, 240, 255, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%);
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
            border-top: 1px solid rgba(0, 240, 255, 0.35);
            border-left: 1px solid rgba(0, 240, 255, 0.35);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(0, 240, 255, 0.1), inset 0 0 20px rgba(0, 240, 255, 0.02);
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
            text-shadow: 0 0 30px rgba(0, 240, 255, 0.3);
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
            background: linear-gradient(90deg, rgba(13, 25, 48, 0.6) 0%, rgba(0,0,0,0.3) 100%);
            border-left: 4px solid var(--accent);
            padding: 0.8rem 1.2rem;
            margin-bottom: 1.5rem;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            height: 110px;
            max-height: 110px;
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
            bottom: 10px;
            right: 15px;
            background: rgba(0, 240, 255, 0.15);
            border: 1px solid rgba(0, 240, 255, 0.3);
            color: var(--accent);
            padding: 4px 10px;
            font-size: 0.75rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            z-index: 10;
        }
        .story-log-trigger:hover {
            background: rgba(0, 240, 255, 0.3);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        }

        .question-box {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: inset 0 0 15px rgba(255, 255, 255, 0.02);
        }

        .question-content {
            font-size: 1.1rem;
            line-height: 1.7;
            color: #cbd5e1;
        }

        .input-group {
            margin-top: 1rem;
        }

        input[type="text"] {
            width: 100%;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(0, 240, 255, 0.2);
            padding: 1rem;
            border-radius: 12px;
            color: #fff;
            font-size: 1.1rem;
            font-family: 'Share Tech Mono', monospace;
            text-align: center;
            transition: all 0.3s;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
        }

        input[type="text"]:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.3), inset 0 2px 4px rgba(0, 0, 0, 0.5);
        }

        .error-msg {
            color: #ff4a4a;
            text-align: center;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            display: none;
            text-shadow: 0 0 10px rgba(255, 74, 74, 0.3);
        }

        .btn-group {
            display: flex;
            justify-content: center;
            opacity: 0;
            transform: translateY(10px);
            transition: opacity 0.8s ease, transform 0.8s ease;
            pointer-events: none;
        }

        .btn {
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.2) 0%, rgba(0, 240, 255, 0.05) 100%);
            border: 1px solid var(--accent);
            color: var(--accent);
            padding: 1rem 3rem;
            font-size: 1.1rem;
            font-weight: 900;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
            box-shadow: 0 4px 15px rgba(0, 240, 255, 0.1);
            letter-spacing: 1px;
        }

        .btn:hover {
            background: linear-gradient(135deg, var(--accent) 0%, rgba(0, 240, 255, 0.6) 100%);
            color: #000;
            box-shadow: 0 0 25px rgba(0, 240, 255, 0.6);
            scale: 1.03;
            text-shadow: none;
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


        .sound-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff;
            padding: 6px 12px;
            font-size: 0.8rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            z-index: 100;
        }
        .sound-toggle:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .progress-container {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
            margin-bottom: 2rem;
            overflow: hidden;
            display: none;
        }

        .progress-bar {
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, var(--accent), #a78bfa);
            box-shadow: 0 0 10px var(--accent);
            transition: width 0.5s ease-in-out;
        }

        @keyframes blink {
            50% { opacity: 0; }
        }

        .log-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            z-index: 999;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(10px);
        }
        .log-content {
            background: #0d0f1e;
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            width: 90%;
            max-width: 600px;
            max-height: 70vh;
            padding: 2rem;
            position: relative;
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 40px rgba(0, 240, 255, 0.2);
        }
        .log-content h2 {
            text-align: left;
            font-size: 1.3rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(0, 240, 255, 0.15);
            padding-bottom: 0.5rem;
            color: var(--accent);
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
        #logContainer::-webkit-scrollbar {
            width: 6px;
        }
        #logContainer::-webkit-scrollbar-thumb {
            background: rgba(0, 240, 255, 0.3);
            border-radius: 3px;
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
            transition: transform 0.2s;
        }
        .close-log:hover {
            transform: scale(1.2);
        }

        @media (max-width: 768px) {
            .glass-panel {
                padding: 1.5rem;
                border-radius: 16px;
            }
            h1 {
                font-size: 1.8rem;
            }
            .story-box {
                height: 80px;
                max-height: 80px;
            }
            .story-text {
                font-size: 0.9rem;
            }
        }
    
        /* 화면 진동 효과 */
        @keyframes shake {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            10% { transform: translate(-2px, -1px) rotate(-0.5deg); }
            20% { transform: translate(-3px, 0px) rotate(1deg); }
            30% { transform: translate(0px, 2px) rotate(0deg); }
            40% { transform: translate(1px, -1px) rotate(1deg); }
            50% { transform: translate(-1px, 2px) rotate(-1deg); }
            60% { transform: translate(-3px, 1px) rotate(0deg); }
            70% { transform: translate(2px, 1px) rotate(-0.5deg); }
            80% { transform: translate(-1px, -1px) rotate(1deg); }
            90% { transform: translate(2px, 2px) rotate(0deg); }
        }
        .shake-effect {
            animation: shake 0.3s ease-in-out;
        }

        /* 적색 레이저 섬광 효과 */
        .laser-flash-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(255, 0, 0, 0.4);
            z-index: 9999;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.15s ease-out;
        }
        .laser-flash-overlay.flash-active {
            opacity: 1;
        }

    </style>
    <!-- MathJax for LaTeX Rendering -->
    <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>

    <button id="soundToggle" class="sound-toggle" onclick="toggleSound()">🔊 소리 켜짐</button>

    <div class="container">
        
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <!-- 0. 인트로 -->
        <div id="intro" class="glass-panel active">
            <img src="assets/m2_01_rational_numbers/intro.png" alt="Background" class="panel-image">
            <h1>사이버 스피드웨이</h1>
            <h2>무한의 루프를 해킹하라</h2>
            <div class="story-box">
                <div class="story-text">
                [레이싱 내비게이션 스피드-N]: "사이버 공간 최고의 레이싱 대회 '순환 스피드웨이'에 출전한 여러분!<br><br>
                    우승 트로피를 눈앞에 둔 순간, 악당 해커가 레이싱 트랙을 끝없는 무한 소수의 늪으로 만들어 버렸습니다.<br><br>
                    결승선으로 도달하려면 분수의 무한 순환 패턴을 해독하고, 분수로 변환하여 20개의 방화벽 결계를 뚫고 전속력으로 탈출하십시오!"
            </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group" style="margin-top: 2rem; width:100%;">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 5)">레이싱 시동 가동</button>
            </div>
        </div>

        <!-- Q1 ~ Q20 Panels will be generated here -->
        {panels_placeholder}

        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h2>MISSION ACCOMPLISHED</h2>
            <img src="assets/m2_01_rational_numbers/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text">
                [레이싱 내비게이션 스피드-N]: ""최종 코드를 업로드하는 순간, 계기판의 순환 소수 루프가 일제히 정지합니다!<br><br>
                    끝없이 쪼개지던 트랙이 하나로 아름답게 정렬되며 결승선이 푸른 네온 사인으로 빛납니다.<br><br>
                    최종 부스터를 점화하여 해커의 차단막을 관통하고 마침내 체커기를 받았습니다. 여러분의 승리입니다!""
            </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem; width:100%;" onclick="location.reload()">새로운 레이스 도전</button>
        </div>

    </div>

    <!-- Audio API setup -->
    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        let isMuted = false;

        function playSynth(freq, type, duration, vol=0.1) {
            if (isMuted) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(vol, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }

        function playClick() { playSynth(800, 'sine', 0.08, 0.15); }
        function playTick() { playSynth(1200, 'sine', 0.03, 0.05); }
        function playSuccess() {
            playSynth(600, 'triangle', 0.15, 0.15);
            setTimeout(() => playSynth(900, 'triangle', 0.25, 0.15), 100);
        }
        function playError() {
            playSynth(150, 'sawtooth', 0.3, 0.2);
        }
        function playVictory() {
            const notes = [523, 659, 783, 1046];
            notes.forEach((note, idx) => {
                setTimeout(() => playSynth(note, 'sine', 0.4, 0.15), idx * 150);
            });
        }

        function toggleSound() {
            isMuted = !isMuted;
            document.getElementById('soundToggle').innerText = isMuted ? '🔇 소리 꺼짐' : '🔊 소리 켜짐';
        }

        // Story historical log
        const storyHistory = [];
        function openLog() {
            const logContainer = document.getElementById('logContainer');
            if (storyHistory.length === 0) {
                logContainer.innerHTML = '기록이 없습니다.';
            } else {
                logContainer.innerHTML = storyHistory.map(entry => `<p style="margin-bottom: 0.8rem;">${entry}</p>`).join('');
            }
            document.getElementById('storyLogModal').style.display = 'flex';
        }
        function closeLog() {
            document.getElementById('storyLogModal').style.display = 'none';
        }

        // Typewriter Engine
        let typeWriterTimeout = null;

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

            let rawLines = htmlContent.split(/<br\s*\/?>/i);
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
                const panelTitle = currentPanel.querySelector('h2') ? currentPanel.querySelector('h2').innerText : '안내문';
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
                // start synth BGM or sound
            }
            const currentEl = document.getElementById(currentId);
            const nextEl = document.getElementById(nextId);
            const progContainer = document.getElementById('progressContainer');
            const progBar = document.getElementById('progressBar');
            
            if (currentEl) {
                currentEl.classList.remove('active');
                currentEl.style.display = 'none';
            }
            
            if (nextEl) {
                nextEl.style.display = 'block';
                setTimeout(() => {
                    if(nextId !== 'intro') progContainer.style.display = 'block';
                    progBar.style.width = progressPercent + '%';
                    nextEl.classList.add('active');
                    
                    // Hide elements inside next panel to trigger after typewriter finishes
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
                    }
                }, 50);
            }
        }

        window.onload = () => {
            const introPanel = document.getElementById('intro');
            const introStoryBox = introPanel.querySelector('.story-box');
            const introBtnGroup = introPanel.querySelector('.btn-group');
            
            if (introBtnGroup) {
                introBtnGroup.style.opacity = '0';
                introBtnGroup.style.transform = 'translateY(10px)';
                introBtnGroup.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
                introBtnGroup.style.pointerEvents = 'none';
            }
            
            if (introStoryBox) {
                typeWriterHTML(introStoryBox, 25, () => {
                    if (introBtnGroup) {
                        introBtnGroup.style.opacity = '1';
                        introBtnGroup.style.transform = 'translateY(0)';
                        introBtnGroup.style.pointerEvents = 'auto';
                    }
                });
            }
        };
    </script>

    <div id="storyLogModal" class="log-modal">
        <div class="log-content">
            <button class="close-log" onclick="closeLog()">닫기 ✕</button>
            <h2>📜 지나온 기록 로그</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>

</body>
</html>
"""

qs = [
    {'qnum': 1, 'title': '사이버 트랙 분석', 'story': '[해커-Z]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 🏎️ <strong>[순환 스피드웨이 진입]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"순환 스피드웨이에 오신 것을 환영합니다! 해커가 첫 번째 트랙의 센서를 교란시켜 분수 신호가 차단되었습니다. 분수 $3/4$을 소수로 변환하여 차량 컴퓨터에 입력해야 트랙 분석이 활성화됩니다.\\"\\"', 'qtext': '<strong>Q1. [유리수와 소수]</strong><br>$\\frac{3}{4}$ 을 소수로 나타내시오.', 'placeholder': '예: 0.5', 'error': '트랙 분석 실패! 소수 변환 값이 틀렸습니다.', 'ans_check': "ans === '0.75'"},
    {'qnum': 2, 'title': '유한소수 게이트', 'story': '[해커-Z]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 🏎️ <strong>[유한한 경계]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"첫 번째 게이트에 도착했습니다. 소수점 아래 0이 아닌 숫자가 유한 번만 나타나는 소수의 명칭을 게이트 패널에 입력하십시오.\\"\\"', 'qtext': '<strong>Q2. [유한소수의 뜻]</strong><br>소수점 아래 0이 아닌 숫자가 유한 번 나타나는 소수를 무엇이라 하는가?', 'placeholder': '네 글자 입력 (예: 무한소수)', 'error': '잘못된 보안 코드! 게이트가 열리지 않습니다.', 'ans_check': "ans === '유한소수'"},
    {'qnum': 3, 'title': '엔진 냉각 조율', 'story': '[해커-Z]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 🏎️ <strong>[냉각 장치 조건]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"엔진 과열 경보! 분수가 유한소수로 깨끗하게 떨어지기 위한 기약분수의 분모 소인수 조건을 충전해야 엔진이 정상 작동합니다.\\"\\"', 'qtext': '<strong>Q3. [유한소수 판별 조건]</strong><br>분수를 유한소수로 나타낼 수 있으려면 기약분수로 나타내었을 때 분모의 소인수가 무엇무엇뿐이어야 하는가? (숫자만 쉼표로 구분)', 'placeholder': '예: 2, 5', 'error': '냉각 장치 오작동! 소인수 조건이 틀렸습니다.', 'ans_check': "(ans.includes('2') && ans.includes('5')) || ans === '2또는5' || ans === '2,5'"},
    {'qnum': 4, 'title': '두 갈래 길 선택', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[스피드-N]: \\"치지직... 들리십니까...? 해커-Z의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q4. [유한소수 판별 1]</strong><br>$\\frac{7}{20}$ 은 유한소수인가, 무한소수인가?', 'placeholder': '유한소수 또는 무한소수 입력', 'error': '함정 트랙으로 진입했습니다! 조종 불능!', 'ans_check': "ans === '유한소수'"},
    {'qnum': 5, 'title': '급커브 코스 감속', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[스피드-N]: \\"치지직... 들리십니까...? 해커-Z의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q5. [유한소수 판별 2]</strong><br>$\\frac{13}{30}$ 은 유한소수인가, 무한소수인가?', 'placeholder': '유한소수 또는 무한소수 입력', 'error': '오버스티어 발생! 차량이 트랙 밖으로 밀려납니다.', 'ans_check': "ans === '무한소수'"},
    {'qnum': 6, 'title': '무한 루프 진입', 'story': '[해커-Z]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 🔄 <strong>[루프의 늪]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"제 2구역 무한 루프 구간에 도달했습니다. 일정한 숫자의 배열이 끝없이 되풀이되는 무한소수의 정확한 이름을 입력하여 동기화하십시오.\\"\\"', 'qtext': '<strong>Q6. [순환소수의 뜻]</strong><br>무한소수 중 일정한 숫자의 배열이 끝없이 되풀이되는 소수를 무엇이라 하는가?', 'placeholder': '네 글자 입력', 'error': '동기화 실패! 무한 루프에 영원히 갇힙니다.', 'ans_check': "ans === '순환소수'"},
    {'qnum': 7, 'title': '순환마디 락 해제', 'story': '[해커-Z]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 🔄 <strong>[기본 코드 해독]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"순환소수 0.3333... 의 무한 루프를 끄기 위해 순환마디 점을 찍은 간략화 코드로 해독하십시오. (대괄호 `[]`로 순환마디를 감싸서 입력하세요. 예: 0.[3])\\"\\"', 'qtext': '<strong>Q7. [순환소수 표현 1]</strong><br>0.3333... 을 순환마디에 점을 찍어 간단히 나타낸 기호를 대괄호 형식을 사용하여 쓰시오.', 'placeholder': '예: 0.[3] 또는 0.(3)', 'error': '해독 코드 불일치! 루프 차단막이 강해집니다.', 'ans_check': "ans === '0.[3]' || ans === '0.(3)' || ans === '0.3'"},
    {'qnum': 8, 'title': '트랙 코어 해킹', 'story': '[해커-Z]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 🔄 <strong>[코어 패턴 인식]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"두 번째 루프 코어입니다. 소수 1.252525... 에서 무한히 반복되는 패턴(순환마디) 자체의 값을 찾아내어 입력하십시오.\\"\\"', 'qtext': '<strong>Q8. [순환마디 구하기 1]</strong><br>1.252525... 의 순환마디를 구하시오.', 'placeholder': '예: 25', 'error': '패턴 인식 오류! 코어가 응답하지 않습니다.', 'ans_check': "ans === '25'"},
    {'qnum': 9, 'title': '복합 루프 우회', 'story': '[해커-Z]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 🔄 <strong>[비대칭 패턴 분석]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"순환하지 않는 소수점 자리가 포함된 복합 루프입니다. 0.4565656... 을 대괄호 `[]` 규칙을 적용해 압축 코드로 우회하십시오. (예: 0.4[56])\\"\\"', 'qtext': '<strong>Q9. [순환소수 표현 2]</strong><br>0.4565656... 을 대괄호 형식을 사용하여 간단히 나타내시오.', 'placeholder': '예: 0.4[56]', 'error': '우회 실패! 백신 프로그램에 발각되었습니다.', 'ans_check': "ans === '0.4[56]' || ans === '0.4(56)' || ans === '0.456'"},
    {'qnum': 10, 'title': '루프 마디 압축', 'story': '🚨 <strong>[비상 경보: 강제 자폭 시스템 작동]</strong> 🚨<br><br>[해커-Z]: \\"더는 참을 수 없군! 모든 데이터를 자폭 폭파하겠다! 5분 내로 전부 잿더미로 만들어주지!\\"<br><br>[스피드-N]: \\"경고! 시스템 온도 상승 중! 제가 방화벽을 전개할 동안 긴급 수치 입력을 끝내십시오!\\"', 'qtext': '<strong>Q10. [순환마디 구하기 2]</strong><br>분수 $\\frac{1}{3}$ 을 소수로 나타낼 때, 순환마디는 무엇인가?', 'placeholder': '숫자만 입력', 'error': '압축기 오작동! 기어 압력이 급상승합니다.', 'ans_check': "ans === '3'"},
    {'qnum': 11, 'title': '방화벽 1단계 돌파', 'story': '[스피드-N]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 🧮 <strong>[포트 변환 1]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"제 3구역 방화벽 구역입니다. 1차 포트 보안을 뚫기 위해 순환소수 $0.\\dot{7}$을 분수로 변환하여 록을 해제하십시오. (예: 7/9)\\"\\"', 'qtext': '<strong>Q11. [순환소수를 분수로 1]</strong><br>순환소수 $0.\\dot{7}$ 을 기약분수로 나타내시오.', 'placeholder': '슬래시(/)를 사용하여 입력 (예: 7/9)', 'error': '포트가 즉시 잠겼습니다! 올바른 분수 값을 입력하세요.', 'ans_check': "ans === '7/9'"},
    {'qnum': 12, 'title': '방화벽 2단계 돌파', 'story': '[스피드-N]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 🧮 <strong>[포트 변환 2]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"2차 보안 해제 단계입니다. 순환소수 $0.\\dot{4}\\dot{5}$의 기약분수 코드를 전송하여 보안 회로를 무력화하십시오.\\"\\"', 'qtext': '<strong>Q12. [순환소수를 분수로 2]</strong><br>$0.\\dot{4}\\dot{5}$ 를 기약분수로 나타내시오.', 'placeholder': '예: 5/11', 'error': '우회 거부! 신호 주파수가 맞지 않습니다.', 'ans_check': "ans === '5/11' || ans === '45/99'"},
    {'qnum': 13, 'title': '방화벽 우회 공식', 'story': '[스피드-N]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 🧮 <strong>[방정식 유도]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"순환소수 $x = 0.\\dot{3}$을 분수로 고치기 위해 $10x - x$ 식을 풀고 있습니다. 이때 좌변 결과인 $9x$의 최종 정수 값을 입력하세요.\\"\\"', 'qtext': '<strong>Q13. [소수점 아래 정리]</strong><br>순환소수 $x = 0.\\dot{3}$ 을 분수로 고치기 위해 $10x - x$ 의 식을 이용한다. 이때 $9x$ 의 값은 얼마인가?', 'placeholder': '숫자만 입력', 'error': '수식 동기화 실패! 데이터 오차가 발생했습니다.', 'ans_check': "ans === '3'"},
    {'qnum': 14, 'title': '방화벽 3단계 돌파', 'story': '[스피드-N]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 🧮 <strong>[정수부 포함 분수]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"3차 방화벽 포트입니다. 정수 부분이 0이 아닌 순환소수 $1.\\dot{2}$를 기약분수 코드로 입력하십시오.\\"\\"', 'qtext': '<strong>Q14. [순환소수를 분수로 3]</strong><br>$1.\\dot{2}$ 를 기약분수로 나타내시오.', 'placeholder': '예: 11/9', 'error': '잘못된 기약분수 전송! 방화벽 압박이 가중됩니다.', 'ans_check': "ans === '11/9'"},
    {'qnum': 15, 'title': '방화벽 마스터 해킹', 'story': '✨ <strong>[조력자 시스템 권한 100% 완전 복구]</strong> ✨<br><br>[스피드-N]: \\"연산 데이터 대조 성공! 이제 시스템 통제권을 제가 절반 확보했습니다. 가자, 복수의 시간입니다!\\"<br><br>[해커-Z]: \\"크으으윽... 하찮은 인간 녀석들이 내 서버까지 잠식해 들어오다니!\\"', 'qtext': '<strong>Q15. [마스터 포트 해킹]</strong><br>순환소수 $x = 0.2\\dot{5}$ 를 기약분수로 나타내시오.', 'placeholder': '예: 23/90', 'error': '해킹 실패! 백신 시스템의 추적이 시작되었습니다!', 'ans_check': "ans === '23/90'"},
    {'qnum': 16, 'title': '부스터 점화 공식', 'story': '[해커-Z]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 🏁 <strong>[출력 부스터 시동]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"마지막 4구역 최종 부스터 구간입니다. $0.1\\dot{2}\\dot{3}$을 공식으로 분수로 바꿀 때, 분모에 적용될 정합 값을 연산해 시동 장치에 입력하세요.\\"\\"', 'qtext': '<strong>Q16. [분모 결정 공식]</strong><br>$0.1\\dot{2}\\dot{3}$ 을 분수로 고칠 때 분모에 들어갈 숫자는 얼마인가?', 'placeholder': '숫자만 입력', 'error': '출력 엔진 미시동! 분모 값이 잘못되었습니다.', 'ans_check': "ans === '990'"},
    {'qnum': 17, 'title': '부스터 출력 충전', 'story': '[해커-Z]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 🏁 <strong>[출력 에너지 전송]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"공식의 분자 값($123 - 1$) 계산을 마저 끝내고, 최종 완성된 기약분수 에너지를 엔진에 공급하십시오.\\"\\"', 'qtext': '<strong>Q17. [기약분수 조율]</strong><br>$0.1\\dot{2}\\dot{3}$ 을 분수로 고칠 때 분자에 들어갈 식은 $123 - 1$ 이다. 계산한 최종 기약분수를 구하시오.', 'placeholder': '예: 61/495', 'error': '에너지 충전 오류! 엔진 과부하!', 'ans_check': "ans === '61/495'"},
    {'qnum': 18, 'title': '최종 부스터 대소비교', 'story': '[해커-Z]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 🏁 <strong>[더 강한 연료 선택]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"두 에너지 팩 $0.\\dot{3}$ 과 $0.3$ 중 더 강력한 출력을 내는 에너지를 입력하여 연소실에 투입하십시오.\\"\\"', 'qtext': '<strong>Q18. [유리수 대소 비교]</strong><br>$0.\\dot{3}$ 과 $0.3$ 중 어느 쪽이 더 큰가?', 'placeholder': '예: 0.[3] 또는 0.(3)', 'error': '추진력 부족! 연료 연소 온도가 급감합니다.', 'ans_check': "ans === '0.[3]' || ans === '0.(3)' || ans === '0.3(dot)' || ans === '0.333...'"},
    {'qnum': 19, 'title': '부스터 잠금 해제', 'story': '[해커-Z]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 🏁 <strong>[참과 거짓 판정]</strong><br><br>[레이싱 내비게이션 스피드-N]: \\"마지막 관문 진입 직전입니다. \'모든 순환소수는 유리수이다.\' 명제의 진위를 가려 회로를 해제하십시오.\\"\\"', 'qtext': '<strong>Q19. [유리수의 정의]</strong><br>모든 순환소수는 유리수이다. ( O / X )', 'placeholder': 'O 또는 X 입력', 'error': '회로 단선! 스파크가 발생합니다!', 'ans_check': "ans === 'O' || ans === 'o' || ans === '오'"},
    {'qnum': 20, 'title': '골인 레이저 가동', 'story': '🔮 <strong>[최종 방화벽 락다운 해제]</strong> 🔮<br><br>[스피드-N]: \\"제 모든 에너지를 출구 개방에 전념하겠습니다. 당신이라면 저 장벽을 해독해 낼 것입니다. 마지막 답을 입력하세요!\\"<br><br>[해커-Z]: \\"안 돼... 내 제어권이... 소멸한다아아!\\"', 'qtext': '<strong>Q20. [순환소수의 극한]</strong><br>$0.\\dot{9}$ 를 분수로 나타내면 얼마인가?', 'placeholder': '숫자만 입력', 'error': '조준 실패! 결승선 돌파 기회를 놓칩니다!', 'ans_check': "ans === '1'"}
]

# Generate Q panels

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
    q['hint'] = generate_hint(q['qtext'], q.get('ans_check', ''))

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
            <img src="assets/m2_01_rational_numbers/q{qnum}.png" alt="Background" class="panel-image">
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
                <button class="btn" onclick="checkQ{qnum}()">{'부스터 가동 시작' if qnum==1 else '다음으로'}</button>

            </div>
        </div>
'''
    panels_html += panel

# JS Answer Checks
js_checks = ""
for q in qs:
    qnum = q['qnum']
    ans_check = q['ans_check']
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    progress = int(qnum * 5)
    
    check_fn = f'''
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value);
            if ({ans_check}) {{
                wrongCount = 0;
                playSuccess();
                nextStage('panel_q{qnum}', {next_stage}, {progress});
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
    js_checks += check_fn

# Common JS functions boilerplate
js_boilerplate = """

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
        let wrongCount = 0;
function cleanString(str) {
            return str.replace(/\\s+/g, '').toUpperCase();
        }

        function showError(panelId, errorId) {
            try { playError(); } catch(e) {}
            const errEl = document.getElementById(errorId);
            if (errEl) {
                errEl.style.display = 'block';
                setTimeout(() => { errEl.style.display = 'none'; }, 3000);
            }
        }
"""

# Compile the final code
final_html = base_html.replace('{panels_placeholder}', panels_html)

# Add checks and boilerplate inside final script tag
# We find window.onload and insert checks before it
script_insert = js_boilerplate + js_checks + "\n"
final_html = final_html.replace('        window.onload = () => {', script_insert + '        window.onload = () => {')


# Apply CSS Minification before writing
import re
def minify_css_builder(html_content):
    def replacer(match):
        css_code = match.group(1)
        css_code = re.sub(r'/\*.*?\*/', '', css_code, flags=re.DOTALL)
        css_code = re.sub(r'\s+', ' ', css_code)
        css_code = re.sub(r'\s*([{}:;,])\s*', r'\1', css_code)
        return f"<style>{css_code}</style>"
    return re.sub(r'<style>(.*?)</style>', replacer, html_content, flags=re.DOTALL)

try:
    final_html = minify_css_builder(final_html)
except NameError:
    pass

try:
    new_content = minify_css_builder(new_content)
except NameError:
    pass

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("app_m2_01_escape_room.html generated successfully.")
