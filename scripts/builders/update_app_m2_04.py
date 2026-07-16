# -*- coding: utf-8 -*-\nimport re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m2_04_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>괴도 X의 암호 편지: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0c101b;
            --glass-bg: rgba(15, 23, 42, 0.75);
            --glass-border: rgba(224, 180, 76, 0.25);
            --accent: #e0b44c;
            --accent-hover: #f5d06e;
            --text-main: #f0fbf0;
            --text-muted: #9abfa0;
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
                radial-gradient(circle at 10% 20%, rgba(50, 205, 50, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(34, 139, 34, 0.08) 0%, transparent 40%);
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
            border-top: 1px solid rgba(50, 205, 50, 0.4);
            border-left: 1px solid rgba(50, 205, 50, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(50, 205, 50, 0.1), inset 0 0 20px rgba(50, 205, 50, 0.02);
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
            border-bottom: 1px solid rgba(50, 205, 50, 0.15);
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
            background: rgba(10, 20, 15, 0.5);
            border: 1px solid rgba(50, 205, 50, 0.15);
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
            background: rgba(50, 205, 50, 0.05);
            border: 1px dashed rgba(50, 205, 50, 0.3);
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
            background: rgba(10, 20, 15, 0.8);
            border: 1px solid rgba(50, 205, 50, 0.3);
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
            box-shadow: 0 0 10px rgba(50, 205, 50, 0.3);
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
            box-shadow: 0 4px 15px rgba(50, 205, 50, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(50, 205, 50, 0.5);
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
            border-bottom: 1px solid rgba(50, 205, 50, 0.2);
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
            <h1>괴도 X의 암호 편지</h1>
            <h2>연립일차방정식의 암호 해독</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_04_equations/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [안티-씨프 AI 가드-X]: "세계적인 미술관에서 전설 of 다이아몬드 '별의 눈물'이 도난당했습니다! 현장에는 오직 괴도 X가 남긴 연립방정식 암호 편지뿐. x와 y 두 개의 미지수로 얽힌 이 단서들 속에 괴도 X의 은신처가 숨겨져 있습니다. 40분 내에 20개의 연립방정식을 풀어 다이아몬드를 되찾아오세요!"
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
                <button class="btn" onclick="tryStartGame('m2_04')">미션 시작</button>
            </div>

        </div>

        {panels_placeholder}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>괴도 X 체포 및 다이아몬드 회수</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_04_equations/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [안티-씨프 AI 가드-X]: "아들의 나이 '10'이라는 마지막 암호를 해독하자, 지도의 특정 좌표가 붉게 빛납니다. 경찰과 함께 은신처를 덮쳐 괴도 X를 체포하고 다이아몬드 '별의 눈물'을 되찾았습니다! 수고하셨습니다, 최고의 <span class="dynamic-captain-name"><span class="dynamic-captain-name">탐정</span></span> 여러분!"
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
    {'qnum': 1, "options": ["2개", "2개 아님", "알 수 없음", "해 없음"], 'title': '보안 장벽 해독', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "명화 전시장 입구의 차단 격벽 시스템을 내 전용 암호로 잠가 두었다. x와 y의 차원을 올바르게 보지 못하는 눈먼 경비원 녀석들!"<br><br><i>지이잉- 거대한 두꺼운 철제 셔터가 전시장 통로를 차단하며, 붉은색 암호 콘솔창이 활성화됩니다. 단서 수식의 미지수 개수를 판별해 키보드에 입력하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "괴도 X가 차단막 해제 코드를 차단했습니다! 주어진 일차방정식 $2x + y - 5 = 0$ 의 총 미지수 개수를 판별해 해제 신호로 쏘십시오!"''', 'qtext': '<strong>Q1. [미지수 2개인 일차방정식]</strong><br>방정식 $2x + y - 5 = 0$ 은 미지수가 몇 개인 일차방정식인가? (예: 2개)', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2개'"},
    {'qnum': 2, "options": ["$x", "$x^2"], 'title': '미술관 회로 판독', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "일차방정식과 고차방정식을 구분하지 못하고 헤매는 꼴이라니, 우습군!"<br><br><i>벽면의 열감지 레이저 제어 보드의 케이블들이 무질서하게 점멸하며 오동작을 냅니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "제어 보드의 주파수를 매핑해야 합니다! 보기 중 미지수가 2개인 일차방정식의 고유 번호를 전송하여 오동작 회로를 정상화하십시오!"''', 'qtext': '<strong>Q2. [일차방정식 판별]</strong><br>다음 중 미지수가 2개인 일차방정식은?<br>(1) $x + 2 = 3$<br>(2) $x + y = 5$<br>(3) $x^2 + y = 1$', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2'"},
    {'qnum': 3, "options": ["-1", "1", "3", "2"], 'title': '유도 장치 매핑', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "두 개의 좌표 조합(순서쌍)이 오직 자연수로만 수렴하도록 설정해 두었다. 미지의 영역에서 길을 잃어라!"<br><br><i>바닥 타일에 설치된 압력식 유도 블록 센서가 황색으로 깜빡거립니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "자연수 한정 해 조건입니다! $x + y = 3$ 을 만족하는 자연수 순서쌍 $(x, y)$의 최종 개수를 압력 조절반에 주입해 통로를 여십시오!"''', 'qtext': '<strong>Q3. [자연수 해 구하기]</strong><br>$x, y$가 자연수일 때, $x + y = 3$ 을 만족하는 순서쌍 $(x, y)$의 개수를 구하시오.', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2' || ans === '2개'"},
    {'qnum': 4, "options": ["2개", "2개 아님", "알 수 없음", "해 없음"], 'title': '레이저 그물 분석', 'story': '''<strong>[보안 그물망 작동으로 통신 혼선]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "치직... 캡틴! 전방 통로 전체에 고전력 레이저 그물이 전개되었습니다! ⚙️ [방정식 2x + y = 5 의 자연수 해의 수량 판정]<br><br>수식을 만족하는 자연수 순서쌍 $(x, y)$의 총 개수를 해독 콘솔에 입력하여 레이저 전력을 차단하십시오!"''', 'qtext': '<strong>Q4. [조건 만족 순서쌍]</strong><br>$x, y$가 자연수일 때, $2x + y = 5$ 를 만족하는 순서쌍 $(x, y)$의 개수는 몇 개인가? (숫자 또는 개 입력)', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2개' || ans === '2'"},
    {'qnum': 5, "options": ["4", "2", "0", "10"], 'title': '상수 매트릭스 도출', 'story': '''<strong>[제단 감시카메라 사각지대 탐색]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "치지직... 괴도 X가 감시카메라 각도를 수식에 고정시켰습니다. 해가 $x=1, y=2$ 일 때, 미지 상수 $a$의 값을 전송해 렌즈 셔터를 수동 해제해 주십시오!"''', 'qtext': '<strong>Q5. [미지수 상수 대입]</strong><br>$x=1, y=2$ 가 방정식 $3x - ay = -1$ 의 해일 때, 상수 $a$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2'"},
    {'qnum': 6, "options": ["연립일차방정식", "연립일차방정식 아님", "알 수 없음", "해 없음"], 'title': '보안 용어 동기화', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "서로 다른 두 개의 방정식 신호가 하나로 얽혀 묶여 버렸다. 이 병합된 단어조차 정합하지 못한다면 명화 갤러리의 문은 영원히 열리지 않는다!"<br><br><i>치이잉- 벽면에 홀로그램으로 거대한 문자가 분사됩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "제2구역 통과를 위한 핵심 보안 명칭 동기화 단계입니다. 두 일차방정식을 한 쌍으로 묶어 나타내는 일곱 글자의 수학적 명칭을 기입하십시오!"''', 'qtext': '<strong>Q6. [연립방정식의 정의]</strong><br>두 일차방정식을 한 쌍으로 묶어 놓은 것을 무엇이라 하는가?', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '연립일차방정식'"},
    {'qnum': 7, "options": ["4", "2", "0", "10"], 'title': '상수 다이얼 매칭', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "두 방정식이 공통으로 만족하는 완벽한 해의 상수 결합이다. 이 미세 상수를 틀리는 즉시 미술관의 모든 전등을 꺼 버리마!"<br><br><i>파랑색 LED 표시 장치가 번쩍이며, 공통 해 $(x=2, y=1)$ 대입 장치 록을 드러냅니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "연립방정식의 각 식에 공통 해를 대입하여 유도되는 상수 $a$의 최종 해를 전송하십시오!"''', 'qtext': '<strong>Q7. [공통 해 대입]</strong><br>$(x=2, y=1)$ 이 연립방정식 $\\begin{cases} x+y=3 \\ ax-y=3 \\end{cases}$ 의 해일 때, $a$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2'"},
    {'qnum': 8, "options": ["6", "1", "3", "5"], 'title': '직관적 평형 복구', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "더하고 빼는 계산 없이, 직관만으로 이 대칭 시스템의 x의 무게 중심을 가려낼 수 있겠느냐!"<br><br><i>천장 환기팬이 비정상적으로 빠르게 돌며 강한 바람이 조종석을 강타합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "연립방정식의 대칭 해를 도출해 환기 장치의 풍압을 복원해야 합니다! 식의 해 중 $x$의 값을 찾아 다이얼에 세팅하십시오!"''', 'qtext': '<strong>Q8. [직관적 해 도출]</strong><br>$\\begin{cases} x+y=5 \\ x-y=1 \\end{cases}$ 의 해 중 $x$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '3'"},
    {'qnum': 9, "options": ["교점", "교점 아님", "알 수 없음", "해 없음"], 'title': '그래프 기하 분석', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "두 개의 선이 우주 공간에서 만나 교차하는 극도의 한 점을 좌표로 증명해 봐라!"<br><br><i>전방 통제 터미널 스크린에 두 개의 일차함수 직선이 겹쳐지며 스파크가 일어납니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "두 직선 그래프가 마주하여 크로싱되는 지점을 수학 용어로 무엇이라 합니까? 두 글자의 답을 입력해 스크린 정렬을 마치십시오!"''', 'qtext': '<strong>Q9. [연립방정식과 그래프]</strong><br>연립방정식의 해는 두 일차방정식의 그래프가 만나는 ( ? )의 좌표와 같다. ?에 들어갈 알맞은 용어는? (두 글자)', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '교점'"},
    {'qnum': 10, "options": ["대입법", "대입법 아님", "알 수 없음", "해 없음"], 'title': '대입 해제 프로토콜', 'story': '''💥 <strong>[비상 로그: 미술관 전시실 중앙 제어 컴퓨터 강제 포맷 작동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "귀찮은 벌레 같은 녀석들! 모든 유도 암호 로그를 삭제하고 미술관을 통째로 락업시키겠다! 5분 뒤 시스템 포맷 시퀀스가 완료되리라!"<br><br><i>경보 혼이 울려 퍼지고 벽면의 전력 패널이 빨갛게 달아오릅니다. 한 미지수를 소거하기 위한 대입 메커니즘 용어를 전송해 셧다운을 긴급 유예하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "노심 용융 한계 봉착! 한 방정식을 다른 방정식에 주입해 연산하는 이 대입식 소거 용어의 명칭(세 글자)을 긴급 입력하십시오!"''', 'qtext': '<strong>Q10. [대입법의 정의]</strong><br>연립방정식을 풀 때 한 방정식을 다른 방정식에 대입하여 미지수를 없애는 방법을 무엇이라 하는가?', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '대입법'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '가감 해제 프로토콜', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "휴... 자폭 지연 3분 확보! 하지만 아직 3구역 메인 도어 게이트들이 단단히 잠겨 있습니다! ⚙️ [가감 소거 프로토콜]"<br><br><i>도어 락 단자에 두 식을 더하거나 빼서 소인수를 정렬하는 세 글자의 수학 용어 신호가 요구됩니다.</i>''', 'qtext': '<strong>Q11. [가감법의 정의]</strong><br>연립방정식을 풀 때 두 방정식을 더하거나 빼서 미지수를 없애는 방법을 무엇이라 하는가?', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '가감법'"},
    {'qnum': 12, 'title': '대입 해법 시뮬레이션', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "좋습니다, 1단계 록 아웃! 2단계 게이트 해치는 대입법의 실제 연산 값을 판독해 작동합니다! ⚙️ [대입식 소거 풀이]"<br><br><i>격벽 단자의 수식 락이 돌아갑니다. 주어진 연립방정식을 대입식으로 연산해 x의 최종 수치를 주입하십시오.</i>''', 'qtext': '<strong>Q12. [대입법 연습]</strong><br>$\\begin{cases} y = 2x \\ x + y = 6 \\end{cases}$ 을 대입법으로 풀 때, $x$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2'"},
    {'qnum': 13, 'title': '가감 조작 선택', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "3단계 보안 해치 게이트입니다! 뺄셈과 덧셈 연산 중 올바른 제어 축 조작을 결정해야 합니다! ⚙️ [연산 축 방향 결정]"<br><br><i>식의 부호를 분석하여 y를 소거하기 위한 작동 단어(더해야 / 빼야)를 입력 패드에 선언하십시오.</i>''', 'qtext': '<strong>Q13. [소거 기호 판정]</strong><br>$\\begin{cases} 2x + y = 7 \\ 2x - y = 1 \\end{cases}$ 을 가감법으로 풀기 위해 두 식을 어떻게 조작(더해야 / 빼야)하는지 쓰시오.', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '더해야'"},
    {'qnum': 14, 'title': '가감 결과 복구', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "성공입니다! 가감 방향이 올바르게 맞춰졌습니다! 이제 이전에 대조한 연립방정식의 정확한 x의 최종 상수를 꽂아 게이트 핀을 올리십시오!"''', 'qtext': '<strong>Q14. [가감법 실제 연산]</strong><br>Q13의 연립방정식 $\\begin{cases} 2x + y = 7 \\ 2x - y = 1 \\end{cases}$ 을 풀어 $x$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2'"},
    {'qnum': 15, 'title': '소거 매트릭스 복구', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X 미술관 센서 통제 제어 100% 완전 환수]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "데이터 추출 완료! 미술관 내의 전력 배전반과 레이저 격자를 완전히 제어하에 두었습니다. 괴도 X의 통제를 해제하기 위해, 주어진 연립방정식의 x의 해를 최종 입력해 전력망을 복구하십시오!"<br><br><i>콘솔 스크린에 선명한 녹색 그리드가 뜨며 경보음이 조용히 잦아듭니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "치사하게 내 통제 루트를 끊어 놓다니! 하지만 은신처로 향하는 진짜 락 수식은 절대 풀지 못할 것이다!"''', 'qtext': '<strong>Q15. [복합 연립방정식 연산]</strong><br>연립방정식 $\\begin{cases} x + 2y = 4 \\ 3x + 2y = 8 \\end{cases}$ 을 풀어 $x$의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '2'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '토끼와 닭의 다리 수', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "은신처 입구의 생물 보안 락이다! 토끼와 닭의 전체 다리 수의 비율 항을 완벽하게 세워야 문이 반응할 것이다!"<br><br><i>지이잉- 은신처 비밀번호 입력용 황동 패널에 수식 입력창이 점멸합니다.</i>''', 'qtext': '<strong>Q16. [다리 개수 식 세우기]</strong><br>토끼와 닭이 섞여 있는 우리에 머리가 모두 10개, 다리가 모두 28개이다. 토끼를 $x$마리, 닭을 $y$마리라 할 때, 다리 수에 대한 방정식 중 토끼 다리의 개수 항(4x)을 쓰시오.', 'placeholder': '예: 4x', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '4X' || ans === '4*X'"},
    {'qnum': 17, 'title': '토끼 개수 추출', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "식을 세웠을지라도, 토끼의 실질 마리수를 오차 없이 유도해내지 못한다면 봉인 격벽이 무거워질 뿐이다!"<br><br><i>철컹-! 비밀번호 단자의 유도 핀이 회전합니다. 토끼의 최종 마리수 수치와 한글 단위를 입력하십시오.</i>''', 'qtext': '<strong>Q17. [토끼 마리 수 해 도출]</strong><br>Q16의 연립방정식을 풀어 토끼($x$)는 몇 마리인지 구하시오. (예: 4마리)', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '4마리' || ans === '4'"},
    {'qnum': 18, 'title': '동전 주머니 식', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "이번엔 내 보물 금고에 채워진 동전 주머니 암호다. 100원짜리 동전의 미지수 상징 기호를 입력하여 금고 다이얼의 축을 고정시켜 봐라!"<br><br><i>황동 금고 다이얼이 회전하며, 100원짜리 동전 개수용 미지수 입력을 대기시킵니다.</i>''', 'qtext': '<strong>Q18. [동전 개수 기호]</strong><br>100원짜리 동전 $x$개와 500원짜리 동전 $y$개를 합하여 10개, 금액이 2600원일 때, 동전 개수에 대한 방정식 중 100원짜리 동전 개수의 미지수 기호(x)를 입력하시오.', 'placeholder': '예: x', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === 'X'"},
    {'qnum': 19, 'title': '100원 동전 개수', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "금고 실린더 기어를 동조시키기 위해, 실질적인 100원짜리 동전 개수 상수를 계산해 꽂아 넣어라!"<br><br><i>지이이잉- 금고 측면 해치 문이 조금씩 열리며 불빛이 새어나옵니다. 100원짜리의 수량을 입력해 핀을 맞추십시오.</i>''', 'qtext': '<strong>Q19. [동전 수량 구하기]</strong><br>Q18의 연립방정식을 풀어 100원짜리 동전($x$)은 몇 개인가? (예: 6개)', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '6개' || ans === '6'"},
    {'qnum': 20, 'title': '최종 은신처 맵핑', 'story': '''🔮 <strong>[괴도 X 최종 은신처 좌표 락다운 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[가드-X]</span>: "조사관님! 이제 괴도 X가 보석을 숨겨둔 밀실 격벽의 최종 나이 코드만 남았습니다! 제 마지막 연산 에너지를 암호 밸브에 투입하겠습니다! 부자 나이 연립 수식을 풀어 현재 아들의 실질 나이 값을 밸브에 입력하여 보석 상자를 오픈하십시오! 이제 마무리를 지을 때입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[괴도-X]</span>: "안 돼... 내 다이아몬드 은신처 전압이... 완전히 셧다운 소거되어 잠기다니!"''', 'qtext': '<strong>Q20. [나이 연립방정식 활용]</strong><br>현재 아버지와 아들의 나이의 합은 50세이고, 5년 후에는 아버지의 나이가 아들의 나이의 3배가 된다. 현재 아들의 나이를 구하시오. (예: 10세)', 'placeholder': '정답 입력', 'error': '틀렸습니다. 다시 시도해보세요.', 'ans_check': "ans === '10세' || ans === '10'", "extra_class": "glitch-bg"}
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
    qn = q['qnum']
    q['img'] = f"https://jk1027.github.io/room-math-story/apps/assets/m2_04_equations/q{qn}.png"

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
            <img src="{q['img']}" alt="Background" class="panel-image">
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

print("app_m2_04_escape_room.html generated successfully.")
