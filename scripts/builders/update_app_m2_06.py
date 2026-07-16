# -*- coding: utf-8 -*-\nimport re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m2_06_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>피라미드 건축가의 비밀: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #14120c;
            --glass-bg: rgba(28, 24, 18, 0.75);
            --glass-border: rgba(212, 175, 55, 0.25);
            --accent: #d4af37;
            --accent-hover: #ffdf00;
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
                radial-gradient(circle at 10% 20%, rgba(212, 175, 55, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(28, 24, 18, 0.3) 0%, transparent 40%);
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
            border-top: 1px solid rgba(212, 175, 55, 0.4);
            border-left: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(212, 175, 55, 0.15), inset 0 0 20px rgba(212, 175, 55, 0.02);
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
            text-shadow: 0 0 30px rgba(50, 205, 50, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(212, 175, 55, 0.15);
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
            background: rgba(28, 24, 18, 0.5);
            border: 1px solid rgba(212, 175, 55, 0.15);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            position: relative;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .story-box:hover {
            background: rgba(10, 20, 15, 0.7);
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
            background: rgba(212, 175, 55, 0.05);
            border: 1px dashed rgba(212, 175, 55, 0.3);
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
            background: rgba(28, 24, 18, 0.8);
            border: 1px solid rgba(212, 175, 55, 0.3);
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
            box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
        }

        .btn-group {
            display: flex;
            justify-content: center;
        }

        .btn {
            background: linear-gradient(135deg, var(--accent) 0%, #1e5c1e 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.85rem 2.5rem;
            font-size: 1.05rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
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
            text-transform: none;
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

        /* Progress Bar */
        .progress-container {
            width: 100%;
            background: rgba(10, 20, 15, 0.6);
            border: 1px solid rgba(50, 205, 50, 0.2);
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

        /* Sound Control */
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
            box-shadow: 0 0 10px rgba(50, 205, 50, 0.2);
        }

        /* Log Modal */
        .log-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(5, 12, 8, 0.85);
            backdrop-filter: blur(8px);
            z-index: 200;
            justify-content: center;
            align-items: center;
        }
        
        .log-content {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            width: 90%;
            max-width: 600px;
            max-height: 70vh;
            padding: 2rem;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        
        .log-content h2 {
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .log-list {
            overflow-y: auto;
            flex: 1;
            padding-right: 5px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .log-item {
            font-size: 0.95rem;
            line-height: 1.6;
            padding: 0.5rem 0.75rem;
            background: rgba(10, 20, 15, 0.4);
            border-radius: 8px;
            border-left: 3px solid var(--accent);
        }
        
        .close-log {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 1.2rem;
            cursor: pointer;
        }
        
        .close-log:hover {
            color: #fff;
        }

        @keyframes blink {
            50% { opacity: 0; }
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

    <button class="sound-ctrl" onclick="toggleSound()">
        🔊 소리 켜짐
    </button>

    <div class="container">
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <!-- Intro Panel -->
        <div id="intro" class="glass-panel active">
            <h1>피라미드 건축가의 비밀</h1>
            <h2>도형의 성질 1 (삼각형과 사각형)</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_06_geometry1/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [고대 홀로그램 임호텝-H]: "고대 이집트의 위대한 건축가 임호텝이 남긴 파피루스 설계도가 발견되었습니다. 이 설계도에는 삼각형과 사각형의 기하학적 성질을 이용한 20개의 암호가 걸려 있습니다. 여러분은 임호텝의 제자가 되어 도형의 성질(내심, 외심, 평행사변형 등)을 파악하고 설계도의 봉인을 해제해야 합니다!"
            </div>
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
                        <div class="info-box" style="background: rgba(220, 38, 38, 0.2); border-left: 4px solid #ef4444; padding: 0.8rem 1.2rem; margin-top: 1.5rem; border-radius: 0 12px 12px 0; color: #f87171; font-size: 0.95rem; line-height: 1.6; text-align: left;">
                ⚠️ <b>주의사항</b><br>
                문제는 총 20문제이며, 한 문제에서 3번 틀릴 경우 해당 구역의 처음으로 되돌아갑니다. <br>
                또한 <b>오답을 제출할 때마다 제한 시간이 1분씩 단축</b>되니 신중하게 도전해 주세요!
            </div>

            <div class="btn-group" style="margin-top: 2rem; width:100%;">
                <button class="btn" onclick="tryStartGame('m2_06')">미션 시작</button>
            </div>

        </div>

        {panels_placeholder}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>황금빛 입체 도면의 탄생</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_06_geometry1/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [고대 홀로그램 임호텝-H]: "정사각형 보석을 대각선에 맞추자, 파피루스 설계도의 모든 선형이 황금빛으로 타오르며 완벽한 피라미드의 입체 도면이 떠오릅니다! 여러분은 임호텝의 기하학적 시험을 통과하고 인류 최고의 건축 기술을 손에 넣었습니다!"
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

        function toggleSound() {
            isMuted = !isMuted;
            document.querySelector('.sound-ctrl').innerText = isMuted ? "🔇 소리 꺼짐" : "🔊 소리 켜짐";
        }

        function playClick() {
            if (isMuted) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.frequency.setValueAtTime(800, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
            
            osc.start();
            osc.stop(audioCtx.currentTime + 0.1);
        }

        function playTick() {
            if (isMuted) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.frequency.setValueAtTime(1200, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.02, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.03);
            
            osc.start();
            osc.stop(audioCtx.currentTime + 0.03);
        }

        function playSuccess() {
            if (isMuted) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); // C5
            osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1); // E5
            osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2); // G5
            
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.08, audioCtx.currentTime + 0.25);
            gain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
            
            osc.start();
            osc.stop(audioCtx.currentTime + 0.35);
        }

        function playError() {
            if (isMuted) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(180, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(100, audioCtx.currentTime + 0.25);
            
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.25);
            
            osc.start();
            osc.stop(audioCtx.currentTime + 0.25);
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
            <h2>📜 지나온 스토리 기록</h2>
            <div id="logContainer" class="log-list">기록이 없습니다.</div>
        </div>
    </div>
</body>
</html>
"""

# Questions configuration
qs = [
    {'qnum': 1, "options": ["이등변삼각형", "이등변삼각형 아님", "알 수 없음", "해 없음"], 'title': '설계도의 기본 뼈대', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "크하하! 이 무덤의 상형문자 차단 시스템은 우리 도굴단이 전부 잠가 버렸다. 고대 피라미드 설계 지식조차 없는 어리석은 서생 녀석들!"<br><br><i>스스스스- 바닥의 모래가 소용돌이치며, 고대 황동 다이얼 패널 위로 삼각형 뼈대 도안이 부조로 솟아오릅니다. 설계도의 기초가 되는 고유 삼각형의 명칭을 기입하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "외지인들이여, 내 무덤의 골조를 정렬해 주십시오. 두 기둥(변)의 길이가 일치해 수평 균형을 유지하는 이 기본적인 삼각형의 기하학적 명칭은 무엇입니까?"''', 'qtext': '<strong>Q1. [삼각형의 기본]</strong><br>두 변의 길이가 같은 삼각형을 무엇이라 하는가?', 'placeholder': '이등변삼각형 입력', 'error': '삼각형의 명칭이 올바르지 않습니다.', 'ans_check': "ans === '이등변삼각형'"},
    {'qnum': 2, "options": ["밑각", "밑각 아님", "알 수 없음", "해 없음"], 'title': '대칭의 각도', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "단순히 이름만 안다고 문이 열릴 줄 알았느냐? 삼각형의 주춧돌이 하중을 견디기 위한 대칭각의 법칙을 대 보아라!"<br><br><i>드르륵- 바닥 돌판이 아래로 10센티미터 주저앉으며 가벼운 마찰 진동이 일어납니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "이등변삼각형이 무너지지 않고 하중을 완벽하게 양분하기 위한 두 밑바닥 각의 명칭을 가로 질러 봉인을 푸십시오."''', 'qtext': '<strong>Q2. [이등변삼각형의 성질 1]</strong><br>이등변삼각형의 두 ( ? )의 크기는 같다. (두 글자)', 'placeholder': '두 글자 입력', 'error': '틀렸습니다. 밑변에 접하는 두 각의 이름입니다.', 'ans_check': "ans === '밑각'"},
    {'qnum': 3, "options": ["70", "72", "140", "68"], 'title': '기단의 경사각 계산', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "꼭대기 상량 각도를 40도로 좁혀 두었다. 기둥 하단이 찢어지며 천장이 무너지기 전에 이 대칭 경사각을 도출해 보아라!"<br><br><i>벽 틈새로 고대 모래시계의 모래가 빠르게 쏟아져 내리기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "서두르십시오. 꼭지각이 40도일 때, 피라미드 기단 양바닥 경사를 결정할 한 밑각의 각도 수치를 계산하여 모래 밸브에 입력해 주십시오!"''', 'qtext': '<strong>Q3. [밑각의 크기 구하기]</strong><br>꼭지각이 40도인 이등변삼각형의 한 밑각의 크기를 구하시오. (숫자만 입력)', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 삼각형 내각의 합(180도)과 꼭지각의 차를 2로 나누어보세요.', 'ans_check': "ans === '70' || ans === '70도'"},
    {'qnum': 4, "options": ["RHS", "RHA", "SSS", "SAS", "ASA"], 'title': '직각 기둥의 대칭 조건', 'story': '''<strong>[제단 감시 방해 전류 노이즈 전개]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "치직... 제 제어 주파수가 교란받고 있습니다! ⚙️ [직각삼각형의 두 합동 조건 판별]<br><br>설계도의 좌우 대칭 직각 기둥이 완전히 서로 포개지는 두 가지 기하학적 영어 기호를 쉼표로 구분해 정수 장치에 쏘아 주십시오!"''', 'qtext': '<strong>Q4. [직각삼각형의 합동 조건]</strong><br>직각삼각형의 합동 조건 두 가지를 영어 기호로 쓰시오. (쉼표로 구분하여 예: RHS, RHA)', 'placeholder': '예: RHS, RHA', 'error': '합동 조건 기호가 올바르지 않습니다. (RHS, RHA 확인)', 'ans_check': "ans.includes('RHS') && ans.includes('RHA')"},
    {'qnum': 5, "options": ["RHS", "RHA", "SSS", "SAS", "ASA"], 'title': '예각의 합동 판정', 'story': '''<strong>[피라미드 회랑의 천장 톱니바퀴 연동]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "치지직... 천장의 가이드 톱니가 돌아갑니다! 빗변과 하나의 예각이 대칭적으로 포개지는 직각 합동의 공식 명칭을 전송하십시오!"''', 'qtext': '<strong>Q5. [RHA 합동의 성질]</strong><br>빗변의 길이와 한 예각의 크기가 같은 두 직각삼각형은 서로 합동이다. 이 조건을 무엇이라 하는가?', 'placeholder': '알파벳 기호 입력', 'error': '틀렸습니다. R...?', 'ans_check': "ans.includes('RHA')"},
    {'qnum': 6, "options": ["외심", "내심", "무게중심", "수심"], 'title': '세 꼭짓점의 외접원', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "삼각형 꼭짓점 세 군데를 모두 가두어 감싸 쥐는 고대 구체 마법의 바깥 핵심 핵(중심)을 해독할 수 있겠느냐!"<br><br><i>쉬이이익- 벽면의 돌출 장치에서 푸른색 원형 궤적이 허공에 투사되며 삼각형을 에워싸기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "제2구역의 마력 천칭입니다. 삼각형의 세 꼭짓점을 감싸 흐르는 외접원의 핵심 중심점 용어(두 글자)를 도출하십시오!"''', 'qtext': '<strong>Q6. [외심의 정의]</strong><br>삼각형의 세 꼭짓점을 지나는 원을 외접원이라 하고, 그 중심을 무엇이라 하는가?', 'placeholder': '두 글자 입력', 'error': '올바른 명칭이 아닙니다. 바깥쪽 원의 중심입니다.', 'ans_check': "ans === '외심'"},
    {'qnum': 7, 'title': '기울어진 기둥의 외심', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "90도보다 더 크게 뒤로 누운 사원 둔각 처마 지붕이다. 이 지붕의 외접원 중심점은 사원 뼈대 안쪽과 바깥쪽 중 대체 어느 위험 구역에 맺힐까?"<br><br><i>우지끈- 사원 서까래 대들보 하나가 삐져나오며 기우뚱하게 가라앉습니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "기울어진 둔각삼각형의 외심 좌표 방향(내부 / 외부)을 결정해 구조물이 으스러지는 것을 방지해 주십시오!"''', 'qtext': '<strong>Q7. [둔각삼각형의 외심 위치]</strong><br>둔각삼각형의 외심은 삼각형의 ( 내부 / 외부 )에 위치한다.', 'placeholder': '내부 또는 외부 입력', 'error': '틀렸습니다. 기하학 모형을 머릿속으로 그려보세요.', 'ans_check': "ans === '외부'"},
    {'qnum': 8, 'title': '직각 지붕의 중심', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "완벽한 직각을 이룬 석실 천장이다. 외심의 좌표가 빗변의 어느 가장 취약한 부위에 맺히는지 계측해 보아라! 무너지기 직전이다!"<br><br><i>쿠구구구- 석실의 천장 돌판이 미세하게 진동을 타며 내려옵니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "천장 붕괴 저지 밸브 가동! 직각삼각형 구조에서 외심이 놓이는 빗변 위의 고유 좌표 지점(두 글자)을 입력하십시오!"''', 'qtext': '<strong>Q8. [직각삼각형의 외심 위치]</strong><br>직각삼각형의 외심은 빗변의 ( ? )에 위치한다. (두 글자)', 'placeholder': '두 글자 입력', 'error': '틀렸습니다. 빗변을 정확히 반으로 가르는 지점입니다.', 'ans_check': "ans === '중점'"},
    {'qnum': 9, "options": ["외심", "내심", "무게중심", "수심"], 'title': '세 내각의 분할점', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "석실 내부의 세 귀퉁이 각도를 반씩 쪼개 융합한 핵심 핵이다. 이 중심 기하학 원리를 해독할 수 있겠나?"<br><br><i>바닥의 원형 마법 문양판의 삼각 라인이 꺾이면서 중심부 구멍으로 노란 빛을 내뿜습니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "석실 봉인을 풀 대칭선 교차 지점입니다. 세 내각의 이등분선이 모이는 삼각형 고유의 중심(내심 / 외심) 명칭을 기입하십시오!"''', 'qtext': '<strong>Q9. [내심의 정의]</strong><br>삼각형의 세 내각의 이등분선이 만나는 점을 무엇이라 하는가?', 'placeholder': '두 글자 입력', 'error': '틀렸습니다. 안쪽 원의 중심입니다.', 'ans_check': "ans === '내심'"},
    {'qnum': 10, 'title': '내심의 거리적 특징', 'story': '''💥 <strong>[비상 로그: 피라미드 노심 보일러 과열 및 강제 자폭 작동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "더는 지체할 수 없다! 설계도고 뭐고 묘실 전체를 폭파해 모조리 매장해 주마! 5분 뒤 모든 전력 제단이 일제히 파괴되리라!"<br><br><i>지진처럼 방 안이 격렬하게 흔들리고 천장에서 돌가루가 우수수 떨어집니다. 내심의 핵심 속성(변 / 꼭짓점)을 규명해 과부하 뇌관을 정지시키십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "노심 열량 95% 도달! 삼각형의 내심에서 세 '이것'에 이르는 거리가 항상 같다는 기하학적 정리를 한 글자로 대입하여 폭발을 막으십시오!"''', 'qtext': '<strong>Q10. [내심의 성질]</strong><br>삼각형의 내심에서 세 ( ? )에 이르는 거리는 같다. (한 글자)', 'placeholder': '한 글자 입력', 'error': '틀렸습니다. 기하학 구조를 확인하세요.', 'ans_check': "ans === '변'", "extra_class": "glitch-bg"},
    {'qnum': 11, "options": ["평행사변형", "평행사변형 아님", "알 수 없음", "해 없음"], 'title': '평행 회랑의 정의', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "후... 자폭 시퀀스 3분 임시 지연 성공! 이제 제3구역 대칭의 사각 회랑 락에 도달했습니다! ⚙️ [평행 사각 제어]"<br><br><i>마주 보는 두 쌍의 테두리 변이 서로 나란히 평행하게 정렬된 이 사각형의 수학 명칭을 입력해 회랑의 잠금 셔터를 열어 주십시오.</i>''', 'qtext': '<strong>Q11. [평행사변형의 정의]</strong><br>마주 보는 두 쌍의 대변이 각각 평행한 사각형을 무엇이라 하는가?', 'placeholder': '다섯 글자 입력', 'error': '올바른 명칭이 아닙니다.', 'ans_check': "ans === '평행사변형'"},
    {'qnum': 12, 'title': '대변의 균형', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "좋습니다, 1단계 게이트 해제! 2단계 게이트는 마주 보는 변(대변)의 길이 비례 평형을 체크합니다! ⚙️ [대변의 대칭성]"<br><br><i>격벽 측면의 기계 조율 장치 홈에 기둥 길이가 일치함을 정의하는 수평 비교 단어(같다 / 다르다)를 입력하십시오.</i>''', 'qtext': '<strong>Q12. [평행사변형의 성질 1]</strong><br>평행사변형에서 마주 보는 대변의 길이는 서로 ( 같다 / 다르다 ).', 'placeholder': '같다 또는 다르다 입력', 'error': '틀렸습니다. 두 대변의 길이를 가늠해보세요.', 'ans_check': "ans === '같다'"},
    {'qnum': 13, 'title': '대각의 평형', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "중앙 회전축 동조율 80% 도달! 마주 보는 코너 각도(대각)의 대칭 크기 관계를 선언하여 밸런서 축을 정렬하십시오! ⚙️ [대각의 대칭성]"<br><br><i>크랭크축 홈이 미세하게 흔들립니다. 대각의 크기가 어떻게 매칭되는지 단답형(같다 / 다르다)으로 답하십시오.</i>''', 'qtext': '<strong>Q13. [평행사변형의 성질 2]</strong><br>평행사변형에서 마주 보는 두 대각의 크기는 서로 ( 같다 / 다르다 ).', 'placeholder': '같다 또는 다르다 입력', 'error': '틀렸습니다. 대칭되는 두 각의 관계를 상기하세요.', 'ans_check': "ans === '같다'"},
    {'qnum': 14, 'title': '대각선의 골조 교차', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "회랑의 대칭 기둥 록 마지막 단계입니다! 사각 대각선 기둥들이 교차하여 서로의 길이를 어떻게 나누는지 네 글자의 해독 키를 넣으십시오!"''', 'qtext': '<strong>Q15. [평행사변형의 성질 3]</strong><br>평행사변형의 두 대각선은 서로 다른 것을 ( ? ) 한다. (네 글자)', 'placeholder': '네 글자 입력', 'error': '틀렸습니다. 서로를 똑같이 둘로 나눕니다.', 'ans_check': "ans.includes('이등분')"},
    {'qnum': 15, "options": ["평행사변형", "평행사변형 아님", "알 수 없음", "해 없음"], 'title': '인접한 두 각의 합', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H 고대 제단 홀로그램 전력 100% 복구]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "설계 분석 완료! 묘실 내의 모든 전력 해치와 통풍 통제권을 완벽하게 장악했습니다! 이제 도굴꾼 G의 오염 가스를 역분출시킵니다. 이웃한 두 각의 합이 항상 180도로 고정 수렴되는 이 대표적 사각형의 명칭을 기입하십시오!"<br><br><i>제단 틈새로 신선한 솔바람이 불어 들며 자욱했던 연기가 빠르게 소거됩니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "제어 가스를 돌려보내다니...! 내 보석 해독 결계는 절대 뚫지 못할 것이다!"''', 'qtext': '<strong>Q15. [이웃한 각의 합]</strong><br>이웃하는 두 내각의 크기의 합이 항상 180도인 사각형은 무엇인가? (다섯 글자)', 'placeholder': '다섯 글자 입력', 'error': '틀렸습니다. 대변이 평행한 사각형입니다.', 'ans_check': "ans === '평행사변형'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '직각 보석함의 형태', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "왕의 마스터 보석함 록이다! 네 모퉁이의 각도가 한 치의 오차도 없이 90도로 정렬된 사각형 상판의 고유 명칭을 입력해 보아라!"<br><br><i>중앙 보석함 황동 두껑 주변에 기하학적인 빛의 선들이 직각 대칭 구도로 가동하기 시작합니다.</i>''', 'qtext': '<strong>Q16. [직사각형의 정의]</strong><br>네 내각의 크기가 모두 90도로 같은 사각형을 무엇이라 하는가?', 'placeholder': '세 글자 입력', 'error': '틀렸습니다. 직각을 이루는 사각형입니다.', 'ans_check': "ans === '직사각형'"},
    {'qnum': 17, 'title': '보석함의 대각선 지지대', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "상판의 밸런스를 가르는 두 대각선 기둥의 길이 관계를 오차 없이 입력(같다 / 다르다)해야 함이 열릴 것이다!"<br><br><i>보석함 정면 다이얼판이 찰칵 회전하며, 대각선 축 크기 조향을 요구합니다.</i>''', 'qtext': '<strong>Q17. [직사각형의 대각선 성질]</strong><br>직사각형의 두 대각선의 길이는 서로 ( 같다 / 다르다 ).', 'placeholder': '같다 또는 다르다 입력', 'error': '틀렸습니다. 직사각형 대각선의 성질을 상기하세요.', 'ans_check': "ans === '같다'"},
    {'qnum': 18, 'title': '대칭 석재의 정렬', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "이번엔 테두리 네 변의 길이가 전부 정밀하게 통일된 황금 석판 격자 암호다. 이 사각형의 명칭을 정확히 선언해 봐라!"<br><br><i>격자벽의 한 부분이 안으로 들어가며 황금 석판 삽입구를 노출합니다.</i>''', 'qtext': '<strong>Q18. [마름모의 정의]</strong><br>네 변의 길이가 모두 같은 사각형을 무엇이라 하는가?', 'placeholder': '세 글자 입력', 'error': '틀렸습니다. 마름모꼴 모양의 사각형입니다.', 'ans_check': "ans === '마름모'"},
    {'qnum': 19, "options": ["O", "X"], 'title': '수직 교차의 법칙', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "마름모 석판 대각선 지지대들이 직각(90도)으로 맞교차하는 진위를 판명해라! 어설프게 찍어서 수평이 무너지는 꼴을 감상해주마!"<br><br><i>삐- 삐- 경보 센서가 점멸하며, 수직 교차 법칙(O/X) 검증 패드를 가동합니다.</i>''', 'qtext': '<strong>Q19. [마름모의 대각선 성질]</strong><br>마름모의 두 대각선은 서로 수직으로 만난다. ( O / X )', 'placeholder': 'O 또는 X 입력', 'error': '틀렸습니다. 마름모 대각선의 직교 성질을 생각해 보세요.', 'ans_check': "ans === 'O' || ans === '오' || ans === 'TRUE'"},
    {'qnum': 20, 'title': '완벽의 정사각형', 'story': '''🔮 <strong>[최종 파피루스 설계도 봉인 전면 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[임호텝-H]</span>: "조사관님! 이제 임호텝 사원의 출구로 향하는 마지막 마스터 정사각형 슬롯만 남았습니다! 제 마지막 에너지를 슬롯 게이트에 투입하겠습니다! 네 변의 길이와 네 내각의 각도가 모두 완전 대칭을 이루는 최고의 다각형 명칭을 입력해 황금 게이트를 여십시오! 이제 밖으로 나갈 순간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[도굴꾼-G]</span>: "안 돼... 내 침투 격벽이... 완전히 셧다운 소멸당하다니...!"''', 'qtext': '<strong>Q20. [정사각형의 정의]</strong><br>네 변의 길이가 같고 네 각의 크기가 모두 같은 사각형의 이름은 무엇인가? (세 글자)', 'placeholder': '세 글자 입력', 'error': '최종 보석의 명칭이 바르지 않습니다.', 'ans_check': "ans === '정사각형'", "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_06_geometry1/q{qnum}.png" alt="Background" class="panel-image">
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
        
        // Chunk typewriter definition
        let typeWriterTimeout = null;
        
        function splitSentences(text) {
            let chunks = [];
            let current = "";
            let i = 0;
            while(i < text.length) {
                let char = text.charAt(i);
                current += char;
                if (char === '.' || char === '!' || char === '?') {
                    let nextChar = text.charAt(i+1);
                    if (!nextChar || nextChar === ' ' || nextChar === '\\n' || nextChar === '<') {
                        chunks.push(current.trim());
                        current = "";
                    }
                }
                i++;
            }
            if (current.trim()) {
                chunks.push(current.trim());
            }
            return chunks;
        }

        function typeWriterHTML(element, speed = 25, onComplete = null) {
            const textEl = element.querySelector('.story-text');
            if(!textEl) return;
            
            let chunks = [];
            let currentChunkIndex = 0;
            let typingFinished = false;
            let isComplete = false;
            
            function triggerComplete() {
                if(!isComplete) {
                    isComplete = true;
                    if(onComplete) onComplete();
                }
            }
            
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
"""

# Compile the final code
final_html = base_html.replace('{panels_placeholder}', panels_html)

# Add checks and boilerplate inside final script tag
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

print("app_m2_06_escape_room.html generated successfully.")
