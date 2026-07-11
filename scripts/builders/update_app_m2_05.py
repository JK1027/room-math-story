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
            height: 220px;
            object-fit: cover;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(50, 205, 50, 0.15);
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
            <h2>일차부등식의 해와 성질</h2>
            <img src="assets/m2_05_functions/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">아름답던 요정 숲에 검은 마법의 안개가 드리워져, 숲의 에너지 균형이 깨졌습니다. 에너지가 한쪽으로 기울어지면 숲은 영원한 어둠에 갇히게 됩니다. 이 불균형을 바로잡을 수 있는 방법은 부등식의 원리를 이해하고 마법의 저울을 원래 상태로 복구하는 것뿐입니다. 20개의 부등식 문제를 풀어 숲을 구원하세요!</div>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 0)">숲의 저울 가동</button>
            </div>
        </div>

        {panels_placeholder}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>요정 숲의 균형 회복</h2>
            <img src="assets/m2_05_functions/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text">음수를 나눌 때 부등호의 방향이 바뀐다는 결정적 사실을 놓치지 않고 20개의 문제를 해결했습니다! 마법 저울이 다시 수평을 되찾고, 요정 숲에 따뜻한 빛이 스며듭니다. 숲의 균형을 되찾은 여러분께 요정들이 감사를 전합니다!</div>
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
    {
        "qnum": 1,
        "title": "스테이지 1",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q1.</strong> 두 변수 $x, y$ 에 대하여 $x$의 값이 정해짐에 따라 $y$의 값이 오직 하나씩 정해지는 관계가 있을 때, $y$를 $x$의 무엇이라 하는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '함수'"
    },
    {
        "qnum": 2,
        "title": "스테이지 2",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q2.</strong> 함수 $f(x) = 2x - 3$ 에서 $x=4$ 일 때의 함숫값 $f(4)$ 를 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '5'"
    },
    {
        "qnum": 3,
        "title": "스테이지 3",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q3.</strong> 함수 $f(x) = \frac{10}{x}$ 에서 $f(2)$ 의 값을 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '5'"
    },
    {
        "qnum": 4,
        "title": "스테이지 4",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q4.</strong> 다음 중 일차함수인 것은? (1) $y = \frac{3}{x}$ (2) $y = x^2$ (3) $y = 3x - 1$ (4) $y = 5$",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '3'"
    },
    {
        "qnum": 5,
        "title": "스테이지 5",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q5.</strong> 일차함수 $y = 4x$ 의 그래프를 $y$축의 방향으로 -2만큼 평행이동한 그래프의 식을 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'y'"
    },
    {
        "qnum": 6,
        "title": "스테이지 6",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q6.</strong> 일차함수의 그래프가 $x$축과 만나는 점의 $x$좌표를 무엇이라 하는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'x절편'"
    },
    {
        "qnum": 7,
        "title": "스테이지 7",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q7.</strong> 일차함수 $y = 2x + 6$ 의 $y$절편을 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '6'"
    },
    {
        "qnum": 8,
        "title": "스테이지 8",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q8.</strong> 일차함수 $y = 2x + 6$ 의 $x$절편을 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '-3'"
    },
    {
        "qnum": 9,
        "title": "스테이지 9",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q9.</strong> 일차함수 $y = -\frac{1}{2}x + 4$ 의 $x$절편을 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '8'"
    },
    {
        "qnum": 10,
        "title": "스테이지 10",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q10.</strong> $y$절편이 5이고 $x$절편이 -5인 일차함수의 식을 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'y'"
    },
    {
        "qnum": 11,
        "title": "스테이지 11",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q11.</strong> 일차함수 $y = 3x - 2$ 에서 $x$의 값이 1만큼 증가할 때 $y$의 값은 얼마나 증가하는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '3'"
    },
    {
        "qnum": 12,
        "title": "스테이지 12",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q12.</strong> 일차함수 $y = ax + b$ 에서 기울기를 나타내는 문자는 무엇인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'a'"
    },
    {
        "qnum": 13,
        "title": "스테이지 13",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q13.</strong> 두 점 $(1, 3)$ 과 $(3, 7)$ 을 지나는 직선의 기울기를 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '2'"
    },
    {
        "qnum": 14,
        "title": "스테이지 14",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q14.</strong> 기울기가 -2이고 $y$절편이 1인 일차함수의 식을 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'y'"
    },
    {
        "qnum": 15,
        "title": "스테이지 15",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q15.</strong> 일차함수 $y = -3x + 4$ 의 그래프는 오른쪽 ( 위 / 아래 ) 로 향하는 직선이다.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '아래'"
    },
    {
        "qnum": 16,
        "title": "스테이지 16",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q16.</strong> 길이가 20cm인 양초에 불을 붙이면 1시간에 2cm씩 짧아진다. $x$시간 후의 양초의 길이를 $y$cm라 할 때, $y$를 $x$의 식으로 나타내시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'y'"
    },
    {
        "qnum": 17,
        "title": "스테이지 17",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q17.</strong> 위 Q16의 양초가 완전히 다 타서 없어지는 것은 불을 붙인 지 몇 시간 후인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '10시간'"
    },
    {
        "qnum": 18,
        "title": "스테이지 18",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q18.</strong> 온도계가 없는 방에서 소리의 속력은 초속 331m이고 기온이 1도 오를 때마다 초속 0.6m씩 증가한다. 기온이 $x$도일 때 소리의 속력 $y$를 식으로 나타내시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'y'"
    },
    {
        "qnum": 19,
        "title": "스테이지 19",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q19.</strong> 기온이 15도일 때, 소리의 속력을 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '초속340m'"
    },
    {
        "qnum": 20,
        "title": "스테이지 20",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q20.</strong> 처음 물통에 50L의 물이 들어 있고 매분 3L씩 물을 빼낸다. 물이 20L가 남는 것은 몇 분 후인지 구하시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '10분'"
    }
]

# Generate Q panels
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
            <img src="assets/m2_05_functions/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
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
                    <button class="btn btn-hint" onclick="alert('💡 힌트: ' + document.getElementById('error{qnum}').innerText)" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>
            </div>
        </div>
'''
    panels_html += panel

# JS Answer Checks
js_checks = ""
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
                wrongCount++;
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
            try { playClick(); } catch(e) {}
            if(currentId === 'intro') {
                try {
                    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                } catch(e) {}
            }
            const currentEl = document.getElementById(currentId);
            const nextEl = document.getElementById(nextId);
            const progContainer = document.getElementById('progressContainer');
            const progBar = document.getElementById('progressBar');
            currentEl.classList.remove('active');
            setTimeout(() => {
                if(nextId !== 'intro') progContainer.style.display = 'block';
                progBar.style.width = progressPercent + '%';
                nextEl.classList.add('active');
                const storyBox = nextEl.querySelector('.story-box');
                if(storyBox) typeWriterHTML(storyBox, 25);
            }, 300);
        }
"""

# Compile the final code
final_html = base_html.replace('{panels_placeholder}', panels_html)

# Add checks and boilerplate inside final script tag
script_insert = js_boilerplate + js_checks + "\n"
final_html = final_html.replace('        window.onload = () => {', script_insert + '        window.onload = () => {')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("app_m2_05_escape_room.html generated successfully.")
