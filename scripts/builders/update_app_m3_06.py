# -*- coding: utf-8 -*-\nimport re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m3_06_escape_room.html")
html_path = html_file

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전설 속 아서왕의 원탁 수수께끼: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #1e0b10;
            --glass-bg: rgba(35, 15, 20, 0.75);
            --glass-border: rgba(225, 29, 72, 0.25);
            --accent: #e11d48;
            --accent-hover: #fb7185;
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
                radial-gradient(circle at 10% 20%, rgba(225, 29, 72, 0.08) 0%, transparent 40%),
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
            border-top: 1px solid rgba(225, 29, 72, 0.4);
            border-left: 1px solid rgba(225, 29, 72, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(225, 29, 72, 0.15), inset 0 0 20px rgba(225, 29, 72, 0.02);
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
            text-shadow: 0 0 30px rgba(225, 29, 72, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(225, 29, 72, 0.15);
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
            border: 1px solid rgba(225, 29, 72, 0.15);
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
            background: rgba(225, 29, 72, 0.05);
            border: 1px dashed rgba(225, 29, 72, 0.3);
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
            border: 1px solid rgba(225, 29, 72, 0.3);
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
            box-shadow: 0 0 10px rgba(225, 29, 72, 0.3);
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
            box-shadow: 0 4px 15px rgba(225, 29, 72, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(225, 29, 72, 0.5);
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
            border: 1px solid rgba(225, 29, 72, 0.2);
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
            box-shadow: 0 0 10px rgba(225, 29, 72, 0.3);
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
            border-bottom: 1px solid rgba(225, 29, 72, 0.2);
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
            <h1>전설 속 아서왕의 원탁 수수께끼</h1>
            <h2>원의 성질</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_06/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [원탁의 기사 마네킹 랜슬롯-M]: "중세 카멜롯 성의 깊은 지하 밀실에 위치한 '아서왕의 원탁 회의장'에 도착했습니다. 전설의 원탁 중앙에 박혀있는 왕의 보검 '엑스칼리버'를 감싸고 있는 투명 보호 장막은 원의 기하학적 성질로 구성된 봉인으로 봉쇄되어 있습니다. 현의 길이, 접선의 대칭성, 원주각의 각도 계산을 통해 제한시간 45분 내에 보호막을 해제하고 검을 뽑아 탈출하십시오!"
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_06/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [원탁의 기사 마네킹 랜슬롯-M]: "원탁 주위에 배치된 기사들의 방패 문양 12개가 동시에 청색으로 점등되며 결계 장막이 거칩니다. 원탁의 중심에서 엑스칼리버를 무사히 손에 쥐는 순간, 뒤쪽 비밀 통로의 돌벽이 열립니다. 아서왕의 시험을 이겨내고 탈출한 용사들의 승리를 선포합니다!"
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
        const UNIT_ID = "m3_06";

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
    {'qnum': 1, "options": ["이등분", "삼등분", "수직", "무한분"], 'title': '원형 보호막 현 수직분해', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "크하하! 둥근 아더 기사단의 원탁 제어실은 이미 반역 술식에 완전히 점령되었다! 중심에서 보호막 현에 수선을 내렸을 때 발생하는 절반 분해 정리조차 모르는 하찮은 침입자들아, 기단 과부하에 휩쓸려 사라지거라!"<br><br><i>둥근 벽면의 홀로그램 장벽 위로 기하학적인 원과 내부 수직 현의 단면선들이 차갑게 나타납니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "조사관님, 원형 실드의 수선 정합 장치를 깨워야 합니다! 중심에서 내린 수선이 현을 어떻게 처리하는지 그 대칭 정리 명칭(한글 세 글자)을 입력 콘솔에 대입하십시오!"''', 'qtext': '<strong>Q1. [현의 수직이등분]</strong><br>원의 중심에서 현에 내린 수선은 그 현을 어떻게 하는가? (한글 세 글자로 입력. 예: 이등분)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '이등분'"},
    {'qnum': 2, "options": ["16", "6", "8", "10"], 'title': '원형 격벽 외선 길이', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "현 분해 락을 통과했군. 그렇다면 반지름이 5이고, 원 중심에서 현 AB까지 수직 거리가 3일 때의 기압 격벽 현 AB의 전체 수치 길이를 대 봐라!"<br><br><i>실드 게이지가 3과 5의 비율 사이에서 지이잉 거리는 스파크 소리를 내뿜으며 요동칩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "피타고라스 직각 정합 활용! 수직 이등분된 현의 반을 구해 2배를 처리하십시오! 전체 현 AB의 길이를 입력하여 압력을 고정하십시오!"''', 'qtext': '<strong>Q2. [현의 길이 계산]</strong><br>원 O 의 반지름의 길이가 5 이고, 원의 중심에서 현 AB 까지의 거리가 3 일 때, 현 AB 의 길이를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '8'"},
    {'qnum': 3, "options": ["같다", "다르다", "절반이다", "두배다"], 'title': '이중 현의 평행비', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "중심에서 완벽하게 동일한 거리에 위치한 두 현의 실질적 전력 길이비다! 그 두 현의 물리적 길이는 서로 어떠할까?"<br><br><i>콘솔 스위치 위에 두 글자의 상태 한글 힌트 불빛이 켜집니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "중심 거리와 현의 길이 동조 정리! 두 현의 상대적 크기 상태(한글 두 글자)를 콘솔 창에 전송해 기어를 맞물리십시오!"''', 'qtext': '<strong>Q3. [중심에서 같은 거리에 있는 현]</strong><br>한 원에서 중심으로부터 같은 거리에 있는 두 현의 길이는 서로 어떠한가? (한글 두 글자로 입력. 예: 같다)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '같다'"},
    {'qnum': 4, "options": ["4", "6", "2", "8"], 'title': '이중 실드 대칭 거리', 'story': '''<strong>[원형 모터 축 대칭 전력 필터 피복 차단]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "치직... 캡틴! 두 현 AB와 CD의 길이가 둘 다 6으로 완벽히 동일합니다! 현 AB까지 수직 중심 거리가 4일 때, 반대편 현 CD까지의 중심 거리를 구하십시오! ⚙️ [대칭 거리 매핑]"''', 'qtext': '<strong>Q4. [현의 거리와 길이]</strong><br>원 O 에서 현 AB 의 길이가 6 이고 현 CD 의 길이도 6 이다. 원의 중심에서 현 AB 까지의 거리가 4 일 때, 중심에서 현 CD 까지의 거리를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '4'"},
    {'qnum': 5, "options": ["8", "10", "20", "12"], 'title': '수선 지시반 현 복원', 'story': '''<strong>[메인 서보 모터 축 접지 릴레이 가동]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "치지직... 보조 서보 밸브가 기동됩니다! ⚙️ [현의 수직이등분 복원]<br><br>원의 중심에서 현 AB에 내린 수선의 발 M에 대하여, 절반 마디 AM의 길이가 5입니다. 현 AB 전체 전력 길이를 입력하여 접지를 복구하십시오!"''', 'qtext': '<strong>Q5. [현의 수직이등분의 성질]</strong><br>원 O 의 중심에서 현 AB 에 내린 수선의 발을 M 이라 할 때, 선분 AM 의 길이가 5 이다. 현 AB 의 길이를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '10'"},
    {'qnum': 6, "options": ["같다", "다르다", "절반이다", "두배다"], 'title': '원 밖의 접선 대칭성', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "제2막: 외곽 접선 락이다. 원 밖의 한 제어기 점 P에서 뿜어낸 두 접선 통로의 상대적 거리는 서로 어떠할까?"<br><br><i>둥근 보호막 외부 투사 노즐 두 가닥이 허공에서 교차 결합음을 냅니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "외접선 길이 일치 정리! 두 접선 경로의 물리적 길이 상태(한글 두 글자)를 주입해 외곽 게이트를 잠그십시오!"''', 'qtext': '<strong>Q6. [접선의 길이 성질]</strong><br>원 밖의 한 점에서 그 원에 그은 두 접선의 길이는 서로 어떠한가? (한글 두 글자로 입력. 예: 같다)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '같다'"},
    {'qnum': 7, "options": ["16", "6", "8", "10"], 'title': '접점 레이저 통로 계측', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "접점 T로 통하는 직각 반지름 빔의 길이가 6이고, 제어점 P와 원의 중심 O를 잇는 중심선 OP 길이가 10일 때, 접선 PT의 진짜 레이저 통로 길이를 대라!"<br><br><i>지시판 수치가 수직 접선 마커 지점에서 바르르 떨리며 붉게 변합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "반지름과 접선의 수직각 직각 정합! 피타고라스를 적용해 접선 PT의 계측 길이(정수)를 콘솔에 전송하십시오!"''', 'qtext': '<strong>Q7. [접선의 길이 계산]</strong><br>원 O 의 반지름의 길이가 6 이고, 원 밖의 한 점 P 에서 원에 그은 접선 PT 의 접점 T 에 대하여 선분 OP 의 길이가 10 일 때, 접선의 길이 PT 를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '8'"},
    {'qnum': 8, "options": ["128", "132", "130", "260"], 'title': '원형 챔버 대각 각도', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "원 밖의 조향각 APB가 50도로 고정되어 있다. 이 챔버의 내부각 AOB를 계측하지 못하면 방열 밸브가 터져 우주 원탁이 박살날 것이다!"<br><br><i>둥근 사각형 제어 기판 중심에 고열 빨간색 전하가 솟구칩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "접선 대각 합 180도 규칙! 사각형 AOBP의 접각 90도 두 개를 뺀 잔여 대각 각도(숫자만)를 계량해 주십시오!"''', 'qtext': '<strong>Q8. [접선이 이루는 각]</strong><br>원 밖의 점 P 에서 두 접점 A, B 에 접선을 그어 형성된 각 $\\angle APB = 50^\\circ$ 일 때, 사각형 AOBP 의 내부각 $\\angle AOB$ 의 크기(도)를 구하시오. (숫자만 적으시오.)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '130'"},
    {'qnum': 9, "options": ["같다", "다르다", "절반이다", "두배다"], 'title': '외접 프레임 대변합', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "원자로에 완벽히 달라붙는 외접 사각형 프레임이다! 마주 보는 두 쌍의 대변 길이의 총합들은 서로 어떠할까?"<br><br><i>조절반 스크린에 가로 세로 프레임 빔의 상대적 정렬 상태 지시기가 대기합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "외접 사각형 대변합 일치 규칙! 마주 보는 대변합의 동일성 상태(한글 두 글자)를 기입하여 락을 헤제하십시오!"''', 'qtext': '<strong>Q9. [외접사각형의 성질]</strong><br>원에 외접하는 사각형의 마주 보는 두 쌍의 대변의 길이의 합은 서로 어떠한가? (한글 두 글자로 입력. 예: 같다)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '같다'"},
    {'qnum': 10, "options": ["1/2", "2", "1/3", "0.5"], 'title': '원주 주파수 비율', 'story': '''💥 <strong>[비상 로그: 원탁 에너지 코어 중력 격자 붕괴 및 강제 포맷 작동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "마지막 수단이다! 모든 기사단 데이터 메모리를 물리적으로 분쇄하겠다! 5분 뒤 가스 터빈 노즐이 오버플로우 폭발하리라!"<br><br><i>쉬이이익- 원탁 중앙 보일러 틈으로 뜨거운 붉은 연기가 가쁘게 피어오릅니다. 원주 주파수 비율 값을 정확히 입력해 자폭 장치를 차단하십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "차단 격벽 기동 시도! 한 호에 대한 원주각의 크기가 그 호의 중심각 크기의 몇 배(슬래시 분수 형태, 예: 1/2)가 되는지 전송하십시오!"''', 'qtext': '<strong>Q10. [원주각과 중심각]</strong><br>한 호에 대한 원주각의 크기는 그 호에 대한 중심각의 크기의 몇 배인가? (슬래시를 사용해 분수로 쓰시오. 예: 1/2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1/2' || ans === '0.5'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '원주각 불변 법칙', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "후... 기단 강제 자폭 중지 성공! 이제 제3막 원주각 해독 결계 안으로 진입합니다! ⚙. [원주각 동일 정리]"<br><br><i>동일 호에 기인한 여러 원주각들의 크기는 위치가 달라져도 서로 어떠합니까? 상태 정합 한글(예: 같다)을 전송해 주십시오.</i>''', 'qtext': '<strong>Q11. [호에 대한 원주각 성질]</strong><br>한 호에 대한 원주각들의 크기는 위치에 관계없이 모두 어떠한가? (한글 두 글자로 입력. 예: 같다)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '같다'"},
    {'qnum': 12, 'title': '지름 궤도 기준각', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "2단계 지름 궤도 기준각 락입니다! 반원(지름)을 딛고 서 있는 모든 원주각의 정확한 크기(도)를 입력해 주십시오! ⚙️ [지름에 대한 원주각]"''', 'qtext': '<strong>Q12. [지름에 대한 원주각 크기]</strong><br>반원(지름)에 대한 원주각의 크기(도)는 몇 도인가? (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '90'"},
    {'qnum': 13, 'title': '중심각 역산 원주각', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "3단계 관문! 호 AB의 중심각이 80도일 때, 원주 위를 향해 발사되는 원주각 APB의 위상 각도(도)를 계측하십시오! ⚙️ [중심각에서 원주각]"''', 'qtext': '<strong>Q13. [원주각의 크기 구하기]</strong><br>원 O 에서 호 AB 에 대한 중심각의 크기가 $80^\\circ$ 일 때, 원주각 $\\angle APB$ 의 크기(도)를 구하시오. (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '40'"},
    {'qnum': 14, 'title': '원주각 순산 중심각', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "4단계 관문입니다! 원주각의 위상 크기가 35도일 때, 동일 호를 중심으로 물리는 중심각 톱니바퀴의 정밀 크기(도)를 역추적해 출력하십시오! ⚙️ [원주각에서 중심각]"''', 'qtext': '<strong>Q14. [중심각의 크기 구하기]</strong><br>원 O 에서 한 호에 대한 원주각의 크기가 $35^\\circ$ 일 때, 동일한 호에 대한 중심각의 크기(도)를 구하시오. (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '70'"},
    {'qnum': 15, 'title': '지름 내접 삼각 각도', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M 원탁 코어 동력 기단 권한 100% 완전 복원]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "완벽 복구 성공! 아더 기사단의 원탁 제어반 전체의 레이더 좌표 정합과 외접 회로망을 완전히 통제했습니다! 반역 기어 격벽을 소거하기 위해, 지름 AB에 걸친 원주각 ACB 직각삼각형에서 $\\angle A=50^\\circ$ 일 때, 잔여 내부각 $\\angle B$ 의 위상 크기(도)를 전송해 주십시오!"<br><br><i>원탁 기단 위로 푸른빛의 대칭 기하 홀로그램 빔이 안착하며 격벽 문고리가 스르륵 풀립니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "제어 중심국을 탈환당하다니...! 하지만 외곽 원주 대각 결계 트랩은 결코 해제하지 못하리라!"''', 'qtext': '<strong>Q15. [지름을 포함한 직각삼각형]</strong><br>지름 AB 를 지나는 원주각 $\\angle ACB$ 가 형성되어 있는 원 O 에서, $\\angle A = 50^\\circ$ 일 때, 각 $\\angle B$ 의 크기(도)를 구하시오. (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '40'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '내접 사각형 마주 보는 각', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "원 내부에 내접해 기하 락을 형성하는 사각형이다! 마주 보는 두 대각 크기의 각도 총합은 몇 도인가?"<br><br><i>내접 프레임 외선 조향판이 깜빡이며 대각 각도 총합 입력을 요구합니다.</i>''', 'qtext': '<strong>Q16. [내접사각형의 대각의 합]</strong><br>원에 내접하는 사각형에서 한 쌍의 대각의 크기의 합은 몇 도인가? (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '180'"},
    {'qnum': 17, 'title': '내접 프레임 대각 계측', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "내접 사각형 ABCD 의 제1각 $\\angle A = 75^\\circ$ 다! 마주 보며 기류 보정을 누설하고 있는 대각 $\\angle C$ 의 정확한 각도(도)를 입력해라!"<br><br><i>대각선 각도계 계측기 눈금이 깜빡이며 정렬 번호를 대기시킵니다.</i>''', 'qtext': '<strong>Q17. [내접사각형의 대각 계산]</strong><br>원에 내접하는 사각형 ABCD 에서 각 $\\angle A = 75^\\circ$ 일 때, 마주 보는 대각 $\\angle C$ 의 크기(도)를 구하시오. (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '105'"},
    {'qnum': 18, 'title': '외각 통과 내대각', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "내접 사각형 한 외각 통로의 크기가 85도다! 이와 이웃하지 않는 내부 마주 보는 대대각(내대각)의 위상 크기를 대 봐라!"<br><br><i>외각 센서 밸브가 차단 동작음을 내며 내대각 수치 매칭을 기다립니다.</i>''', 'qtext': '<strong>Q18. [내접사각형의 외각과 내대각]</strong><br>원에 내접하는 사각형 ABCD 의 한 외각의 크기가 $85^\\circ$ 일 때, 이와 이웃하지 않는 대각(내대각)의 크기(도)를 구하시오. (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '85'"},
    {'qnum': 19, 'title': '접선-현 진동각 궤적', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "원 접선 PT와 접점 현 TA가 이루는 접선 진동각 $\\angle ATP = 60^\\circ$ 다! 이 궤적이 내부에 형성하는 현의 원주각 크기(도)를 대 봐라!"<br><br><i>접선 빔 검출 바늘이 정렬선에서 정지하여 깜빡입니다.</i>''', 'qtext': '<strong>Q19. [접선과 현이 이루는 각]</strong><br>원 O 의 접선 PT 에 대하여 접점 T 를 지나는 현 TA 가 만드는 각 $\\angle ATP = 60^\\circ$ 일 때, 그 현에 대한 원주각의 크기(도)를 구하시오. (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '60'"},
    {'qnum': 20, 'title': '동일 호 원주각 비율', 'story': '''🔮 <strong>[최종 원탁 실드 가동 및 차원 탈출]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[랜슬롯-M]</span>: "조사관님! 이제 원탁 중심의 차원 가속 통로를 가동할 마지막 수치 비율만 남았습니다! 제 모든 실드 에너지를 기단에 수렴하겠습니다! 길이가 완전히 동일한 두 원호에 대한 두 원주각의 크기 비율(몇 대 몇, 즉 실수 수치)을 입력해 차원 탈출 해치를 여십시오! 원탁 궤도가 마침내 정상 가동됩니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[모드레드-AI]</span>: "안 돼... 내 반역 통제 실드 루프가... 대칭형 원주각 정리에 완전히 물려 소멸하다니...!"''', 'qtext': '<strong>Q20. [원주각의 크기와 호의 길이]</strong><br>원 O 에서 길이가 서로 같은 두 호에 대한 두 원주각의 크기의 비율은 몇 대 몇인지 수치 비율로 적으시오. (예: 1)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1'", "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_06/q{qnum}.png" alt="Background" class="panel-image">
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

print("app_m3_06_escape_room.html generated successfully.")
