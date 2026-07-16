# -*- coding: utf-8 -*-\nimport re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m2_05_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>자율주행 택시의 길찾기: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #050508;
            --glass-bg: rgba(13, 10, 25, 0.75);
            --glass-border: rgba(255, 0, 127, 0.25);
            --accent: #ff007f;
            --accent-hover: #ff3399;
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
                radial-gradient(circle at 10% 20%, rgba(255, 0, 127, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(13, 10, 25, 0.3) 0%, transparent 40%);
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
            border-top: 1px solid rgba(255, 0, 127, 0.4);
            border-left: 1px solid rgba(255, 0, 127, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(255, 0, 127, 0.15), inset 0 0 20px rgba(255, 0, 127, 0.02);
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
            border-bottom: 1px solid rgba(255, 0, 127, 0.15);
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
            background: rgba(13, 10, 25, 0.5);
            border: 1px solid rgba(255, 0, 127, 0.15);
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
            background: rgba(255, 0, 127, 0.05);
            border: 1px dashed rgba(255, 0, 127, 0.3);
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
            background: rgba(13, 10, 25, 0.8);
            border: 1px solid rgba(255, 0, 127, 0.3);
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
            box-shadow: 0 0 10px rgba(255, 0, 127, 0.3);
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
            box-shadow: 0 4px 15px rgba(255, 0, 127, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 0, 127, 0.5);
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
            <h1>자율주행 택시의 길찾기</h1>
            <h2>일차함수와 그 그래프</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_05_functions/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [자율주행 관제 로봇 루트-R]: "미래 도시 '네오 서울', 여러분이 탄 자율주행 택시의 내비게이션이 바이러스에 감염되어 경로를 이탈했습니다. 택시는 절벽을 향해 달리고 있습니다! 유일한 제어 방법은 일차함수의 그래프를 이용해 주행 궤적을 수정하는 것뿐입니다. 기울기와 절편을 조절해 20개의 경로 포인트를 맞추고 택시를 안전한 목적지로 안내하세요!"
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
                <button class="btn" onclick="tryStartGame('m2_05')">미션 시작</button>
            </div>

        </div>

        {panels_placeholder}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>네오 서울 중앙역 무사 도착</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m2_05_functions/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [자율주행 관제 로봇 루트-R]: "정확히 10분을 입력하자 내비게이션이 정상 궤도를 회복했습니다! 택시가 절벽을 아슬아슬하게 피하며 네오 서울 중앙역에 부드럽게 멈춰 섭니다. 일차함수의 <span class="dynamic-captain-name"><span class="dynamic-captain-name">마법사</span></span> 여러분, 무사 생환을 축하합니다!"
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
    {'qnum': 1, "options": ["함수", "함수 아님", "알 수 없음", "해 없음"], 'title': '시스템 함수 정의', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "자율주행 택시의 기어를 임의로 변속시켰다! x라는 입력 기어가 굴러갈 때 y 기어가 단 하나로 완벽히 바인딩되는 함수 관계의 정의조차 입력하지 못해 절벽에 처박힐 녀석들!"<br><br><i>지이이잉- 계기판 제어 패널이 주황색 경고등과 함께 지직거리며 흐려집니다. 일차 연결 관계의 가장 핵심적인 정의 단어가 해독 장치에 요구됩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "조사관님, 자율주행 보정이 필요합니다! 변수 $x$에 의해 $y$가 오직 하나씩 유도되는 이 핵심 관계 용어(두 글자)를 콘솔에 전송해 엔진 보드를 깨우십시오!"''', 'qtext': '<strong>Q1. [함수의 정의]</strong><br>두 변수 $x, y$ 에 대하여 $x$의 값이 정해짐에 따라 $y$의 값이 오직 하나씩 정해지는 관계가 있을 때, $y$를 $x$의 무엇이라 하는가?', 'placeholder': '두 글자 입력', 'error': '시스템 용어가 올바르지 않습니다. 두 글자 명사입니다.', 'ans_check': "ans === '함수'"},
    {'qnum': 2, "options": ["10", "3", "7", "5"], 'title': '기본 궤적 연산', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "겨우 부팅했군. 일차함수 $f(x)=2x-3$ 식의 출력 주파수가 흔들린다. 입력값 $x=4$에 해당하는 실질 출력 전압 세기를 계산할 수 있겠나?"<br><br><i>차량 전방 서스펜션이 찌르르 떨리며 궤적이 오른쪽 차선 밖으로 쏠리기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "궤적 복원 전류 계산 시작! 함수 $f(x)=2x-3$ 에서 $x=4$ 일 때의 함숫값을 연산해 메인 가이드 빔에 쏘아 주십시오!"''', 'qtext': '<strong>Q2. [함숫값 연산 1]</strong><br>함수 $f(x) = 2x - 3$ 에서 $x=4$ 일 때의 함숫값 $f(4)$ 를 구하시오.', 'placeholder': '숫자만 입력', 'error': '연산 결과가 올바르지 않습니다. $2 \times 4 - 3$을 다시 계산해보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 3, "options": ["10", "3", "7", "5"], 'title': '속도 제어 밸브', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "연료 분사 노즐에 오염 코드를 주입했다! 반비례 분사 공식의 전압 $f(2)$를 정확히 맞춰 노즐을 열지 않으면 불꽃에 휩싸이리라!"<br><br><i>푸슈슈슉- 보닛 틈새로 뜨거운 증기가 솟구쳐 오르고 엔진 가동 한계 온도가 위험 수준으로 급증합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "엔진 밸브 보정 공식 작동! 함수 $f(x)=\\frac{10}{x}$ 에서 $f(2)$ 의 최종 값을 주입하여 분사량을 안정시키십시오!"''', 'qtext': '<strong>Q3. [함숫값 연산 2]</strong><br>함수 $f(x) = \frac{10}{x}$ 에서 $f(2)$ 의 값을 구하시오.', 'placeholder': '숫자만 입력', 'error': '출력 전압이 맞지 않습니다. 10을 2로 나누어보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 4, "options": ["$y"], 'title': '일차함수 판별', 'story': '''<strong>[위상 감지 센서 장애 및 신호 격차 스파크 발생]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "치지직... 조사관님! 전방에 에러가 전개한 네 갈래 교차 코드로가 보입니다! ⚙️ [일차함수 판별 제어]<br><br>진짜 일차함수 성질을 만족하는 올바른 도로 차선 번호를 선택해 차량 진행 방향을 교정하십시오!"''', 'qtext': '<strong>Q4. [일차함수의 판별]</strong><br>다음 중 일차함수인 것은?<br>(1) $y = \frac{3}{x}$<br>(2) $y = x^2$<br>(3) $y = 3x - 1$<br>(4) $y = 5$', 'placeholder': '번호만 입력 (예: 3)', 'error': '오류 패킷입니다. $y = ax + b$ (단, $a \neq 0$) 형태의 식을 찾으세요.', 'ans_check': "ans === '3' || ans === '(3)'"},
    {'qnum': 5, "options": ["Y=4X-2", "Y=4X-2 아님", "알 수 없음", "해 없음"], 'title': '궤적 평행이동', 'story': '''<strong>[제동 유도 광선 왜곡 점멸]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "치직... 택시 주행축이 가로로 휘어졌습니다! $y=4x$ 그래프의 평행이동 변위 수치를 계측해 제어 코드를 전송해야 합니다! ⚙️ [y축 방향 -2 평행이동 수식 조립]"''', 'qtext': '<strong>Q5. [평행이동 식 세우기]</strong><br>일차함수 $y = 4x$ 의 그래프를 $y$축의 방향으로 -2만큼 평행이동한 그래프의 식을 구하시오. (공백 없이 입력)', 'placeholder': '예: y = 4x - 2', 'error': '수식이 올바르지 않습니다. 평행이동한 만큼 상수항을 붙여 완성하세요.', 'ans_check': "ans.replace(/\s+/g, '') === 'Y=4X-2'"},
    {'qnum': 6, "options": ["X절편", "X절편 아님", "알 수 없음", "해 없음"], 'title': '축 교점 분석', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "가로 교차 장벽에 들이받고 고철이 될 시간이다. x축의 한계 선을 넘는 교차점의 정확한 수학 용어를 선언할 수 있겠느냐!"<br><br><i>쾅쾅-! 차량 범퍼가 가상의 빨간색 x축 차단벽과 강하게 마주하며 불꽃을 일으킵니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "가로축 접점의 수학 명칭(세 글자)을 해독 장치에 입력해 전방 차단막을 관통하십시오!"''', 'qtext': '<strong>Q6. [x축과의 교점]</strong><br>일차함수의 그래프가 $x$축과 만나는 점의 $x$좌표를 무엇이라 하는가?', 'placeholder': '세 글자 입력', 'error': '올바른 명칭이 아닙니다. x...?', 'ans_check': "ans === 'X절편' || ans === '엑스절편'"},
    {'qnum': 7, 'title': '출발지 복원 ($y$절편)', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "세로 중심 회선의 원점 높이를 비틀었다! 출발지의 세로 높이조차 읽지 못하는 눈먼 내비게이션 같으니!"<br><br><i>지직- 헤드라이트 조준선이 세로 방향으로 왜곡되어 땅바닥을 향합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "출발 기준 고도 복구 시도! 직선 $y=2x+6$의 세로축 절편($y$절편) 상수를 입력하여 라이트 조준선을 정상으로 돌리십시오!"''', 'qtext': '<strong>Q7. [y절편 구하기]</strong><br>일차함수 $y = 2x + 6$ 의 $y$절편을 구하시오.', 'placeholder': '숫자만 입력', 'error': '절편 연산에 실패했습니다. $x=0$일 때의 $y$값을 구하세요.', 'ans_check': "ans === '6'"},
    {'qnum': 8, 'title': '제동 장벽 통과 ($x$절편)', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "세로를 고정했다면 가로 정합선은 어떨까? 정확한 접지 정합 제동 좌표를 대지 못하면 격벽에 가로막힐 뿐이다!"<br><br><i>전방 노면에서 회색 철제 격벽 셔터가 위아래로 움직이며 주행을 방해합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "격벽 개방 주파수 산출! 직선 $y=2x+6$의 가로축 절편($x$절편) 값을 마이너스 기호를 포함해 신속히 입력하십시오!"''', 'qtext': '<strong>Q8. [x절편 구하기 1]</strong><br>일차함수 $y = 2x + 6$ 의 $x$절편을 구하시오.', 'placeholder': '음수는 마이너스 기호 포함 입력', 'error': '틀렸습니다. $y=0$일 때의 $x$값을 찾아보세요. ($2x+6=0$)', 'ans_check': "ans === '-3'"},
    {'qnum': 9, 'title': '회전 각도 정합', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "하강 각도로 덮쳐오는 이 미끄럼 방해 빔을 이겨낼 수 있을까? 충돌까지 남은 거리는 고작 50미터다!"<br><br><i>위이이잉- 전방에서 거대한 회전 스위퍼 암이 다가오며 차량 범퍼를 위협합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "회전 암 차단 코드 갱신! 궤적 $y=-\\frac{1}{2}x+4$의 가로축 도킹선($x$절편) 수치를 대입하여 스위퍼 암을 즉시 멈추십시오!"''', 'qtext': '<strong>Q9. [x절편 구하기 2]</strong><br>일차함수 $y = -\frac{1}{2}x + 4$ 의 $x$절편을 구하시오.', 'placeholder': '숫자만 입력', 'error': '오류입니다. $-\frac{1}{2}x + 4 = 0$이 되는 $x$값을 구하세요.', 'ans_check': "ans === '8'"},
    {'qnum': 10, "options": ["Y=X+5", "Y=X+5 아님", "알 수 없음", "해 없음"], 'title': '궤적 방정식 조립', 'story': '''💥 <strong>[비상 로그: 자율주행 차량 메인 뇌파 칩셋 강제 폭파 시퀀스 작동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "끈질기게 버티는구나! 내 너희의 스마트카 코어를 전부 불태워 포맷하겠다! 5분 뒤 모든 전력 콘덴서가 터져 나가리라!"<br><br><i>경보 부저음과 흰색 연기가 대시보드 틈새에서 새어 나오기 시작합니다. 절편 정보를 결합한 정상 궤도 일차함수 식을 긴급 조립하십시오!</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "노심 전류 과부하 봉착! $y$절편이 5이고 $x$절편이 -5인 정상 궤도의 일차함수 완성 식을 공백 없이 입력해 셧다운을 파쇄하십시오!"''', 'qtext': '<strong>Q10. [절편을 활용한 식 세우기]</strong><br>$y$절편이 5이고 $x$절편이 -5인 일차함수의 식을 구하시오. (공백 없이 입력)', 'placeholder': '예: y = x + 5', 'error': '방정식이 잘못 조립되었습니다. 기울기와 $y$절편을 바탕으로 식을 완성하세요.', 'ans_check': "ans.replace(/\s+/g, '') === 'Y=X+5'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '변화율 계산', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "후... 자폭 시퀀스 3분 지연 성공! 하지만 차량이 가파른 경사 궤도를 타고 오르며 속력이 불안정하게 요동칩니다! ⚙️ [가속 변화율 조율]"<br><br><i>가상 궤도 빔이 가파르게 하늘을 향해 치솟습니다. 수식 $y = 3x - 2$ 에서 시간 변수 x가 1초 경과할 때 주행축 y가 오르는 변화량 상수를 구하십시오.</i>''', 'qtext': '<strong>Q11. [x의 증가량에 따른 y의 증가량]</strong><br>일차함수 $y = 3x - 2$ 에서 $x$의 값이 1만큼 증가할 때 $y$의 값은 얼마나 증가하는가?', 'placeholder': '숫자만 입력', 'error': '계측 오류입니다. 일차함수 $y=ax+b$에서 $x$의 계수가 의미하는 변화량을 찾아보세요.', 'ans_check': "ans === '3'"},
    {'qnum': 12, 'title': '기울기 심볼', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "조향 제어 모듈에 연결할 기울기의 공식 문자 상징을 요구하고 있습니다! ⚙️ [기울기 변수 선언]"<br><br><i>주 조향 장치 키패드 상단에 기울기 계수를 의미하는 알파벳 기호 입력 슬롯이 점멸합니다.</i>''', 'qtext': '<strong>Q12. [기울기의 정의]</strong><br>일차함수 $y = ax + b$ 에서 기울기를 나타내는 문자는 무엇인가? (알파벳 소문자)', 'placeholder': '알파벳 1글자 입력', 'error': '올바른 시스템 심볼이 아닙니다. $x$의 계수에 해당하는 변수 이름입니다.', 'ans_check': "ans === 'A' || ans === 'a'"},
    {'qnum': 13, 'title': '두 점 사이의 구배', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "안전 조향 궤도의 구배(기울기)를 도출해야 내비게이션의 꺾임각이 맞아떨어집니다! ⚙️ [두 점 사이의 기울기 연산]"<br><br><i>유도 경로상의 두 점 $(1,3)$과 $(3,7)$을 관통하는 최적 궤도의 기울기 수치를 기입창에 주입하십시오.</i>''', 'qtext': '<strong>Q13. [기울기 구하기]</strong><br>두 점 $(1, 3)$ 과 $(3, 7)$ 을 지나는 직선의 기울기를 구하시오.', 'placeholder': '숫자만 입력', 'error': '구배 연산에 실패했습니다. (y의 증가량) / (x의 증가량) 공식을 이용하세요.', 'ans_check': "ans === '2'"},
    {'qnum': 14, "options": ["Y=-2X+1", "Y=-2X+1 아님", "알 수 없음", "해 없음"], 'title': '경로 함수 합성', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "경로 제어 마스터 록 단계입니다! 기울기와 절편 결합 수식을 조립하여 차량 조향 모터에 즉시 인젝션하십시오! ⚙️ [최종 궤적 합성]"<br><br><i>경로 지시계에 기울기 -2, y절편 1을 가지는 전용 주행 공식 궤적을 공백 없이 입력하십시오!</i>''', 'qtext': '<strong>Q14. [기울기와 y절편으로 식 세우기]</strong><br>기울기가 -2이고 $y$절편이 1인 일차함수의 식을 구하시오. (공백 없이 입력)', 'placeholder': '예: y = -2x + 1', 'error': '합성 식에 오류가 있습니다. 기울기와 $y$절편을 순서대로 식에 넣으세요.', 'ans_check': "ans.replace(/\s+/g, '') === 'Y=-2X+1'"},
    {'qnum': 15, 'title': '조향 방향 결정', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R 메인 제어 콘솔 권한 100% 완전 환수]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "동기화 완료, 조사관님! 차량의 중앙 조향 샤프트 통제권을 완벽하게 환수했습니다! 이제 해커의 가상 급커브 결계를 회피합니다. 하강형 궤도 $y=-3x+4$의 진행 방향(위 / 아래)을 판단해 선언하십시오!"<br><br><i>계기판 홀로그램이 파랗게 정렬되며 차량 서스펜션이 안정적인 대칭 구도로 펴집니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "내 통제 라인을 뚫었다고 좋아하지 마라! 연료 소모 한도 내에 안전지대로 들어가지 못하고 멈추리라!"''', 'qtext': '<strong>Q15. [기울기의 부호와 그래프 방향]</strong><br>일차함수 $y = -3x + 4$ 의 그래프는 오른쪽 ( 위 / 아래 ) 로 향하는 직선이다.', 'placeholder': '위 또는 아래 입력', 'error': '틀렸습니다. 기울기의 부호가 음수(-)일 때 직선이 향하는 방향을 생각해보세요.', 'ans_check': "ans === '아래'", "extra_class": "glitch-bg"},
    {'qnum': 16, "options": ["Y=20-2X", "Y=20-2X 아님", "알 수 없음", "해 없음"], 'title': '소모 패턴 식화', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "배터리 전하 연소 시뮬레이션 식이다! 최초 20L의 고성능 액화 연료가 매시간 2L 속도로 감쇠할 때의 잔여물 공식을 완벽히 매핑해 봐라!"<br><br><i>액화 연료 게이지의 주황색 게이지바가 아래로 흐릅니다. 시간 x와 잔여량 y의 올바른 일차함수 식을 입력창에 전송하십시오.</i>''', 'qtext': '<strong>Q16. [일차함수 활용 식 세우기]</strong><br>길이가 20cm인 양초에 불을 붙이면 1시간에 2cm씩 짧아진다. $x$시간 후의 양초의 길이를 $y$cm라 할 때, $y$를 $x$의 식으로 나타내시오. (공백 없이 입력)', 'placeholder': '예: y = 20 - 2x', 'error': '수식이 올바르지 않습니다. 처음 전지 길이에서 시간당 소모량을 차감하는 식을 세우세요.', 'ans_check': "ans.replace(/\s+/g, '') === 'Y=20-2X' || ans.replace(/\s+/g, '') === 'Y=-2X+20'"},
    {'qnum': 17, 'title': '완전 방전 시간', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "식을 조립했다면, 연료 전지가 완전히 0으로 소진되어 차량이 서 버리는 진짜 데드라인 한계 시간 상수를 도출해 봐라!"<br><br><i>엔진 구동 경보기가 깜빡이며 전하 고갈까지 남은 가상의 도달 시간을 연산 콘솔에 대기시킵니다.</i>''', 'qtext': '<strong>Q17. [함수 활용 값 구하기 1]</strong><br>위 Q16의 양초가 완전히 다 타서 없어지는 것은 불을 붙인 지 몇 시간 후인가?', 'placeholder': '예: 10시간', 'error': '틀렸습니다. 냉각 연료 봉의 잔여 길이인 $y$가 0이 되는 시간 $x$를 구하세요.', 'ans_check': "ans === '10' || ans === '10시간'"},
    {'qnum': 18, "options": ["Y=0.6X+331", "Y=0.6X+331 아님", "알 수 없음", "해 없음"], 'title': '음파 내비게이션 복구', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "지하 주행 터널 내벽의 보정 공식을 망가뜨렸다. 기온 x도에 상응해 증가하는 소리의 음파 속력 y 보정 식을 복구해 바라!"<br><br><i>초음파 전파 보정 미터기가 노이즈로 세게 흔들립니다. 온도 가산 속력 공식 식을 전송해 주십시오.</i>''', 'qtext': '<strong>Q18. [일차함수 활용 식 세우기 2]</strong><br>기온이 0도일 때 소리의 속력은 초속 331m이고 기온이 1도 오를 때마다 초속 0.6m씩 증가한다. 기온이 $x$도일 때 소리의 속력 $y$를 식으로 나타내시오. (공백 없이 입력)', 'placeholder': '예: y = 0.6x + 331', 'error': '물리 보정 식이 바르지 않습니다. 기온에 따른 가산율을 계산 식에 포함하세요.', 'ans_check': "ans.replace(/\s+/g, '') === 'Y=0.6X+331' || ans.replace(/\s+/g, '') === 'Y=331+0.6X'"},
    {'qnum': 19, 'title': '최종 기온 속력 정합', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "터널 출구 주변의 기상 센서 온도는 현재 15도다. 이 기온 대역의 음파 속력 물리량을 정확히 꽂지 못하면 레이더 피드백이 불타버릴 것이다!"<br><br><i>기온 센서 다이어그램이 15도를 가리킵니다. 보정 상수를 대입한 음파 속력 정수를 출력 패드에 기입하십시오!</i>''', 'qtext': '<strong>Q19. [함수 활용 값 구하기 2]</strong><br>기온이 15도일 때, 소리의 속력을 구하시오. (숫자만 입력)', 'placeholder': '예: 340', 'error': '오차 기온 속력입니다. $331 + 0.6 \times 15$를 연산해 보세요.', 'ans_check': "ans === '340' || ans === '340M/S' || ans === '초속340M'"},
    {'qnum': 20, 'title': '감속 냉각 시간', 'story': '''🔮 <strong>[최종 네오 서울 중앙 터미널 게이트 오픈]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[루트-R]</span>: "조사관님! 이제 네오 서울 중앙역 활주로로 진입하는 마지막 격벽 차단막만 남았습니다! 제 마지막 백업 연산 에너지를 비상 정지 감속 밸브에 투입하겠습니다! 물통 유량 식 $50 - 3x = 20$의 잔여 20L가 남는 최종 감속 시간(분)을 밸브 제어기에 입력하여 택시를 제동하십시오! 이제 안전지대로 나갈 시간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[시스템-에러]</span>: "말도 안 돼... 내 주행 폭주 궤적 제어 루프가... 완전히 0으로 제동되어 멈추다니!"''', 'qtext': '<strong>Q20. [일차함수 최종 활용]</strong><br>처음 물통에 50L의 물이 들어 있고 매분 3L씩 물을 빼낸다. 물이 20L가 남는 것은 몇 분 후인지 구하시오. (숫자만 입력)', 'placeholder': '예: 10', 'error': '브레이크 동작 실패! 유량 잔액 식 $50 - 3x = 20$을 만족하는 변수 값을 다시 구하십시오.', 'ans_check': "ans === '10' || ans === '10분'", "extra_class": "glitch-bg"}
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
    q['img'] = f"https://jk1027.github.io/room-math-story/apps/assets/m2_05_functions/q{qn}.png"

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

print("app_m2_05_escape_room.html generated successfully.")
