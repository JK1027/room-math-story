# -*- coding: utf-8 -*-\nimport re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m3_05_escape_room.html")
html_path = html_file

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>그리스 수학자 테오도루스의 천문 측정대: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #1c140a;
            --glass-bg: rgba(35, 25, 15, 0.75);
            --glass-border: rgba(245, 158, 11, 0.25);
            --accent: #f59e0b;
            --accent-hover: #fbbf24;
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
                radial-gradient(circle at 10% 20%, rgba(245, 158, 11, 0.08) 0%, transparent 40%),
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
            border-top: 1px solid rgba(245, 158, 11, 0.4);
            border-left: 1px solid rgba(245, 158, 11, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(245, 158, 11, 0.15), inset 0 0 20px rgba(245, 158, 11, 0.02);
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
            text-shadow: 0 0 30px rgba(245, 158, 11, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(245, 158, 11, 0.15);
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
            border: 1px solid rgba(245, 158, 11, 0.15);
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
            background: rgba(245, 158, 11, 0.05);
            border: 1px dashed rgba(245, 158, 11, 0.3);
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
            border: 1px solid rgba(245, 158, 11, 0.3);
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
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
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
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
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
            border: 1px solid rgba(245, 158, 11, 0.2);
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
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
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
            border-bottom: 1px solid rgba(245, 158, 11, 0.2);
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
            <h1>그리스 수학자 테오도루스의 천문 측정대</h1>
            <h2>삼각비</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_05/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [별빛 관측기 아스트로-A]: "고대 그리스의 유명한 천문 측정 학자 테오도루스의 천체 관측소에 입장하셨습니다. 하늘에 흩어진 신비한 별자리들의 거리와 고도를 측정하여 천문 관측 구체의 고정 장치를 해제해야 합니다. 별빛의 각도와 삼각형의 변의 비율을 나타내는 '삼각비' 공식을 사용해 45분 내에 모든 측정대 센서를 동기화하고 탈출하십시오!"
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_05/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [별빛 관측기 아스트로-A]: "천체 구체 모델의 렌즈 각도들이 오차 없이 맞아떨어지며 관측 구체가 웅장한 회전 소리를 내며 빛을 투사합니다. 돔탑의 쇠사슬 빗장이 덜컥 풀리며 지상의 문이 개방됩니다. 삼각비의 지배자로 거듭나 천문 관측소 탈출에 성공했습니다!"
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
        const UNIT_ID = "m3_05";

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
    {'qnum': 1, "options": ["사인", "코사인", "탄젠트"], 'title': '중력 기준비 측정', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "크하하! 우리 우주선은 특이점 중력 결계에 걸려 멈추었다! 빗변과 높이의 비율 조향각 명칭조차 선언하지 못하는 하찮은 탐사대원들아, 그대로 빨려 들어가 궤적의 먼지가 되거라!"<br><br><i>우주선 메인 디스플레이에 차원 지향 기하 삼각형 각도가 빨갛게 점멸합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "탐사 조사관님, 조향 코어 센서를 깨워 주십시오! 직각삼각형 빗변에 대한 높이의 삼각비 명칭(한글 두 글자)을 정확히 입력해 제어 주파수를 고정하십시오!"''', 'qtext': '<strong>Q1. [삼각비의 정의]</strong><br>직각삼각형에서 빗변의 길이에 대한 높이의 비율을 나타내는 삼각비의 명칭을 구하시오. (한글 두 글자로 입력. 예: 사인)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '사인'"},
    {'qnum': 2, "options": ["1/2", "0.5", "√3/2", "1"], 'title': '중력 30도 경사각', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "30도 각도의 미세 조향 장치를 망가뜨려 놓았다. 이 각도의 고유 분수 지수 $\\sin 30^\\circ$ 의 출력 수치조차 정렬하지 못하면 우주선은 찌그러질 것이다!"<br><br><i>지이이잉- 조향 로터 방향 다이얼이 폭주하며 위험 임계치 근처를 가리킵니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "특수각 삼각비 대입 시도! 슬래시(/)를 이용해 $\\sin 30^\\circ$ 의 정확한 분수 값을 입력하십시오!"''', 'qtext': '<strong>Q2. [특수각의 삼각비 1]</strong><br>$\\sin 30^\\circ$ 의 값을 구하시오. (슬래시를 사용해 분수로 나타내시오. 예: 1/2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1/2' || ans === '0.5'"},
    {'qnum': 3, "options": ["√2/2", "√3/2", "1/2", "1"], 'title': '밑변 45도 센서', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "이번엔 45도 수평 밸런서다! 이 궤도의 수평 융합률 $\\cos 45^\\circ$ 의 기하 수식 비율을 입력창에 전송할 수 있겠나?"<br><br><i>메인 가로 복원 엔진 격벽이 45도 경사를 이루며 우주선 몸체가 한쪽으로 기웁니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "수평 각도 복원 시작! 특수 기호 루트 $\\sqrt{}$ 와 슬래시(/)를 사용해 $\\cos 45^\\circ$ 의 값(예: √2/2)을 입력 콘솔에 전입하십시오!"''', 'qtext': '<strong>Q3. [특수각의 삼각비 2]</strong><br>$\\cos 45^\\circ$ 의 값을 구하시오. (루트와 분수를 사용해 공백 없이 나타내시오. 예: √2/2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√2/2'"},
    {'qnum': 4, "options": ["√3", "√2", "1", "3"], 'title': '상승 60도 빔 노즐', 'story': '''<strong>[우주선 수평 빔 노즐 전자기 실드 보정]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "치직... 조사관님! 60도 경사 방어 레이저의 빔 강도인 $\\tan 60^\\circ$ 수식이 왜곡되었습니다! ⚙️ [탄젠트 빔 복원]<br><br>루트 기호를 사용하여 빔의 증폭 수치를 입력창에 전입하십시오!"''', 'qtext': '<strong>Q4. [특수각의 삼각비 3]</strong><br>$\\tan 60^\\circ$ 의 값을 구하시오. (예: √3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√3'"},
    {'qnum': 5, "options": ["4/5", "3/5", "1", "0.8"], 'title': '가변 삼각 격자비', 'story': '''<strong>[우주선 중앙 가변 격벽 락 장치 기동]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "치지직... 격자 통제 룸 개방을 위해 기하 차원 정합을 완료해야 합니다! ⚙️ [직각삼각형의 삼각비]<br><br>각 $B=90^\\circ$, 빗변 $AC=5$, 높이 $BC=4$, 밑변 $AB=3$ 인 격벽 모듈에서 $\\sin A$ 의 융합 비(분수)를 입력하십시오!"''', 'qtext': '<strong>Q5. [삼각비의 계산]</strong><br>직각삼각형 ABC 에서 $\\angle B = 90^\\circ$ 이고, 빗변 $AC = 5$, 높이 $BC = 4$, 밑변 $AB = 3$ 일 때, $\\sin A$ 의 값을 구하시오. (슬래시 분수 입력 예: 4/5)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '4/5' || ans === '0.8'"},
    {'qnum': 6, "options": ["1", "0", "1/2", "√3/2"], 'title': '중력 최대 지향점 90도', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "제2막: 삼각비의 한계선이다. 조향 실린더가 수직 수평을 완전히 벗어나는 한계 각도 90도 상태다! $\\sin 90^\\circ$ 의 극점 상수를 통과시키지 못하면 실린더는 파괴된다!"<br><br><i>위이이잉- 수직 레이저 조준 빔이 벽 끝까지 도달하며 붉게 오버로드됩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "수직 극점 정합! 사인 함수가 가질 수 있는 90도 최대 정수 값을 기입하여 리밸런싱해 주십시오!"''', 'qtext': '<strong>Q6. [임계 삼각비 1]</strong><br>$\\sin 90^\\circ$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1'"},
    {'qnum': 7, "options": ["0", "1", "1/2", "√2/2"], 'title': '수평 수축 한계 90도', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "이번엔 수평의 소멸 수치다! 수평 성분이 완전히 0이 되는 $\\cos 90^\\circ$ 의 결과 값을 도출해 계기판을 잠가봐라!"<br><br><i>수평 조향 기어의 회전 반경 눈금이 수축해 지시선이 바닥을 칩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "수평 성분 소멸 상수 입력! 코사인이 90도 각도에서 수축해 소멸하는 수치를 대입하여 기어를 정렬하십시오!"''', 'qtext': '<strong>Q7. [임계 삼각비 2]</strong><br>$\\cos 90^\\circ$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '0'"},
    {'qnum': 8, "options": ["1", "√3", "√3/3", "0"], 'title': '대칭 반사각 45도', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "대칭 반사 빔 각도 $\\tan 45^\\circ$ 다! 밑변과 높이가 같아 완전한 균형을 이루는 이 비례 수치를 입력해라!"<br><br><i>레이저 반사경이 정확히 45도 격자 눈금에 머물러 정렬 대기음을 내뿜습니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "대칭비 입력! 수평 밑변과 수직 높이가 동일할 때의 탄젠트 비율 상수를 입력창에 전송하십시오!"''', 'qtext': '<strong>Q8. [임계 삼각비 3]</strong><br>$\\tan 45^\\circ$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1'"},
    {'qnum': 9, "options": ["1", "0", "1/2", "√3/2"], 'title': '출발 수평각 0도', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "우주선이 비행을 시작하기 전 각도 0도의 원점 상태다. $\\cos 0^\\circ$ 의 최대 수평 결속 계수를 기입창에 정합해 봐라!"<br><br><i>출발 조종간 바늘이 완전히 수평선(0도)으로 젖혀지며 경고등이 깜빡입니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "수평 결속 계수 대입! 코사인 각도가 0도일 때 지니는 최대 비율 수치 정수를 콘솔에 입력하십시오!"''', 'qtext': '<strong>Q9. [임계 삼각비 4]</strong><br>$\\cos 0^\\circ$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1'"},
    {'qnum': 10, "options": ["√3", "2√3", "1", "0"], 'title': '합성 삼각 주파수', 'story': '''💥 <strong>[비상 로그: 블랙홀 중력 왜곡 엔진 노심 온도 임계점 돌파 및 강제 붕괴 작동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "더는 지체할 시간 없다! 블랙홀 노심을 붕괴시켜 우주선과 너희를 모조리 소멸시키겠다! 5분 뒤 강제 폭발 시퀀스가 완료된다!"<br><br><i>끼이이익- 웅장한 중력 격벽이 조여 오며 붉은빛 경보 스파크가 기계를 태웁니다. 두 특수각 삼각비의 덧셈 합성 주파수 값을 입력해 자폭 칩셋을 우회 차단하십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "붕괴 제동 시스템 전개 시도! 수식 $\\sin 60^\\circ + \\cos 30^\\circ$ 의 계산된 최종 수치(예: √3)를 기입창에 주입하십시오!"''', 'qtext': '<strong>Q10. [삼각비의 덧셈 계산]</strong><br>$\\sin 60^\\circ + \\cos 30^\\circ$ 의 값을 구하시오. (루트를 사용해 공백 없이 입력. 예: √3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√3'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '수직 제로 조향각 0도', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "후... 붕괴 위기 3분 연장 성공! 이제 제3막 삼각 궤적 해독 관문으로 접근합니다! ⚙️ [제로 조향각 정렬]"<br><br><i>경사각이 전혀 없는 수평 상태에서 발생하는 수직 기압 상승비인 $\\tan 0^\\circ$ 의 결과 정수 값을 전송해 게이트를 개방하십시오.</i>''', 'qtext': '<strong>Q11. [기본 삼각비 5]</strong><br>$\\tan 0^\\circ$ 의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '0'"},
    {'qnum': 12, 'title': '동조 융합곱 45도', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "2단계 융합곱 락입니다! 대칭 에너지파 $\\sin 45^\\circ$ 와 $\\cos 45^\\circ$ 의 고주파 곱을 도출하십시오! ⚙️ [삼각비의 곱셈]"<br><br><i>두 특수 값을 곱한 분수(슬래시 이용, 예: 1/2)를 입력창에 주입하십시오.</i>''', 'qtext': '<strong>Q12. [삼각비의 곱셈 계산]</strong><br>$\\sin 45^\\circ \\times \\cos 45^\\circ$ 의 값을 구하시오. (슬래시를 사용해 분수로 나타내시오. 예: 1/2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1/2' || ans === '0.5'"},
    {'qnum': 13, 'title': '유리화된 레이저 위상', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "3단계 해치 관문입니다! 유리화 처리된 레이저 빔 위상인 $\\tan 30^\\circ$ 의 수식을 계측하십시오! ⚙️ [분모의 유리화]"<br><br><i>삼각비 표에 의거해 유리화된 값(예: √3/3)을 입력창에 전송하십시오.</i>''', 'qtext': '<strong>Q13. [유리화된 삼각비]</strong><br>$\\tan 30^\\circ$ 의 값을 구하시오. (루트와 분수를 사용해 공백 없이 나타내시오. 예: √3/3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√3/3'"},
    {'qnum': 14, 'title': '항해 빗변 투영 고도', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "4단계 관문입니다! 직각삼각형 항해 포트에서 빗변 $AB=10$, 조향각 $\\angle A=30^\\circ$ 일 때, 수직 투영 고도인 높이 $BC$의 실제 길이를 계측해 주십시오! ⚙️ [빗변과 사인의 응용]"''', 'qtext': '<strong>Q14. [빗변과 높이의 계산]</strong><br>직각삼각형 ABC 에서 $\\angle C = 90^\\circ$ 이고 빗변 $AB = 10$, $\\angle A = 30^\\circ$ 일 때, 높이 $BC$ 의 길이를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 15, 'title': '수평 경사 높이 정합', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A 우주선 메인 항법 제어반 100% 완전 환수]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "동기화 완료! 블랙홀 중력장 속 우주선 중력 리펄서와 차원 필터를 완벽히 제어국으로 복귀시켰습니다! 이제 블랙홀의 최종 탈출 외각 격벽을 엽니다. 밑변 $AC=8$, 경사각 $\\angle A=45^\\circ$ 인 항로에서 수직 대변 $BC$의 실 정수 길이를 전송하여 외각 도킹 해치를 연방 개방하십시오!"<br><br><i>우주선 메인 활주 윈도우 위로 푸른빛의 안전 비행 삼각선들이 그려지며, 블랙홀 흡수 영역을 가로질러 탈출 경로가 열립니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "중앙 제어 망을 빼앗기다니...! 하지만 미지 영역의 삼각비 넓이 활용 트랩은 결코 넘지 못하리라!"''', 'qtext': '<strong>Q15. [밑변과 탄젠트 응용]</strong><br>직각삼각형 ABC 에서 $\\angle C = 90^\\circ$ 이고 밑변 $AC = 8$, $\\angle A = 45^\\circ$ 일 때, 대변 $BC$ 의 길이를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '8'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '예각 에너지 융합 넓이 1', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "두 가닥 빔의 융합 길이 4와 6, 그리고 사이 각도 30도를 활용해 합성되는 삼각 에너지 넓이를 선언해 봐라! 넓이 수치가 틀어지면 융합 기압이 차올라 전송망이 끊어지리라!"<br><br><i>양방향 에너지 게이지 빔이 삼각형 격자를 형성하며 충전됩니다.</i>''', 'qtext': '<strong>Q16. [삼각형의 넓이 계산 1]</strong><br>두 변의 길이가 각각 4, 6이고 그 사잇각이 $30^\\circ$ 인 삼각형의 넓지를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '6'"},
    {'qnum': 17, 'title': '예각 에너지 융합 넓이 2', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "그렇다면 45도 반사 각도 레이저 빔이다! 두 변 6, 8과 사이 반사각 45도로 형성되는 삼각형 에너지 넓이 식을 정확히 해독해 봐라!"<br><br><i>계기판 모니터 도면 위로 복잡한 루트가 포함된 에너지 총합 단위가 요구됩니다.</i>''', 'qtext': '<strong>Q17. [삼각형의 넓이 계산 2]</strong><br>두 변의 길이가 각각 6, 8이고 그 사잇각이 $45^\\circ$ 인 삼각형의 넓이를 구하시오. (루트를 사용해 공백 없이 나타내시오. 예: 12√2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '12√2'"},
    {'qnum': 18, 'title': '둔각 궤도 에너지 감쇄 넓이', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "사잇각이 90도를 넘어서는 120도의 둔각 감쇄 빔 구간이다! 두 변 4, 5와 사이 둔각 120도로 형성되는 둔각 감쇄 삼각형의 넓이를 도출해라!"<br><br><i>둔각 빔 보정기가 회전하며 감쇄각 $180^\\circ - 120^\\circ$의 대입을 대기시킵니다.</i>''', 'qtext': '<strong>Q18. [둔각삼각형의 넓이]</strong><br>두 변의 길이가 각각 4, 5이고 그 사잇각이 $120^\\circ$ 인 둔각삼각형의 넓이를 구하시오. (루트를 사용해 공백 없이 나타내시오. 예: 5√3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5√3'"},
    {'qnum': 19, 'title': '이중 평행 궤도 넓이', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "이중 평행 비행 구역이다! 이웃한 두 변 5, 8과 사이 각도 60도를 만족하는 이중 평행사변형 보호막의 융합 면적 넓이를 산출해라!"<br><br><i>이중 실드 회로망에 대칭형 평행사변형 면적 출력 값을 기입해야 합니다.</i>''', 'qtext': '<strong>Q19. [평행사변형의 넓이]</strong><br>이웃한 두 변의 길이가 5, 8이고 그 사잇각이 $60^\\circ$ 인 평행사변형의 넓이를 구하시오. (루트를 사용해 공백 없이 나타내시오. 예: 20√3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '20√3'"},
    {'qnum': 20, 'title': '최종 탈출 관측소 높이', 'story': '''🔮 <strong>[최종 하이퍼드라이브 충전 완료 및 차원 도약]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[아스트로-A]</span>: "조사관님! 드디어 블랙홀을 완전히 통과하는 하이퍼드라이브 차원 도약 순간입니다! 제 모든 제어 출력을 추진 에너지로 전환합니다! 돔탑 기준 지면 10m 외곽에서 올려다본 각도 30도 삼각 기준선에 따른 관측소 돔탑의 높이 수치 식(예: 10√3/3)을 기입창에 주입해 최종 도약을 승인하십시오! 블랙홀 너머의 차원문이 열립니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[블랙홀-B]</span>: "안 돼... 내 거대한 특이점 탈출 결계 공식이... 단 하나의 오차도 없는 삼각비에 조율되어 붕괴되다니...!"''', 'qtext': '<strong>Q20. [삼각비의 높이 측정 활용]</strong><br>관측소 돔탑 밑동에서 10m 떨어진 지점에서 돔탑 꼭대기를 올려다본 각도가 $30^\\circ$ 일 때, 돔탑의 높이를 구하시오. (루트와 분수를 사용해 공백 없이 나타내시오. 예: 10√3/3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '10√3/3'", "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_05/q{qnum}.png" alt="Background" class="panel-image">
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

print("app_m3_05_escape_room.html generated successfully.")
