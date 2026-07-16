# -*- coding: utf-8 -*-\nimport re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m3_02_escape_room.html")
html_path = html_file

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>수수께끼의 인수분해 연금술 공방: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #061a12;
            --glass-bg: rgba(10, 30, 20, 0.75);
            --glass-border: rgba(16, 185, 129, 0.25);
            --accent: #10b981;
            --accent-hover: #34d399;
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
                radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.08) 0%, transparent 40%),
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
            border-top: 1px solid rgba(16, 185, 129, 0.4);
            border-left: 1px solid rgba(16, 185, 129, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(16, 185, 129, 0.15), inset 0 0 20px rgba(16, 185, 129, 0.02);
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
            text-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(16, 185, 129, 0.15);
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
            border: 1px solid rgba(16, 185, 129, 0.15);
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
            background: rgba(16, 185, 129, 0.05);
            border: 1px dashed rgba(16, 185, 129, 0.3);
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
            border: 1px solid rgba(16, 185, 129, 0.3);
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
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
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
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
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
            border: 1px solid rgba(16, 185, 129, 0.2);
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
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
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
            border-bottom: 1px solid rgba(16, 185, 129, 0.2);
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
            <h1>수수께끼의 인수분해 연금술 공방</h1>
            <h2>다항식의 곱셈과 인수분해</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_02/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [연금술 호문쿨루스 알케미-H]: "연금술사 파라켈수스의 비밀 공방에 발을 들여놓았습니다. 이곳의 모든 황금 제조법과 비약의 비밀 배합 공식은 '인수분해'와 '곱셈공식'의 암호로 잠겨 있습니다. 복잡하게 얽힌 수식들을 풀어내어 알맞은 인수들로 쪼개고 결합해야만 탈출의 열쇠를 완성할 수 있습니다. 45분 내에 연금술의 궁극의 공식을 복원하고 탈출하십시오!"
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_02/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [연금술 호문쿨루스 알케미-H]: "배합 비약 항아리에서 황금빛 증기가 뿜어져 나오며 현자의 돌이 모습을 드러냅니다. 공방의 연금술 결계가 스르륵 풀리며 굳게 잠겨있던 문이 열립니다. PARACELSUS의 위대한 비법을 밝혀내어 연금술 공방을 탈출하는 데 성공했습니다!"
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
        const UNIT_ID = "m3_02";

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
    {'qnum': 1, "options": ["10", "3", "7", "5"], 'title': '배합식의 기본 전개', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "크하하! 위대한 파라켈수스의 황금 비약 공방은 이미 뇌사 상태다! 첫 다항식 전개 배합의 핵심 계수조차 쪼개지 못해 도가니가 터져 나갈 것이다!"<br><br><i>부글부글- 청동 도가니 내부에서 불길한 보랏빛 증기가 끓어오르며 압력 눈금이 가파르게 상승합니다. 다항식 $(x+2)(x+3)$ 을 전개할 때 $x$의 일차 계수를 해독 필터에 넣으십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "연금술 조사관님, 조제 밸브를 안정시켜야 합니다! 전개식의 $x$ 계수 값을 대입해 압력을 진정시켜 주십시오!"''', 'qtext': '<strong>Q1. [다항식의 전개]</strong><br>$(x+2)(x+3)$ 을 전개했을 때, $x$의 계수를 구하시오. (숫자만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 2, "options": ["X²+6X+9", "X²+6X+9 아님", "알 수 없음", "해 없음"], 'title': '완전제곱식 조제', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "겨우 첫 약품 밸브를 잠갔군. 하지만 두 번째 증폭 팩 $(x+3)^2$ 의 완전제곱 전개 수식 밸런스를 흐트러뜨려 놨다. 과연 그 식을 완벽히 조립해 낼 수 있겠나?"<br><br><i>지직- 증기 파이프 압력 조절 다이얼 위로 붉은색 수식 가이드 라인이 번뜩입니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "완전제곱식 전개 공식 $(a+b)^2$ 을 사용하십시오! 조절창에 공백 없이 $(x+3)^2$의 최종 전개 수식(대문자 입력)을 기입하십시오!"''', 'qtext': '<strong>Q2. [완전제곱식의 전개 1]</strong><br>$(x+3)^2$ 을 전개한 식을 구하시오. (공백 없이 대문자로 예: X^2+6X+9)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === 'X²+6X+9' || ans === 'X^2+6X+9'"},
    {'qnum': 3, "options": ["4A²-4AB+B²", "4A²-4AB+B² 아님", "알 수 없음", "해 없음"], 'title': '음수 항의 대칭성', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "음수와 복합 계수가 섞인 비약 증폭기 $(2a-b)^2$ 다! 계수 곱하기 공식을 조금만 실수해도 화학 불꽃이 인가되어 타버릴 것이다!"<br><br><i>보닛 밸브 위로 보랏빛 전하 스파크가 발생하며 조제 레토르트 관이 떨립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "계수의 두 배 곱에 주의하십시오! 공식 $(a-b)^2$ 에 의거해 $(2a-b)^2$ 의 전개 식(공백 없이 대문자)을 밸브 패드에 입력해 주십시오!"''', 'qtext': '<strong>Q3. [완전제곱식의 전개 2]</strong><br>$(2a-b)^2$ 을 전개한 식을 구하시오. (공백 없이 대문자로 예: 4A^2-4AB+B^2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '4A²-4AB+B²' || ans === '4A^2-4AB+B^2'"},
    {'qnum': 4, "options": ["X²-16", "X²-16 아님", "알 수 없음", "해 없음"], 'title': '합차 공식의 융합', 'story': '''<strong>[연금 촉매 보정 레지스터 통신 잡음 차단]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "치직... 캡틴! 촉매 융합 장치의 합차 기어 $(x+4)(x-4)$ 가 오염되었습니다! ⚙️ [합차 공식 전개]<br><br>기호 항들이 상쇄되는 융합 식을 조립하여 비약 배합관에 인젝션하십시오!"''', 'qtext': '<strong>Q4. [합차 공식의 전개]</strong><br>$(x+4)(x-4)$ 을 전개한 식을 구하시오. (공백 없이 대문자로 예: X^2-16)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === 'X²-16' || ans === 'X^2-16'"},
    {'qnum': 5, "options": ["-17", "-30", "-13", "-15"], 'title': '상수 유도 연산', 'story': '''<strong>[도가니 하단 약품 주입 밸브 개방]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "치지직... 하단의 보조 주입 밸브를 열어 정밀 정합을 수행해야 합니다! $(x-3)(x+5)$ 식 전개 시 방화벽 밸브에 도출되는 상수항의 정수 값을 마이너스 기호 포함하여 입력하십시오!"''', 'qtext': '<strong>Q5. [전개와 상수항]</strong><br>$(x-3)(x+5)$ 을 전개했을 때, 상수항의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '-15'"},
    {'qnum': 6, "options": ["-3", "-1", "1", "-2"], 'title': '계수 혼합 분석', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "제2막: 공통의 열쇠다. 복합 일차 항들 $(2x+1)(3x-2)$ 의 대각 연산 혼합 계수다. 이 일차 $x$항 계수조차 짚어내지 못한다면 배합 공식은 굳어 버릴 것이다!"<br><br><i>드르륵- 도가니 기단 회전반 위에 수식 복잡 계수 기어가 솟아오릅니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "대각선 곱셈 덧셈 공식을 활용하십시오! 일차항 $x$의 정확한 계수 상수를 입력하여 기어 회전을 멈추십시오!"''', 'qtext': '<strong>Q6. [복잡한 식의 계수]</strong><br>$(2x+1)(3x-2)$ 을 전개했을 때, $x$의 계수를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '-1'"},
    {'qnum': 7, "options": ["(1)", "(2)", "(3)"], 'title': '편리한 배합 공식 선별', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "에너지 노심의 기폭 온도인 $101^2$ 도를 안전하게 환산해 줄 편리한 공식의 번호를 알아맞혀 봐라! 어설프게 아무 번호나 입력했다간 회로가 전소될 뿐이다!"<br><br><i>콘솔에 3개의 대수 공식 번호 선택 패드가 붉은 빛으로 대기합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "온도 $101$은 $(100+1)$ 로 나눌 수 있습니다! 이와 가장 일치하는 완전제곱식 공식의 번호를 선별해 전송하십시오!"''', 'qtext': '<strong>Q7. [곱셈공식의 활용 선별]</strong><br>곱셈 공식을 이용하여 $101^2$ 의 값을 가장 편리하게 계산할 수 있는 공식의 번호를 선택하시오.<br>(1) $(a+b)^2 = a^2+2ab+b^2$<br>(2) $(a-b)^2 = a^2-2ab+b^2$<br>(3) $(a+b)(a-b) = a^2-b^2$', 'placeholder': '번호 입력 (예: 1)', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1' || ans === '(1)' || ans === '1번'"},
    {'qnum': 8, "options": ["2AB", "2AB 아님", "알 수 없음", "해 없음"], 'title': '공통 약수의 격리', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "배합 식 $2a^2b - 4ab^2$ 속에 숨겨진 최대 공통 약수 덩어리를 통째로 격리하지 못한다면, 약물이 넘쳐 역류하리라!"<br><br><i>유리 레토르트 관 내부 수치가 위험 한도선까지 급격히 흔들립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "계수와 문자들의 공통 성분을 최대로 격리하십시오! 공통인수 수식(공백 없이 대문자)을 기입해 압력을 고정하십시오!"''', 'qtext': '<strong>Q8. [공통인수의 추출]</strong><br>다항식 $2a^2b - 4ab^2$ 을 인수분해할 때, 꺼내야 할 가장 큰 공통인수를 구하시오. (공백 없이 대문자로 예: 2AB)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2AB'"},
    {'qnum': 9, 'title': '노심 밸브의 압축 정합', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "확장된 상태의 식 $x^2 + 6x + 9$ 를 원래의 원자로 완전제곱 인수분해 캡슐로 압축하지 못하면, 노심 방화벽이 영구 셧다운될 것이다!"<br><br><i>위이이잉- 경보 차단막이 절반 내려옵니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "완전제곱식으로 되돌릴 시간입니다! 인수분해 결과 수식(공백 없이 대문자로 예: (X+3)^2)을 전송하십시오!"''', 'qtext': '<strong>Q9. [완전제곱식 인수분해]</strong><br>$x^2 + 6x + 9$ 를 인수분해한 식을 구하시오. (공백 없이 대문자로 예: (X+3)^2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(X+3)^2' || ans === '(X+3)²'"},
    {'qnum': 10, "options": ["27", "50", "25", "23"], 'title': '노심 제동 계수 산출', 'story': '''💥 <strong>[비상 로그: 화학 노심 보일러 폭주 및 강제 포맷 시퀀스 기동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "너희의 영리함도 여기까지다! 모든 데이터를 강제 소거해 주마! 5분 뒤 모든 플라스크가 과열 폭발하리라!"<br><br><i>경보 혼 사운드와 함께 노란 연기가 기계실을 채우기 시작합니다. 완전제곱이 되도록 보정 상수 $a$를 산출해 셧다운을 파쇄하십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "과부하 경보 해제 시도! 식 $x^2 - 10x + a$ 가 완전제곱이 되게 할 정밀 상수 $a$의 값을 전송해 폭발을 막으십시오!"''', 'qtext': '<strong>Q10. [완전제곱식이 될 조건]</strong><br>이차식 $x^2 - 10x + a$ 가 완전제곱식이 되기 위한 상수 $a$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '25'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '사다리꼴 배합 게이트 1', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "후... 노심 융합 시퀀스 3분 연장 성공! 이제 제3막 공식 해독 결계에 도달했습니다! ⚙️ [합차 인수분해 게이트]"<br><br><i>화학 게이드 잠금 판넬의 식 $a^2 - 16$ 을 대칭 인수들의 곱 공식(공백 없이 대문자)으로 쪼개어 해독 칩셋을 정렬하십시오!</i>''', 'qtext': '<strong>Q11. [제곱의 차 인수분해]</strong><br>$a^2 - 16$ 을 인수분해한 식을 구하시오. (공백 없이 대문자로 예: (A+4)(A-4))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(A+4)(A-4)' || ans === '(A-4)(A+4)'"},
    {'qnum': 12, 'title': '사다리꼴 배합 게이트 2', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "2단계 합차 회로 통과! 이번엔 다중 문자 계수가 혼합된 $x^2 - 4y^2$ 의 분해 락입니다! ⚙️ [다문자 합차]"<br><br><i>공식의 형태 $a^2 - b^2$ 형태를 유도해 분해한 식(공백 없이 대문자)을 전송하십시오.</i>''', 'qtext': '<strong>Q13. [복합 합차 인수분해]</strong><br>$x^2 - 4y^2$ 을 인수분해한 식을 구하시오. (공백 없이 대문자로 예: (X+2Y)(X-2Y))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(X+2Y)(X-2Y)' || ans === '(X-2Y)(X+2Y)'"},
    {'qnum': 13, 'title': '합과 곱의 마법 기어', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "3단계 기어 밸브입니다! 합해서 5, 곱해서 6이 되는 두 비약 성분 상수를 찾아 식 $x^2 + 5x + 6$ 의 결합 인수를 조립하십시오! ⚙️ [합곱 인수분해]"''', 'qtext': '<strong>Q13. [이차식의 인수분해 1]</strong><br>$x^2 + 5x + 6$ 을 인수분해한 식을 구하시오. (공백 없이 대문자로 예: (X+2)(X+3))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(X+2)(X+3)' || ans === '(X+3)(X+2)'"},
    {'qnum': 14, 'title': '음의 부호 비약 유입', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "4단계 해치 밸브! 합해서 -8, 곱해서 12가 되는 음성 결합 인수를 활용해 식 $x^2 - 8x + 12$ 의 결속을 쪼개십시오! ⚙️ [음수 합곱]"''', 'qtext': '<strong>Q14. [이차식의 인수분해 2]</strong><br>$x^2 - 8x + 12$ 를 인수분해한 식을 구하시오. (공백 없이 대문자로 예: (X-2)(X-6))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(X-2)(X-6)' || ans === '(X-6)(X-2)'"},
    {'qnum': 15, 'title': '대각선 기어 크로스', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H 공방 중앙 코어 제어 100% 완전 환수]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "동기화 정렬 성공! 연금술 공방의 비약 혼합용 대각선 크로스 기어를 완전히 복원했습니다! 이제 흑마법사의 오염 촉매를 정화합니다. 2차 복합식 $2x^2 + 7x + 3$의 대각 결합 인수분해 식을 대문자로 전송하여 주입구 차단을 완성하십시오!"<br><br><i>공방 전면에 환한 에메랄드빛 조명 격자선들이 정렬되며 비약 정제기가 작동하기 시작합니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "제어기 핵심을 탈환했다 해도 내 최종 연산 포뮬러 비약의 덧뺄셈은 절대 풀지 못할 터!"''', 'qtext': '<strong>Q15. [대각선 인수분해]</strong><br>$2x^2 + 7x + 3$ 을 인수분해한 식을 구하시오. (공백 없이 대문자로 예: (2X+1)(X+3))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(2X+1)(X+3)' || ans === '(X+3)(2X+1)'", "extra_class": "glitch-bg"},
    {'qnum': 16, "options": ["6", "1", "3", "5"], 'title': '공통 약수의 선행 묶기', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "배합 원액 $3x^2 - 12$ 다! 공통 계수를 선행 처리로 분배하여 분해하지 못하면 과압으로 렌즈가 파괴될 것이다!"<br><br><i>스위치 패널의 압축 압력이 가파르게 차오르며 경고 부저가 작동합니다.</i>''', 'qtext': '<strong>Q16. [공통인수와 인수분해]</strong><br>다항식 $3x^2 - 12$ 를 인수분해한 식을 구하시오. (공통인수를 먼저 묶어내어 계산하십시오. 공백 없이 대문자로 예: 3(X+2)(X-2))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '3(X+2)(X-2)' || ans === '3(X-2)(X+2)'"},
    {'qnum': 17, 'title': '현자의 수치 연산', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "인수분해를 이용한 $99^2 - 1$ 도가니 가동 수치다! 대수 공식을 실 수치에 투영하여 암산을 끝마쳐라!"<br><br><i>도가니 압력 노즐 위에 최종 중량 연산 값이 요구됩니다.</i>''', 'qtext': '<strong>Q17. [인수분해와 수치 계산]</strong><br>인수분해 공식을 활용하여 $99^2 - 1$ 의 값을 구하시오. (최종 정수 계산 값만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '9800'"},
    {'qnum': 18, 'title': '비약 밀도 대입', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "원소 밀도 값 $x=98$을 식 $x^2 + 4x + 4$ 에 대입해야 할 마지막 정합 시간이다! 대입 속도를 보정할 대수 공식을 활용해 봐라!"<br><br><i>밀도 지시기가 위험 구역 사이에서 흔들립니다.</i>''', 'qtext': '<strong>Q18. [식의 대입 계산]</strong><br>$x=98$ 일 때, 식 $x^2 + 4x + 4$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '10000'"},
    {'qnum': 19, 'title': '공식 비약의 내적 가치', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "두 개의 원소 값 $a+b=5$ 와 $a-b=3$ 이 융합 반응을 일으킬 때, 화합물의 반응 수치 $a^2 - b^2$ 의 최종 출력을 대어라!"<br><br><i>약물 계량 피스톤이 상하 운동 속도를 감속하지 못하고 오작동 지연을 일으킵니다.</i>''', 'qtext': '<strong>Q19. [식의 값 구하기]</strong><br>$a+b=5, a-b=3$ 일 때, $a^2 - b^2$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '15'"},
    {'qnum': 20, "options": ["2X-2", "2X-2 아님", "알 수 없음", "해 없음"], 'title': '최종 비약 배합비의 합산', 'story': '''🔮 <strong>[최종 현자의 돌 배합 완료 및 차원 관문 개방]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[알케미-H]</span>: "조사관님! 이제 원래의 연금술 아카데미 광장으로 차원 이동할 마지막 마스터 슬롯만 남았습니다! 제 모든 마스터 에너지를 차원 슬롯에 투입하겠습니다! 곱이 $x^2 - 2x - 15$를 형성하는 두 개 일차 비약의 최종 합산 식(공백 없이 대문자)을 입력하여 탈출 문을 여십시오! 연금술의 완성이 코앞입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[흑마법사-M]</span>: "안 돼... 내 철저했던 연금 파괴 술식이... 완벽한 인수분해 기어에 물려 영구 격리 소멸되다니...!"''', 'qtext': '<strong>Q20. [일차식의 합 구하기]</strong><br>두 일차식의 곱이 $x^2 - 2x - 15$ 일 때, 이 두 일차식의 합을 구하시오. (공백 없이 대문자로 예: 2X-2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2X-2'", "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_02/q{qnum}.png" alt="Background" class="panel-image">
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

print("app_m3_02_escape_room.html generated successfully.")
