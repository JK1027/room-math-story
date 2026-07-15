import re
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
    {'qnum': 1, 'title': '마법 저울의 눈금', 'story': '[다크-엘프]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? ⚖️ <strong>[저울 작동 테스트]</strong><br><br>[숲의 정령 실프-F]: \\"숲을 구하기 위해 마법 저울의 해를 부등식으로 표기하여 가동해 주십시오.<br> \'x는 3보다 크거나 같다\'를 부등호로 나타내십시오.\\"\\"', 'qtext': '<strong>Q1. [부등식의 표시]</strong><br>$x$는 3보다 크거나 같다를 부등호로 나타내시오.', 'placeholder': '예: x>=3', 'error': '저울 측정 실패! 바늘이 격렬하게 흔들립니다.', 'ans_check': "ans === 'X>=3' || ans === 'X\\\\GE3'"},
    {'qnum': 2, 'title': '저울의 해 찾기', 'story': '[다크-엘프]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? ⚖️ <strong>[해의 판정]</strong><br><br>[숲의 정령 실프-F]: \\"저울 눈금판에 균형 해를 찾아 입력하십시오. 주어진 보기 중에서 $x=2$가 해인 부등식을 지목하십시오.\\"\\"', 'qtext': '<strong>Q2. [부등식의 해]</strong><br>다음 중 $x=2$가 해인 부등식은?<br>(1) $2x - 1 &lt; 0$<br>(2) $3x \\\\ge 6$<br>(3) $-x &gt; 0$', 'placeholder': '예: (2) 또는 2', 'error': '오답 입력! 저울이 한쪽으로 요동칩니다.', 'ans_check': "ans === '(2)' || ans === '2' || ans === '②'"},
    {'qnum': 3, 'title': '미만의 눈금 조율', 'story': '[다크-엘프]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? ⚖️ <strong>[경계값 분석]</strong><br><br>[숲의 정령 실프-F]: \\"안개가 다시 차오릅니다. \'x는 5 미만이다\'의 수학 기호를 저울에 기입하십시오.\\"\\"', 'qtext': '<strong>Q3. [미만의 정의]</strong><br>$x$는 5 미만이다를 부등호로 나타내시오.', 'placeholder': '예: x<5', 'error': '부등호 방향 오류! 기류가 흐트러집니다.', 'ans_check': "ans === 'X<5'"},
    {'qnum': 4, 'title': '자연수 해 결합', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[실프-F]: \\"치지직... 들리십니까...? 다크-엘프의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q4. [조건을 만족하는 해]</strong><br>부등식 $x + 2 &lt; 5$ 를 만족하는 자연수 $x$를 모두 구하시오.', 'placeholder': '예: 1,2', 'error': '조합 실패! 마법석이 어두워집니다.', 'ans_check': "ans === '1,2' || ans === '1,2개' || ans === '1과2'"},
    {'qnum': 5, 'title': '한계 질량 구하기', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[실프-F]: \\"치지직... 들리십니까...? 다크-엘프의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q5. [해의 최대값]</strong><br>부등식 $2x \\\\le 8$ 을 만족하는 가장 큰 정수를 구하시오.', 'placeholder': '예: 4', 'error': '질량 초과! 저울 리미터가 울립니다.', 'ans_check': "ans === '4' || ans === '4개'"},
    {'qnum': 6, 'title': '저울의 덧셈 성질', 'story': '[다크-엘프]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! ⚖️ <strong>[양변에 더하기]</strong><br><br>[숲의 정령 실프-F]: \\"2구역 저울의 성질 구역입니다. $a &lt; b$ 일 때, 양변에 똑같이 2를 더한 $a + 2$ 와 $b + 2$ 의 대소 관계를 입력하십시오.\\"\\"', 'qtext': '<strong>Q6. [부등식의 성질 1]</strong><br>$a &lt; b$ 일 때, $a + 2$ 와 $b + 2$ 의 대소를 비교하시오.', 'placeholder': '예: a+2<b+2', 'error': '평형 오류! 저울 받침대가 삐걱거립니다.', 'ans_check': "ans === 'A+2<B+2' || ans === 'B+2>A+2'"},
    {'qnum': 7, 'title': '저울의 곱셈 성질', 'story': '[다크-엘프]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! ⚖️ <strong>[양변에 양수 곱하기]</strong><br><br>[숲의 정령 실프-F]: \\"$a &lt; b$ 일 때, 양변에 똑같이 양수 3을 곱한 $3a$ 와 $3b$ 의 대소 관계를 저울에 설정하십시오.\\"\\"', 'qtext': '<strong>Q7. [부등식의 성질 2]</strong><br>$a &lt; b$ 일 때, $3a$ 와 $3b$ 의 대소를 비교하시오.', 'placeholder': '예: 3a<3b', 'error': '에너지 증폭 이상! 스파크가 튑니다.', 'ans_check': "ans === '3A<3B' || ans === '3B>3A'"},
    {'qnum': 8, 'title': '음수 곱셈의 반전', 'story': '[다크-엘프]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! ⚖️ <strong>[양변에 음수 곱하기]</strong><br><br>[숲의 정령 실프-F]: \\"주의하십시오! $a &lt; b$ 일 때, 양변에 똑같이 음수 -2를 곱한 $-2a$ 와 $-2b$ 의 대소 관계를 입력하십시오.\\"\\"', 'qtext': '<strong>Q8. [부등식의 성질 3]</strong><br>$a &lt; b$ 일 때, $-2a$ 와 $-2b$ 의 대소 관계를 부등호로 나타내시오.', 'placeholder': '예: -2a>-2b', 'error': '반전 에러! 저울이 균형을 완전히 잃고 기울어집니다.', 'ans_check': "ans === '-2A>-2B' || ans === '-2B<-2A'"},
    {'qnum': 9, 'title': '방향 반전 법칙', 'story': '[다크-엘프]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! ⚖️ <strong>[부등호 방향의 진실]</strong><br><br>[숲의 정령 실프-F]: \\"음수를 곱하거나 나눌 때 부등호의 방향은 어떻게 되는가? 단답으로 입력해 저울의 봉인을 푸십시오. (바뀐다 / 그대로다)\\"\\"', 'qtext': '<strong>Q9. [부등호의 핵심 법칙]</strong><br>음수를 곱하거나 나눌 때 부등호의 방향은 어떻게 되는가?', 'placeholder': '바뀐다 또는 그대로다 입력', 'error': '법칙 위반! 숲의 정령들이 길을 막습니다.', 'ans_check': "ans === '바뀐다' || ans === '변한다' || ans === '바뀜'"},
    {'qnum': 10, 'title': '음수 나눗셈의 완성', 'story': '🚨 <strong>[비상 경보: 강제 자폭 시스템 작동]</strong> 🚨<br><br>[다크-엘프]: \\"더는 참을 수 없군! 모든 데이터를 시스템을 포맷하겠다! 5분 내로 전부 초기화 시켜주지!\\"<br><br>[실프-F]: \\"경고! 시스템 온도 상승 중! 제가 방화벽을 전개할 동안 긴급 수치 입력을 끝내십시오!\\"', 'qtext': '<strong>Q10. [음수 나눗셈 연습]</strong><br>$-3x &gt; 9$ 양변을 -3으로 나누면 부등식은 어떻게 되는가?', 'placeholder': '예: x<-3', 'error': '부호 오류! 2구역 탈출 밸브가 차단됩니다.', 'ans_check': "ans === 'X<-3'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '마법진 1차 해제', 'story': '[실프-F]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! ⚖️ <strong>[일차부등식 풀이]</strong><br><br>[숲의 정령 실프-F]: \\"3구역 불균형 해소 마법진입니다. 일차부등식 $2x - 4 &gt; 0$ 의 해를 풀어 입력하십시오.\\"\\"', 'qtext': '<strong>Q11. [기초 부등식 풀이]</strong><br>일차부등식 $2x - 4 &gt; 0$ 의 해를 구하시오.', 'placeholder': '예: x>2', 'error': '마법 해제 실패! 마법진이 붉게 점멸합니다.', 'ans_check': "ans === 'X>2'"},
    {'qnum': 12, 'title': '마법진 2차 해제', 'story': '[실프-F]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! ⚖️ <strong>[이항과 음수 나눗셈]</strong><br><br>[숲의 정령 실프-F]: \\"이항을 이용하여 일차부등식 $3x + 1 \\\\le 7$ 의 해를 구하십시오. 차분하게 상수를 옮기십시오.\\"\\"', 'qtext': '<strong>Q12. [이항 계산]</strong><br>일차부등식 $3x + 1 \\\\le 7$ 의 해를 구하시오.', 'placeholder': '예: x<=2', 'error': '이항 연산 미스! 결합 에너지가 소멸됩니다.', 'ans_check': "ans === 'X<=2' || ans === 'X\\\\LE2'"},
    {'qnum': 13, 'title': '양변 이항 결합', 'story': '[실프-F]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! ⚖️ <strong>[양변의 미지수 정리]</strong><br><br>[숲의 정령 실프-F]: \\"미지수가 양변에 존재합니다. $5x - 2 &lt; 3x + 8$ 을 이항하여 깔끔한 부등식 해로 도출하십시오.\\"\\"', 'qtext': '<strong>Q13. [복합 이항]</strong><br>일차부등식 $5x - 2 &lt; 3x + 8$ 의 해를 구하시오.', 'placeholder': '예: x<5', 'error': '이항 부호 에러! 에너지 균형이 흐트러집니다.', 'ans_check': "ans === 'X<5'"},
    {'qnum': 14, 'title': '음수 계수 이항', 'story': '[실프-F]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! ⚖️ <strong>[음수 계수 처리]</strong><br><br>[숲의 정령 실프-F]: \\"중요한 고비입니다! 일차부등식 $-2x + 5 \\\\ge x - 4$ 의 해를 구하십시오. 마지막 나눗셈의 부등호 반전에 유의하십시오.\\"\\"', 'qtext': '<strong>Q14. [음수 계수 이항]</strong><br>일차부등식 $-2x + 5 \\\\ge x - 4$ 의 해를 구하시오.', 'placeholder': '예: x<=3', 'error': '반전 연산 실패! 마법진 온도가 급격히 올라갑니다.', 'ans_check': "ans === 'X<=3' || ans === 'X\\\\LE3'"},
    {'qnum': 15, 'title': '괄호 마법진 돌파', 'story': '✨ <strong><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\"><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\"><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\">[조력자 시스템 권한 100% 완전 복구]</span></span></span></strong> ✨<br><br>[실프-F]: \\"연산 데이터 대조 성공! 이제 시스템 통제권을 제가 절반 확보했습니다. 가자, 복수의 시간입니다!\\"<br><br>[다크-엘프]: \\"크으으윽... 하찮은 인간 녀석들이 내 서버까지 잠식해 들어오다니!\\"', 'qtext': '<strong>Q15. [괄호가 있는 부등식]</strong><br>일차부등식 $2(x - 1) &gt; 4$ 의 해를 구하시오.', 'placeholder': '예: x>3', 'error': '괄호 분배 오류! 마법진이 비상 셧다운 모드로 돌입합니다.', 'ans_check': "ans === 'X>3'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '연속하는 자연수 씨앗', 'story': '[다크-엘프]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! ⚖️ <strong>[자연수 씨앗 분배]</strong><br><br>[숲의 정령 실프-F]: \\"4구역 생명의 씨앗 분배 장치입니다. 연속하는 두 자연수의 합이 15보다 크다고 할 때, 이를 만족하는 가장 작은 두 자연수를 쉼표로 적으십시오.\\"\\"', 'qtext': '<strong>Q16. [자연수 응용]</strong><br>연속하는 두 자연수의 합이 15보다 크다고 할 때, 이를 만족하는 가장 작은 두 자연수를 구하시오.', 'placeholder': '예: 8,9', 'error': '수치 조합 오류! 씨앗 공급 장치가 걸립니다.', 'ans_check': "ans === '8,9' || ans === '8과9'"},
    {'qnum': 17, 'title': '장미 꽃잎 제단', 'story': '[다크-엘프]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! ⚖️ <strong>[제단 비용 부등식]</strong><br><br>[숲의 정령 실프-F]: \\"한 송이에 800원인 장미 $x$송이와 1000원짜리 포장을 하여 전체 비용을 6000원 이하로 맞추는 부등식을 세우십시오. (공백 없이 입력)\\"\\"', 'qtext': '<strong>Q17. [식 세우기]</strong><br>한 송이에 800원인 장미 $x$송이와 1000원짜리 포장을 하여 전체 비용을 6000원 이하로 하려고 한다. 부등식을 세우시오.', 'placeholder': '예: 800x+1000<=6000', 'error': '부등식 기호 불일치! 제단의 마법 빛이 사그라듭니다.', 'ans_check': "ans === '800X+1000<=6000' || ans === '800X+1000\\\\LE6000'"},
    {'qnum': 18, 'title': '장미의 최대 송이', 'story': '[다크-엘프]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! ⚖️ <strong>[최대 장미 수량]</strong><br><br>[숲의 정령 실프-F]: \\"이전 제단의 부등식을 바탕으로, 살 수 있는 장미의 최대 송이수를 계산해 제단 바구니에 입력하십시오.\\"\\"', 'qtext': '<strong>Q18. [최대값 구하기]</strong><br>Q17 조건에서 장미는 최대 몇 송이까지 살 수 있는가?', 'placeholder': '예: 6 또는 6송이', 'error': '꽃잎 수량 한계 초과! 저울이 균형을 잃습니다.', 'ans_check': "ans === '6' || ans === '6송이'"},
    {'qnum': 19, 'title': '동생의 저금 역전', 'story': '[다크-엘프]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! ⚖️ <strong>[저금 역전 시기]</strong><br><br>[숲의 정령 실프-F]: \\"형의 저금통에는 20000원, 동생은 10000원이 있습니다. 다음 달부터 매월 형은 2000원, 동생은 3000원씩 저금합니다. 동생이 형보다 많아지는 것은 몇 개월 후입니까?\\"\\"', 'qtext': '<strong>Q19. [실생활 활용]</strong><br>몇 개월 후부터 동생의 저금액이 형의 저금액보다 많아지는지 구하시오.', 'placeholder': '예: 11 또는 11개월', 'error': '연도 계산 오류! 이자가 바닥납니다.', 'ans_check': "ans === '11' || ans === '11개월' || ans === '11개월후'"},
    {'qnum': 20, 'title': '생명의 숲 최소 면적', 'story': '🔮 <strong>[최종 방화벽 락다운 해제]</strong> 🔮<br><br>[실프-F]: \\"제 모든 에너지를 출구 개방에 전념하겠습니다. 당신이라면 저 장벽을 해독해 낼 것입니다. 마지막 답을 입력하세요!\\"<br><br>[다크-엘프]: \\"안 돼... 내 제어권이... 정지한다아아!\\"', 'qtext': '<strong>Q20. [최종 면적 구하기]</strong><br>요정 숲의 남은 면적은 최소 얼마 초과인가?', 'placeholder': '숫자만 또는 초과 입력 (예: 30)', 'error': '정화 범위 미달! 숲 전체가 봉인 모드로 잠겨버립니다!', 'ans_check': "ans === '30' || ans === '30초과'", "extra_class": "glitch-bg"}
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
                    showError('panel_q{qnum}', 'error{qnum}');
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

        function showError(panelId, errorId) {
            try { playError(); } catch(e) {}
            const errEl = document.getElementById(errorId);
            if (errEl) {
                errEl.style.display = 'block';
                setTimeout(() => { errEl.style.display = 'none'; }, 3000);
            }
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
