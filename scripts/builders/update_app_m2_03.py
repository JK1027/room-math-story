# -*- coding: utf-8 -*-\nimport re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m2_03_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>요정 숲의 불균형: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #07150f;
            --glass-bg: rgba(10, 30, 20, 0.75);
            --glass-border: rgba(50, 205, 50, 0.25);
            --accent: #32cd32;
            --accent-hover: #5cfc5c;
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
            <h1>요정 숲의 불균형</h1>
            <h2>일차부등식의 해와 성질</h2>
            <img src="assets/m2_03_inequalities/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [숲의 정령 실프-F]: "아름답던 요정 숲에 검은 마법의 안개가 드리워져, 숲의 에너지 균형이 깨졌습니다. 에너지가 한쪽으로 기울어지면 숲은 영원한 어둠에 갇히게 됩니다. 이 불균형을 바로잡을 수 있는 방법은 부등식의 원리를 이해하고 마법의 저울을 원래 상태로 복구하는 것뿐입니다. 20개의 부등식 문제를 풀어 숲을 구원하세요!"
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
                <button class="btn" onclick="tryStartGame('m2_03')">미션 시작</button>
            </div>

        </div>

        {panels_placeholder}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>요정 숲의 균형 회복</h2>
            <img src="assets/m2_03_inequalities/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [숲의 정령 실프-F]: "음수를 나눌 때 부등호의 방향이 바뀐다는 결정적 사실을 놓치지 않고 20개의 문제를 해결했습니다! 마법 저울이 다시 수평을 되찾고, 요정 숲에 따뜻한 빛이 스며듭니다. 숲의 균형을 되찾은 여러분께 요정들이 감사를 전합니다!"
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
    {'qnum': 1, "options": ["X>=3", "X>=3 아님", "알 수 없음", "해 없음"], 'title': '마법 저울의 눈금', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "하찮은 침입자여! 요정 숲의 마력 저울에 칠흑의 불균형 봉인을 걸었다. 너희가 이 부등식의 경계를 올바르게 판정해 낼 것 같으냐?"<br><br><i>쿠구구궁- 이끼 낀 고대 돌탁자 위에 거대한 천칭 마법 저울이 솟아오르며 한쪽으로 요란하게 기웁니다. 저울의 경계선을 맞추어 제어 핀을 배치해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "요정 숲의 에너지 밸런스를 잡기 위해, 'x는 3보다 크거나 같다'의 기하학 부등호 수식을 콘솔에 입력하십시오! 첫 장벽을 무너뜨려야 합니다!"''', 'qtext': '<strong>Q1. [부등식의 표시]</strong><br>$x$는 3보다 크거나 같다를 부등호로 나타내시오.', 'placeholder': '예: x>=3', 'error': '저울 측정 실패! 바늘이 격렬하게 흔들립니다.', 'ans_check': "ans === 'X>=3' || ans === 'X\\GE3'"},
    {'qnum': 2, "options": ["$2x", "$3x", "$-x"], 'title': '저울의 해 찾기', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "우연히 저울을 굴렸군. 하지만 진짜 마력 해를 지목하지 못한다면, 오염된 연쇄 전류가 네놈들을 순식간에 휘감아 버릴 것이다!"<br><br><i>저울 바닥의 이끼들이 검게 타들어가며 보라색 노이즈 스파크가 사방으로 튑니다. 보기 중 x=2가 참이 되는 완벽한 해를 골라 다이얼을 정렬해 주십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "조사관님! $x=2$가 성립하는 정합 부등식 번호를 짚어 에너지 폭주를 상쇄하십시오!"''', 'qtext': '<strong>Q2. [부등식의 해]</strong><br>다음 중 $x=2$가 해인 부등식은?<br>(1) $2x - 1 &lt; 0$<br>(2) $3x \\ge 6$<br>(3) $-x &gt; 0$', 'placeholder': '예: (2) 또는 2', 'error': '오답 입력! 저울이 한쪽으로 요동칩니다.', 'ans_check': "ans === '(2)' || ans === '2' || ans === '②'"},
    {'qnum': 3, "options": ["X<5", "X<5 아님", "알 수 없음", "해 없음"], 'title': '미만의 눈금 조율', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "마법 저울의 지지 한도를 비틀어 두었다. 5에 채 미치지 못하고 부스러질 필멸자 녀석들!"<br><br><i>천장에서 검은 마력 안개가 자욱하게 뿜어져 나오며 시야를 뿌옇게 가리기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "안개가 시야를 갉아먹고 있습니다! 'x는 5 미만이다'의 부등식 기호를 정밀하게 조율해 안개 포트를 정화하십시오!"''', 'qtext': '<strong>Q3. [미만의 정의]</strong><br>$x$는 5 미만이다를 부등호로 나타내시오.', 'placeholder': '예: x<5', 'error': '부등호 방향 오류! 기류가 흐트러집니다.', 'ans_check': "ans === 'X<5'"},
    {'qnum': 4, 'title': '자연수 해 결합', 'story': '''<strong>[마법 장벽 역류 및 노이즈 발생]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "치지직... 조사관님! 다크-엘프가 저울 통신선을 차단하고 방해 코드를 심었습니다! ⚙️ [자연수 해의 판별]<br><br>저울 수식 $x + 2 &lt; 5$ 를 만족하는 진짜 자연수 해를 쉼표로 나열하여 방해 코드를 무력화하십시오!"''', 'qtext': '<strong>Q4. [조건을 만족하는 해]</strong><br>부등식 $x + 2 &lt; 5$ 를 만족하는 자연수 $x$를 모두 구하시오.', 'placeholder': '예: 1,2', 'error': '조합 실패! 마법석이 어두워집니다.', 'ans_check': "ans === '1,2' || ans === '1,2개' || ans === '1과2'"},
    {'qnum': 5, 'title': '한계 질량 구하기', 'story': '''<strong>[제단 돌벽 하강 경보]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "치지직... 제어 회로 복구율 45%! 위에서 떨어지는 돌판의 한계 질량이 부등식 $2x \\le 8$ 에 연동되어 내려오고 있습니다! 이를 만족하는 최대 정수 값을 입력해 돌벽의 하강을 저지해 주십시오!"''', 'qtext': '<strong>Q5. [해의 최대값]</strong><br>부등식 $2x \\le 8$ 을 만족하는 가장 큰 정수를 구하시오.', 'placeholder': '예: 4', 'error': '질량 초과! 저울 리미터가 울립니다.', 'ans_check': "ans === '4' || ans === '4개'"},
    {'qnum': 6, 'title': '저울의 덧셈 성질', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "자연수를 넘어서 기하학적 저울의 절대 대칭 성질을 건드렸다. 양변에 똑같은 질량을 얹었을 때의 수평 관계를 예측할 수 있을까?"<br><br><i>저울 좌우 플레이트에서 청색 불꽃이 피어오릅니다. 양변에 똑같이 2를 더해 대칭시켰을 때의 대소 관계식을 정확히 선언해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "제2구역 저울 성질 동조화입니다! $a &lt; b$ 일 때, $a+2$ 와 $b+2$ 의 정합 관계식을 입력해 주십시오!"''', 'qtext': '<strong>Q6. [부등식의 성질 1]</strong><br>$a &lt; b$ 일 때, $a + 2$ 와 $b + 2$ 의 대소를 비교하시오.', 'placeholder': '예: a+2<b+2', 'error': '평형 오류! 저울 받침대가 삐걱거립니다.', 'ans_check': "ans === 'A+2<B+2' || ans === 'B+2>A+2'"},
    {'qnum': 7, 'title': '저울의 곱셈 성질', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "더하기 정도는 상식이로군. 그렇다면 양변의 크기를 동시에 3배로 팽창시켰을 때는 어떨까? 거대해진 저울의 균형추가 흔들려 으스러지리라!"<br><br><i>황동 천칭이 기괴한 마찰음을 내며 더 무겁게 삐걱거리기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "에너지가 3배로 팽창했습니다! 양수 3을 곱했을 때의 새로운 부등식 기호 $3a$ 와 $3b$ 의 관계를 록 패널에 새기십시오!"''', 'qtext': '<strong>Q7. [부등식의 성질 2]</strong><br>$a &lt; b$ 일 때, $3a$ 와 $3b$ 의 대소를 비교하시오.', 'placeholder': '예: 3a<3b', 'error': '에너지 증폭 이상! 스파크가 튑니다.', 'ans_check': "ans === '3A<3B' || ans === '3B>3A'"},
    {'qnum': 8, 'title': '음수 곱셈의 반전', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "크크크... 진짜 지옥은 지금부터다. 음의 기류를 흘려보내 저울의 방향을 통째로 꼬아버리겠다!"<br><br><i>파지직- 저울대에 어두운 보랏빛 마력이 흘러들어가며, 바늘의 방향 지시가 정반대로 요동치기 시작합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "비상! 음수 -2가 곱해지면서 부등식 에너지의 방향이 틀어졌습니다! $-2a$ 와 $-2b$ 의 올바른 대소 관계를 역연산해 입력하십시오!"''', 'qtext': '<strong>Q8. [부등식의 성질 3]</strong><br>$a &lt; b$ 일 때, $-2a$ 와 $-2b$ 의 대소 관계를 부등호로 나타내시오.', 'placeholder': '예: -2a>-2b', 'error': '반전 에러! 저울이 균형을 완전히 잃고 기울어집니다.', 'ans_check': "ans === '-2A>-2B' || ans === '-2B<-2A'"},
    {'qnum': 9, 'title': '방향 반전 법칙', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "방향이 바뀐다는 원리를 알았다면, 이 음수 나눗셈의 절대 규칙을 단답형 단어로 증명해 봐라! 기하학의 금기를 어길 수 있을쏘냐!"<br><br><i>천장 덩굴들이 촉수처럼 뻗어 나와 출구를 단단히 틀어막습니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "조사관님! 음수를 곱하거나 나눌 때 부등호의 성질이 어떻게 변하는지, 세 글자의 핵심 선언 단어를 주입하여 덩굴을 후퇴시키십시오!"''', 'qtext': '<strong>Q9. [부등호의 핵심 법칙]</strong><br>음수를 곱하거나 나눌 때 부등호의 방향은 어떻게 되는가?', 'placeholder': '바뀐다 또는 그대로다 입력', 'error': '법칙 위반! 숲의 정령들이 길을 막습니다.', 'ans_check': "ans === '바뀐다' || ans === '변한다' || ans === '바뀜'"},
    {'qnum': 10, "options": ["X<-3", "X<-3 아님", "알 수 없음", "해 없음"], 'title': '음수 나눗셈의 완성', 'story': '''💥 <strong>[비상 로그: 숲의 마력 코어 자폭 포맷 가동!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "더는 참을 수 없군! 모든 고대 숲의 데이터를 파괴하고 시스템을 리셋하겠다! 5분 뒤 이 일대의 모든 마나 셀이 자폭 개시하리라!"<br><br><i>위이이잉- 경보 룬 문자들이 주위 벽면에서 붉게 깜빡이며 진동하기 시작합니다. 음수 나눗셈 부등식 수치 $-3x > 9$ 를 풀어 락을 정지시켜야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "비상! 노심 열량 임계치 돌파! 양변을 -3으로 나눈 최종 부등식 해를 전송하십시오! 제가 정화 배리어를 최대로 작동시켜 지연시키겠습니다!"''', 'qtext': '<strong>Q10. [음수 나눗셈 연습]</strong><br>$-3x &gt; 9$ 양변을 -3으로 나누면 부등식은 어떻게 되는가?', 'placeholder': '예: x<-3', 'error': '부호 오류! 2구역 탈출 밸브가 차단됩니다.', 'ans_check': "ans === 'X<-3'", "extra_class": "glitch-bg"},
    {'qnum': 11, "options": ["X>2", "X>2 아님", "알 수 없음", "해 없음"], 'title': '마법진 1차 해제', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "후... 자폭 유예 시간 3분 확보! 하지만 아직 3구역의 숲 정화 마법진 록들이 가로막고 있습니다! ⚙️ [일차부등식 1단계]"<br><br><i>콘솔 상단의 이끼 낀 돌 마법진의 틈새로 부등식 $2x - 4 > 0$ 포트가 빛납니다. 이 식을 이항 연산한 정확한 해를 주입하십시오.</i>''', 'qtext': '<strong>Q11. [기초 부등식 풀이]</strong><br>일차부등식 $2x - 4 &gt; 0$ 의 해를 구하시오.', 'placeholder': '예: x>2', 'error': '마법 해제 실패! 마법진이 붉게 점멸합니다.', 'ans_check': "ans === 'X>2'"},
    {'qnum': 12, "options": ["X<=2", "X<=2 아님", "알 수 없음", "해 없음"], 'title': '마법진 2차 해제', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "1단계 록 해제 성공! 다음 2단계는 상수 이항의 정확성을 체크합니다! ⚙️ [이항과 부등호 유지]"<br><br><i>파랑색 마나 기류가 부등식 $3x + 1 \\le 7$ 의 이항 정합 각도를 요구합니다. 해를 계산해 전송하십시오.</i>''', 'qtext': '<strong>Q12. [이항 계산]</strong><br>일차부등식 $3x + 1 \\le 7$ 의 해를 구하시오.', 'placeholder': '예: x<=2', 'error': '이항 연산 미스! 결합 에너지가 소멸됩니다.', 'ans_check': "ans === 'X<=2' || ans === 'X\\LE2'"},
    {'qnum': 13, "options": ["X<5", "X<5 아님", "알 수 없음", "해 없음"], 'title': '양변 이항 결합', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "정화 마법진 복구율 80%! 양변의 미지수와 상수를 각각 정방향 이항 결합하여 정화 빔을 발사해야 합니다! ⚙️ [양변 이항 정리]"<br><br><i>마법진 중앙에 $5x - 2 < 3x + 8$ 의 기하학 도식이 회전하며, x의 참 범위를 밸런서에 대기시킵니다.</i>''', 'qtext': '<strong>Q13. [복합 이항]</strong><br>일차부등식 $5x - 2 &lt; 3x + 8$ 의 해를 구하시오.', 'placeholder': '예: x<5', 'error': '이항 부호 에러! 에너지 균형이 흐트러집니다.', 'ans_check': "ans === 'X<5'"},
    {'qnum': 14, "options": ["X<=3", "X<=3 아님", "알 수 없음", "해 없음"], 'title': '음수 계수 이항', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "이제 정화 마법진 마지막 3단계입니다! 음수 계수의 복합 연산 코드를 전송하십시오! ⚙ [최종 계수 반전 제어]"<br><br><i>지이잉- 마법진의 메인 차단막 슬롯이 멈추며 부등식 $-2x + 5 \\ge x - 4$ 의 최종 해를 매핑할 준비를 합니다.</i>''', 'qtext': '<strong>Q14. [음수 계수 이항]</strong><br>일차부등식 $-2x + 5 \\ge x - 4$ 의 해를 구하시오.', 'placeholder': '예: x<=3', 'error': '반전 연산 실패! 마법진 온도가 급격히 올라갑니다.', 'ans_check': "ans === 'X<=3' || ans === 'X\\LE3'"},
    {'qnum': 15, "options": ["X>3", "X>3 아님", "알 수 없음", "해 없음"], 'title': '괄호 마법진 돌파', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F 요정 제단 권한 100% 완전 복구]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "해독 완료, 조사관님! 숲의 메인 룬 제단 통제권을 완벽하게 환수했습니다! 이제 다크-엘프의 검은 기류를 차단합니다. 괄호가 적용된 부등식 $2(x - 1) &gt; 4$ 의 해를 주입하여 락을 파쇄하십시오!"<br><br><i>제단 중앙에 아름다운 에메랄드빛 마나 분수가 솟구치며 주변의 검은 가스가 일제히 소멸합니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "내 핵심 룬 제어 락이 무너지다니...! 최종 실생활 억제 사슬로 숲의 중심부에 가두어 주마!"''', 'qtext': '<strong>Q15. [괄호가 있는 부등식]</strong><br>일차부등식 $2(x - 1) &gt; 4$ 의 해를 구하시오.', 'placeholder': '예: x>3', 'error': '괄호 분배 오류! 마법진이 비상 셧다운 모드로 돌입합니다.', 'ans_check': "ans === 'X>3'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '연속하는 자연수 씨앗', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "생명의 숲을 재생시키는 자연수의 씨앗 조화비를 알아맞히지 못하면, 싹조차 틔우지 못하고 고사하리라!"<br><br><i>바닥의 씨앗 분배기 함이 어긋나며 쇠마찰음을 냅니다. 연속하는 두 자연수의 합이 15보다 큰 최소 조합을 입력창에 정확히 대십시오.</i>''', 'qtext': '<strong>Q16. [자연수 응용]</strong><br>연속하는 두 자연수의 합이 15보다 크다고 할 때, 이를 만족하는 가장 작은 두 자연수를 구하시오.', 'placeholder': '예: 8,9', 'error': '수치 조합 오류! 씨앗 공급 장치가 걸립니다.', 'ans_check': "ans === '8,9' || ans === '8과9'"},
    {'qnum': 17, "options": ["800X+1000<=6000", "800X+1000<=6000 아님", "알 수 없음", "해 없음"], 'title': '장미 꽃잎 제단', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "제단의 가중 밸런서를 흐트러뜨렸다. 한 송이 800원짜리 장미 x송이와 포장비 1000원을 더해 6000원 한도를 초과하지 않는 제단 예산 부등식을 완성해 봐라!"<br><br><i>장미꽃 제단의 황동 저울 밸브가 위험 수위로 가파르게 돌아갑니다. 정확한 한도 식을 입력창에 투사하십시오.</i>''', 'qtext': '<strong>Q17. [식 세우기]</strong><br>한 송이에 800원인 장미 $x$송이와 1000원짜리 포장을 하여 전체 비용을 6000원 이하로 하려고 한다. 부등식을 세우시오.', 'placeholder': '예: 800x+1000<=6000', 'error': '부등식 기호 불일치! 제단의 마법 빛이 사그라듭니다.', 'ans_check': "ans === '800X+1000<=6000' || ans === '800X+1000\\LE6000'"},
    {'qnum': 18, 'title': '장미의 최대 송이', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "식을 세웠다 한들, 한도 내에서 제단에 최대로 바칠 수 있는 장미 수량을 오차 없이 계수해 올리지 못하면 마법 제단이 무너지리라!"<br><br><i>부등식을 만족하는 장미의 실질적 최대 송이수를 다이얼 창에 입력해 예산 장벽을 여십시오.</i>''', 'qtext': '<strong>Q18. [최대값 구하기]</strong><br>Q17 조건에서 장미는 최대 몇 송이까지 살 수 있는가?', 'placeholder': '예: 6 또는 6송이', 'error': '꽃잎 수량 한계 초과! 저울이 균형을 잃습니다.', 'ans_check': "ans === '6' || ans === '6송이'"},
    {'qnum': 19, 'title': '동생의 저금 역전', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "시간이 갈수록 쌓여가는 형제의 저금 에너지 역전 공식이다! 동생이 형보다 부등식 상으로 자금이 많아지는 시점을 연산해 낼 수 있겠느냐!"<br><br><i>형 20000원(매월 2000원 저금), 동생 10000원(매월 3000원 저금) 조건의 역전 개월 상수를 계산하십시오!</i>''', 'qtext': '<strong>Q19. [실생활 활용]</strong><br>몇 개월 후부터 동생의 저금액이 형의 저금액보다 많아지는지 구하시오.', 'placeholder': '예: 11 또는 11개월', 'error': '연도 계산 오류! 이자가 바닥납니다.', 'ans_check': "ans === '11' || ans === '11개월' || ans === '11개월후'"},
    {'qnum': 20, 'title': '생명의 숲 최소 면적', 'story': '''🔮 <strong>[최종 탈출 요정 포탈 해제]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[실프-F]</span>: "조사관님! 이제 숲의 사막 바깥 지상으로 통하는 마지막 고대 포탈 게이트만 남았습니다! 제 마지막 정령 에너지를 기압 단자에 집중하겠습니다! 요정 숲의 활성화 최소 면적 초과 수치를 입력해 포탈 게이트를 여십시오! 이제 숲으로 돌아갈 시간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[다크-엘프]</span>: "안 돼... 내 최종 어둠의 결계가... 완전히 해제당해 정지한다아앗!"''', 'qtext': '<strong>Q20. [최종 면적 구하기]</strong><br>요정 숲의 남은 면적은 최소 얼마 초과인가?', 'placeholder': '숫자만 또는 초과 입력 (예: 30)', 'error': '정화 범위 미달! 숲 전체가 봉인 모드로 잠겨버립니다!', 'ans_check': "ans === '30' || ans === '30초과'", "extra_class": "glitch-bg"}
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
            <img src="assets/m2_03_inequalities/q{qnum}.png" alt="Background" class="panel-image">
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

print("app_m2_03_escape_room.html generated successfully.")
