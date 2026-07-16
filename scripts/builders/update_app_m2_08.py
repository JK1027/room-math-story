# -*- coding: utf-8 -*-\nimport re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m2_08_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>행운의 카지노 로얄: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #061c10;
            --glass-bg: rgba(6, 28, 16, 0.75);
            --glass-border: rgba(220, 53, 69, 0.25);
            --accent: #dc3545;
            --accent-hover: #ff4d5a;
            --text-main: #f8fbf9;
            --text-muted: #9abfb5;
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
                radial-gradient(circle at 10% 20%, rgba(220, 53, 69, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(6, 28, 16, 0.3) 0%, transparent 40%);
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
            border-top: 1px solid rgba(220, 53, 69, 0.4);
            border-left: 1px solid rgba(220, 53, 69, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(220, 53, 69, 0.15), inset 0 0 20px rgba(220, 53, 69, 0.02);
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
            border-bottom: 1px solid rgba(220, 53, 69, 0.15);
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
            background: rgba(6, 28, 16, 0.5);
            border: 1px solid rgba(220, 53, 69, 0.15);
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
            background: rgba(220, 53, 69, 0.05);
            border: 1px dashed rgba(220, 53, 69, 0.3);
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
            background: rgba(6, 28, 16, 0.8);
            border: 1px solid rgba(220, 53, 69, 0.3);
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
            box-shadow: 0 0 10px rgba(220, 53, 69, 0.3);
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
            box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(220, 53, 69, 0.5);
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
            border-bottom: 1px solid rgba(220, 53, 69, 0.2);
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
            <h1>행운의 카지노 로얄</h1>
            <h2>경우의 수와 확률</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_08_probability/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [딜러 로봇 잭팟-D]: "화려한 라스베이거스의 카지노, 악당 갬블러 '잭팟'이 카지노의 시스템을 조작해 모든 돈을 털어가려 합니다. 이를 막기 위해서는 주사위, 동전, 카드 게임 속에 숨겨진 확률의 법칙 20개를 정확히 계산해 그를 게임에서 파산시켜야 합니다! 운이 아닌 수학으로 승부하세요!"
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
                <button class="btn" onclick="tryStartGame('m2_08')">미션 시작</button>
            </div>

        </div>

        {panels_placeholder}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>수학은 완벽한 행운을 이긴다</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_08_probability/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [딜러 로봇 잭팟-D]: "마지막 오답 확률 80%를 계산해 내며 잭팟의 카드 패가 사기임을 만천하에 증명했습니다! 잭팟은 결국 파산하여 무릎을 꿇고, 카지노에는 정의가 구현되었습니다. 수학의 힘으로 완벽한 카지노의 위기를 물리쳤습니다!"
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
    {'qnum': 1, "options": ["6", "1", "3", "5"], 'title': '딜러의 주사위 분석 1', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "크하하! 이 화려한 네온사인 아래 모든 경우의 수는 나의 예측 알고리즘 아래 지배된다! 카지노 중앙 서버의 첫 번째 룰렛 주사위 조작을 너희가 풀 수 있을 것 같나?"<br><br><i>지이이잉- 녹색 벨벳 테이블 위의 디지털 룰렛 홀로그램이 회전하며 주사위를 낙하시킵니다. 짝수의 눈이 발생하여 딜러의 베팅 알고리즘을 우회할 실질 경우의 수 상수를 주입하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "조사관님, 카지노 쉴드를 해제해야 합니다! 주사위를 굴렸을 때 짝수의 눈이 발생하는 모든 경우의 수(숫자)를 기입창에 주입해 시스템을 동조하십시오!"''', 'qtext': '<strong>Q1. [짝수의 경우의 수]</strong><br>1에서 6까지 있는 주사위 한 개를 던질 때, 짝수의 눈이 나오는 경우의 수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 짝수는 2, 4, 6입니다.', 'ans_check': "ans === '3'"},
    {'qnum': 2, "options": ["36", "72", "34", "38"], 'title': '쌍주사위의 전수 조합', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "주사위 한 개는 너무 뻔하지. 두 개의 컵에 담긴 더블 다이스가 동시에 굴러갈 때 발생하는 물리 공간의 모든 기하학적 경우의 수를 도출해 봐라!"<br><br><i>달그락- 달그락- 룰렛 진동판 위에 두 개의 가상 주사위 컵이 요란하게 흔들립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "더블 다이스 시뮬레이터 가동! 두 개의 주사위를 동시에 회전시켰을 때 발생하는 전체 경우의 수를 계산해 락 다이얼을 정렬하십시오!"''', 'qtext': '<strong>Q2. [두 주사위의 경우의 수]</strong><br>서로 다른 두 개의 주사위를 동시에 던질 때, 일어날 수 있는 모든 경우의 수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 각 주사위당 6가지씩 동시에 일어나는 경우입니다.', 'ans_check': "ans === '36'"},
    {'qnum': 3, "options": ["14", "24", "10", "12"], 'title': '동전과 주사위의 링크', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "동전의 극성 물리량과 주사위의 면을 링크시켰다! 이 연계 매트릭스의 전수 조합 한계를 규명하지 못한다면 모든 전원 보드가 과부하로 차단되리라!"<br><br><i>전방 계기판에 동전 회전 원판과 주사위 계수기가 레이저 도선으로 연결되어 스파크를 일으킵니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "연계 매트릭스 차단 성공 코드 대기! 동전 1개와 주사위 1개가 만드는 동시 조합 수치를 대입하여 회로를 차단하십시오!"''', 'qtext': '<strong>Q3. [동전과 주사위의 연계]</strong><br>동전 1개와 주사위 1개를 동시에 던질 때 일어나는 모든 경우의 수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 동전의 경우의 수와 주사위의 경우의 수를 곱해보세요.', 'ans_check': "ans === '12'"},
    {'qnum': 4, "options": ["6", "1", "3", "5"], 'title': '잭팟의 히든카드 추적', 'story': '''<strong>[블랙잭 테이블 보안 오버레이 신호 점멸]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "치직... 캡틴! 리퍼-R이 히든 슬롯에 숨겨 둔 10장의 전용 암호 카드 중 3의 배수를 매핑하여 필터링해야 합니다! ⚙️ [배수 카드 추적]<br><br>3의 배수가 표시되는 카드의 총 경우의 수를 입력하여 조작 패를 소거하십시오!"''', 'qtext': '<strong>Q4. [배수의 경우의 수]</strong><br>1에서 10까지 적힌 10장의 카드에서 1장을 뽑을 때, 3의 배수가 나오는 경우의 수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 10 이하의 수 중 3의 배수들의 개수입니다.', 'ans_check': "ans === '3'"},
    {'qnum': 5, "options": ["6", "1", "3", "5"], 'title': '주사위 합의 조작선', 'story': '''<strong>[슬롯 휠 다이얼 회전 격변]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "치지직... 슬롯 베팅 눈금의 수치가 4로 고정 조작되어 역류합니다! ⚙| [합이 4가 되는 경우의 수 연산]<br><br>두 주사위 눈의 합이 정확히 4가 나오는 모든 순서쌍 개수를 구하여 휠 가동을 역제어하십시오!"''', 'qtext': '<strong>Q5. [합이 특정 수가 되는 경우]</strong><br>두 개의 주사위를 동시에 던질 때, 눈의 합이 4가 되는 경우의 수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 합이 4가 되는 순서쌍 (x, y)의 개수를 구하세요.', 'ans_check': "ans === '3'"},
    {'qnum': 6, "options": ["14", "24", "10", "12"], 'title': '딜러의 위장 복장', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "경비용 딜러 안드로이드들의 의상을 무작위로 위장시켰다. 이 딜러들의 옷장 제복 조합을 전부 순회하여 위장 딜러를 탐지할 수 있겠나?"<br><br><i>홀로그램 매장 스크린에 상의 3종과 하의 4종의 보안 유니폼 실루엣이 번뜩입니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "위장 딜러 식별용 드레스 코드 연산! 상의 3벌과 하의 4벌로 조합할 수 있는 모든 유니폼 경우의 수를 입력창에 대입해 주십시오!"''', 'qtext': '<strong>Q6. [동시 일어나는 경우의 수]</strong><br>상의 3벌, 하의 4벌이 있을 때, 짝을 지어 입는 경우의 수는?', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 상의 선택과 하의 선택은 연달아 일어나므로 곱의 법칙을 적용합니다.', 'ans_check': "ans === '12'"},
    {'qnum': 7, "options": ["10", "3", "7", "5"], 'title': '탈출 경로의 탐색', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "카지노 비상 셔터가 전부 닫혔다. 외곽 탈출로인 모노레일 3개 노선과 지하 터널 2개 노선 중 단 하나만을 뚫어 도망쳐 보아라!"<br><br><i>덜커덩-! 셔터들이 하강하며 기계 소음이 발생합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "단일 이동 수단 합의 법칙 적용! 버스 노선 3가지와 기차 노선 2가지 중 하나만 취할 수 있는 선택 경우의 수를 도출해 셔터를 개방하십시오!"''', 'qtext': '<strong>Q7. [합의 법칙의 적용]</strong><br>서울에서 부산으로 가는 버스가 3가지, 기차가 2가지 있을 때, 서울에서 부산으로 가는 경우의 수는?', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 동시에 타는 것이 아닌 선택지 중 하나이므로 합의 법칙을 씁니다.', 'ans_check': "ans === '5'"},
    {'qnum': 8, "options": ["4", "6", "8", "12"], 'title': '경호원 보안 레이아웃', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "보안 복도의 경비 안드로이드 3대가 빈틈없는 레이아웃으로 순번 정렬 감시를 시작했다. 이 경비 라인을 뚫을 순서 조합을 읊어 보아라!"<br><br><i>철컥- 복도 게이트에 빨간색 센서 레이저가 격자로 드리워집니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "보안 레이아웃 순열 연산 작동! 3대의 안드로이드 A, B, C를 일렬로 배치하는 순번 경우의 수를 구하여 레이저 축을 정렬하십시오!"''', 'qtext': '<strong>Q8. [일렬로 세우는 경우의 수]</strong><br>A, B, C 세 명의 학생을 일렬로 세우는 경우의 수는?', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 3명을 순서대로 배열하는 경우의 수($3 \times 2 \times 1$)입니다.', 'ans_check': "ans === '6'"},
    {'qnum': 9, "options": ["14", "24", "10", "12"], 'title': '카지노 임원진 선출', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "보안실 핵심 칩셋의 메인 마스터 권한(반장)과 보조 권한(부반장)을 4개의 노드 중 뽑아야 제어 회선을 우회할 텐데, 가능하겠는가?"<br><br><i>마스터 노드 키 입력 장치 슬롯 2개가 지직거리며 황색 램프를 깜빡입니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "회선 우회 키 할당 수치 도출! 4명의 임원(노드) 중 직책이 다른 대표 2명을 순서대로 뽑아 매칭하는 경우의 수를 대입하십시오!"''', 'qtext': '<strong>Q9. [직책이 다른 대표 뽑기]</strong><br>4명 중 반장 1명, 부반장 1명을 뽑는 경우의 수는?', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 순서와 직책이 있으므로 $4 \times 3$으로 연산합니다.', 'ans_check': "ans === '12'"},
    {'qnum': 10, "options": ["4", "6", "8", "12"], 'title': '수사팀 구성 조합', 'story': '''💥 <strong>[비상 로그: 카지노 정전 및 금고 메인 제어반 강제 파괴 시퀀스 가동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "하찮은 시스템 녀석들, 금고의 메인 보드와 함께 통째로 암전 소멸되거라! 5분 뒤 모든 캐시 메모리를 리셋하겠다!"<br><br><i>시끄러운 사이렌 소리와 함께 빨간색 경보 장벽이 내려옵니다. 자격이 동일한 대표 2명의 조합 연산 키를 즉시 입력해 시퀀스를 차단하십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "제어반 강제 차단 임시 코드 전송 대기! 4명의 후보 노드 중 자격이 똑같은 공동 수사대표 2명을 뽑는 경우의 수를 입력하십시오!"''', 'qtext': '<strong>Q10. [자격이 같은 대표 뽑기]</strong><br>4명 중 자격이 같은 대표 2명을 뽑는 경우의 수는?', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 자격이 같으므로 뽑는 순서의 중복을 제거해야 합니다. ($(4 \times 3) \div 2$)', 'ans_check': "ans === '6'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '확률의 기본 범위', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "휴... 금고 셧다운 3분 지연 성공! 하지만 해커가 확률 범위 상수 칩을 오염시켜 칩 환전 한도를 조작하고 있습니다! ⚙️ [확률 범위 정합]"<br><br><i>메인 모니터에 확률 변수 p의 안전 한도 한계선을 규정하는 부등식(0<=p<=1) 입력 슬롯이 활성화됩니다. 공백 없이 정확한 범위를 타이핑하십시오.</i>''', 'qtext': '<strong>Q11. [확률의 기본 성질 1]</strong><br>어떤 사건이 일어날 확률을 $p$라고 할 때, $p$의 범위는 어떻게 되는가? (공백 없이 입력)', 'placeholder': '예: 0<=p<=1', 'error': '부등식 표현이 잘못되었습니다. 확률은 0 이상 1 이하의 범위를 가집니다.', 'ans_check': "ans.replace(/\s+/g, '') === '0<=P<=1' || ans.replace(/\s+/g, '') === '0<=P<=1.0'"},
    {'qnum': 12, 'title': '치명적 잭팟의 실패율', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "환전 한도 복구 완료! 2단계 게이트는 절대로 일어날 수 없는 에러 상태의 확률을 요구하고 있습니다! ⚙️ [불가능 확률 해독]"<br><br><i>슬롯에서 7번 주사위 면이 검출되는 것과 같은 절대 불가능한 오류 사건의 수학 확률 정수를 기입하십시오.</i>''', 'qtext': '<strong>Q12. [확률의 기본 성질 2]</strong><br>절대로 일어날 수 없는 사건의 확률은 얼마인가? (정수 입력)', 'placeholder': '숫자만 입력', 'error': '틀렸습니다. 불가능한 사건의 확률 값입니다.', 'ans_check': "ans === '0'"},
    {'qnum': 13, 'title': '동전 승부의 진실', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "3단계 게이트입니다! 룰렛 코인 뒤집기 승부에서 리퍼가 세팅한 조작 패를 무력화할 앞면 기댓 확률을 분수로 기입하십시오! ⚙️ [단일 확률 연산]"<br><br><i>기록 패널에 물리적인 동전 한 개를 던질 때의 앞면 획득 확률 코드를 전송해 주십시오.</i>''', 'qtext': '<strong>Q13. [기본 확률 구하기]</strong><br>동전 한 개를 던질 때 앞면이 나올 확률을 구하시오. (분수 형태로 입력)', 'placeholder': '분수 형태로 입력 (예: 1/2)', 'error': '틀렸습니다. 동전의 단면은 앞면과 뒷면 총 두 가지입니다.', 'ans_check': "ans === '1/2' || ans === '0.5'"},
    {'qnum': 14, 'title': '소수 슬롯머신', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "4단계 게이트! 슬롯 실린더 주사위에서 소수(2,3,5)의 눈이 걸려 조작 패배 트랩을 우회할 확률을 분수로 도출하십시오! ⚙️ [소수 확률 연산]"<br><br><i>슬롯머신의 가상 주사위 패널이 깜빡이며 기하학 코드를 대기시킵니다.</i>''', 'qtext': '<strong>Q14. [소수의 확률]</strong><br>주사위 한 개를 던질 때 소수의 눈이 나올 확률을 구하시오. (분수 형태로 입력)', 'placeholder': '분수 형태로 입력 (예: 1/2)', 'error': '틀렸습니다. 6개 눈 중 소수(2, 3, 5)의 비율을 구하세요.', 'ans_check': "ans === '1/2' || ans === '0.5'"},
    {'qnum': 15, 'title': '2 이하의 안전 룰', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D 카지노 마스터 서버 전력 100% 완전 환수]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "서버 동조 성공! 카지노 내부의 가상 리플렉터 및 안전 쉴드 제어권을 완벽히 환수했습니다! 이제 리퍼의 폭주 레이저 출력을 격하합니다. 주사위 눈이 2 이하로 격하되어 쉴드를 지켜낼 분수 확률을 전송하십시오!"<br><br><i>실내 조명이 눈부신 금빛 네온으로 정렬되며 공기가 차분해집니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "내 핵심 조작 루프를 걷어내다니...! 마지막 포커 확률 계산까지 버틸 수 있을까!"''', 'qtext': '<strong>Q15. [이하의 확률]</strong><br>주사위 한 개를 던질 때, 2 이하의 눈이 나올 확률을 구하시오. (기약분수로 입력)', 'placeholder': '분수 형태로 입력 (예: 1/3)', 'error': '틀렸습니다. 전체 6가지 중 1, 2 두 가지입니다. 약분하여 기약분수로 적으세요.', 'ans_check': "ans === '1/3'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '포커 덱의 홀수 확률', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "포커 카드 5장 중 짝수가 아닌 덱을 뽑아 나의 딜링을 격파할 실질 확률을 분수로 가져와라!"<br><br><i>카드 스피릿 창에 1부터 5까지의 카드 카운터가 돌아갑니다. 홀수를 뽑아 승리할 연산 코드를 주입하십시오.</i>''', 'qtext': '<strong>Q16. [여사건의 확률 1]</strong><br>1부터 5까지 적힌 5장의 카드 중 1장을 뽑을 때, 짝수가 아닐 확률을 구하시오. (분수 형태로 입력)', 'placeholder': '분수 형태로 입력 (예: 3/5)', 'error': '틀렸습니다. 5장 중 홀수 카드의 장수 비율입니다.', 'ans_check': "ans === '3/5' || ans === '0.6'"},
    {'qnum': 17, 'title': '비 올 확률의 대칭', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "기상 조작 빔의 습도 연산이다! 오늘 비가 올 확률이 $3/5$ 일 때, 시스템 가열을 유지해 줄 비가 오지 않을 대칭 확률을 도출해라!"<br><br><i>습도 보정 게이지에 여사건 비례 칩을 삽입해야 폭발을 피할 수 있습니다.</i>''', 'qtext': '<strong>Q17. [여사건의 확률 2]</strong><br>비가 올 확률이 $\frac{3}{5}$ 일 때, 비가 오지 않을 확률을 구하시오. (분수 형태로 입력)', 'placeholder': '분수 형태로 입력 (예: 2/5)', 'error': '틀렸습니다. 전체 확률 1에서 비가 올 확률 3/5을 빼서 계산하세요.', 'ans_check': "ans === '2/5' || ans === '0.4'"},
    {'qnum': 18, 'title': '색상 칩 주머니', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "주머니 속에 섞어 놓은 빨간 칩 3개와 파란 칩 2개 중, 빨간 칩을 단발로 꺼낼 최적 분수 확률을 맞춰 봐라!"<br><br><i>홀로그램 주머니가 룰렛 테이블 중앙에 나타나고 색상 필터링 확률이 콘솔에 연동됩니다.</i>''', 'qtext': '<strong>Q18. [공 꺼내기 확률]</strong><br>주머니에 빨간 공 3개와 파란 공 2개가 들어 있다. 임의로 1개를 꺼낼 때 빨간 공이 나올 확률은? (분수 형태로 입력)', 'placeholder': '분수 형태로 입력 (예: 3/5)', 'error': '틀렸습니다. 전체 공의 개수 중 빨간 공의 개수 비율입니다.', 'ans_check': "ans === '3/5' || ans === '0.6'"},
    {'qnum': 19, 'title': '더블 코인 플립', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "동전 2개를 공중에 던져 둘 다 앞면이 나오는 황금의 잭팟 확률을 분수로 대봐라! 네 녀석들의 운이 다할 차례다!"<br><br><i>더블 코인 플립 지시창이 회전 지연음을 냅니다.</i>''', 'qtext': '<strong>Q19. [동시 일어나는 확률]</strong><br>동전 2개를 동시에 던질 때, 모두 앞면이 나올 확률을 구하시오. (분수 형태로 입력)', 'placeholder': '분수 형태로 입력 (예: 1/4)', 'error': '틀렸습니다. 각 동전의 앞면 확률 1/2을 서로 곱해보십시오.', 'ans_check': "ans === '1/4' || ans === '0.25'"},
    {'qnum': 20, 'title': '마지막 선택의 순간', 'story': '''🔮 <strong>[최종 카지노 탈출 도어 락 확률 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[잭팟-D]</span>: "조사관님! 이제 이 조작된 카지노 빌딩을 무사히 탈출하는 최종 출구 게이트만 남았습니다! 제 모든 확률 에너지를 게이트 실린더에 투입하겠습니다! 객관식 5지선다 문제 중 임의로 찍었을 때 틀릴(오답) 확률 분수를 입력하여 락을 푸십시오! 이제 화려한 네온을 벗어날 순간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[리퍼-R]</span>: "안 돼... 내 철저했던 조작 시나리오가... 완벽한 수학 확률 법칙에 짓눌려 파산하다니...!"''', 'qtext': '<strong>Q20. [오답의 확률]</strong><br>객관식 5지 선다형 문제 1개를 임의로 찍었을 때, 틀릴 확률을 구하시오. (분수 형태로 입력)', 'placeholder': '분수 형태로 입력 (예: 4/5)', 'error': '틀렸습니다. 정답 확률이 1/5이므로 오답(틀릴) 확률을 구하십시오.', 'ans_check': "ans === '4/5' || ans === '0.8'", "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_08_probability/q{qnum}.png" alt="Background" class="panel-image">
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

print("app_m2_08_escape_room.html generated successfully.")
