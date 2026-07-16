# -*- coding: utf-8 -*-\nimport re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_02_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>(중1) 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0B0E14;
            --glass-bg: rgba(13, 20, 30, 0.75);
            --glass-border: rgba(168, 85, 247, 0.25);
            --accent: #A855F7;
            --accent-hover: #C084FC;
            --text-main: #E9D5FF;
            --text-muted: #A78BFA;
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
                radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(88, 28, 135, 0.15) 0%, transparent 40%);
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
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(168, 85, 247, 0.05);
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
            background: linear-gradient(90deg, rgba(30, 15, 45, 0.5) 0%, rgba(0,0,0,0.3) 100%);
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
            color: rgba(168, 85, 247, 0.05);
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
            border: 1px solid rgba(168, 85, 247, 0.3);
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
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.4), inset 0 2px 4px rgba(0,0,0,0.5);
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
            background: linear-gradient(90deg, #7C3AED, var(--accent));
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
            background: linear-gradient(135deg, #6B21A8, #4C1D95);
            color: white;
            border: 1px solid #8B5CF6;
            padding: 0.6rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 900;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 3px;
            width: 100%;
            box-shadow: 0 10px 25px rgba(76, 29, 149, 0.5), inset 0 2px 5px rgba(255,255,255,0.3);
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
            box-shadow: 0 15px 30px rgba(168, 85, 247, 0.5), inset 0 2px 5px rgba(255,255,255,0.5);
            border-color: #A78BFA;
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
            background: #11091C;
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

    <button id="soundToggle" class="sound-toggle" onclick="toggleSound()">🔊 소리 켜짐</button>

    <div class="container">
        
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <!-- 0. 인트로 -->
        <div id="intro" class="glass-panel active">
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_02_rational_numbers/intro.png" alt="Background" class="panel-image">
            <h1>마법 학교 아르카나</h1>
            <h2>20관문 최종 입학 시험</h2>
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                    세계 최고의 마법 학교 '아르카나'의 최종 입학 시험장에 오신 것을 환영합니다.<br><br>
                    이곳의 마법은 단순한 주문이 아니라 '정수와 유리수'의 수학적 원리를 통해 발동합니다.<br><br>
                    제한 시간 40분 내에 20개의 수식 결계를 완벽하게 풀어내어 아르카나 수석 입학의 영광을 쟁취하십시오!
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            
            <div class="info-box" style="background: rgba(220, 38, 38, 0.2); border-left: 4px solid #ef4444; padding: 0.8rem 1.2rem; margin-top: 1.5rem; border-radius: 0 12px 12px 0; color: #f87171; font-size: 0.95rem; line-height: 1.6; text-align: left;">
                ⚠️ <b>주의사항</b><br>
                문제는 총 20문제이며, 한 문제에서 3번 틀릴 경우 해당 구역의 처음으로 되돌아갑니다. <br>
                또한 <b>오답을 제출할 때마다 제한 시간이 1분씩 단축</b>되니 신중하게 도전해 주세요!
            </div>
            
            <div class="student-info-form" style="margin-top: 1.5rem; text-align: left; background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="margin-bottom: 1rem;">
                    <label for="studentId" style="display: block; margin-bottom: 0.5rem; color: #60A5FA; font-weight: bold; font-size: 1rem;">학번</label>
                    <input type="text" id="studentId" placeholder="예: 1130" style="width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(96, 165, 250, 0.4); background: rgba(15,23,42,0.6); color: white; font-size: 1.1rem; font-weight: bold; box-sizing: border-box;">
                </div>
                <div>
                    <label for="studentName" style="display: block; margin-bottom: 0.5rem; color: #60A5FA; font-weight: bold; font-size: 1rem;">이름</label>
                    <input type="text" id="studentName" placeholder="예: 홍길동" style="width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(96, 165, 250, 0.4); background: rgba(15,23,42,0.6); color: white; font-size: 1.1rem; font-weight: bold; box-sizing: border-box;">
                </div>
            </div>
            <div class="btn-group" style="margin-top: 2rem; width:100%;">
                <button class="btn" onclick="tryStartGame('m1_02')">입학 시험 시작</button>
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
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-mechanical-keyboard-clicks-2266.wav" type="audio/wav">
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

                // GAS 로직
                try {
                    if(typeof google !== 'undefined' && google.script && google.script.run) {
                        google.script.run
                            .withSuccessHandler(function(row) { window.userRecordRow = row; })
                            .recordStart(sid.value.trim(), sname.value.trim(), unitId);
                    }
                } catch(e) { console.warn('GAS 연동 안됨:', e); }
            }
            
            // 브라우저 오디오 엔진 시작 (외부 링크 의존 없음)
            try {
                if (!isMuted) {
                    initAudio();
                    startBGM();
                }
            } catch(e) {}
            
            nextStage('intro', 'panel_q1', 5);
        }

        

        

        

        

        

        


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
        let audioCtx = null;
        let bgmOsc = null;
        let bgmGain = null;
        let bgmLfo = null;

        function initAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function playSynth(freq, type, duration, vol) {
            if (isMuted) return;
            try {
                initAudio();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(vol, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration);
            } catch(e){}
        }

        function stopBGM() {
            try {
                if(bgmOsc) { bgmOsc.stop(); bgmOsc.disconnect(); bgmOsc = null; }
                if(bgmLfo) { bgmLfo.stop(); bgmLfo.disconnect(); bgmLfo = null; }
            } catch(e){}
        }

        function startBGM() {
            if (isMuted) return;
            try {
                initAudio();
                if(bgmOsc) return;
                bgmOsc = audioCtx.createOscillator();
                bgmGain = audioCtx.createGain();
                bgmOsc.type = 'triangle';
                bgmOsc.frequency.setValueAtTime(55.00, audioCtx.currentTime);
                bgmGain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                bgmOsc.connect(bgmGain);
                bgmGain.connect(audioCtx.destination);
                bgmOsc.start();
                
                bgmLfo = audioCtx.createOscillator();
                bgmLfo.type = 'sine';
                bgmLfo.frequency.setValueAtTime(0.15, audioCtx.currentTime); 
                const lfoGain = audioCtx.createGain();
                lfoGain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                bgmLfo.connect(lfoGain);
                lfoGain.connect(bgmGain.gain);
                bgmLfo.start();
            } catch(e) {}
        }

        function toggleSound() {
            isMuted = !isMuted;
            const btn = document.getElementById('soundToggle');
            if (isMuted) {
                if(btn) btn.innerText = '🔇 소리 꺼짐';
                stopBGM();
            } else {
                if(btn) btn.innerText = '🔊 소리 켜짐';
                startBGM();
            }
        }

        function playClick() { playSynth(800, 'sine', 0.1, 0.5); }
        function playTick() { playSynth(1500, 'square', 0.04, 0.15); }
        function playSuccess() { 
            playSynth(523.25, 'sine', 0.15, 0.7); 
            setTimeout(()=>playSynth(659.25, 'sine', 0.15, 0.7), 150); 
            setTimeout(()=>playSynth(783.99, 'sine', 0.3, 0.7), 300); 
        }
        function playError() {
            playSynth(150, 'sawtooth', 0.3, 0.6);
            setTimeout(()=>playSynth(100, 'sawtooth', 0.4, 0.6), 200);
        }
        function playVictory() {
            stopBGM();
            [523.25, 659.25, 783.99, 1046.50].forEach((f, i) => {
                setTimeout(()=>playSynth(f, 'square', 0.2, 0.6), i*150);
            });
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

        function showError(panelId, errorId, currentWrongCount) {
            try { playError(); } catch(e) {}
            const panel = document.getElementById(panelId);
            const err = document.getElementById(errorId);
            err.style.display = 'block';
            
            if (currentWrongCount !== undefined) {
                if (!err.dataset.origText) {
                    err.dataset.origText = err.innerText;
                }
                err.innerText = err.dataset.origText + " (오답 횟수: " + currentWrongCount + "/3)";
            }
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
            <h2>📜 지나온 시험 기록</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>

</body>
</html>
"""

qs = [
    {'qnum': 1, "options": ["-500m", "-500m 아님", "알 수 없음", "해 없음"], 'title': '빛과 어둠의 대비', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "크하하! 이 아르카나 시험장은 내 공허(Void)에 잠식당했다! 감히 보안 격벽을 통과할 수 있을 것 같으냐?"<br><br><i>스산한 공허의 기운이 조종 패널 주위를 휘감으며, 해수면을 기준으로 하는 고대 마법 축이 공중에 드러납니다. 해발 고도와 해저 심도를 구분하여 보안 기호를 반전시켜야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "치직... 캡틴, 그리무어 시스템이 가까스로 접속했습니다! 마법 해발 수치를 부호 기준에 매칭해 포탈 방향을 설정하십시오!" """, 'qtext': '<strong>Q1. [양수와 음수]</strong><br>해발 1000m를 +1000m로 나타낼 때, 해저 500m는 어떻게 나타내는가?', 'placeholder': '예: -300m', 'error': '마력이 충돌합니다! 방향과 부호를 다시 확인하십시오.', 'ans_check': "ans === '-500m' || ans === '-500'"},
    {'qnum': 2, "options": ["-3", "0", "1.5", "7"], 'title': '정수의 조건', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "첫 단계를 우회하다니 기특하구나. 하지만 정수가 아닌 불순물 숫자가 섞인 채로는 마법진의 순도가 떨어져 붕괴하고 말 것이다!"<br><br><i>네 개의 스크롤 상자가 연단 위로 떠오르고, 각각의 상자에서 푸른 마나 흐름이 흘러나옵니다. 정수의 범주에 속하지 않는 불안정한 속성을 골라내어 소거해야 격벽이 열립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "캡틴! 마법진의 평형을 위해 정수가 아닌 유리수 스크롤을 지정해 주십시오!" """, 'qtext': '<strong>Q2. [정수의 판별]</strong><br>다음 중 정수가 아닌 것의 번호를 쓰시오.<br>(1) -3 &nbsp;&nbsp;(2) 0 &nbsp;&nbsp;(3) 1.5 &nbsp;&nbsp;(4) 7', 'placeholder': '보기 번호 입력', 'error': '스파크가 튑니다! 정수가 아닌 수를 다시 골라 보십시오.', 'ans_check': "ans === '3' || ans === '1.5' || ans === '(3)'"},
    {'qnum': 3, "options": ["원점", "y축", "x축", "좌표평면"], 'title': '수직선의 기점', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "마법의 기준축조차 정의하지 못하는 미숙아에게는 공허의 심연만이 허락될 뿐이다! 기준이 되는 점의 이름을 대라!"<br><br><i>공중에 투사된 황금빛 수직선의 한가운데에서 불안정한 백색 스파크가 튀며 다이얼 입력창이 솟아오릅니다. 모든 숫자의 기점이자 힘이 시작되는 중심의 이름을 묻고 있습니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "캡틴! 수직선의 시작이자 중심이 되는 바로 그 고유 명칭을 한글로 입력해 락을 해제하세요!" """, 'qtext': '<strong>Q3. [원점]</strong><br>수직선에서 0을 나타내는 점을 무엇이라 하는가?', 'placeholder': '한글 단어 입력', 'error': '수직선 기점이 정렬되지 않습니다!', 'ans_check': "ans === '원점'"},
    {'qnum': 4, "options": ["5", "14", "7", "9"], 'title': '정수의 개수', 'story': """<strong>[시스템 통신 장애 및 붉은 노이즈 발생]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "치지직... 보이드-마스터의 교란 코드가 영역 내부에 정수 지뢰를 매설했습니다! -5와 3 사이의 안전 구역에 매설된 정수의 개수를 파악해 해독 코드로 전송하십시오! 빨리!"<br><br><i>지지직- 조종 스크린이 심하게 떨리며 회로 라인이 검붉은 색으로 오염되어 갑니다.</i>""", 'qtext': '<strong>Q4. [두 수 사이의 정수]</strong><br>-5와 3 사이에 있는 정수는 모두 몇 개인가?', 'placeholder': '숫자 또는 개수 입력', 'error': '수치가 맞지 않아 문이 닫힙니다!', 'ans_check': "ans === '7' || ans === '7개'"},
    {'qnum': 5, "options": ["10", "3", "7", "5"], 'title': '속성 에너지 융합', 'story': """🚨 <strong>[조종석 내부 기온 급강하 및 결계 압축]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "치직... 제어 복구율 50%! 실내 온도가 마이너스로 치닫고 있습니다! 두 지점 a와 b의 마력 평형 상태인 a+b 값을 계산해 제어 노드에 강제 주입하십시오! 결계 압력을 낮추어야 합니다!"<br><br><i>사방의 냉기 벽면이 쩍쩍 갈라지는 소리를 내며 조종 패널을 조여오기 시작합니다.</i>""", 'qtext': '<strong>Q5. [수직선 위의 점]</strong><br>두 정수 a, b에 대하여 a는 원점으로부터의 거리가 4이고, b는 -2보다 3만큼 큰 수이다. a가 양수일 때 a+b의 값을 구하시오.', 'placeholder': '숫자만 입력', 'error': '융합 실패! 에너지 폭발 조짐이 보입니다.', 'ans_check': "ans === '5'"},
    {'qnum': 6, "options": ["8", "10", "20", "12"], 'title': '마법 절댓값 장벽', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "하찮은 조력자의 방어막은 내 절댓값 보라색 중력장 앞에서는 무용지물이다! 짓눌려 소멸해라!"<br><br><i>쿠구구궁- 통로 정면에 거대한 자줏빛 마력 구체가 형성되며 주변 중력이 급격히 증가해 숨을 쉬기 힘들어집니다. 두 에너지의 절댓값 합을 연산해 중력 역전 상수로 주입해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "캡틴, 엄청난 중력 압박입니다! 각 마력의 절대 크기를 합산해 반중력 펄스를 생성하십시오!" """, 'qtext': '<strong>Q6. [절댓값 계산]</strong><br>|-7| + |3| 의 값을 구하시오.', 'placeholder': '숫자만 입력', 'error': '장벽의 절댓값이 꿈쩍도 하지 않습니다!', 'ans_check': "ans === '10'"},
    {'qnum': 7, "options": ["16", "6", "8", "10"], 'title': '상반되는 속성의 거리', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "중력장을 돌파했다고? 하지만 절댓값 양극단의 괴리를 메우지 못한다면 이 공간의 차원 왜곡에 갇히게 될 것이다!"<br><br><i>치지직- 수직선 양방향으로 뻗어나간 두 개의 타오르는 화염 링이 차원의 벽면을 강하게 타격합니다. 절댓값 힘이 4인 양극단 지점의 실제 차원 거리를 도출해야 게이트가 열립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "차원 균열이 감지되었습니다! 두 지점 사이의 물리적 거리를 구해 왜곡을 안정화하십시오!" """, 'qtext': '<strong>Q7. [절댓값의 성질]</strong><br>절댓값이 4인 두 수의 차를 구하시오. (큰 수에서 작은 수를 뺌)', 'placeholder': '숫자만 입력', 'error': '수치 동조 실패! 축의 거리가 맞지 않습니다.', 'ans_check': "ans === '8'"},
    {'qnum': 8, "options": ["-8", "-6", "-4", "-2"], 'title': '최강의 절댓값 보석', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "내 다섯 봉인의 에너지 중 가장 파괴적인 절댓값을 가진 어둠의 원석이 무엇인지 찾을 수 있겠는가? 잘못 선택하면 이 방의 대기가 완전히 소멸될 것이다!"<br><br><i>제단 위에 다섯 개의 오라클 마력석이 칠흑 같은 빛을 내뿜으며 차례로 정렬됩니다. 이 중 절대적인 인장 강도가 가장 큰 에너지를 판별해 원래 수치를 입력하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "경고! 각 원석의 마력 절댓값을 대조하십시오! 절대력이 가장 강력한 원석의 값을 주입해야 제단 락이 분해됩니다!" """, 'qtext': '<strong>Q8. [절댓값의 대소]</strong><br>다음 수 중 절댓값이 가장 큰 수를 쓰시오.<br>[-2.5, 3, -4, 0, 1.5]', 'placeholder': '해당 수 입력 (부호 포함)', 'error': '제단이 보석을 밀어냅니다!', 'ans_check': "ans === '-4'"},
    {'qnum': 9, "options": ["10", "3", "7", "5"], 'title': '부등식과 영역', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "슬슬 에너지가 바닥나는군. 공허의 압력 벨브를 격리하겠다. 한계를 초과하는 밀도 속에 갇혀서 서서히 질식해라!"<br><br><i>쉬이이익- 고온의 증기가 배출관에서 뿜어져 나오며 통로 전체가 격리벽으로 굳게 폐쇄되기 시작합니다. 조건식 -3 < x <= 2 를 만족하는 정수 마나의 총 개수를 해독해야 안전 밸브가 열립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "압력이 한계에 달했습니다! 조건 영역 안의 정수 마나 개수를 입력해 가스 우회 방출을 시도해 주십시오!" """, 'qtext': '<strong>Q9. [부등호의 이해]</strong><br>-3 < x <= 2 를 만족하는 정수 x의 개수를 구하시오.', 'placeholder': '숫자 또는 개수 입력', 'error': '압력이 새어나갑니다! 다시 계산하십시오.', 'ans_check': "ans === '5' || ans === '5개'"},
    {'qnum': 10, "options": ["4", "2", "0", "10"], 'title': '균형의 추', 'story': """💥 <strong>[비상 로그: 강제 자폭 코어 온라인!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "크하하! 더는 두고 볼 수 없군! 모든 시험 데이터를 포맷하고 아카데미 메인 프레임을 자폭시키겠다! 5분 내로 전부 먼지로 변하거라!"<br><br><i>경보 사일렌이 울리며 조종 콘솔 한가운데의 균형 추가 급격히 비대칭으로 요동치기 시작합니다. 수직선 위의 -4와 8의 정중앙 균형점 수치를 찾아 자폭 코드를 상쇄해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "캡틴! 마력로 온도가 급상승 중입니다! 대칭 균형점의 위치를 찾아 정밀 평형 코드로 전송하십시오! 제가 방화벽으로 에너지를 버티겠습니다!" """, 'qtext': '<strong>Q10. [한가운데 있는 수]</strong><br>수직선에서 -4와 8의 한가운데 있는 점이 나타내는 수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '조율 실패! 추가 비대칭으로 기울어집니다.', 'ans_check': "ans === '2'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '기초 마법진 덧셈', 'story': """<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "방화벽 출력 75%! 연산 상수를 지속적으로 입력하여 열에너지를 상쇄하고 마법진을 우회 통과해야 합니다! 🪄 [덧셈 마법진]"<br><br><i>바닥의 거대한 기하학 마법진이 스파크를 튀기며 과열되기 시작합니다. 식 (-5) + (+8)의 정밀 값을 도출하여 마력로 덧셈 노드에 안전하게 주입하십시오.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "계산해 봤자 결코 폭발 한계를 늦추지 못할 것이다!" """, 'qtext': '<strong>Q11. [정수의 덧셈]</strong><br>(-5) + (+8) 의 값을 구하시오.', 'placeholder': '숫자만 입력', 'error': '마법진에 스파크가 튊니다! 연산이 틀렸습니다.', 'ans_check': "ans === '3'"},
    {'qnum': 12, 'title': '기초 마법진 뺄셈', 'story': """<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "성공입니다! 온도가 내려가기 시작했습니다. 하지만 이어서 반전 뺄셈 노드가 가로막고 있습니다. 에너지를 역제어해야 합니다! 🪄 [뺄셈 에너지 반전]"<br><br><i>흐르는 마력 배선의 뺄셈 펄스에 대입할 (+3) - (-7)의 연산 결과치를 전송하여, 회로의 고압 마나가 흐르도록 평형 전압을 조절해 주십시오.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "에너지의 방향을 꺾는다고? 어림없다! 역류하는 고압 펄스에 타버려라!" """, 'qtext': '<strong>Q12. [정수의 뺄셈]</strong><br>(+3) - (-7) 의 값을 구하시오.', 'placeholder': '숫자만 입력', 'error': '반전 에너지가 제어되지 않습니다!', 'ans_check': "ans === '10'"},
    {'qnum': 13, 'title': '소수점 마나 정렬', 'story': """<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "휴... 마력 평형이 다시 흔들립니다! 소수점으로 분열된 음의 마나 결성체들을 정렬해야 합니다! 🪄 [유리수의 덧셈]"<br><br><i>제어 화면에서 조각난 유리수 마나 노드들이 거칠게 회전하며 경고음을 울립니다. (-2.5) + (-1.5)의 연산 결과치를 입력하여 유리수 마나를 안전하게 결합하십시오.</i>""", 'qtext': '<strong>Q13. [유리수의 덧셈]</strong><br>(-2.5) + (-1.5) 의 값을 구하시오.', 'placeholder': '숫자만 입력 (부호 포함)', 'error': '마나 강도 어긋남! 폭주 위험!', 'ans_check': "ans === '-4'"},
    {'qnum': 14, 'title': '3중 혼합 마나', 'story': """<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "과전류 유입 극도로 상승! 세 갈래로 얽힌 혼합 수식의 락을 즉시 해제해야 전류가 상쇄됩니다! 🪄 [혼합 연산]"<br><br><i>지이잉- 콘솔 보드에 세 개의 전하 루프가 과전하를 뿜어내고 있습니다. 수식 5 - 9 + 3 의 정답 수치를 입력하여 고압 마나를 차단 프로토콜로 상쇄시키십시오!</i>""", 'qtext': '<strong>Q15. [정수의 덧뺄셈 혼합]</strong><br>5 - 9 + 3 의 값을 구하시오.', 'placeholder': '숫자만 입력 (부호 포함)', 'error': '과전류 차단 실패! 회로 차단 경고!', 'ans_check': "ans === '-1'"},
    {'qnum': 15, 'title': '기억의 왜곡 복원', 'story': """✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G 메인 프레임 권한 100% 완전 복구]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "해독 성공! 드디어 아카데미 시스템 제어권을 보이드-마스터로부터 완벽히 탈환했습니다. 이제 역정화 주문을 실행합니다! 왜곡된 마법 기억 공식을 원상태로 복원하십시오!"<br><br><i>조종석 전체가 부드러운 청색 아우라로 뒤덮이고 에러 메시지들이 정화 코드로 교체됩니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "크으으윽... 하찮은 인간 녀석들이 내 서버의 심연을 정화하러 들어오다니! 하지만 마지막 관문은 뚫지 못할 것이다!" """, 'qtext': '<strong>Q15. [식의 바른 계산]</strong><br>어떤 수에서 -3을 빼야 할 것을 잘못하여 더했더니 5가 되었다. 바르게 계산한 답을 구하시오.', 'placeholder': '숫자만 입력', 'error': '왜곡 복원 실패! 기억 마법이 정지됩니다.', 'ans_check': "ans === '11'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '대마법 곱셈 시전', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "아직 끝난 것이 아니다! 내 마지막 어둠의 사칙연산 장벽으로 서버를 무한히 왜곡시켜 주마! 🎇 [어둠의 곱셈]"<br><br><i>벽면 격벽에 거대한 검은색 기호들이 떠돌며 차례로 전력을 차단합니다. 음과 양의 교차 곱셈 수식인 (-4) × (+6)의 파장값을 입력해 전하를 소거하십시오!</i>""", 'qtext': '<strong>Q16. [정수의 곱셈]</strong><br>(-4) × (+6) 의 값을 구하시오.', 'placeholder': '숫자만 입력 (부호 포함)', 'error': '곱셈 역류 발생! 차단막이 두꺼워집니다.', 'ans_check': "ans === '-24'"},
    {'qnum': 17, 'title': '대마법 나눗셈 시전', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "음의 에너지들이 충돌하여 소멸해봤자, 남은 파편들이 내 서버를 무한 분열시킬 뿐이다! 어디 몫을 계산해 보아라! 🎇 [음수의 분열]"<br><br><i>격벽 전면의 레이저 링들이 음수 충돌 상태를 형성합니다. (-15) ÷ (-3)의 정밀 나눗셈 결과 몫을 입력해 결계 파장을 안정시키십시오.</i>""", 'qtext': '<strong>Q17. [정수의 나눗셈]</strong><br>(-15) ÷ (-3) 의 값을 구하시오.', 'placeholder': '숫자만 입력', 'error': '마나가 불균일하게 분열됩니다!', 'ans_check': "ans === '5'"},
    {'qnum': 18, 'title': '거듭제곱 마법', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "내 공허의 비명이 세 번 거듭하여 울려 퍼질 때, 네 정신과 고막은 차원의 저편으로 영원히 조각나 흩어질 것이다! 🎇 [거듭제곱 메아리]"<br><br><i>웅웅웅- 온 조종실 전체가 강렬한 공진 주파수로 뒤흔들리며 고주파 소음 장벽이 옥죄어 옵니다. 음수 -2의 3제곱 연산 수치를 도출해 전방의 소리 장벽을 무력화하십시오!</i>""", 'qtext': '<strong>Q18. [거듭제곱]</strong><br>$(-2)^3$ 의 값을 구하시오.', 'placeholder': '숫자만 입력 (부호 포함)', 'error': '메아리가 너무 큽니다! 귀를 막고 다시 입력하세요.', 'ans_check': "ans === '-8'"},
    {'qnum': 19, 'title': '사칙 혼합 제어', 'story': """<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "끝까지 버티는군! 하지만 사칙연산이 다중 융합된 복합 매핑 프로토콜을 해독할 지능이 네놈들에게 존재할까? 🎇 [연산 제어 스크린]"<br><br><i>천장에서 하강하는 다중 격자 레이저 그물이 통로를 조각내며 빠르게 내려오기 시작합니다. 식 $(-2) \times (-3) - (+10) \div (-2)$ 의 최종 값을 주입하여 방화벽 보안 그물을 강제로 무력화하십시오!</i>""", 'qtext': '<strong>Q19. [유리수의 사칙혼합 1]</strong><br>$(-2) \times (-3) - (+10) \div (-2)$ 의 값을 구하시오.', 'placeholder': '숫자만 입력', 'error': '해킹 방어 프로토콜 작동! 수치 리셋 경고!', 'ans_check': "ans === '11'"},
    {'qnum': 20, 'title': '최종 마법진의 해', 'story': """🔮 <strong>[최종 탈출 포탈 방화벽 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[그리무어-G]</span>: "캡틴! 이제 보이드-마스터의 메인 포탈 격벽 하나만이 남았습니다. 제 전력 셀 에너지를 전부 동력 포탈에 투사하겠습니다! 마지막 복합 다중 락 수식인 $12 - [ 5 - \{ (-2) \times 3 - 4 \} ]$ 의 해를 입력하여 이곳을 탈출하십시오!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[보이드-마스터]</span>: "안 돼... 내 공허 제어 코어가... 정지하고 있어어어!" """, 'qtext': '<strong>Q20. [유리수의 사칙혼합 2]</strong><br>$12 - [ 5 - \{ (-2) \times 3 - 4 \} ]$ 의 값을 구하시오.', 'placeholder': '숫자만 입력 (부호 포함)', 'error': '시험 통과 실패! 최종 마나 코어가 작동하지 않습니다.', 'ans_check': "ans === '-3'"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_02_rational_numbers/q{qnum}.png" alt="Background" class="panel-image">
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
                <button class="btn" onclick="checkQ{qnum}()">{'마법 시전 시작' if qnum==1 else '다음으로'}</button>

            </div>
        </div>
'''
    panels_html += panel

outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>시험 합격!</h1>
            <h2>아르카나 마법 학교 입학 허가</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_02_rational_numbers/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">마지막 패스코드 '-3'을 입력하고 주문을 외우자, 거대한 연산 마법진이 황금빛 오라를 뿜어내며 하늘 높이 솟아오릅니다! 
                이마에 찬란한 입학 허가 인장이 새겨지고 시험장의 철문이 천천히 열리며 환호하는 아카데미 선배들이 나타납니다. 
                정수와 유리수의 완벽한 사칙연산 제어로 험난한 마력 결계를 돌파해 낸 신입 마법사, 아르카나 수석 입학을 대성공으로 축하합니다!</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

js_checks = "let totalWrongCount = 0;\n"
for q in qs:
    qnum = q['qnum']
    ans_check = q.get('ans_check', 'false')
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    victory_call = 'try { playVictory(); } catch(e) {}' if qnum == 20 else 'try { playSuccess(); } catch(e) {}'
    
    if qnum <= 5:
        reset_qnum = 1
        reset_prog = 0
        zone_name = "1구역"
    elif qnum <= 10:
        reset_qnum = 6
        reset_prog = 25
        zone_name = "2구역"
    elif qnum <= 15:
        reset_qnum = 11
        reset_prog = 50
        zone_name = "3구역"
    else:
        reset_qnum = 16
        reset_prog = 75
        zone_name = "4구역"
        
    # GAS 종료 호출 로직 추가 (Q20)
    gas_end_call = ""
    if qnum == 20:
        gas_end_call = '''
                // GAS 기록 종료 호출
                try {
                    if (window.userRecordRow && typeof google !== 'undefined' && google.script && google.script.run) {
                        google.script.run.recordEnd(window.userRecordRow, 'm1_02');
                    }
                } catch(e) {
                    console.warn("구글 시트 종료 기록 실패(로컬 테스트 모드):", e);
                }
                
                // 멀티 엔딩 처리
                let outroDiv = document.getElementById("outro-dynamic-text");
                if (outroDiv) {
                    if (totalWrongCount < 5) {
                        outroDiv.innerHTML = `마지막 패스코드 '-3'을 입력하고 주문을 외우자, 거대한 연산 마법진이 황금빛 오라를 뿜어내며 하늘 높이 솟아오릅니다! 
                이마에 찬란한 입학 허가 인장이 새겨지고 시험장의 철문이 천천히 열리며 환호하는 아카데미 선배들이 나타납니다. 
                정수와 유리수의 완벽한 사칙연산 제어로 험난한 마력 결계를 돌파해 낸 신입 마법사, 아르카나 수석 입학을 대성공으로 축하합니다!`;
                    } else {
                        outroDiv.innerHTML = "탈출 장치가 기동되는 순간! 시스템이 크게 요동칩니다.<br><br>잦은 오답과 연산 지연의 여파로 시스템이 과부하에 걸렸고, 데이터의 일부가 유실되었습니다. 하지만 여러분은 끝까지 포기하지 않고 방화벽을 해제하여 간신히 탈출구로 몸을 피했습니다! 상처투성이의 탈출이었지만, 수학의 지혜로 보물을 획득했습니다. 미션 성공!";
                    }
                }'''

    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace('(','').replace(')','');
            if ({ans_check}) {{
                wrongCount = 0;
                {victory_call} {gas_end_call}
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                wrongCount++;\n                totalWrongCount++;
                if (wrongCount >= 3) {{
                    showGlitchOverlay();
                    alert("🚨 3회 오답 패널티! {zone_name} 처음으로 이동됩니다.");
                    wrongCount = 0;
                    document.getElementById('ans{reset_qnum}').value = '';
                    nextStage('panel_q{qnum}', 'panel_q{reset_qnum}', {reset_prog});
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}', wrongCount);
                }}
            }}
        }}
'''
    js_checks += js

# Compile
new_content = re.sub(r'<!-- Q1.*?-->', lambda m: '<!-- Q1 -->\n' + panels_html + '\n    ', base_html, flags=re.DOTALL)
new_content = re.sub(r'// Q1[\s\S]*?(?=window\.onload = \(\) => \{)', lambda m: '// Q1\n' + js_checks + '\n        ', new_content)


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

new_content = minify_css_builder(new_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("app_m1_02_escape_room.html created successfully.")
