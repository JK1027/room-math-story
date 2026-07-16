# -*- coding: utf-8 -*-\nimport re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m3_07_escape_room.html")
html_path = html_file

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>은하계 연합의 산포도 데이터베이스: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #06181e;
            --glass-bg: rgba(10, 28, 35, 0.75);
            --glass-border: rgba(6, 182, 212, 0.25);
            --accent: #06b6d4;
            --accent-hover: #22d3ee;
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
                radial-gradient(circle at 10% 20%, rgba(6, 182, 212, 0.08) 0%, transparent 40%),
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
            border-top: 1px solid rgba(6, 182, 212, 0.4);
            border-left: 1px solid rgba(6, 182, 212, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(6, 182, 212, 0.15), inset 0 0 20px rgba(6, 182, 212, 0.02);
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
            text-shadow: 0 0 30px rgba(6, 182, 212, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(6, 182, 212, 0.15);
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
            border: 1px solid rgba(6, 182, 212, 0.15);
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
            background: rgba(6, 182, 212, 0.05);
            border: 1px dashed rgba(6, 182, 212, 0.3);
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
            border: 1px solid rgba(6, 182, 212, 0.3);
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
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
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
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
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
            border: 1px solid rgba(6, 182, 212, 0.2);
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
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
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
            border-bottom: 1px solid rgba(6, 182, 212, 0.2);
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
            <h1>은하계 연합의 산포도 데이터베이스</h1>
            <h2>통계</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_07/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [은하계 통계 코어 갤럭시-G]: "우주 은하연합의 거대한 중앙 통계 분석실 '산포도 데이터베이스'에 도착했습니다. 이곳의 방대한 우주선 궤도 예측 자료와 기후 데이터는 통계 수치 결계로 암호화되어 있어 시스템 조작이 불가능합니다. 우주선 통계 변량들의 대푯값과 흩어진 정도를 나타내는 산포도를 계산하여 제한시간 45분 내에 시스템 락을 해제하고 무사히 궤도를 복구하여 귀환하십시오!"
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_07/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [은하계 통계 코어 갤럭시-G]: "은하 연합의 거대한 홀로그램 맵에 안정적인 우주선 궤도선들이 다시 한 번 안전한 선으로 점등됩니다. 통계 데이터 분석실의 비상 잠금장치가 모두 해제되며 우주 귀환선의 해치가 열립니다. 데이터를 마스터한 통계 분석관의 귀환을 환영합니다!"
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
        const UNIT_ID = "m3_07";

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
    {'qnum': 1, "options": ["대푯값", "평균값", "변량값", "중앙값"], 'title': '대표 스펙트럼 분류', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "크하하! 은하 탐사선의 에너지 스펙트럼 콘솔은 이미 내 반물질 파동으로 가득 차 무력화되었다! 우주선 전체 가용 데이터의 성격을 대표하는 핵심 명칭조차 선언하지 못하면, 항로를 잃고 미아가 될 것이다!"<br><br><i>스펙트럼 계기판 액정 화면 위로 불규칙한 원소 분석 데이터 바들이 폭포수처럼 쏟아집니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "조사관님, 분석 필터를 깨워야 합니다! 자료들의 특징을 대표적으로 나타내는 총칭 단어(한글 세 글자)를 입력해 첫 번째 방어벽 콘솔을 해제하십시오!"''', 'qtext': '<strong>Q1. [대푯값의 정의]</strong><br>자료 전체의 특징을 대표적으로 나타내는 값을 통틀어 무엇이라 부르는가? (한글 세 글자로 입력. 예: 대푯값)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '대푯값'"},
    {'qnum': 2, "options": ["평균", "합계", "분산", "편차"], 'title': '스펙트럼 평균 락', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "수치 락을 한 번 해독했군. 그렇다면 모든 원소 성분의 합을 전체 검출 노즐 수로 공평하게 나눈 이 보정 대푯값은 무엇이라 하나?"<br><br><i>모니터 눈금자가 위아래로 가쁘게 진동하다 한글 두 글자 칸을 표시해 멈춥니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "기본 나눗셈 대푯값 연산! 전체 자료 총합을 개수로 나눈 고유 대푯값(한글 두 글자)을 입력창에 전송하십시오!"''', 'qtext': '<strong>Q2. [평균의 정의]</strong><br>자료의 값을 모두 더하여 자료의 개수로 나눈 값을 구하시오. (한글 두 글자로 입력. 예: 평균)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '평균'"},
    {'qnum': 3, "options": ["중앙값", "최빈값", "대푯값", "평균값"], 'title': '중앙 궤도 주파수', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "이번엔 중앙 주파수 락이다! 성분 크기 순으로 주파수를 쭉 정렬했을 때, 정중앙에 위치하는 이 대표 궤도값의 고유 명칭은 무엇인가?"<br><br><i>메인 통제 레버가 강한 자력으로 고정되어 움직이지 않습니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "크기순 정가운데 위치 정리! 해당하는 대표 용어(한글 세 글자)를 입력창에 주입해 레버 고정을 푸십시오!"''', 'qtext': '<strong>Q3. [중앙값의 정의]</strong><br>자료의 값을 크기순으로 나열했을 때 가장 한가운데에 위치하는 값을 무엇이라 하는가? (한글 세 글자로 입력. 예: 중앙값)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '중앙값'"},
    {'qnum': 4, "options": ["최빈값", "중앙값", "대푯값", "편차"], 'title': '최다 검출 성분', 'story': '''<strong>[우주선 다중 분석 회선 노이즈 필터링]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "치직... 캡틴! 반물질 이상 기류에서 가장 높은 빈도로 최다 검출되는 스펙트럼 변량 용어를 추출해 주십시오! ⚙️ [최다 빈도 대푯값]<br><br>해당 용어(한글 세 글자)를 입력창에 전송하여 노이즈를 격리하십시오!"''', 'qtext': '<strong>Q4. [최빈값의 정의]</strong><br>자료의 값 중 가장 자주 나타나는 값을 무엇이라 하는가? (한글 세 글자로 입력. 예: 최빈값)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '최빈값'"},
    {'qnum': 5, "options": ["10", "3", "7", "5"], 'title': '원소 데이터 평균 보정', 'story': '''<strong>[메인 노즐 차원 도약 추진 수치 보정]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "치지직... 보조 추진 노즐이 작동합니다! ⚙️ [실전 평균 연산]<br><br>다섯 개의 우주 성분 데이터 1, 3, 5, 7, 9 의 평균(정수)을 도출해 추진 밸브를 개방하십시오!"''', 'qtext': '<strong>Q5. [평균의 계산]</strong><br>다섯 개의 우주 변량 데이터 1, 3, 5, 7, 9 의 평균을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 6, "options": ["5", "14", "7", "9"], 'title': '짝수 궤도 중앙 제어', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "제2막: 산포도와 편차다. 여섯 가닥 짝수 궤도 데이터 2, 4, 6, 8, 10, 12 의 중앙 제어 주파수를 대 봐라! 짝수 개 데이터의 절반 연산에서 길을 잃을 것이다!"<br><br><i>여섯 가닥 레이저 빔 중 가운데 두 빔이 보랏빛으로 격렬하게 스파크를 냅니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "가운데 두 값의 평균 산출! 중앙값(정수)을 전송하여 레이저 간섭을 안정화하십시오!"''', 'qtext': '<strong>Q6. [중앙값의 계산]</strong><br>여섯 개의 우주 데이터 2, 4, 6, 8, 10, 12 의 중앙값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '7'"},
    {'qnum': 7, "options": ["16", "6", "8", "10"], 'title': '최빈 기압 정합', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "이번엔 빈도 밀도 결계다! 다중 압력 검측 수치 3, 5, 5, 7, 8, 8, 8 속에서 기압을 짓누르는 최빈 밀도 값을 대라!"<br><br><i>산소 정화기 실린더 주위 압력계 수치가 8을 향해 가파르게 올라갑니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "밀도 계수 최빈값 검출! 가장 출현 빈도가 높은 수치를 입력해 산소 밀도를 정상 복원하십시오!"''', 'qtext': '<strong>Q7. [최빈값의 계산]</strong><br>데이터 3, 5, 5, 7, 8, 8, 8 의 최빈값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '8'"},
    {'qnum': 8, "options": ["중앙값", "평균값", "최빈값", "편차"], 'title': '극단값 영향 방어', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "노심에 99999 라는 억만급 이상 과전류(극단값)를 주입했다. 노심 평균 계수를 소멸시켰으니, 이제 이 극단적 오차에 영향을 받지 않는 대푯값 필터는 과연 무엇일까?"<br><br><i>메인 파워 그리드 모니터에 터무니없이 큰 스파이크 파형이 잡힙니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "극단치 오차 방어 대푯값 선정! 순서 크기 배열에 입각하는 대푯값(한글 세 글자)을 입력해 방전망을 복구하십시오!"''', 'qtext': '<strong>Q8. [중앙값의 성질]</strong><br>대푯값 중 극단적인 값(아주 크거나 아주 작은 값)에 영향을 가장 적게 받아, 치우친 자료에 유용한 대푯값을 쓰시오. (한글 세 글자로 입력. 예: 중앙값)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '중앙값'"},
    {'qnum': 9, "options": ["편차", "분산", "평균", "제곱"], 'title': '평균과의 이격 수치', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "각 노즐의 실제 분사 압력과 기준치 평균 사이의 이격 격차(변량 - 평균)다! 이 오차 오프셋 계수의 용어는 무엇인가?"<br><br><i>도선 회로 차단막에 빨갛게 두 글자의 통계 용어 기입 패드가 열립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "오차 오프셋 계수 입력! 기준평균 대비 수치 차이를 뜻하는 용어(한글 두 글자)를 전송해 차단막을 푸십시오!"''', 'qtext': '<strong>Q9. [편차의 정의]</strong><br>변량들이 평균으로부터 떨어져 있는 차이(즉, 변량 - 평균)를 무엇이라 부르는가? (한글 두 글자로 입력. 예: 편차)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '편차'"},
    {'qnum': 10, "options": ["-1", "1", "0", "2"], 'title': '오차 편차의 총합', 'story': '''💥 <strong>[비상 로그: 반물질 핵분열 노심 제동 장치 폭주 및 강제 셧다운 기동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "끝장을 내주마! 노심의 전자기장을 붕괴시켜 우주선을 폭발 소멸시키겠다! 5분 뒤 모든 전력이 소거된다!"<br><br><i>삐- 삐- 경보 기압 부저가 격렬하게 작동하며 붉은 경보 스파크가 튀기 시작합니다. 편차 총합 수치 정수를 대입해 비상 셧다운을 긴급 우회 차단하십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "비상 접지 루프 전개 시도! 모든 편차들을 다 더한 물리적 총합 상수(숫자)를 기입창에 주입해 폭발을 저지하십시오!"''', 'qtext': '<strong>Q10. [편차의 성질]</strong><br>변량들의 편차의 총합은 항상 얼마인가? (숫자 하나만 입력)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '0'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '오차 제곱 평균 분산', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "후... 셧다운 정지 3분 연장 성공! 이제 제3막 산포도 기하 해독 관문으로 접근합니다! ⚙️ [제곱 평균의 분산]"<br><br><i>편차들의 마이너스를 지우기 위해 제곱하여 낸 평균 통계치 용어(한글 두 글자, 예: 분산)를 전송해 게이트를 작동시키십시오.</i>''', 'qtext': '<strong>Q11. [분산의 정의]</strong><br>편차의 제곱의 평균을 구하여 산포도를 나타내는 통계 값을 무엇이라 부르는가? (한글 두 글자로 입력. 예: 분산)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '분산'"},
    {'qnum': 12, 'title': '단위 정합 표준 오차', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "2단계 정합 락입니다! 분산에 다시 양의 제곱근 루트를 씌워 실제 데이터와 단위를 맞춘 산포도 용어를 대십시오! ⚙️ [분산의 제곱근]"''', 'qtext': '<strong>Q12. [표준편차의 정의]</strong><br>분산의 음이 아닌 양의 제곱근 값을 구하여 실제 변량과 단위를 맞춘 산포도 값을 무엇이라 하는가? (한글 네 글자로 입력. 예: 표준편차)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '표준편차'"},
    {'qnum': 13, 'title': '수치 산포 분포율', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "3단계 게이트입니다! 자료들이 흩어진 정도를 나타내는 통계적 수치 분포율 총칭 용어를 입력하십시오! ⚙️ [흩어진 정도]"''', 'qtext': '<strong>Q13. [산포도의 정의]</strong><br>자료들의 흩어진 정도를 나타내는 하나의 수치를 통틀어 무엇이라 하는가? (한글 세 글자로 입력. 예: 산포도)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '산포도'"},
    {'qnum': 14, 'title': '원탁 분산 실제 측정', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "4단계 관문! 세 추진 변량 3, 5, 7 의 정확한 분산 비율(슬래시 분수 형태, 예: 8/3)을 계측해 제동기 출력을 감속 정합하십시오! ⚙️ [실전 분산 계산]"''', 'qtext': '<strong>Q14. [분산의 계산]</strong><br>세 변량 3, 5, 7 의 분산을 구하시오. (슬래시를 사용해 분수로 나타내시오. 예: 8/3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '8/3'"},
    {'qnum': 15, 'title': '표준편차 빔 동조', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G 은하 코어 통제권 100% 완전 환원]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "동기화 완료! 은하 탐사선의 모든 비상 전자기 필터와 파워 서플라이를 완전 장악했습니다! 이제 반물질의 붕괴 왜곡 격벽을 분쇄합니다. 네 변량 1, 3, 5, 7 의 정확한 표준편차 수식(루트 기호 포함, 예: √5)을 전송하여 잔여 격벽 해치를 완전히 작동시키십시오!"<br><br><i>탐사선 콕핏 전면 창에 푸른색 은하 궤도 그리드가 복구 정렬되며, 차원 탈출 슬롯이 열립니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "제어 중심국을 탈취당하다니...! 하지만 두 인자의 역학 관계 트랩은 결코 해독하지 못할 것이다!"''', 'qtext': '<strong>Q15. [표준편차의 계산]</strong><br>네 변량 1, 3, 5, 7 의 표준편차를 구하시오. (루트 기호를 사용하여 나타내시오. 예: √5)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '√5'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '상관 빔 분포 도면', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "두 가닥 데이터 축의 연동성을 좌표평면 위에 무수히 많은 점으로 나타낸 이 통계 분석 차트의 명칭은 무엇이냐?"<br><br><i>레이더 모니터 격자판 위에 수많은 백색 반점 빔들이 무리지어 켜집니다.</i>''', 'qtext': '<strong>Q16. [산점도의 정의]</strong><br>두 변량의 상관관계를 한눈에 알아보기 위해 좌표평면 위에 점으로 나타낸 그림을 무엇이라 하는가? (한글 세 글자로 입력. 예: 산점도)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '산점도'"},
    {'qnum': 17, 'title': '동반 우상향 주파수', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "한 변량 x가 치솟을 때 y도 같이 대체로 증가하며 동반 상승하는 이 아름다운 정비례 상관관계의 명칭을 대라!"<br><br><i>지시판 수치가 우상향 그래프 경사를 띄고 점등됩니다.</i>''', 'qtext': '<strong>Q17. [양의 상관관계]</strong><br>한 변량 $x$의 값이 증가할 때, 다른 변량 $y$의 값도 대체로 증가하는 관계를 무슨 상관관계라 하는가? (공백 없이 한글 일곱 글자로 입력. 예: 양의상관관계)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '양의상관관계'"},
    {'qnum': 18, 'title': '상쇄 우하향 주파수', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "반대로 한 변량 x가 팽창할 때 y는 감쇄하며 동반 하락하는 상쇄 상관관계의 정확한 명칭은 무엇인가?"<br><br><i>그래프선이 우하향으로 교차하며 통제 밸브 눈금을 짓누릅니다.</i>''', 'qtext': '<strong>Q18. [음의 상관관계]</strong><br>한 변량 $x$의 값이 증가할 때, 다른 변량 $y$의 값은 대체로 감소하는 관계를 무슨 상관관계라 하는가? (공백 없이 한글 일곱 글자로 입력. 예: 음의상관관계)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '음의상관관계'"},
    {'qnum': 19, 'title': '독립 인자 기압 무관계', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "사람들의 키와 지능지수(IQ)처럼 서로 아무런 영향을 미치지 않는 독립 인자들 사이에는 어떤 상관관계가 성립하는지 판단해 봐라!"<br><br><i>계기판 모니터 도면이 어떠한 방향성도 없이 사방으로 흩뿌려집니다.</i>''', 'qtext': '<strong>Q19. [상관관계가 없는 경우]</strong><br>"사람들의 키와 지능지수(IQ) 사이의 상관관계"는 어떤 관계가 있는지 쓰시오. (한글 세 글자로 입력. 예: 없다)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '없다'"},
    {'qnum': 20, 'title': '기온과 가스 난방 밀도', 'story': '''🔮 <strong>[최종 은하 궤도 복원 및 워프 게이트 작동]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[갤럭시-G]</span>: "조사관님! 드디어 반물질 폭풍 영역을 완전히 빠져나갈 최종 공간 워프 도약 준비가 끝났습니다! 제 모든 동력을 탈출 콘솔에 정렬하겠습니다! 실외 평균 기온과 난방비 사이의 역상관 분포 규칙 용어(공백 없이 일곱 글자)를 기입하여 셧다운 워프 게이트를 여십시오! 탈출구 도킹이 눈앞입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[안티-매터]</span>: "안 돼... 내 정교했던 반물질 왜곡 파장이... 완벽한 통계 상관관계 락에 풀려 공명 소멸하다니...!"''', 'qtext': '<strong>Q20. [상관관계 실생활 활용]</strong><br>"겨울철 실외 평균 기온과 각 가정의 가스 난방비 사이의 상관관계"는 어떤 관계가 있는지 쓰시오. (공백 없이 한글 일곱 글자로 입력. 예: 음의상관관계)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '음의상관관계'", "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_07/q{qnum}.png" alt="Background" class="panel-image">
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

print("app_m3_07_escape_room.html generated successfully.")
