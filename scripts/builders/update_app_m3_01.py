# -*- coding: utf-8 -*-\nimport re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m3_01_escape_room.html")
html_path = html_file

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>피타고라스의 숨겨진 무리수 사원: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #120a1d;
            --glass-bg: rgba(25, 15, 38, 0.75);
            --glass-border: rgba(168, 85, 247, 0.25);
            --accent: #a855f7;
            --accent-hover: #c084fc;
            --text-main: #fbfbf3;
            --text-muted: #cbbba0;
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
                radial-gradient(circle at 10% 20%, rgba(168, 85, 247, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(15, 23, 42, 0.3) 0%, transparent 40%);
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
            box-shadow: 0 0 50px rgba(168, 85, 247, 0.15), inset 0 0 20px rgba(168, 85, 247, 0.02);
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
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(168, 85, 247, 0.15);
            padding-bottom: 0.75rem;
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
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(168, 85, 247, 0.15);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            position: relative;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .story-box:hover {
            background: rgba(15, 23, 42, 0.7);
        }

        .story-text {
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text-main);
            min-height: 110px;
            word-break: keep-all;
        }
        
        #intro .story-text {
            min-height: 80px;
        }

        .story-log-trigger {
            position: absolute;
            bottom: 8px;
            right: 12px;
            background: none;
            border: none;
            color: var(--accent);
            font-size: 0.8rem;
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.2s;
        }
        
        .story-log-trigger:hover {
            opacity: 1;
        }

        .question-box {
            background: rgba(168, 85, 247, 0.05);
            border: 1px dashed rgba(168, 85, 247, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .question-content {
            font-size: 1.05rem;
            line-height: 1.6;
            margin-bottom: 1rem;
            font-weight: 500;
        }

        .input-group {
            margin-top: 1rem;
            display: flex;
            gap: 10px;
        }

        input[type="text"] {
            flex: 1;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: #fff;
            font-size: 1rem;
            transition: all 0.3s;
            font-family: 'Share Tech Mono', monospace;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 10px rgba(168, 85, 247, 0.3);
        }

        .btn-group {
            display: flex;
            justify-content: center;
        }

        .btn {
            background: linear-gradient(135deg, var(--accent) 0%, #1a2a3a 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.85rem 2.5rem;
            font-size: 1.05rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
            background: linear-gradient(135deg, var(--accent-hover) 0%, var(--accent) 100%);
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
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        .btn-hint:hover {
            background: rgba(16, 185, 129, 0.4);
            color: #fff;
            box-shadow: 0 0 10px rgba(52, 211, 153, 0.4);
        }

        .error-msg {
            color: #ff6b6b;
            font-size: 0.9rem;
            text-align: center;
            margin-top: -0.5rem;
            margin-bottom: 1rem;
            display: none;
            font-weight: 500;
            text-shadow: 0 0 10px rgba(255, 107, 107, 0.2);
        }

        .progress-container {
            width: 100%;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(168, 85, 247, 0.2);
            border-radius: 50px;
            height: 10px;
            margin-bottom: 2rem;
            overflow: hidden;
            display: none;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--accent) 0%, var(--accent-hover) 100%);
            width: 0%;
            transition: width 0.5s ease;
            box-shadow: 0 0 15px var(--accent);
        }

        .sound-ctrl {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            padding: 0.5rem 1rem;
            border-radius: 50px;
            cursor: pointer;
            z-index: 100;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            transition: all 0.3s;
        }
        .sound-ctrl:hover {
            border-color: var(--accent);
            box-shadow: 0 0 10px rgba(168, 85, 247, 0.3);
        }

        .info-panel {
            position: fixed;
            top: 20px;
            left: 20px;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            padding: 0.5rem 1rem;
            border-radius: 50px;
            z-index: 100;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .log-modal {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            display: none;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(5px);
        }
        
        .log-content {
            background: var(--bg-main);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            width: 90%;
            max-width: 500px;
            max-height: 70vh;
            padding: 2rem;
            overflow-y: auto;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .close-log {
            position: absolute;
            top: 15px; right: 15px;
            background: none; border: none; color: #fff;
            font-size: 1.2rem; cursor: pointer;
        }
        
        .log-list {
            margin-top: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .log-item {
            padding: 0.75rem;
            background: rgba(255,255,255,0.03);
            border-left: 3px solid var(--accent);
            font-size: 0.9rem;
            line-height: 1.5;
            border-radius: 4px;
        }
        
        .log-content h2 {
            border-bottom: 1px solid rgba(168, 85, 247, 0.2);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }

        @media (max-width: 600px) {
            .container { padding: 1rem; }
            .glass-panel { padding: 1.5rem; border-radius: 16px; }
            h1 { font-size: 1.8rem; }
            h2 { font-size: 1.1rem; }
            .story-text { font-size: 0.9rem; min-height: 140px; }
            .btn { width: 100%; }
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
</head>
<body>
    <button class="sound-ctrl" onclick="toggleMute()">
        <span id="soundIcon">🔊</span> <span id="soundText">Sound ON</span>
    </button>
    
    <div class="info-panel" id="infoPanel" style="display: none;">
        <span id="displayStudentId">학번: -</span>
        <span id="displayName">이름: -</span>
    </div>

    <div class="container">
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <!-- Intro Panel -->
        <div id="intro" class="glass-panel active">
            <h1>피타고라스의 숨겨진 무리수 사원</h1>
            <h2>제곱근과 실수</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_01/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [사원의 파수꾼 피타고라스-P]: "고대 그리스의 수학자 피타고라스가 살아생전 무리수의 존재를 숨기기 위해 설계했다는 깊은 사막 속의 '무리수 사원'에 도달했습니다. 사원의 중심부로 갈수록 알 수 없는 수학 결계들이 여러분의 앞길을 가로막습니다. 사원에 가득 찬 제곱근의 기호를 해독하여 제한시간 45분 내에 무리수의 비밀을 밝히고 무사히 탈출하십시오!"
            </div>
            </div>
                        <div class="info-box" style="background: rgba(220, 38, 38, 0.2); border-left: 4px solid #ef4444; padding: 0.8rem 1.2rem; margin-top: 1.5rem; border-radius: 0 12px 12px 0; color: #f87171; font-size: 0.95rem; line-height: 1.6; text-align: left;">
                ⚠️ <b>주의사항</b><br>
                문제는 총 20문제이며, 한 문제에서 3번 틀릴 경우 해당 구역의 처음으로 되돌아갑니다. <br>
                또한 <b>오답을 제출할 때마다 제한 시간이 1분씩 단축</b>되니 신중하게 도전해 주세요!
            </div>

            <div class="btn-group">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 0)">탈출 시도 개시</button>
            </div>
        </div>

        {{panels_placeholder}}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>최종 봉인 탈출 성공</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_01/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [사원의 파수꾼 피타고라스-P]: "무리수의 모든 결계가 사그라지며 사원 지하 깊은 곳에 묻혀있던 황금 피라미드가 솟아오릅니다. 고대 수학자들이 영원히 숨겨두려 했던 세상의 비밀이 밝혀지는 순간입니다. <span class="dynamic-captain-name"><span class="dynamic-captain-name"><span class="dynamic-captain-name"><span class="dynamic-captain-name">탐사대원</span></span></span></span> 여러분, 무리수 사원 탈출 성공을 축하합니다!"
            </div>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="location.reload()">다시 하기</button>
            </div>
        </div>
    </div>

    <!-- Web Audio API Sound Generation -->
    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        let isMuted = false;

        function toggleMute() {
            isMuted = !isMuted;
            document.getElementById('soundIcon').innerText = isMuted ? "🔇" : "🔊";
            document.getElementById('soundText').innerText = isMuted ? "Sound OFF" : "Sound ON";
        }

        function playBeep(freq, type, duration) {
            if (isMuted) return;
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }

        function playSuccess() {
            playBeep(523.25, 'triangle', 0.15); // C5
            setTimeout(() => playBeep(659.25, 'triangle', 0.15), 100); // E5
            setTimeout(() => playBeep(783.99, 'triangle', 0.3), 200); // G5
        }

        function playFail() {
            playBeep(220.00, 'sawtooth', 0.25); // A3
        }

        function playClick() {
            playBeep(440.00, 'sine', 0.05); // A4
        }
    </script>

    <script>
        let studentId = "";
        let studentName = "";
        let recordRow = null;
        let wrongCount = 0;
        const UNIT_ID = "m3_01";

        function cleanString(str) {
            return str.replace(/\s+/g, '').toUpperCase();
        }

        
        function tryStartGame(unitId) {
            const sid = document.getElementById('studentId');
            const sname = document.getElementById('studentName');
            if(sid && sname) {
                if(!sid.value.trim() || !sname.value.trim()) {
                    alert('학번과 이름을 모두 입력해주세요!');
                    return;
                }

            // 이름 동적 개인화 처리 (복성 예외 처리 반영 및 전역 변수 바인딩)
            try {
                let rawName = "";
                if (typeof sname !== 'undefined' && sname) {
                    rawName = (typeof sname.value !== 'undefined') ? sname.value.trim() : (typeof sname === 'string' ? sname.trim() : "");
                } else if (typeof studentName !== 'undefined') {
                    rawName = (typeof studentName.value !== 'undefined') ? studentName.value.trim() : (typeof studentName === 'string' ? studentName.trim() : "");
                }
                if (!rawName) {
                    const nameInput = document.getElementById('studentName');
                    if (nameInput) rawName = nameInput.value.trim();
                }
                if (rawName) {
                    const doubleLastNames = ["제갈", "황보", "사공", "남궁", "서문", "독고", "선우"];
                    let firstName = rawName;
                    if (rawName.length > 2) {
                        let prefix2 = rawName.substring(0, 2);
                        if (doubleLastNames.includes(prefix2)) {
                            firstName = rawName.substring(2);
                        } else {
                            firstName = rawName.substring(1);
                        }
                    }
                    window.playerFirstName = firstName;
                    document.querySelectorAll(".dynamic-captain-name").forEach(el => {
                        let originalRole = el.getAttribute("data-original-role") || el.innerText;
                        if (!el.hasAttribute("data-original-role")) {
                            el.setAttribute("data-original-role", originalRole);
                        }
                        el.innerHTML = firstName + " " + originalRole;
                    });
                    // 아웃트로 동적 텍스트 내 개인화 처리
                    let outroTextEl = document.getElementById("outro-dynamic-text");
                    if (outroTextEl) {
                        outroTextEl.querySelectorAll(".dynamic-captain-name").forEach(el => {
                            let originalRole = el.getAttribute("data-original-role") || el.innerText;
                            if (!el.hasAttribute("data-original-role")) {
                                el.setAttribute("data-original-role", originalRole);
                            }
                            el.innerHTML = firstName + " " + originalRole;
                        });
                    }
                }
            } catch(e) { console.error("이름 개인화 에러:", e); }


            // 이름 동적 개인화 처리
            try {
                let rawName = "";
                if (typeof sname !== 'undefined' && sname) {
                    rawName = (typeof sname.value !== 'undefined') ? sname.value.trim() : (typeof sname === 'string' ? sname.trim() : "");
                } else if (typeof studentName !== 'undefined') {
                    rawName = (typeof studentName.value !== 'undefined') ? studentName.value.trim() : (typeof studentName === 'string' ? studentName.trim() : "");
                }
                if (!rawName) {
                    const nameInput = document.getElementById('studentName');
                    if (nameInput) rawName = nameInput.value.trim();
                }
                if (rawName) {
                    let firstName = rawName.length > 2 ? rawName.substring(1) : rawName;
                    document.querySelectorAll(".dynamic-captain-name").forEach(el => {
                        let originalRole = el.getAttribute("data-original-role") || el.innerText;
                        if (!el.hasAttribute("data-original-role")) {
                            el.setAttribute("data-original-role", originalRole);
                        }
                        el.innerHTML = firstName + " " + originalRole;
                    });
                    // 아웃트로 동적 텍스트 내 개인화 처리
                    let outroTextEl = document.getElementById("outro-dynamic-text");
                    if (outroTextEl) {
                        outroTextEl.querySelectorAll(".dynamic-captain-name").forEach(el => {
                            let originalRole = el.getAttribute("data-original-role") || el.innerText;
                            if (!el.hasAttribute("data-original-role")) {
                                el.setAttribute("data-original-role", originalRole);
                            }
                            el.innerHTML = firstName + " " + originalRole;
                        });
                    }
                }
            } catch(e) { console.error("이름 개인화 에러:", e); }

                try {
                    if(typeof google !== 'undefined' && google.script && google.script.run) {
                        google.script.run
                            .withSuccessHandler(function(row) { window.userRecordRow = row; })
                            .recordStart(sid.value.trim(), sname.value.trim(), unitId);
                    }
                } catch(e) { console.warn('GAS 연동 안됨:', e); }
            }
            
            // 이름 동적 개인화 처리
            try {
                let rawName = sname.value.trim();
                if (rawName) {
                    let firstName = rawName.length > 2 ? rawName.substring(1) : rawName;
                    document.querySelectorAll(".dynamic-captain-name").forEach(el => {
                        let originalRole = el.getAttribute("data-original-role") || el.innerText;
                        if (!el.hasAttribute("data-original-role")) {
                            el.setAttribute("data-original-role", originalRole);
                        }
                        el.innerHTML = firstName + " " + originalRole;
                    });
                }
            } catch(e) { console.error("이름 개인화 에러:", e); }
            
            nextStage('intro', 'panel_q1', 0);
        }

        function nextStage(currentId, nextId, progressPercent) {
            try { playClick(); } catch(e) {}
            
            // Record registration at the start of stage 1
            if (currentId === 'intro') {
                studentId = prompt("학번을 입력하세요 (예: 20101):");
                studentName = prompt("이름을 입력하세요:");
                if (!studentId || !studentName) {
                    alert("학번과 이름을 반드시 입력해야 진행할 수 있습니다.");
                    return;
                }

            // 이름 동적 개인화 처리
            try {
                let rawName = "";
                if (typeof sname !== 'undefined' && sname) {
                    rawName = (typeof sname.value !== 'undefined') ? sname.value.trim() : (typeof sname === 'string' ? sname.trim() : "");
                } else if (typeof studentName !== 'undefined') {
                    rawName = (typeof studentName.value !== 'undefined') ? studentName.value.trim() : (typeof studentName === 'string' ? studentName.trim() : "");
                }
                if (!rawName) {
                    const nameInput = document.getElementById('studentName');
                    if (nameInput) rawName = nameInput.value.trim();
                }
                if (rawName) {
                    let firstName = rawName.length > 2 ? rawName.substring(1) : rawName;
                    document.querySelectorAll(".dynamic-captain-name").forEach(el => {
                        let originalRole = el.getAttribute("data-original-role") || el.innerText;
                        if (!el.hasAttribute("data-original-role")) {
                            el.setAttribute("data-original-role", originalRole);
                        }
                        el.innerHTML = firstName + " " + originalRole;
                    });
                    // 아웃트로 동적 텍스트 내 개인화 처리
                    let outroTextEl = document.getElementById("outro-dynamic-text");
                    if (outroTextEl) {
                        outroTextEl.querySelectorAll(".dynamic-captain-name").forEach(el => {
                            let originalRole = el.getAttribute("data-original-role") || el.innerText;
                            if (!el.hasAttribute("data-original-role")) {
                                el.setAttribute("data-original-role", originalRole);
                            }
                            el.innerHTML = firstName + " " + originalRole;
                        });
                    }
                }
            } catch(e) { console.error("이름 개인화 에러:", e); }


            // 이름 동적 개인화 처리
            try {
                let rawName = "";
                if (typeof sname !== 'undefined' && sname) {
                    rawName = (typeof sname.value !== 'undefined') ? sname.value.trim() : (typeof sname === 'string' ? sname.trim() : "");
                } else if (typeof studentName !== 'undefined') {
                    rawName = (typeof studentName.value !== 'undefined') ? studentName.value.trim() : (typeof studentName === 'string' ? studentName.trim() : "");
                }
                if (!rawName) {
                    const nameInput = document.getElementById('studentName');
                    if (nameInput) rawName = nameInput.value.trim();
                }
                if (rawName) {
                    let firstName = rawName.length > 2 ? rawName.substring(1) : rawName;
                    document.querySelectorAll(".dynamic-captain-name").forEach(el => {
                        let originalRole = el.getAttribute("data-original-role") || el.innerText;
                        if (!el.hasAttribute("data-original-role")) {
                            el.setAttribute("data-original-role", originalRole);
                        }
                        el.innerHTML = firstName + " " + originalRole;
                    });
                    // 아웃트로 동적 텍스트 내 개인화 처리
                    let outroTextEl = document.getElementById("outro-dynamic-text");
                    if (outroTextEl) {
                        outroTextEl.querySelectorAll(".dynamic-captain-name").forEach(el => {
                            let originalRole = el.getAttribute("data-original-role") || el.innerText;
                            if (!el.hasAttribute("data-original-role")) {
                                el.setAttribute("data-original-role", originalRole);
                            }
                            el.innerHTML = firstName + " " + originalRole;
                        });
                    }
                }
            } catch(e) { console.error("이름 개인화 에러:", e); }

                
                document.getElementById('displayStudentId').innerText = "학번: " + studentId;
                document.getElementById('displayName').innerText = "이름: " + studentName;
                document.getElementById('infoPanel').style.display = "flex";
                document.getElementById('progressContainer').style.display = "block";
                
                try {
                    google.script.run
                        .withSuccessHandler(function(row) {
                            recordRow = row;
                        })
                        .recordStart(studentId, studentName, UNIT_ID);
                } catch (err) {
                    console.log("GAS Not Connected");
                }
            }

            const currentPanel = document.getElementById(currentId);
            const nextPanel = document.getElementById(nextId);

            currentPanel.classList.remove('active');
            setTimeout(() => {
                currentPanel.style.display = 'none';
                nextPanel.style.display = 'block';
                setTimeout(() => {
                    nextPanel.classList.add('active');
                    const storyBox = nextPanel.querySelector('.story-box');
                    if (storyBox) {
                        const textElement = storyBox.querySelector('.story-text');
                        if (textElement && !textElement.dataset.typed) {
                            typeWriterHTML(textElement, 25);
                            textElement.dataset.typed = "true";
                        }
                    }
                }, 50);
            }, 500);

            // Update Progress Bar
            document.getElementById('progressBar').style.width = progressPercent + '%';

            // Completion check at Outro
            if (nextId === 'outro') {
                try {
                    google.script.run.recordEnd(recordRow, UNIT_ID);
                } catch (err) {
                    console.log("GAS Not Connected");
                }
            }
        }

        function showError(panelId, errorId) {
            try { playFail(); } catch(e) {}
            const errorMsg = document.getElementById(errorId);
            errorMsg.style.display = 'block';
            
            const panel = document.getElementById(panelId);
            panel.style.transform = 'translateX(10px)';
            setTimeout(() => panel.style.transform = 'translateX(-10px)', 100);
            setTimeout(() => panel.style.transform = 'translateX(5px)', 200);
            setTimeout(() => panel.style.transform = 'translateX(-5px)', 300);
            setTimeout(() => panel.style.transform = 'translateX(0)', 400);

            setTimeout(() => {
                errorMsg.style.display = 'none';
            }, 3000);
        }

        function typeWriterHTML(element, speed) {
            const htmlContent = element.innerHTML.strip ? element.innerHTML.strip() : element.innerHTML;
            element.innerHTML = "";
            element.style.visibility = "visible";
            
            let progress = 0;
            let currentHTML = "";
            
            // Extract dialog speaker prefix
            const speakerMatch = htmlContent.match(/^(\[[^\]]+\]|【[^】]+】|[^:]+:)/);
            let speakerPrefix = "";
            let remainingHTML = htmlContent;
            
            if (speakerMatch) {
                speakerPrefix = speakerMatch[0];
                remainingHTML = htmlContent.slice(speakerPrefix.length);
                element.innerHTML = speakerPrefix;
            }

            const tokens = [];
            let i = 0;
            while (i < remainingHTML.length) {
                if (remainingHTML[i] === '<') {
                    let endIdx = remainingHTML.indexOf('>', i);
                    if (endIdx !== -1) {
                        tokens.push({ type: 'tag', content: remainingHTML.slice(i, endIdx + 1) });
                        i = endIdx + 1;
                        continue;
                    }
                }
                tokens.push({ type: 'text', content: remainingHTML[i] });
                i++;
            }

            function type() {
                if (progress < tokens.length) {
                    const token = tokens[progress];
                    if (token.type === 'tag') {
                        element.innerHTML += token.content;
                    } else {
                        element.innerHTML += token.content;
                    }
                    progress++;
                    setTimeout(type, speed);
                }
            }
            
            type();
        }

        let storyHistory = [];
        
        function openLog() {
            const modal = document.getElementById('storyLogModal');
            const container = document.getElementById('logContainer');
            container.innerHTML = storyHistory.map(log => `<div class="log-item">${log}</div>`).join('') || '<div class="log-item">기록된 이전 대사가 없습니다.</div>';
            modal.style.display = 'flex';
        }
        
        function closeLog() {
            document.getElementById('storyLogModal').style.display = 'none';
        }

        // Q1 Load setup
        window.onload = () => {
            const introPanel = document.getElementById('intro');
            const introStoryBox = introPanel.querySelector('.story-box');
            if (introStoryBox) typeWriterHTML(introStoryBox, 25);
        };
    </script>

    <div id="storyLogModal" class="log-modal">
        <div class="log-content">
            <button class="close-log" onclick="closeLog()">닫기 ✕</button>
            <h2>📜 지나온 스토리 기록</h2>
            <div id="logContainer" class="log-list">기록이 없습니다.</div>
        </div>
    </div>
</body>
</html>
"""

# Questions configuration
qs = [
    {'qnum': 1, "options": ["±3", "±3 아님", "알 수 없음", "해 없음"], 'title': '제곱근의 기초 각인', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "크하하! 이 무리수 사원의 고대 기하학 방화벽은 내가 모조리 장악했다! 너희 중 그 누구도 사원의 기초 수식 관문을 뚫고 원래 세계로 돌아가지 못하리라!"<br><br><i>지이이잉- 거대한 모래 늪 장벽 위로 황동 다이얼 회전판이 점멸합니다. 9를 형성하는 두 개의 근원적인 뿌리값(제곱근)을 해독 장치에 기입하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "사원의 방문자들이여, 두려워 마십시오. 9의 대칭 근원 제곱근 값을 찾아내 다이얼에 주입하십시오. 부호 양쪽 모두를 규명해야 합니다!"''', 'qtext': '<strong>Q1. [제곱근의 정의]</strong><br>9의 제곱근을 구하시오. (단, 답이 2개인 경우 ± 기호를 사용해 나타내시오. 예: ±3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '±3' || ans === '+-3' || ans === '3,-3' || ans === '-3,3'"},
    {'qnum': 2, "options": ["4", "6", "2", "8"], 'title': '근호의 해독', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "겨우 첫 다이얼을 정렬했군. 하지만 이 단단한 근호($\\sqrt{}$) 껍질 속에 가두어 둔 16의 실질 출력을 꺼낼 수 있겠느냐!"<br><br><i>벽면의 상형문자 지시판에서 $\\sqrt{16}$ 문양이 빨갛게 깜빡이기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "근호 해독 센서 가동! $\\sqrt{16}$의 값을 단순화하여 근호 밖으로 완전히 탈출시켜 주십시오!"''', 'qtext': '<strong>Q2. [근호의 성질]</strong><br>$\sqrt{16}$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '4'"},
    {'qnum': 3, "options": ["10", "3", "7", "5"], 'title': '제곱근의 명칭 구분', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "후후... 그렇다면 제곱근 자체의 고유 명칭과 대칭성을 헷갈리지 않고 '제곱근 25'의 크기만을 정확히 분별해 낼 수 있겠나?"<br><br><i>지직- 다이어그램의 파란 전선이 붉은 전선과 교차하며 혼선을 빚어냅니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "주의하십시오! '제곱근 25'는 대칭 부호가 아닌, 순수한 플러스 근호인 $\\sqrt{25}$의 값만을 가리킵니다. 올바른 정수 상수를 전송하십시오!"''', 'qtext': '<strong>Q3. [제곱근 읽기]</strong><br>제곱근 25의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 4, "options": ["6", "1", "3", "5"], 'title': '음수 제곱의 양의 근', 'story': '''<strong>[사원 내 연도별 백업 레지스터 전압 충돌]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "치직... 캡틴! 이단자가 조작한 역부호 레지스터 $(-3)^2$의 전압이 강하게 상승합니다! ⚙️ [양의 제곱근 도출]<br><br>그 수치의 두 제곱근 중 양수에 해당하는 최종 값을 해독창에 대입해 안전 제동을 거십시오!"''', 'qtext': '<strong>Q4. [제곱근의 성질 2]</strong><br>$(-3)^2$의 제곱근 중 양수인 것을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '3'"},
    {'qnum': 5, "options": ["(1)", "(2)", "(3)", "(4)"], 'title': '유리수와 무리수의 경계', 'story': '''<strong>[사원 중앙 광장의 비석 패턴 점멸]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "치지직... 바닥의 4개 석판 타일 중 오직 하나만이 끝없는 소수로 흘러가는 무리수(순환하지 않는 무한소수) 안전 지대입니다! ⚙️ [무리수 선별]<br><br>무리수가 기록된 타일의 번호를 입력하여 그 위에 안전하게 안착하십시오!"''', 'qtext': '<strong>Q5. [무리수 판별]</strong><br>다음 보기 중 무리수인 것의 번호를 쓰시오.<br>(1) $0.1$<br>(2) $\sqrt{4}$<br>(3) $\pi$<br>(4) $-\frac{1}{2}$', 'placeholder': '번호 입력 (예: 3)', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '3' || ans === '(3)'"},
    {'qnum': 6, "options": ["√3", "√3 아님", "알 수 없음", "해 없음"], 'title': '대소 관계 분석', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "세상의 모든 크고 작음은 이 무리수 좌표에 의해 결정된다! 두 무리수 $\\sqrt{2}$와 $\\sqrt{3}$ 중 더 단단하고 강력한 에너지를 내뿜는 큰 수를 선언해 봐라!"<br><br><i>키패드 조향기 축이 왼쪽으로 삐거덕거리며 기울어집니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "수평 정렬 가동! 근호 안의 수치 대소를 비교해 더 큰 무리수 공식 기호(예: $\\sqrt{3}$)를 입력창에 주입해 수평을 맞추십시오!"''', 'qtext': '<strong>Q6. [실수의 대소 비교]</strong><br>두 실수 $\sqrt{2}$와 $\sqrt{3}$ 중 더 큰 수를 쓰시오. (루트 기호 포함 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√3' || ans === '루트3'"},
    {'qnum': 7, "options": ["4", "2", "0", "10"], 'title': '정수 궤도 매핑', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "길을 잃었군. $\\sqrt{5}$ 라는 정체불명의 빛이 좌표 평면의 어느 정수 층간 구역에 수렴하는지 그 정수 부분을 짚어낼 수 있겠느냐?"<br><br><i>벽면의 기압 게이지 지시침이 요동치며 정수 단위 눈금 사이에서 오르락내리락합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "정수 층계 보정 가동! $\\sqrt{5}$의 실제 값 대역인 $2.xxxx$ 에서 가장 기본 정수 부분을 주입해 센서 범위를 고정하십시오!"''', 'qtext': '<strong>Q7. [무리수의 정수 부분]</strong><br>$\sqrt{5}$의 정수 부분을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2'"},
    {'qnum': 8, "options": ["√5-2", "√5-2 아님", "알 수 없음", "해 없음"], 'title': '소수 부분의 잔여 에너지', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "정수를 걷어내고 남은, 순환하지 않는 끝없는 꼬리(소수 부분)의 실질 수식을 완전한 기하학 식으로 나타낼 수 있을까?"<br><br><i>지이이잉- 미세 제어 콘솔에 소수 에너지 잔량을 계산하는 수식 입력 대기 창이 깜빡입니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "전체 무리수 값에서 정수 부분을 차감하는 규칙을 활용해 $\\sqrt{5}$의 소수 부분을 수식(공백 없이 예: $\\sqrt{5}-2$)으로 조립하십시오!"''', 'qtext': '<strong>Q8. [무리수의 소수 부분]</strong><br>$\sqrt{5}$의 소수 부분을 구하시오. (루트 기호를 사용하여 식으로 나타내시오. 예: √5-2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√5-2'"},
    {'qnum': 9, "options": ["10", "3", "7", "5"], 'title': '소인수 정합의 밖', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "사원 지하의 중량석 $\\sqrt{12}$의 질량을 밖으로 꺼내 단순화하지 못한다면, 그 압력에 눌려 뼈도 못 추리게 될 것이다!"<br><br><i>쿠구구구- 천장에서 거대한 삼각 쐐기돌이 천천히 하강하여 하중 압력을 가해옵니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "중량석 수식 압축 시작! $\\sqrt{12}$를 $a\\sqrt{b}$ 형태로 축소 변환하여 두 계수의 합 $a+b$를 긴급 계산하십시오!"''', 'qtext': '<strong>Q9. [a√b 형태로 나타내기]</strong><br>$\sqrt{12}$를 $a\sqrt{b}$ 꼴로 나타낼 때, 자연수 $a, b$에 대하여 $a+b$의 값을 구하시오. (단, $b$는 가장 작은 자연수)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 10, "options": ["√5", "√5 아님", "알 수 없음", "해 없음"], 'title': '수직선 좌표 정합', 'story': '''💥 <strong>[비상 로그: 사원 마그마 노심 활성화 및 강제 자폭 시퀀스 발동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "여기까지 오다니 불사해 주마! 모든 제어 노드를 불태워 포맷하겠다! 5분 뒤 이 사원은 모래 폭풍 속으로 가라앉으리라!"<br><br><i>지진처럼 방 안이 격렬하게 상하로 요동치며 기계장치들이 스파크를 일으킵니다. 두 수의 수직선 대소 비교를 완벽히 매핑해 셧다운을 파쇄하십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "노심 온도 위험 수준 봉착! 2와 $\\sqrt{5}$ 중 수직선 위에서 더 우측(큰 수)에 위치하는 무리수를 공백 없이 입력해 차단막을 정지시키십시오!"''', 'qtext': '<strong>Q10. [수직선 대소 비교]</strong><br>수직선 위에서 2와 $\sqrt{5}$ 중 더 우측에 있는 수를 쓰시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√5' || ans === '루트5'", "extra_class": "glitch-bg"},
    {'qnum': 11, "options": ["√15", "√15 아님", "알 수 없음", "해 없음"], 'title': '사칙 마법진: 곱셈', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "후... 자폭 3분 지연 성공! 이제 사원의 사칙 마법진 게이트에 돌입했습니다! ⚙️ [무리수 곱셈 빔 결합]"<br><br><i>두 갈래로 뿜어져 나오는 레이저 빔 $\\sqrt{3}$과 $\\sqrt{5}$를 단일 렌즈 수식 빔으로 조율하여 입력창에 주사해 주십시오!</i>''', 'qtext': '<strong>Q11. [근호의 곱셈]</strong><br>$\sqrt{3} \times \sqrt{5}$ 의 값을 구하시오. (루트 기호 포함 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√15' || ans === '루트15'"},
    {'qnum': 12, 'title': '사칙 마법진: 나눗셈', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "1단계 마법진 해제! 2단계 게이트는 나눗셈 감쇠기입니다! ⚙️ [나눗셈 밸브 조율]"<br><br><i>유량 공식 $\\sqrt{18} \\div \\sqrt{2}$ 의 축소 감쇠 결과 정수 상수를 밸브 콘솔에 대입해 수압을 조절하십시오.</i>''', 'qtext': '<strong>Q12. [근호의 나눗셈]</strong><br>$\sqrt{18} \div \sqrt{2}$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '3'"},
    {'qnum': 13, 'title': '혼합 빔의 조율', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "3단계 해치입니다! 계수와 무리수가 혼합된 전자기 유도 공식 $2\\sqrt{6} \\times 3\\sqrt{3}$의 주파수를 단순화하여 스캔 코드로 전송하십시오! ⚙️ [혼합 곱셈]"''', 'qtext': '<strong>Q13. [근호의 곱셈 2]</strong><br>$2\sqrt{6} \times 3\sqrt{3}$ 의 값을 구하시오. (간단히 나타내시오. 예: 18√2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '18√2' || ans === '18루트2'"},
    {'qnum': 14, 'title': '유리화의 수식 변환', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "4단계 게이트! 분모가 무리수 $\\sqrt{3}$인 위험 회로를 안정적인 유리수로 중화하는 '유리화 작업'을 수행하십시오! ⚙️ [분모의 유리화]"<br><br><i>공식 $\\frac{6}{\\sqrt{3}}$ 회로의 유리화 결과 식을 주입하여 기판 스파크를 제거하십시오!</i>''', 'qtext': '<strong>Q14. [분모의 유리화]</strong><br>$\frac{6}{\sqrt{3}}$의 분모를 유리화한 값을 구하시오. (예: 2√3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2√3' || ans === '2루트3'"},
    {'qnum': 15, 'title': '에너지 핵 융합', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P 사원 코어 권한 100% 완전 환수]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "동기화 완료! 사원 중심부의 모든 기하학적 정렬 장치 통제권을 탈환했습니다! 이제 이단자의 격자 장벽을 역소거합니다. 공식 $\\sqrt{20} \\times \\sqrt{5}$의 융합 정수 에너지를 메인 게이트에 쏘아 주십시오!"<br><br><i>공중에 흩어져 있던 모래 먼지가 가라앉고, 화사한 백색 홀로그램 통로가 정면으로 개방됩니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "내 통제권을 빼앗다니...! 하지만 최종 결계의 복잡한 덧뺄셈 꼬임은 결코 풀지 못하리라!"''', 'qtext': '<strong>Q15. [기본 곱셈 연산]</strong><br>$\sqrt{20} \times \sqrt{5}$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '10'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '동류항 합산 공식', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "무리수의 덧셈 꼬임이다! 동일 무리수 기호를 문자처럼 묶어 융합할 수 있는 지적 능력이 네 녀석들에게 있느냐!"<br><br><i>전방 셔터 슬롯에 $3\\sqrt{2} + 5\\sqrt{2}$ 수식의 통합 조립 결과를 기입해 빗장을 거두십시오.</i>''', 'qtext': '<strong>Q16. [근호를 포함한 식의 덧셈]</strong><br>$3\sqrt{2} + 5\sqrt{2}$ 의 값을 구하시오. (예: 8√2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '8√2' || ans === '8루트2'"},
    {'qnum': 17, 'title': '분배의 마법진', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "이번엔 분배 법칙을 이용한 괄호 확장 록이다. 괄호를 깨뜨리고 분출되는 이 공식 에너지를 수식으로 나타내 봐라!"<br><br><i>복도 벽면에 설치된 톱니바퀴 홈들에 $\\sqrt{2}(\\sqrt{2} + \\sqrt{6})$ 수식 해독 값을 공백 없이 정합해 기동을 멈추십시오.</i>''', 'qtext': '<strong>Q17. [분배법칙과 근호]</strong><br>$\sqrt{2}(\sqrt{2} + \sqrt{6})$ 의 값을 분배법칙을 이용해 계산하시오. (예: 2+2√3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2+2√3' || ans === '2+2루트3'"},
    {'qnum': 18, 'title': '수식 압축 및 감쇄', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "단순 뺄셈처럼 보이나, $\\sqrt{12}$ 속에 숨겨진 제곱 인수를 빼내어 감쇄 연산을 정확히 처리해야만 회로가 타버리지 않을 것이다!"<br><br><i>제어 콘솔 패널이 붉은색 스파크를 일으키며 굉음을 냅니다.</i>''', 'qtext': '<strong>Q18. [근호의 변형과 뺄셈]</strong><br>$5\sqrt{3} - \sqrt{12}$ 의 값을 구하시오. (예: 3√3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '3√3' || ans === '3루트3'"},
    {'qnum': 19, 'title': '유리수와 무리수의 분리', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "유리수 회로망과 무리수 회로망이 극성 충돌을 유발하고 있다. 이 통화량을 하나로 분리 정리해 정수 값으로 나타내 보아라!"<br><br><i>안전 계측 미터기 눈금이 한쪽 극으로 지나치게 치우치기 시작합니다.</i>''', 'qtext': '<strong>Q19. [실수의 사칙연산]</strong><br>$(2 + \sqrt{3}) + (3 - \sqrt{3})$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 20, 'title': '최종 분수 정합 및 복원', 'story': '''🔮 <strong>[최종 무리수 사원 마스터 록 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[피타고라스-P]</span>: "조사관님! 이제 사원 밖 사막 오아시스로 통하는 최후의 게이트 포탈만 남았습니다! 제 모든 백업 마력을 해독 프리즘 렌즈에 투입하겠습니다! $\\frac{\\sqrt{3}}{\\sqrt{2}} + \\frac{\\sqrt{2}}{\\sqrt{3}}$ 수식의 통분 및 최종 분모 유리화 결과 코드를 입력하여 봉인을 해제하십시오! 자유를 찾을 시간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[이단자-X]</span>: "말도 안 돼... 내 무리수 격차 결계가... 완전히 동조 정렬되어 셧다운 되다니...!"''', 'qtext': '<strong>Q20. [유리화와 혼합 계산]</strong><br>$\frac{\sqrt{3}}{\sqrt{2}} + \frac{\sqrt{2}}{\sqrt{3}}$ 을 계산하여 분모를 유리화한 값을 구하시오. (예: 5√6/6)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5√6/6' || ans === '5루트6/6'", "extra_class": "glitch-bg"}
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
    
    # Year 3 unit 1 specific hints
    elif '제곱근' in qtext_clean: return "어떤 수 x를 제곱하여 a가 될 때, x를 a의 제곱근(±)이라고 부릅니다."
    elif '유리화' in qtext_clean: return "분모와 분자에 분모에 있는 루트 기호와 똑같은 무리수를 곱해서 분모를 유리수로 만들어 보세요."
    elif '무리수' in qtext_clean: return "순환하지 않는 무한소수를 찾으세요. 루트 기호가 완전히 안 벗겨지는 수가 무리수입니다."
    elif '삼각비' in qtext_clean or '사인' in qtext_clean or '코사인' in qtext_clean or '탄젠트' in qtext_clean: return "직각삼각형에서 대변과 빗변, 밑변 간의 삼각비 공식(sin, cos, tan)을 확인하세요."
    elif '이차방정식' in qtext_clean: return "방정식을 ax² + bx + c = 0 꼴로 정리한 후 인수분해하거나 근의 공식을 사용하세요."
    elif '이차함수' in qtext_clean: return "이차함수 y = a(x-p)² + q 꼴로 고치면 꼭짓점의 좌표가 (p, q)가 됨을 활용해 보세요."
    
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
            <h2>제 {qnum}구역: {title}</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_01/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">{story}</div>
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

# JS Answer Checks
js_checks = "let totalWrongCount = 0;\n"
for q in qs:
    qnum = q['qnum']
    ans_check = q['ans_check']
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    progress = int(qnum * 5)
    
    check_fn = f'''
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value);
            if ({ans_check}) {{
                try {{ playSuccess(); }} catch(e) {{}}
                wrongCount = 0;
                
                // Add current dialogue story to history log
                const currentStory = document.querySelector('#panel_q{qnum} .story-text').innerText;
                storyHistory.push("🔊 제 {qnum}구역: " + currentStory);
                
                nextStage('panel_q{qnum}', {next_stage}, {progress});
            }} else {{
                wrongCount++;\n                totalWrongCount++;
                if (wrongCount >= 3) {{
                    showGlitchOverlay();
                    alert("🚨 3회 오답 패널티! 1구역으로 강제 이동됩니다.");
                    wrongCount = 0;
                    document.getElementById('ans1').value = '';
                    nextStage('panel_q{qnum}', 'panel_q1', 0);
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}', wrongCount);
                }}
            }}
        }}
'''
    js_checks += check_fn

# Common JS functions boilerplate
js_boilerplate = """
"""

final_html = base_html.replace("{{panels_placeholder}}", panels_html) + "\n<script>\n" + js_checks + "\n</script>"


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

print("app_m3_01_escape_room.html generated successfully.")
