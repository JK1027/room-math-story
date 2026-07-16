# -*- coding: utf-8 -*-\nimport re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m2_07_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>거울 나라의 축소 광선: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0b111e;
            --glass-bg: rgba(15, 23, 42, 0.75);
            --glass-border: rgba(0, 240, 255, 0.25);
            --accent: #00f0ff;
            --accent-hover: #33f3ff;
            --text-main: #f0fbfb;
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
                radial-gradient(circle at 10% 20%, rgba(0, 240, 255, 0.08) 0%, transparent 40%),
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
            border-top: 1px solid rgba(0, 240, 255, 0.4);
            border-left: 1px solid rgba(0, 240, 255, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(0, 240, 255, 0.15), inset 0 0 20px rgba(0, 240, 255, 0.02);
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
            border-bottom: 1px solid rgba(0, 240, 255, 0.15);
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
            border: 1px solid rgba(0, 240, 255, 0.15);
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
            background: rgba(0, 240, 255, 0.05);
            border: 1px dashed rgba(0, 240, 255, 0.3);
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
            border: 1px solid rgba(0, 240, 255, 0.3);
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
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
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
            box-shadow: 0 4px 15px rgba(0, 240, 255, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 240, 255, 0.5);
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
            border-bottom: 1px solid rgba(0, 240, 255, 0.2);
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
            <h1>거울 나라의 축소 광선</h1>
            <h2>도형의 닮음 (평행선과 선분의 비)</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_07_geometry2/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [체스 퀸 AI 앨리스-Q]: "실수로 거울 나라의 축소 광선을 맞은 여러분! 몸집이 장난감만 해졌습니다. 원래 크기로 돌아가려면 거울 성에 숨겨진 '닮음비'와 '비례식'에 관련된 20개의 퍼즐을 풀어 해독 광선을 가동해야 합니다. 축소된 몸이 굳기 전에 45분 안에 서둘러야 합니다!"
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
                <button class="btn" onclick="tryStartGame('m2_07')">미션 시작</button>
            </div>

        </div>

        {panels_placeholder}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>원래 크기로 무사 복원</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_07_geometry2/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [체스 퀸 AI 앨리스-Q]: "정확한 비례식을 입력하자, 해독 광선이 눈부시게 빛나며 여러분을 감쌉니다. 순식간에 시야가 다시 넓어지고 거울에 비친 여러분의 몸이 원래 크기로 완벽하게 되돌아옵니다! 닮음의 지혜로 거울 나라를 무사히 탈출했습니다!"
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
    {'qnum': 1, "options": ["닮음", "합동", "대칭", "닮음비"], 'title': '닮음의 문양 계측', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "크하하! 거울 성문 안쪽으로 한 걸음도 들여놓지 못한다! 축소 광선을 맞아 장난감만 해진 몸뚱이로 문고리에 짓눌려 으스러져라!"<br><br><i>지이이잉- 눈앞의 거울 성문 표면에 크기와 비율이 다른 두 개의 마법 기하학 문양이 빛나기 시작합니다. 이 두 도형의 대칭/축소 관계를 나타내는 수학 용어를 주입해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "조사관님, 몸집이 줄어들어 문고리가 아득히 높습니다! 한 도형을 확대하거나 축소하여 포개질 때 성립하는 이 일치 관계 용어(두 글자)를 전송해 성문을 여십시오!"''', 'qtext': '<strong>Q1. [닮음의 정의]</strong><br>한 도형을 일정한 비율로 확대하거나 축소한 도형이 다른 도형과 합동이 될 때, 두 도형은 서로 ( ? )인 관계에 있다고 한다.', 'placeholder': '두 글자 입력', 'error': '틀렸습니다. 대칭과 축소의 기본 관계 단어입니다.', 'ans_check': "ans === '닮음'"},
    {'qnum': 2, "options": ["닮음", "합동", "대칭", "닮음비"], 'title': '축소의 배율', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "너희의 작아진 몸뚱이와 원래의 신체 선분 길이 사이의 축소 척도를 읽어낼 지능이 있느냐? 비율조차 모르는 하찮은 인형들이여!"<br><br><i>벽면의 유리 파이프를 통해 붉은색 축소 용액이 흐르고, 해독 렌즈의 대응 핀이 위아래로 흔들리기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "해독 광선 충전을 위해 선분 길이의 비율을 상징하는 단어가 필요합니다! 대응하는 변의 길이비 명칭(세 글자)을 선언하십시오!"''', 'qtext': '<strong>Q2. [닮음비의 정의]</strong><br>서로 닮은 두 평면도형에서 대응하는 선분의 길이의 비를 무엇이라 하는가?', 'placeholder': '세 글자 입력', 'error': '틀렸습니다. 닮음인 두 도형의 선분 길이의 비입니다.', 'ans_check': "ans === '닮음비'"},
    {'qnum': 3, "options": ["O", "X"], 'title': '원형 거울의 굴절', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "내 거울 나라에 흩어진 모든 원형 거울들을 모조리 뒤틀어 놓았다. 반사각이 다른 이 원들이 닮음 형태인지 판명할 수 있겠나?"<br><br><i>파지직- 벽면의 크고 작은 비눗방울 모양 원형 거울들이 보랏빛 전류 노이즈를 내며 점멸합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "원의 닮음 영속성 판정 단계입니다! 모든 원이 항상 대칭적으로 닮은 도형을 유지하는지의 진위(O/X)를 즉시 입력하십시오!"''', 'qtext': '<strong>Q3. [원의 닮음]</strong><br>두 원은 항상 닮은 도형인가? ( O / X )', 'placeholder': 'O 또는 X 입력', 'error': '틀렸습니다. 모든 원은 중심에서 테두리까지 비율이 균일합니다.', 'ans_check': "ans === 'O' || ans === '오'"},
    {'qnum': 4, 'title': '축소된 액자의 가로', 'story': '''<strong>[거울 파편의 굴절로 인한 통신 왜곡 발생]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "치직... 캡틴! 전방의 액자 문틀이 비례식 $2:3 = 4:x$ 배율로 비틀어졌습니다! ⚙️ [액자의 가로축 복원비 계측]<br><br>비례식을 만족하는 큰 액자의 가로 길이 값을 도출해 액자 틀을 일치시키십시오!"''', 'qtext': '<strong>Q4. [비례식의 연산]</strong><br>닮음비가 2:3인 두 직사각형이 있다. 작은 직사각형의 가로가 4cm일 때, 큰 직사각형의 가로는 몇 cm인가? (숫자만 입력)', 'placeholder': "단위 없이 숫자만 또는 '6cm' 입력", 'error': '틀렸습니다. 비례식 $2:3 = 4:x$를 해결해보세요.', 'ans_check': "ans === '6' || ans === '6CM'"},
    {'qnum': 5, "options": ["O", "X"], 'title': '체스판 타일의 닮음', 'story': '''<strong>[체스판 바닥 타일 함몰 격동]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "치지직... 타일 함정이 가동됩니다! 크기가 서로 다른 모든 정사각형 타일들이 항상 기하학적으로 닮아 있는지(O/X)를 판정해 딛고 설 안전 타일을 고르십시오!"''', 'qtext': '<strong>Q5. [정사각형의 닮음]</strong><br>모든 정사각형은 항상 서로 닮은 도형인가? ( O / X )', 'placeholder': 'O 또는 X 입력', 'error': '틀렸습니다. 정사각형은 네 변의 길이가 같고 네 각이 90도로 고정되어 있습니다.', 'ans_check': "ans === 'O' || ans === '오'"},
    {'qnum': 6, "options": ["SSS", "SAS", "AA", "ASA"], 'title': '세 변의 닮음 조건', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "도형의 뼈대를 이루는 세 변의 비를 전부 비틀었다. 원래의 안정화 코드로 정렬할 닮음 조건(영문 3글자)을 증명해 봐라!"<br><br><i>드르륵- 벽면에 삼각형 세 쌍의 길이 비율 지시선이 황동색 불빛으로 회전합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "삼각형의 세 쌍의 변의 비례가 일치할 때 적용되는 닮음 판정 기호(영문 대문자)를 키패드에 기입하십시오!"''', 'qtext': '<strong>Q6. [삼각형의 닮음 조건 1]</strong><br>삼각형의 세 쌍의 대응하는 변의 길이의 비가 같을 때의 닮음 조건을 쓰시오. (영문 대문자)', 'placeholder': '영문 세 글자 입력 (예: SSS)', 'error': '기호가 올바르지 않습니다. Side-Side-Side의 약자입니다.', 'ans_check': "ans === 'SSS'"},
    {'qnum': 7, "options": ["SSS", "SAS", "AA", "ASA"], 'title': '변과 사잇각의 조건', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "각도 하나와 주변의 두 변의 비를 뒤엉켜 놨다. 이 비대칭 기하학 락을 풀 닮음 코드(영문 3글자)를 짚어낼 수 있을까?"<br><br><i>보랏빛 레이저 슬롯이 이리저리 교차하며 삼각형의 사잇각 대역을 스캔합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "두 변의 비가 일정하고 사잇각이 같을 때 성립하는 고유의 닮음 조건을 전송하십시오!"''', 'qtext': '<strong>Q7. [삼각형의 닮음 조건 2]</strong><br>삼각형의 두 쌍의 대응하는 변의 길이의 비가 같고, 그 끼인각의 크기가 같을 때의 닮음 조건을 쓰시오.', 'placeholder': '영문 세 글자 입력 (예: SAS)', 'error': '기호가 올바르지 않습니다. Side-Angle-Side의 약자입니다.', 'ans_check': "ans === 'SAS'"},
    {'qnum': 8, "options": ["SSS", "SAS", "AA", "ASA"], 'title': '두 각의 닮음 조건', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "변의 길이 정보를 모두 지워 버렸다! 각도 두 개만 가지고 이 문을 열어젖힐 닮음 기호(영문 2글자)가 과연 존재할까?"<br><br><i>철컥-! 콘솔의 모든 수치 미터기가 영(0)으로 떨어지고 모퉁이 각 지시기 2개만 점등됩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "두 개의 내각 크기가 같으면 성립하는 가장 대표적인 삼각형 닮음 약어 기호를 신속히 입력하십시오!"''', 'qtext': '<strong>Q8. [삼각형의 닮음 조건 3]</strong><br>삼각형의 두 쌍의 대응하는 각의 크기가 같을 때의 닮음 조건을 쓰시오.', 'placeholder': '영문 두 글자 입력 (예: AA)', 'error': '기호가 올바르지 않습니다. Angle-Angle의 약자입니다.', 'ans_check': "ans === 'AA'"},
    {'qnum': 9, "options": ["SSS", "SAS", "AA", "ASA"], 'title': '정삼각형의 정합비', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "60도 내각으로 고정된 정삼각형 방이다. 어떤 닮음 공식 조건에 의해 이 방의 수평이 강제로 맞춰지는지 증명하라!"<br><br><i>지이이잉- 정삼각형 격실 셔터 밸브 단자에 기하학 조건 기호가 요구됩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "정삼각형의 세 각이 60도로 동일하게 동조되는 성질을 가진 닮음 조건 기호(AA)를 입력하여 게이트를 통과하십시오!"''', 'qtext': '<strong>Q9. [정삼각형의 닮음]</strong><br>한 각이 60도인 두 정삼각형은 무조건 어떤 닮음 조건에 의해 닮음인가?', 'placeholder': '예: AA닮음', 'error': '조건이 틀렸습니다. 세 각의 크기가 모두 60도로 동일하게 되는 성질을 생각하세요.', 'ans_check': "ans === 'AA' || ans === 'AA닮음'"},
    {'qnum': 10, "options": ["닮음", "합동", "대칭", "닮음비"], 'title': '수선 궤적의 쪼개짐', 'story': '''💥 <strong>[비상 로그: 거울 성 제어 콘솔 마력 오버플로우 및 자폭 작동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "하찮은 인간들, 축소된 채로 이 차원의 균열과 함께 산산조각이 나거라! 5분 뒤 모든 해독 렌즈 코어가 과열 폭발하리라!"<br><br><i>경보 혼 문자가 공중에 홀로그램으로 붉게 흩날리며 진동합니다. 수선을 내려 쪼개진 두 직각삼각형 간의 핵심 기하학 관계를 선언해 자폭을 긴급 유예하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "노심 마력 95% 돌파! 직각삼각형 빗변에 수선을 내렸을 때 분할 생성되는 두 작은 삼각형 간의 기하학적 용어(두 글자)를 긴급 입력하십시오!"''', 'qtext': '<strong>Q10. [직각삼각형의 닮음]</strong><br>직각삼각형 내부에서 직각인 꼭짓점에서 빗변에 수선을 내렸을 때 만들어지는 두 개의 작은 직각삼각형은 서로 ( ? ) 관계이다.', 'placeholder': '두 글자 입력', 'error': '틀렸습니다. 크기는 다르지만 모양이 똑같습니다.', 'ans_check': "ans === '닮음'", "extra_class": "glitch-bg"},
    {'qnum': 11, "options": ["평행", "수직", "일치", "꼬인 위치"], 'title': '평행 관계의 사다리', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "휴... 자폭 지연 3분 확보! 하지만 아직 3구역 평행 비례 사다리 록이 가로막고 있습니다! ⚙️ [중점 연결 기하 락]"<br><br><i>사다리의 양옆 중점을 연결한 가로 선분 MN과 맨 밑단 BC 기둥 간의 기하학적 위치 관계 용어(두 글자)를 입력하여 사다리를 내리십시오.</i>''', 'qtext': '<strong>Q11. [중점연결정리와 위치]</strong><br>삼각형 ABC에서 변 AB의 중점 M, 변 AC의 중점 N을 이은 선분 MN은 변 BC와 어떤 위치 관계에 있는가? (두 글자)', 'placeholder': '두 글자 입력 (예: 평행)', 'error': '틀렸습니다. 두 기둥이 나란히 뻗어 있습니다.', 'ans_check': "ans === '평행'"},
    {'qnum': 12, 'title': '중점 연결의 길이 비', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "1단계 사다리 잠금 오프! 2단계 게이트는 중점 연결 선분의 길이 비례 계수를 판독합니다! ⚙️ [길이비 연산]"<br><br><i>선분 MN의 길이가 밑변 BC의 길이의 몇 분의 몇(분수)에 해당하는지 슬래시(/)를 사용하여 입력하십시오.</i>''', 'qtext': '<strong>Q12. [중점연결정리와 길이비]</strong><br>삼각형 중점 연결 정리에서 선분 MN의 길이는 선분 BC의 길이의 ( 몇 분의 몇 ) 인가? (예: 1/2)', 'placeholder': '예: 1/2 또는 절반', 'error': '틀렸습니다. 중점을 연결했으므로 크기가 절반으로 축소됩니다.', 'ans_check': "ans === '1/2' || ans === '절반' || ans === '0.5'"},
    {'qnum': 13, 'title': '평행 차단막의 닮음', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "3단계 해치 게이트입니다! 삼각형 변에 나란하게 배치된 가로 레이저 장벽의 궤적 법칙을 판명해야 합니다! ⚙️ [평행선 분할비]"<br><br><i>가로지르는 평행 장벽에 의해 분리된 상단 작은 삼각형이 큰 삼각형과 맺는 관계(두 글자)를 전송해 레이저 출력을 우회시키십시오.</i>''', 'qtext': '<strong>Q13. [평행선과 닮음]</strong><br>삼각형의 한 변에 평행한 선분을 그어 다른 두 변과 만나게 하면, 새로 만들어진 작은 삼각형은 원래 삼각형과 ( ? ) 관계이다.', 'placeholder': '두 글자 입력', 'error': '틀렸습니다. 세 각의 크기가 같은 비례형 삼각형입니다.', 'ans_check': "ans === '닮음'"},
    {'qnum': 14, 'title': '평행 빔의 등가 비율', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "마지막 사다리 조절 해치 4단계입니다! 평행선 사이를 교차하는 두 사선에 의해 잘린 선분들의 비례 관계를 계측하십시오! ⚙️ [대응 선분 길이비]"<br><br><i>잘려 나간 양 사선의 대응 선분비가 서로 어떠한지 단답(같다 / 다르다)으로 콘솔에 기록하십시오.</i>''', 'qtext': '<strong>Q14. [평행선 사이의 선분비]</strong><br>평행한 세 직선이 두 직선과 만날 때, 잘린 대응하는 선분의 길이의 비는 서로 ( 같다 / 다르다 ).', 'placeholder': '같다 또는 다르다 입력', 'error': '틀렸습니다. 평행선 사이의 선분 비례 공식을 생각하세요.', 'ans_check': "ans === '같다'"},
    {'qnum': 15, 'title': '질량 중심의 분할비', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q 거울 방 제어 시스템 권한 100% 완전 환수]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "해독 대조 성공! 거울 방의 모든 해독 프리즘과 리플렉터 배율을 완벽히 흡수했습니다! 이제 붉은 여왕의 차원 붕괴 주파수를 차단합니다. 무게중심이 중선을 분할하는 황금비 수치(예: 2:1)를 입력하십시오!"<br><br><i>전방 렌즈 빔 제어 창이 화사한 노란색 격자망으로 재정렬되며 축소 전류가 진정됩니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "내 핵심 렌즈 통제망이 전멸당하다니...! 최종 입체 차원비로 발사 각도를 가두어 주마!"''', 'qtext': '<strong>Q15. [무게중심의 성질]</strong><br>삼각형의 무게중심은 세 중선의 길이를 꼭짓점으로부터 각각 몇 대 몇의 비율로 나누는가? (예: 2:1)', 'placeholder': '예: 2:1 또는 2대1', 'error': '비율이 올바르지 않습니다. 위쪽이 아래쪽보다 두 배 더 깁니다.', 'ans_check': "ans.replace(/\s+/g, '') === '2:1' || ans.replace(/\s+/g, '') === '2대1'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '넓이의 차원비', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "닮음비 m:n의 거울 표면적(넓이) 비율 공식이다! 제곱식 차원 계수를 맞춰 렌즈 표면을 터뜨려 봐라!"<br><br><i>해독 렌즈 표면 코팅막이 과열 팽창으로 쩍쩍 금이 가려 합니다. 거듭제곱 기호(^)를 사용해 기하학 넓이비 공식을 기입하십시오.</i>''', 'qtext': '<strong>Q16. [닮음비와 넓이비]</strong><br>두 평면도형의 닮음비가 $m:n$ 일 때, 넓이의 비는 얼마인가? (거듭제곱 기호 ^ 사용)', 'placeholder': '예: m^2:n^2', 'error': '비율 식이 잘못되었습니다. 넓이의 비는 닮음비의 제곱의 비입니다.', 'ans_check': "ans.replace(/\s+/g, '') === 'M^2:N^2' || ans.replace(/\s+/g, '') === 'M2:N2' || ans.replace(/\s+/g, '') === 'M^2대N^2'"},
    {'qnum': 17, 'title': '정육면체 거울 상자의 표면적', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "닮음비 1:2의 두 정육면체 에너지 팩이다! 이 상자들의 겉넓이 비율을 맞추지 못하면 전압이 역류하여 합선되리라!"<br><br><i>변전 스위치 격자판이 황색 스파크를 튀기며 작동 지연음을 냅니다.</i>''', 'qtext': '<strong>Q17. [입체도형의 겉넓이비]</strong><br>두 정육면체의 닮음비가 1:2 일 때, 넓이(겉넓이)의 비는 얼마인가? (예: 1:4)', 'placeholder': '예: 1:4 또는 1대4', 'error': '틀렸습니다. 닮음비가 1:2이면 넓이의 비는 제곱의 비입니다.', 'ans_check': "ans.replace(/\s+/g, '') === '1:4' || ans.replace(/\s+/g, '') === '1대4'"},
    {'qnum': 18, 'title': '부피의 차원비', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "이번엔 공간 체적(부피)의 차원비다. 닮음비 m:n 일 때의 입체 공간 비례를 세제곱 기호(^)를 사용해 맞추어라!"<br><br><i>메인 빔 렌즈 경통이 팽창음과 함께 뜨겁게 달아오릅니다.</i>''', 'qtext': '<strong>Q18. [닮음비와 부피비]</strong><br>두 입체도형의 닮음비가 $m:n$ 일 때, 부피의 비는 얼마인가? (세제곱 기호 ^ 사용)', 'placeholder': '예: m^3:n^3', 'error': '부피의 비는 닮음비의 세제곱에 비례합니다.', 'ans_check': "ans.replace(/\s+/g, '') === 'M^3:N^3' || ans.replace(/\s+/g, '') === 'M3:N3' || ans.replace(/\s+/g, '') === 'M^3대N^3'"},
    {'qnum': 19, 'title': '거울 구슬의 체적비', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "1:3 닮음비를 지닌 거울 구슬 제어 장치의 체적 부피 비율 상수를 연산판에 도출해 봐라!"<br><br><i>구슬 모양 축소 필터 유도관의 지시창이 깜빡이며, 두 구슬 파츠의 최종 부피 비례를 요구합니다.</i>''', 'qtext': '<strong>Q19. [구슬의 부피비]</strong><br>닮음비가 1:3 인 두 구슬의 부피의 비는 얼마인가? (예: 1:27)', 'placeholder': '예: 1:27', 'error': '틀렸습니다. 1과 3을 각각 세제곱하여 비율을 구하세요.', 'ans_check': "ans.replace(/\s+/g, '') === '1:27' || ans.replace(/\s+/g, '') === '1대27'"},
    {'qnum': 20, 'title': '광선 증폭의 최종 비례식', 'story': '''🔮 <strong>[최종 거울 게이트 닮음 비례식 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[앨리스-Q]</span>: "조사관님! 이제 원래의 거대한 몸집으로 돌아가는 최후의 광선 발사대 렌즈만 남았습니다! 제 모든 마나 증폭 에너지를 발사 패널에 연동하겠습니다! 컵의 닮음비 2:3을 활용한 최종 부피 비례식을 입력해 격벽 해독 게이트를 여십시오! 탈출 시간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[붉은-여왕]</span>: "안 돼... 내 거울 속 축소 매트릭스가... 완전히 해제 정지되어 파쇄되다니...!"''', 'qtext': '<strong>Q20. [부피 활용 비례식]</strong><br>작은 컵의 부피가 10mL이다. 닮음비가 2:3인 큰 컵이 있다면, 큰 컵의 부피(x)를 구하기 위한 비례식을 세워보시오. (공백 없이 입력)', 'placeholder': '예: 8:27=10:x', 'error': '비례식 세팅 실패! 부피비는 닮음비의 세제곱인 8:27임을 이용해 10:x와 연계해 세우세요.', 'ans_check': "ans.replace(/\s+/g, '') === '8:27=10:X' || ans.replace(/\s+/g, '') === '10:X=8:27'", "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_07_geometry2/q{qnum}.png" alt="Background" class="panel-image">
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

print("app_m2_07_escape_room.html generated successfully.")
