import re
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
            <div class="btn-group">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 0)">내비게이션 제어 시작</button>
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
                [자율주행 관제 로봇 루트-R]: "정확히 10분을 입력하자 내비게이션이 정상 궤도를 회복했습니다! 택시가 절벽을 아슬아슬하게 피하며 네오 서울 중앙역에 부드럽게 멈춰 섭니다. 일차함수의 마법사 여러분, 무사 생환을 축하합니다!"
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
    {'qnum': 1, 'title': '시스템 함수 정의', 'story': '[시스템-에러]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 자율주행 택시의 제어 콘솔이 겨우 켜졌습니다. 시스템 복구의 첫 단계로, 독립 변수 $x$에 따른 종속 변수 $y$의 기본 연결 관계인 함수의 개념을 규정해야 합니다.\\"', 'qtext': '<strong>Q1.</strong> 두 변수 $x, y$ 에 대하여 $x$의 값이 정해짐에 따라 $y$의 값이 오직 하나씩 정해지는 관계가 있을 때, $y$를 $x$의 무엇이라 하는가?', 'placeholder': '두 글자 입력', 'error': '시스템 용어가 올바르지 않습니다. 두 글자 명사입니다.', 'ans_check': "ans === '함수'"},
    {'qnum': 2, 'title': '기본 궤적 연산', 'story': '[시스템-에러]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 기본 주행 함수 $f(x)=2x-3$이 활성화되었습니다. 입력 신호 $x=4$에 도달했을 때 출력 전압(함숫값)의 세기를 계산하여 장치를 구동시키세요.\\"', 'qtext': '<strong>Q2.</strong> 함수 $f(x) = 2x - 3$ 에서 $x=4$ 일 때의 함숫값 $f(4)$ 를 구하시오.', 'placeholder': '숫자만 입력', 'error': '연산 결과가 올바르지 않습니다. $2 \\times 4 - 3$을 다시 계산해보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 3, 'title': '속도 제어 밸브', 'story': '[시스템-에러]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 엔진의 안전 속도를 계산하는 시스템 함수 식을 점검합니다. 입력값이 2일 때 제어 장치의 밸브 값 $f(2)$를 정확하게 입력창에 전송하세요.\\"', 'qtext': '<strong>Q3.</strong> 함수 $f(x) = \\frac{10}{x}$ 에서 $f(2)$ 의 값을 구하시오.', 'placeholder': '숫자만 입력', 'error': '출력 전압이 맞지 않습니다. 10을 2로 나누어보세요.', 'ans_check': "ans === '5'"},
    {'qnum': 4, 'title': '일차함수 판별', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[루트-R]: \\"치지직... 들리십니까...? 시스템-에러의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q4.</strong> 다음 중 일차함수인 것은? (1) $y = \\frac{3}{x}$ (2) $y = x^2$ (3) $y = 3x - 1$ (4) $y = 5$', 'placeholder': '번호만 입력 (예: 3)', 'error': '오류 패킷입니다. $y = ax + b$ (단, $a \\neq 0$) 형태의 식을 찾으세요.', 'ans_check': "ans === '3' || ans === '(3)'"},
    {'qnum': 5, 'title': '궤적 평행이동', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[루트-R]: \\"치지직... 들리십니까...? 시스템-에러의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q5.</strong> 일차함수 $y = 4x$ 의 그래프를 $y$축의 방향으로 -2만큼 평행이동한 그래프의 식을 구하시오.', 'placeholder': '예: y = 4x - 2', 'error': '수식이 올바르지 않습니다. 평행이동한 만큼 상수항을 붙여 완성하세요.', 'ans_check': "ans.replace(/\\s+/g, '') === 'Y=4X-2'"},
    {'qnum': 6, 'title': '축 교점 분석', 'story': '[시스템-에러]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 택시 궤적이 모니터의 중심축인 $x$축과 정확히 만나는 지점을 계측해야 우회 도로에 안착합니다. 그래프가 $x$축과 만나는 교점의 $x$좌표를 일컫는 수학적 명칭을 찾아내세요.\\"', 'qtext': '<strong>Q6.</strong> 일차함수의 그래프가 $x$축과 만나는 점의 $x$좌표를 무엇이라 하는가?', 'placeholder': '세 글자 입력', 'error': '올바른 명칭이 아닙니다. x...?', 'ans_check': "ans === 'X절편' || ans === '엑스절편'"},
    {'qnum': 7, 'title': '출발지 복원 ($y$절편)', 'story': '[시스템-에러]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 택시의 이탈을 방지하기 위해 중심 회선($y$축)과 마주치는 원점 시작 높이를 구해야 합니다. 함수 $y=2x+6$의 $y$축 절편 값을 알아내세요.\\"', 'qtext': '<strong>Q7.</strong> 일차함수 $y = 2x + 6$ 의 $y$절편을 구하시오.', 'placeholder': '숫자만 입력', 'error': '절편 연산에 실패했습니다. $x=0$일 때의 $y$값을 구하세요.', 'ans_check': "ans === '6'"},
    {'qnum': 8, 'title': '제동 장벽 통과 ($x$절편)', 'story': '[시스템-에러]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 안전 제동 구역인 $x$축의 가로 교점을 알아내야 장벽 충돌을 막을 수 있습니다. 직선 $y=2x+6$의 $x$절편을 구하세요.\\"', 'qtext': '<strong>Q8.</strong> 일차함수 $y = 2x + 6$ 의 $x$절편을 구하시오.', 'placeholder': '음수는 마이너스 기호 포함 입력', 'error': '틀렸습니다. $y=0$일 때의 $x$값을 찾아보세요. ($2x+6=0$)', 'ans_check': "ans === '-3'"},
    {'qnum': 9, 'title': '회전 각도 정합', 'story': '[시스템-에러]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 반대편 선로에서 미끄러져 오는 궤적 $y=-\\frac{1}{2}x+4$의 차단 장치 도킹 좌표($x$절편)를 구하여 정면충돌 위험을 원천 제거하십시오.\\"', 'qtext': '<strong>Q9.</strong> 일차함수 $y = -\\frac{1}{2}x + 4$ 의 $x$절편을 구하시오.', 'placeholder': '숫자만 입력', 'error': '오류입니다. $-\\frac{1}{2}x + 4 = 0$이 되는 $x$값을 구하세요.', 'ans_check': "ans === '8'"},
    {'qnum': 10, 'title': '궤적 방정식 조립', 'story': '🚨 <strong>[비상 경보: 강제 자폭 시스템 작동]</strong> 🚨<br><br>[시스템-에러]: \\"더는 참을 수 없군! 모든 데이터를 자폭 폭파하겠다! 5분 내로 전부 잿더미로 만들어주지!\\"<br><br>[루트-R]: \\"경고! 시스템 온도 상승 중! 제가 방화벽을 전개할 동안 긴급 수치 입력을 끝내십시오!\\"', 'qtext': '<strong>Q10.</strong> $y$절편이 5이고 $x$절편이 -5인 일차함수의 식을 구하시오.', 'placeholder': '예: y = x + 5', 'error': '방정식이 잘못 조립되었습니다. 기울기와 $y$절편을 바탕으로 식을 완성하세요.', 'ans_check': "ans.replace(/\\s+/g, '') === 'Y=X+5'", "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '변화율 계산', 'story': '[루트-R]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 택시가 경사 진 직선 도로에 접어들며 비상 가속을 시작합니다. 시간 단위인 $x$가 1초 흘러갈 때 주행축 $y$는 얼마나 가속 변동하는지 가파른 변화율을 계측하세요.\\"', 'qtext': '<strong>Q11.</strong> 일차함수 $y = 3x - 2$ 에서 $x$의 값이 1만큼 증가할 때 $y$의 값은 얼마나 증가하는가?', 'placeholder': '숫자만 입력', 'error': '계측 오류입니다. 일차함수 $y=ax+b$에서 $x$의 계수가 의미하는 변화량을 찾아보세요.', 'ans_check': "ans === '3'"},
    {'qnum': 12, 'title': '기울기 심볼', 'story': '[루트-R]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 궤도선의 변화 각을 제어하기 위해 시스템 표준으로 설정된 \'기울기\' 매개변수를 수치화하는 공식 시스템 심볼(문자 기호)을 입력기에 타이핑하십시오.\\"', 'qtext': '<strong>Q12.</strong> 일차함수 $y = ax + b$ 에서 기울기를 나타내는 문자는 무엇인가?', 'placeholder': '알파벳 1글자 입력', 'error': '올바른 시스템 심볼이 아닙니다. $x$의 계수에 해당하는 변수 이름입니다.', 'ans_check': "ans === 'A'"},
    {'qnum': 13, 'title': '두 점 사이의 구배', 'story': '[루트-R]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 안전 주행 영역의 제1 포인트 $(1,3)$과 제2 포인트 $(3,7)$을 잇는 안전 벨트 궤도의 가파르기(기울기)를 도출해 내야 센서가 길을 잃지 않습니다.\\"', 'qtext': '<strong>Q13.</strong> 두 점 $(1, 3)$ 과 $(3, 7)$ 을 지나는 직선의 기울기를 구하시오.', 'placeholder': '숫자만 입력', 'error': '구배 연산에 실패했습니다. (y의 증가량) / (x의 증가량) 공식을 이용하세요.', 'ans_check': "ans === '2'"},
    {'qnum': 14, 'title': '경로 함수 합성', 'story': '[루트-R]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 점점 가속도가 꺾여 하강하는 기울기 -2와 정적 시작 오프셋 1을 지닌 긴급 조향용 경로 제어용 일차함수 수식을 합성하여 릴레이 보드에 입력하세요.\\"', 'qtext': '<strong>Q14.</strong> 기울기가 -2이고 $y$절편이 1인 일차함수의 식을 구하시오.', 'placeholder': '예: y = -2x + 1', 'error': '합성 식에 오류가 있습니다. 기울기와 $y$절편을 순서대로 식에 넣으세요.', 'ans_check': "ans.replace(/\\s+/g, '') === 'Y=-2X+1'"},
    {'qnum': 15, 'title': '조향 방향 결정', 'story': '✨ <strong><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\"><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\">[조력자 시스템 권한 100% 완전 복구]</span></span></strong> ✨<br><br>[루트-R]: \\"연산 데이터 대조 성공! 이제 시스템 통제권을 제가 절반 확보했습니다. 가자, 복수의 시간입니다!\\"<br><br>[시스템-에러]: \\"크으으윽... 하찮은 인간 녀석들이 내 서버까지 잠식해 들어오다니!\\"', 'qtext': '<strong>Q15.</strong> 일차함수 $y = -3x + 4$ 의 그래프는 오른쪽 ( 위 / 아래 ) 로 향하는 직선이다.', 'placeholder': '위 또는 아래 입력', 'error': '틀렸습니다. 기울기의 부호가 음수(-)일 때 직선이 향하는 방향을 생각해보세요.', 'ans_check': "ans === '아래'", "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '소모 패턴 식화', 'story': '[시스템-에러]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 자율주행 택시의 비상 예비 배터리 연료가 떨어지고 있습니다. 최초 20cm의 초고온 냉각 전지가 1시간에 2cm 비율로 감소할 때, 잔여량 $y$에 대한 시간 $x$의 식을 주입하세요.\\"', 'qtext': '<strong>Q16.</strong> 길이가 20cm인 양초에 불을 붙이면 1시간에 2cm씩 짧아진다. $x$시간 후의 양초의 길이를 $y$cm라 할 때, $y$를 $x$의 식으로 나타내시오.', 'placeholder': '예: y = 20 - 2x', 'error': '수식이 올바르지 않습니다. 처음 전지 길이에서 시간당 소모량을 차감하는 식을 세우세요.', 'ans_check': "ans.replace(/\\s+/g, '') === 'Y=20-2X' || ans.replace(/\\s+/g, '') === 'Y=-2X+20'"},
    {'qnum': 17, 'title': '완전 방전 시간', 'story': '[시스템-에러]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 냉각 연료 전지가 완전히 0(바닥)이 될 때까지 주행할 수 있는 한계 시간(안전 제한 시간)을 계측해 택시가 그전에 멈추도록 예비 방전 도달 시간을 설정하세요.\\"', 'qtext': '<strong>Q17.</strong> 위 Q16의 양초가 완전히 다 타서 없어지는 것은 불을 붙인 지 몇 시간 후인가?', 'placeholder': '예: 10시간', 'error': '틀렸습니다. 냉각 연료 봉의 잔여 길이인 $y$가 0이 되는 시간 $x$를 구하세요.', 'ans_check': "ans === '10' || ans === '10시간'"},
    {'qnum': 18, 'title': '음파 내비게이션 복구', 'story': '[시스템-에러]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 도시 터널을 지나기 위해 센서의 음속 보정 공식을 복원해야 합니다. 0도에서 초속 331m이고 기온 $x$가 1도씩 오를 때마다 속력 $y$가 0.6m/s씩 증가하는 보정 식을 제출하세요.\\"', 'qtext': '<strong>Q18.</strong> 온도계가 없는 방에서 소리의 속력은 초속 331m이고 기온이 1도 오를 때마다 초속 0.6m씩 증가한다. 기온이 $x$도일 때 소리의 속력 $y$를 식으로 나타내시오.', 'placeholder': '예: y = 0.6x + 331', 'error': '물리 보정 식이 바르지 않습니다. 기온에 따른 가산율을 계산 식에 포함하세요.', 'ans_check': "ans.replace(/\\s+/g, '') === 'Y=0.6X+331' || ans.replace(/\\s+/g, '') === 'Y=331+0.6X'"},
    {'qnum': 19, 'title': '최종 기온 속력 정합', 'story': '[시스템-에러]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 외부 기상 센서에 측정된 네오 서울 터널 안의 기온은 현재 15도입니다. 이 환경에서 음파 레이더 거리를 정확히 계산할 때의 전파 속력 값을 계산해 적용하세요.\\"', 'qtext': '<strong>Q19.</strong> 기온이 15도일 때, 소리의 속력을 구하시오.', 'placeholder': "단위 없이 숫자만 또는 '초속...m' 형태로 입력", 'error': '오차 기온 속력입니다. $331 + 0.6 \\times 15$를 연산해 보세요.', 'ans_check': "ans === '340' || ans === '340M/S' || ans === '초속340M'"},
    {'qnum': 20, 'title': '감속 냉각 시간', 'story': '🔮 <strong>[최종 방화벽 락다운 해제]</strong> 🔮<br><br>[루트-R]: \\"제 모든 에너지를 출구 개방에 전념하겠습니다. 당신이라면 저 장벽을 해독해 낼 것입니다. 마지막 답을 입력하세요!\\"<br><br>[시스템-에러]: \\"안 돼... 내 제어권이... 소멸한다아아!\\"', 'qtext': '<strong>Q20.</strong> 처음 물통에 50L의 물이 들어 있고 매분 3L씩 물을 빼낸다. 물이 20L가 남는 것은 몇 분 후인지 구하시오.', 'placeholder': "단위 없이 숫자만 또는 '10분' 형태로 입력", 'error': '브레이크 동작 실패! 유량 잔액 식 $50 - 3x = 20$을 만족하는 변수 값을 다시 구하십시오.', 'ans_check': "ans === '10' || ans === '10분'", "extra_class": "glitch-bg"}
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
