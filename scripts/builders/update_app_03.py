import re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_03_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

# 1. Base template of app_m1_03_escape_room.html
base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>우주 정거장 델타의 비상 탈출: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0B0F19;
            --glass-bg: rgba(13, 25, 48, 0.7);
            --glass-border: rgba(6, 182, 212, 0.25);
            --accent: #06B6D4;
            --accent-hover: #22D3EE;
            --text-main: #E2E8F0;
            --text-muted: #94A3B8;
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
                radial-gradient(circle at 20% 30%, rgba(6, 182, 212, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.15) 0%, transparent 40%);
            z-index: -2;
        }

        /* Twinkling Space Stars simulation */
        body::after {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px);
            background-size: 550px 550px, 350px 350px;
            background-position: 0 0, 40px 60px;
            opacity: 0.3;
            z-index: -1;
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
            border-top: 1px solid rgba(6, 182, 212, 0.4);
            border-left: 1px solid rgba(6, 182, 212, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(6, 182, 212, 0.1);
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
            font-size: 2.8rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #FFF 30%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(6, 182, 212, 0.3);
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
            border: 1px solid rgba(6, 182, 212, 0.2);
        }

        .story-box {
            position: relative;
            background: linear-gradient(90deg, rgba(8, 47, 73, 0.5) 0%, rgba(0,0,0,0.3) 100%);
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
            color: rgba(6, 182, 212, 0.05);
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
            border: 1px solid rgba(6, 182, 212, 0.3);
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
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.4), inset 0 2px 4px rgba(0,0,0,0.5);
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
            background: linear-gradient(90deg, #3B82F6, var(--accent));
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
            background: linear-gradient(135deg, #0284C7, #0369A1);
            color: white;
            border: 1px solid #0EA5E9;
            padding: 0.6rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 900;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 3px;
            width: 100%;
            box-shadow: 0 10px 25px rgba(2, 132, 199, 0.5), inset 0 2px 5px rgba(255,255,255,0.4);
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
            box-shadow: 0 15px 30px rgba(6, 182, 212, 0.6), inset 0 2px 5px rgba(255,255,255,0.6);
            border-color: #22D3EE;
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
            .graph-container { padding: 1rem; }
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
            background: #0d1930;
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
            <img src="assets/m1_03_equations/intro.png" alt="Background" class="panel-image">
            <h1>우주 정거장 델타</h1>
            <h2>비상 탈출 프로토콜 가동</h2>
            <div class="story-box">
                <div class="story-text">
                    여러분은 우주 정거장 '델타'의 핵심 엔지니어들입니다.<br><br>
                    갑작스러운 소행성 충돌 경보가 울리고 델타의 메인 시스템이 다운되었습니다!<br><br>
                    탈출 포드에 전력을 공급하려면 미지의 문자로 이루어진 시스템 방정식 20개를 수동으로 풀어야 합니다. 45분 내에 일차방정식을 풀어 탈출에 성공하십시오!
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
        // Audio Module with Autoplay Failure Prevention
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
                    bgm.play().catch(e => console.log("BGM Autoplay blocked: play on user interaction"));
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

        // Clean answer string utility
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
            
            // Remove previous shake class
            err.classList.remove('shake');
            void err.offsetWidth; // Trigger reflow to restart animation
            err.classList.add('shake');
            
            setTimeout(() => {
                err.style.display = 'none';
            }, 3000);
        }

        // Visual Novel Log Module
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

        // Visual Novel chunk Typewriter Engine
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
                    if(s.trim()) {
                        chunks.push(s.trim());
                    }
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

        // Navigation
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
                if(storyBox) {
                    typeWriterHTML(storyBox, 25);
                }
            }, 300);
        }

        function prevStage(currentId, prevId, progressPercent) {
            try { playClick(); } catch(e) {}
            const currentEl = document.getElementById(currentId);
            const prevEl = document.getElementById(prevId);
            const progContainer = document.getElementById('progressContainer');
            const progBar = document.getElementById('progressBar');

            currentEl.classList.remove('active');
            
            setTimeout(() => {
                if(prevId === 'intro') {
                    progContainer.style.display = 'none';
                }
                progBar.style.width = progressPercent + '%';
                prevEl.classList.add('active');

                const storyBox = prevEl.querySelector('.story-box');
                if(storyBox) {
                    typeWriterHTML(storyBox, 25);
                }
            }, 300);
        }

        // Q1

        window.onload = () => {
            // Start intro typing
            const introPanel = document.getElementById('intro');
            const introStoryBox = introPanel.querySelector('.story-box');
            if (introStoryBox) {
                typeWriterHTML(introStoryBox, 25);
            }
        };
    </script>

    <!-- Story Log UI -->
    <div id="storyLogModal" class="log-modal">
        <div class="log-content">
            <button class="close-log" onclick="closeLog()">닫기 ✕</button>
            <h2>📜 지나온 우주 기록</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>

