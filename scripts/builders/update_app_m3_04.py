# -*- coding: utf-8 -*-\nimport re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m3_04_escape_room.html")
html_path = html_file

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>포물선 궤도의 사이버 드론 관제실: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0d0e22;
            --glass-bg: rgba(18, 19, 45, 0.75);
            --glass-border: rgba(99, 102, 241, 0.25);
            --accent: #6366f1;
            --accent-hover: #818cf8;
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
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
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
            border-top: 1px solid rgba(99, 102, 241, 0.4);
            border-left: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(99, 102, 241, 0.15), inset 0 0 20px rgba(99, 102, 241, 0.02);
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
            text-shadow: 0 0 30px rgba(99, 102, 241, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(99, 102, 241, 0.15);
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
            border: 1px solid rgba(99, 102, 241, 0.15);
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
            background: rgba(99, 102, 241, 0.05);
            border: 1px dashed rgba(99, 102, 241, 0.3);
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
            border: 1px solid rgba(99, 102, 241, 0.3);
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
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
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
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
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
            border: 1px solid rgba(99, 102, 241, 0.2);
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
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
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
            border-bottom: 1px solid rgba(99, 102, 241, 0.2);
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
            <h1>포물선 궤도의 사이버 드론 관제실</h1>
            <h2>이차함수</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_04/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [드론 요격 AI 이글-E]: "사이버 도시의 드론 비행을 통제하는 '드론 관제실'에 비상경보가 울렸습니다. 해킹 프로그램으로 인해 드론들의 비행 궤적이 엉망이 되어 도시의 빌딩들과 충돌하기 직전입니다! 드론들의 비행선인 '포물선 궤도(이차함수)'를 올바르게 해독하여 조종 시스템을 복구하십시오. 제한시간 45분 내에 충돌 사고를 막고 관제실을 정상화해야 탈출할 수 있습니다!"
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_04/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [드론 요격 AI 이글-E]: "정렬 신호가 들어오며 도시 상공의 수백 대 드론이 질서정연하게 안착합니다. 충돌 궤도들이 녹색선으로 교체되며 해킹 시스템이 완전 격퇴되었습니다. 사이버 도시의 하늘을 지켜낸 여러분의 활약을 치하합니다!"
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
        const UNIT_ID = "m3_04";

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
    {'qnum': 1, "options": ["(1)", "(2)", "(3)", "(4)"], 'title': '사이버 비행 함수 감지', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "크하하! 도시 상공의 관제 레이더망을 전부 오염시켰다! 2차 곡선형 비행 공식조차 구별하지 못하는 구형 관제 컴퓨터들은 일제히 교신 단절 상태로 추락할 것이다!"<br><br><i>지이이잉- 디지털 콘솔 스크린에 네 종류의 드론 궤적 주파수 식들이 요동치며 나타납니다. 이차함수를 만족하는 올바른 포물선 궤도 번호를 선별하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "관제 조사관님, 중앙 통제 장치를 깨워 주십시오! 이차함수 법칙을 따르는 고유 궤도 번호(숫자)를 기입창에 주입해 레이더를 작동시켜야 합니다!"''', 'qtext': '<strong>Q1. [이차함수 판별]</strong><br>다음 보기 중 $y$가 $x$에 대한 이차함수인 것의 번호를 쓰시오.<br>(1) $y = 3x - 1$<br>(2) $y = x^2 - 4$<br>(3) $y = \frac{2}{x}$<br>(4) $y = 2^x$', 'placeholder': '번호 입력 (예: 2)', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2' || ans === '(2)' || ans === '2번'"},
    {'qnum': 2, "options": ["(0,0)", "(0,0) 아님", "알 수 없음", "해 없음"], 'title': '기본 비행 코어 꼭짓점', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "기본 궤도 레이더를 켰군. 하지만 비행 고도가 0인 비행 기본형 $y=3x^2$ 그래프의 꼭짓점 좌표를 판독할 코드가 입력되지 않았다! 충돌 위험 80%다!"<br><br><i>벽면의 디지털 네비게이션 지시기가 점차 아래로 처지며 비정상 경로 진입음을 보냅니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "비행 코어 축 보정 가동! 기본형 $y=3x^2$ 의 원점 꼭짓점 좌표를 괄호를 포함(예: (0,0))하여 입력창에 주입해 경로를 동조해 주십시오!"''', 'qtext': '<strong>Q2. [기본형의 꼭짓점]</strong><br>이차함수 $y=3x^2$ 그래프의 꼭짓점 좌표를 구하시오. (괄호를 포함하여 공백 없이 적으시오. 예: (0,0))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(0,0)' || ans === '0,0'"},
    {'qnum': 3, "options": ["X=0", "X=0 아님", "알 수 없음", "해 없음"], 'title': '중앙 조향 대칭축', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "이번엔 음의 대칭축이다! 아래로 급강하하는 포물선 궤도 $y=-2x^2$ 의 정중앙 대칭축 방정식을 정확히 규정해 봐라!"<br><br><i>드르륵- 드론 조종 피스톤 밸브가 중앙 정렬 상태에서 왼쪽으로 흔들립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "대칭 조향 축 보정 시작! 축의 방정식 수식(예: x=0)을 기입창에 대입하여 좌우 밸런스를 즉시 동조하십시오!"''', 'qtext': '<strong>Q3. [기본형의 대칭축]</strong><br>이차함수 $y=-2x^2$ 그래프의 대칭축(축의 방정식)을 구하시오. (공백 없이 예: x=0)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === 'X=0'"},
    {'qnum': 4, "options": ["4", "2", "0", "10"], 'title': '궤도 통과 계수 유도', 'story': '''<strong>[드론 자이로 가속 센서 전자기 노이즈 필터링]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "치직... 캡틴! 드론 자이로 센서가 궤적 상의 좌표 $(2,8)$ 을 안전하게 관통할 수 있도록 가속도 상수 $a$를 산출해야 합니다! ⚙️ [좌표 통과 계수 대입]<br><br>식 $y=ax^2$ 에 좌표를 대입하여 $a$의 값을 도출하십시오!"''', 'qtext': '<strong>Q4. [좌표의 대입]</strong><br>이차함수 $y=ax^2$ 의 그래프가 점 $(2,8)$ 을 지날 때, 상수 $a$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2'"},
    {'qnum': 5, "options": ["Y=X²+3", "Y=X²+3 아님", "알 수 없음", "해 없음"], 'title': 'y축 방향 수직 천이', 'story': '''<strong>[드론 수직 상승 추진 로터 가동]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "치지직... 도시 고층 빌딩 충돌 방지 고도 보정 작동! ⚙️ [y축 방향 3 평행이동]<br><br>수직 고도를 3만큼 상승 조정한 드론 비행 포물선 식(공백 없이 예: y=x^+3)을 대입해 충돌선을 상승시키십시오!"''', 'qtext': '<strong>Q5. [y축 평행이동]</strong><br>이차함수 $y=x^2$ 의 그래프를 $y$축의 양의 방향으로 3만큼 평행이동한 그래프의 식을 구하시오. (공백 없이 대문자로 예: y=x^2+3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === 'Y=X²+3' || ans === 'Y=X^2+3'"},
    {'qnum': 6, 'title': '수평 비행 평행이동', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "제2막: 평행이동의 궤적이다. 수평 궤도를 1만큼 천이시켜서 묶은 표준식 $y=3(x-1)^2$ 이다. 이 꼭짓점 좌표를 오차 없이 입력할 수 있겠나?"<br><br><i>드론 조향 레이저 포인터가 수평 방향으로 1단위 꺾여 정렬됩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "수평 꼭짓점 복원 시도! 괄호를 포함하여 꼭짓점 좌표(예: (1,0))를 입력 장치에 기입하십시오!"''', 'qtext': '<strong>Q6. [x축 평행이동 꼭짓점]</strong><br>이차함수 $y=3(x-1)^2$ 그래프의 꼭짓점 좌표를 구하시오. (괄호를 포함하여 공백 없이 적으시오. 예: (1,0))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(1,0)' || ans === '1,0'"},
    {'qnum': 7, 'title': '복합 입체 꼭짓점 좌표', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "그렇다면 수평으로 2, 수직으로 4만큼 동시에 천이시킨 복합 궤도 $y=-(x-2)^2 + 4$ 의 마스터 꼭짓점은 과연 어디일까?"<br><br><i>계기판 모니터 도면에 녹색 드론 기단이 두 방향 좌표선 중앙으로 가쁘게 움직입니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "복합 평행이동 꼭짓점 정렬! 괄호를 포함하여 $(p,q)$ 형태의 좌표(예: (2,4))를 입력하여 궤도를 고정하십시오!"''', 'qtext': '<strong>Q7. [표준형의 꼭짓점]</strong><br>이차함수 $y=-(x-2)^2 + 4$ 그래프의 꼭짓점 좌표를 구하시오. (괄호를 포함하여 공백 없이 적으시오. 예: (2,4))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(2,4)' || ans === '2,4'"},
    {'qnum': 8, "options": ["X=-3", "X=-3 아님", "알 수 없음", "해 없음"], 'title': '표준형 대칭축', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "이차 포물선 비행축 $y=2(x+3)^2 - 5$ 의 중앙 대칭 보조축이다. 이 축의 노선이 이탈하면 날개 밸런스가 파열될 것이다!"<br><br><i>드론 추진기 모터 회전수가 양쪽으로 불균등하게 분배되어 흔들리기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "대칭축 방정식 동조화! 축의 공식(예: x=-3)을 기입창에 주입해 날개 추진 각도를 수평으로 고정하십시오!"''', 'qtext': '<strong>Q8. [표준형의 대칭축]</strong><br>이차함수 $y=2(x+3)^2 - 5$ 그래프의 대칭축의 방정식을 구하시오. (공백 없이 예: x=-3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === 'X=-3'"},
    {'qnum': 9, "options": ["6", "1", "3", "5"], 'title': '레이저 레이더 원점 절편', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "관제탑의 정면 수직 레이저 기준축과 교차하는 궤도 높이를 계측해 봐라. 식 $y=(x-1)^2 + 2$ 의 y축 도킹 좌표이다!"<br><br><i>수직 도킹 통과선 눈금자가 위아래로 미세하게 눈금 번호를 대기시킵니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "레이더 수직 교점 연산! $x=0$을 대입하여 y축과 마주치는 도킹 수치 정수를 출력창에 전송하십시오!"''', 'qtext': '<strong>Q9. [y축과의 교점]</strong><br>이차함수 $y=(x-1)^2 + 2$ 그래프가 $y$축과 만나는 점의 $y$좌표를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '3'"},
    {'qnum': 10, "options": ["Y=X²", "Y=X² 아님", "알 수 없음", "해 없음"], 'title': '중앙 반전 궤도', 'story': '''💥 <strong>[비상 로그: 관제 코어 냉각 회로 정지 및 강제 셧다운 시퀀스 가동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "끈질긴 녀석들! 모든 관제 데이터를 오버플로우로 포맷하겠다! 5분 뒤 모든 시스템 캐시가 소멸되리라!"<br><br><i>경보 사운드가 시끄럽게 울리며 붉은 연기가 스며 나오기 시작합니다. 대칭 반전 식을 전송해 자폭 회로를 우회 차단하십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "냉각 기류 복구 시도! 식 $y=-x^2$ 과 가로 x축을 기준으로 대칭인 반사 반전 궤도 식(공백 없이 대문자)을 기입해 자폭을 정지시키십시오!"''', 'qtext': '<strong>Q10. [대칭인 그래프]</strong><br>이차함수 $y=-x^2$ 의 그래프와 $x$축에 대하여 서로 대칭인 그래프의 식을 구하시오. (공백 없이 대문자로 예: y=x^2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === 'Y=X²' || ans === 'Y=X^2'", "extra_class": "glitch-bg"},
    {'qnum': 11, "options": ["4", "6", "8", "12"], 'title': '일반 궤도의 기하 분석', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "후... 자폭 정지 3분 연장 성공! 이제 제3막 일반 비행 궤도의 정밀 해석에 들어갑니다! ⚙️ [일반형 식의 합성 보정]"<br><br><i>이차식 일반 폼 $y=x^2 - 4x + 7$ 을 표준 폼 $y=a(x-p)^2+q$ 로 변환하여 도출되는 세 조절 변수 $a, p, q$의 합산 정수를 입력해 주십시오!</i>''', 'qtext': '<strong>Q11. [일반형을 표준형으로 변형]</strong><br>이차함수 $y=x^2 - 4x + 7$ 을 표준형 $y=a(x-p)^2+q$ 꼴로 나타낼 때, 세 상수 $a, p, q$에 대하여 $a+p+q$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '6'"},
    {'qnum': 12, 'title': '일반형 꼭짓점 도출', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "2단계 일반 꼭짓점 정렬 록입니다! 비행 궤도 식 $y=x^2 - 6x + 5$ 의 꼭짓점 좌표를 해독해 주십시오! ⚙️ [이차식 꼭짓점]"<br><br><i>괄호를 포함하여 쉼표로 연결된 꼭짓점 좌표(예: (3,-4))를 입력창에 전송하십시오.</i>''', 'qtext': '<strong>Q12. [일반형의 꼭짓점]</strong><br>이차함수 $y=x^2 - 6x + 5$ 그래프의 꼭짓점 좌표를 구하시오. (괄호를 포함하여 공백 없이 적으시오. 예: (3,-4))', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '(3,-4)' || ans === '3,-4'"},
    {'qnum': 13, "options": ["-3,1", "-3,1 아님", "알 수 없음", "해 없음"], 'title': '가로 활주로 교점', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "3단계 해치 관문입니다! 드론 비행선이 가로 x축 활주로와 교차 접지하는 두 교점의 x좌표 수치를 도출해 주십시오! ⚙️ [x축과의 교점]"<br><br><i>식 $y=x^2 + 2x - 3$ 이 x축과 마주치는 두 좌표를 작은 수부터 쉼표로 연결해 기입하십시오! (예: -3,1)</i>''', 'qtext': '<strong>Q13. [x축과의 교점의 x좌표]</strong><br>이차함수 $y=x^2 + 2x - 3$ 그래프가 $x$축과 만나는 두 점의 $x$좌표를 구하시오. (작은 수부터 적으시오. 예: -3, 1)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '-3,1'"},
    {'qnum': 14, "options": ["6", "1", "3", "5"], 'title': '최고 정밀 고도 계측', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "4단계 관문입니다! 복합식 $y=-2x^2 + 8x - 5$ 포물선의 꼭짓점 수직 y좌표 최고 고도 상수를 계측하십시오! ⚙️ [꼭짓점 y좌표]"''', 'qtext': '<strong>Q14. [꼭짓점의 y좌표]</strong><br>이차함수 $y=-2x^2 + 8x - 5$ 그래프의 꼭짓점의 $y$좌표를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '3'"},
    {'qnum': 15, "options": ["X=2", "X=2 아님", "알 수 없음", "해 없음"], 'title': '중앙 조향 대칭축 복원', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E 드론 관제 컴퓨터 권한 100% 완전 장악]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "동기화 완료! 관제탑의 모든 드론 모터 출력과 무선 레이더 주파수를 장악했습니다! 이제 재머의 비행 왜곡 격벽을 역동조화합니다. 식 $y=x^2 - 4x$ 의 조향 대칭축 공식을 전송해 격벽을 무력화하십시오!"<br><br><i>메인 비행 차트 스크린이 노란색 포물선 궤도선들로 깔끔하게 동조 정렬됩니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "중앙 제어국을 뚫다니...! 최종 한계 고도의 이차 포물선 활용 트랩은 결코 넘지 못하리라!"''', 'qtext': '<strong>Q15. [일반형의 대칭축]</strong><br>이차함수 $y=x^2 - 4x$ 그래프의 대칭축의 방정식을 구하시오. (공백 없이 예: x=2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === 'X=2'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '포물선 조향 극성', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "아래로 볼록한 U자형 비행 슬롯이다! 궤도식 $y=ax^2+bx+c$ 에서 이 조향 극성을 결정하는 계수 $a$의 부호 범위를 기호로 선언해 봐라!"<br><br><i>제어반 기판의 방향 조절 지시등이 깜빡입니다. 부등호 기호를 포함해 입력하십시오. (예: >0)</i>''', 'qtext': '<strong>Q16. [이차함수 그래프의 볼록한 방향]</strong><br>이차함수 $y=ax^2+bx+c$ 의 그래프 모양이 아래로 볼록할 때, $a$의 값의 부호를 쓰시오. (기호를 포함해 예: >0)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '>0'"},
    {'qnum': 17, 'title': '원점 통과 빔 참거짓', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "식 $y=x^2 + 2x$ 의 레이더 빔이 원점 $(0,0)$ 을 안전 지대로 통과하는지 진위를 판단해라! 참 또는 거짓 둘 중 하나다!"<br><br><i>콘솔에 참 / 거짓 스위치 2개가 교차 가동음을 냅니다.</i>''', 'qtext': '<strong>Q17. [함수와 원점 통과]</strong><br>"이차함수 $y=x^2 + 2x$ 의 그래프는 항상 원점$(0,0)$을 지난다." 이 명제가 맞으면 참, 틀리면 거짓을 쓰시오.', 'placeholder': '참 또는 거짓 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '참'"},
    {'qnum': 18, 'title': 'y축 접지 도킹 고도', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "이차함수 $y=x^2 - 2x - 3$ 이 y축과 만나는 최종 접지 고도 수치를 입력창에 전송해 봐라!"<br><br><i>y축 접지 레벨 바늘이 하강선 마커에 도달해 깜빡입니다.</i>''', 'qtext': '<strong>Q18. [일반형의 y절편]</strong><br>이차함수 $y=x^2 - 2x - 3$ 그래프가 $y$축과 만나는 점의 $y$좌표를 구하시오. (음수 마이너스 포함 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '-3'"},
    {'qnum': 19, 'title': '최저 안착 한도 고도', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "상승 포물선 비행로 $y=3(x-2)^2 + 1$ 이다! 드론이 도달할 수 있는 가장 최저 안착 한도 고도(최솟값)를 선언해 봐라!"<br><br><i>최저 안전 착륙 한도선 경보기가 삐- 삐- 가동 지연을 일으킵니다.</i>''', 'qtext': '<strong>Q19. [이차함수의 최솟값]</strong><br>이차함수 $y=3(x-2)^2 + 1$ 의 최솟값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1'"},
    {'qnum': 20, 'title': '최고 회피 고도 정합', 'story': '''🔮 <strong>[최종 포물선 궤도 안전 정렬 및 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[이글-E]</span>: "조사관님! 이제 관제탑 비행 게이트 밖 하늘로 나가는 마지막 최고 회피 고도 밸브만 남았습니다! 제 모든 레이더 조종 전력을 관제 시스템에 연동하겠습니다! 포물선 궤도 식 $y = -x^2 + 4x$ 가 나타내는 비행선 최고 정점 높이(y좌표 최댓값)를 입력하여 게이트 문을 여십시오! 탈출할 순간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[재머-J]</span>: "안 돼... 내 포물선 해킹 결계가... 완전 제어 정점 데이터에 차단되어 소멸하다니...!"''', 'qtext': '<strong>Q20. [이차함수의 최댓값 활용]</strong><br>보안 드론의 회피 포물선 비행 궤도 식은 $y = -x^2 + 4x$ 이다. 이 드론이 도달할 수 있는 가장 높은 지점의 높이($y$좌표)를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '4'", "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_04/q{qnum}.png" alt="Background" class="panel-image">
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

print("app_m3_04_escape_room.html generated successfully.")