</body>
</html>
"""

# Write base template first
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(base_html)

# 2. 20 Questions Data for Unit 3 Equations
qs = [
    # Area 1: 시스템 식 복구 (문자와 식)
    {"qnum": 1, "title": "시스템 식 복구", "story": "🚀 <strong>[코드 단순화]</strong><br><br>손상된 전송 코드를 수신했습니다. 방정식 엔진에 식을 단순화해 입력해야 모듈이 활성화됩니다.", "qtext": "<strong>Q1. [문자의 사용]</strong><br>$a \\times b \\times a \\times 3$ 을 곱셈 기호를 생략하고 거듭제곱을 사용하여 간단히 나타내시오.", "placeholder": "예: 3a^2b", "error": "구문 오류! 시스템 연결 실패!", "ans_check": "ans === '3a^2b' || ans === '3ba^2'"},
    {"qnum": 2, "title": "시스템 식 복구", "story": "🚀 <strong>[식 세우기]</strong><br><br>소형 포드와 대형 포드의 전력 소모량을 계산해 총 에너지 요구 식을 완성하세요.", "qtext": "<strong>Q2. [식 세우기]</strong><br>소형 포드 1개 작동에 $x$ kW, 대형 포드 1개 작동에 $1000$ kW가 듭니다. 소형 포드 $5$개와 대형 포드 $1$개를 동시에 작동할 때 필요한 총 전력량을 $x$에 대한 식으로 나타내시오.", "placeholder": "예: 5x+1000", "error": "에너지 초과 경고!", "ans_check": "ans === '5x+1000' || ans === '1000+5x'"},
    {"qnum": 3, "title": "시스템 식 복구", "story": "🚀 <strong>[식의 대입]</strong><br><br>현재 엔진 온도 조건 x = -2일 때, 냉각 시스템 계수를 계산하십시오.", "qtext": "<strong>Q3. [식의 값]</strong><br>$x = -2$ 일 때, 대입 식 $3x + 5$ 의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "냉각수 부족! 온도가 상승합니다!", "ans_check": "ans === '-1'"},
    {"qnum": 4, "title": "시스템 식 복구", "story": "🚀 <strong>[계수 추출]</strong><br><br>안정 장치의 다항식 코드에서 핵심 증폭 계수를 추출하십시오.", "qtext": "<strong>Q4. [다항식과 일차식]</strong><br>다항식 $2x^2 - 5x + 3$ 에서 $x$의 계수를 구하시오. (부호 포함)", "placeholder": "숫자만 입력", "error": "증폭 계수 불일치! 차단벽 가동!", "ans_check": "ans === '-5'"},
    {"qnum": 5, "title": "시스템 식 복구", "story": "🚀 <strong>[분배법칙]</strong><br><br>두 개의 예비 회로를 병렬로 통합하기 위해 괄호를 풀어 회로식을 단순화하세요.", "qtext": "<strong>Q5. [일차식의 계산 1]</strong><br>식 $3(2x - 4) + 2x$ 를 분배법칙을 활용해 간단히 정리한 식을 입력하시오.", "placeholder": "예: 8x-12", "error": "회로 쇼트 경고! 전력 누출!", "ans_check": "ans === '8x-12'"},
    
    # Area 2: 전력망 동기화 (일차식의 계산)
    {"qnum": 6, "title": "전력망 동기화", "story": "🔋 <strong>[전압 분배]</strong><br><br>메인 전력 노드의 전압을 2개의 서브 배터리로 균등 분배합니다.", "qtext": "<strong>Q6. [일차식의 나눗셈]</strong><br>식 $(6x - 4) \\div 2$ 를 간단히 한 식을 입력하시오.", "placeholder": "예: 3x-2", "error": "배터리 과부하! 전력이 역류합니다!", "ans_check": "ans === '3x-2'"},
    {"qnum": 7, "title": "전력망 동기화", "story": "🔋 <strong>[통분 계산]</strong><br><br>두 라인의 전파 동기화 신호를 합쳐 최적의 주파수 대역을 확보하세요.", "qtext": "<strong>Q7. [일차식의 계산 2]</strong><br>식 $\\frac{1}{2}(4x - 6) - \\frac{1}{3}(3x + 9)$ 를 계산하여 간단히 하시오.", "placeholder": "예: x-6", "error": "주파수 왜곡! 동기화 실패!", "ans_check": "ans === 'x-6'"},
    {"qnum": 8, "title": "전력망 동기화", "story": "🔋 <strong>[일차식 구분]</strong><br><br>일차식 전원 코어만 선택해야 회로가 타지 않습니다.", "qtext": "<strong>Q8. [일차식 판별]</strong><br>다음 중 차수가 1인 <strong>일차식</strong>의 번호만 쓰시오.<br>(1) $3x^2$ &nbsp;&nbsp;(2) $0 \\times x + 2$ &nbsp;&nbsp;(3) $\\frac{1}{x} + 1$ &nbsp;&nbsp;(4) $-2x + 1$", "placeholder": "숫자만 입력", "error": "회로 폭발! 코어가 과열되었습니다!", "ans_check": "ans === '4'"},
    {"qnum": 9, "title": "전력망 동기화", "story": "🔋 <strong>[동류항 정리]</strong><br><br>두 동축 케이블의 잔류 저항값을 합산하여 상쇄시키십시오.", "qtext": "<strong>Q9. [동류항 정리]</strong><br>식 $2x - 3 - (x - 5)$ 를 계산하여 간단히 정리하시오.", "placeholder": "예: x+2", "error": "저항 매칭 실패! 감전 위험!", "ans_check": "ans === 'x+2'"},
    {"qnum": 10, "title": "전력망 동기화", "story": "🔋 <strong>[대입 정리]</strong><br><br>시스템 부하값 A와 B를 조합한 최종 부하 공식을 도출하십시오.", "qtext": "<strong>Q10. [식의 대입 정리]</strong><br>$A = x - 2$, $B = -2x + 3$ 일 때, $2A - B$ 를 $x$에 대한 식으로 나타내시오.", "placeholder": "예: 4x-7", "error": "시스템 임계치 돌파! 비상 경보!", "ans_check": "ans === '4x-7'"},
    
    # Area 3: 메인 엔진 재가동 (일차방정식의 풀이)
    {"qnum": 11, "title": "메인 엔진 재가동", "story": "🛰️ <strong>[방정식 검증]</strong><br><br>참과 거짓이 미지수에 따라 결정되는 진짜 보안 방정식을 감지하세요.", "qtext": "<strong>Q11. [방정식의 이해]</strong><br>다음 식 중 미지수 $x$에 따라 참도 되고 거짓도 되는 <strong>방정식</strong>인 것의 번호를 쓰시오.<br>(1) $2x + 3$ &nbsp;&nbsp;(2) $x + x = 2x$ &nbsp;&nbsp;(3) $3x - 1 = 5$ &nbsp;&nbsp;(4) $3 < 5$", "placeholder": "숫자만 입력", "error": "위조 보안식 감지! 암호화 록!", "ans_check": "ans === '3'"},
    {"qnum": 12, "title": "메인 엔진 재가동", "story": "🛰️ <strong>[등식의 성질]</strong><br><br>엔진 연료 이송 밸브의 양방향 수압을 평형 상태로 맞추세요.", "qtext": "<strong>Q12. [일차방정식 1]</strong><br>방정식 $x - 4 = 6$ 의 해를 구하시오.", "placeholder": "숫자만 입력", "error": "연료 부족! 엔진 시동 지연!", "ans_check": "ans === '10'"},
    {"qnum": 13, "title": "메인 엔진 재가동", "story": "🛰️ <strong>[이항 정리]</strong><br><br>이항 법칙에 따라 제어 장치의 밸브 각도를 조정하십시오.", "qtext": "<strong>Q13. [일차방정식 2]</strong><br>방정식 $2x + 5 = 11$ 의 해를 구하시오.", "placeholder": "숫자만 입력", "error": "조정 각도 이탈! 압력 경보!", "ans_check": "ans === '3'"},
    {"qnum": 14, "title": "메인 엔진 재가동", "story": "🛰️ <strong>[미지수 이항]</strong><br><br>미지수 항과 상수 항을 각 변으로 격리하여 해를 구합니다.", "qtext": "<strong>Q14. [일차방정식 3]</strong><br>방정식 $3x - 2 = x + 6$ 의 해를 구하시오.", "placeholder": "숫자만 입력", "error": "격리 실패! 동력원 손상!", "ans_check": "ans === '4'"},
    {"qnum": 15, "title": "메인 엔진 재가동", "story": "🛰️ <strong>[비례식 해결]</strong><br><br>비례 배분 제어 펌프의 내외항 동력비를 맞춰 해를 연산하십시오.", "qtext": "<strong>Q15. [비례식 풀이]</strong><br>비례식 $(x - 1) : 2 = (2x + 1) : 5$ 을 만족하는 해 $x$의 값을 구하시오.", "placeholder": "숫자만 입력", "error": "비율 붕괴! 기어 훼손 경고!", "ans_check": "ans === '7'"},
    
    # Area 4: 탈출 포드 사출 (일차방정식의 활용)
    {"qnum": 16, "title": "탈출 포드 사출", "story": "🌠 <strong>[연속하는 수]</strong><br><br>순차적으로 발사할 세 포드의 번호를 계산해야 충돌을 방지합니다.", "qtext": "<strong>Q16. [연속하는 세 수]</strong><br>연속하는 세 자연수의 합이 36일 때, 세 자연수 중 가장 큰 자연수를 구하시오.", "placeholder": "숫자만 입력", "error": "궤도 겹침 감지! 발사 중단!", "ans_check": "ans === '13'"},
    {"qnum": 17, "title": "탈출 포드 사출", "story": "🌠 <strong>[어떤 수 연산]</strong><br><br>메인 컴퓨터가 유실한 어떤 시스템 정수를 방정식으로 복원하세요.", "qtext": "<strong>Q17. [식의 활용 1]</strong><br>어떤 수의 3배에서 5를 뺀 수는 어떤 수의 2배보다 4만큼 크다. 이 어떤 수를 구하시오.", "placeholder": "숫자만 입력", "error": "데이터 복원 실패!", "ans_check": "ans === '9'"},
    {"qnum": 18, "title": "탈출 포드 사출", "story": "🌠 <strong>[과부족 계산]</strong><br><br>대피 요원들의 탈출 포드 탑승 인원 분배를 해결하십시오.", "qtext": "<strong>Q18. [과부족 문제]</strong><br>요원들에게 산소 팩을 나누어 주는데, 한 명에게 4개씩 주면 3개가 남고, 5개씩 주면 2개가 부족하다. 요원 수(명)를 구하시오.", "placeholder": "숫자만 입력", "error": "산소 배분 실패! 탑승 불가!", "ans_check": "ans === '5'"},
    {"qnum": 19, "title": "탈출 포드 사출", "story": "🌠 <strong>[거리 속력 시간]</strong><br><br>정거장 비상 해치까지 가장 빠르게 도달할 통로 거리를 연산하십시오.", "qtext": "<strong>Q19. [거리 속력 시간]</strong><br>해치까지 가는데 시속 4km로 걸어가면 시속 12km로 호버보드를 타고 가는 것보다 20분 늦게 도착한다. 총 통로 거리(km)를 구하시오.", "placeholder": "숫자만 입력", "error": "도착 시간 지연! 폭발 경보!", "ans_check": "ans === '2' || ans === '2km'"},
    {"qnum": 20, "title": "탈출 포드 사출", "story": "🌠 <strong>[농도 희석]</strong><br><br>탈출 엔진 연료를 6% 농도로 희석하기 위해 주입할 희석수 양을 구하세요.", "qtext": "<strong>Q20. [소금물 농도 활용]</strong><br>10%의 액체 연료 300g에 몇 g의 희석수를 더 넣으면 6%의 혼합 연료가 되는가?", "placeholder": "숫자만 입력", "error": "연료 비율 오류! 역화 경고!", "ans_check": "ans === '200' || ans === '200g'"}
]

# Generate panels HTML
panels_html = ""
for q in qs:
    qnum = q['qnum']
    title = q['title']
    story = q['story']
    qtext = q['qtext']
    placeholder = q['placeholder']
    error = q['error']
    
    prev_stage = f"'panel_q{qnum-1}'" if qnum > 1 else "'intro'"
    prev_progress = (qnum-1)*5
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    
    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel">
            <h2>제 {qnum}구역: {title}</h2>
            <img src="assets/m1_03_equations/q{qnum}.png" alt="Background" class="panel-image">
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
                <button class="btn" onclick="checkQ{qnum}()">{'시스템 복구 시작' if qnum==1 else '다음으로' if qnum < 20 else '탈출하기'}</button>
                    <button class="btn btn-hint" onclick="alert('💡 힌트: ' + document.getElementById('error{qnum}').innerText)" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>
                    <button class="btn btn-hint" onclick="alert('💡 힌트: ' + document.getElementById('error{qnum}').innerText)" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>
            </div>
        </div>
'''
    panels_html += panel

# Outro panel
outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>우주 정거장 델타의 비상 탈출</h2>
            <img src="assets/m1_03_equations/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">여러분들이 마지막 암호 '200'을 입력하자, 굉음과 함께 굳게 닫혀 있던 비상 해치가 개방되며 소형 탈출 포드가 사출 궤도로 미끄러져 들어갑니다! 
                카운트다운이 0을 가리키는 순간, 포드가 불꽃을 뿜으며 암흑 속 우주 정거장 델타를 빠져나와 지구를 향해 아름다운 호를 그리며 나아갑니다. 
                문자와 식의 규칙을 찾아내고, 소행성 충돌 시간을 일차방정식으로 풀어 극적으로 살아남은 요원들, 미션 완벽 성공입니다!</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

# Generate JS checks
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

# Perform Replacements
# Inject panels_html right after <!-- Q1 --> tag inside container
new_content = re.sub(r'<!-- Q1.*?-->', lambda m: '<!-- Q1 -->\n' + panels_html + '\n    ', base_html, flags=re.DOTALL)

# Inject JS checks right after let isMuted = ...
# Search where cleanString is or // Q1
new_content = re.sub(r'// Q1[\s\S]*?(?=window\.onload = \(\) => \{)', lambda m: '// Q1\n' + js_checks + '\n        ', new_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("app_m1_03_escape_room.html created and compiled successfully with 20 questions.")
