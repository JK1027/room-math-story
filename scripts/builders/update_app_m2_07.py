import re
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
            --bg-main: #0f0a14;
            --glass-bg: rgba(25, 15, 35, 0.75);
            --glass-border: rgba(192, 192, 192, 0.25);
            --accent: #c0c0c0;
            --accent-hover: #ffffff;
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
            <h1>거울 나라의 축소 광선</h1>
            <h2>일차부등식의 해와 성질</h2>
            <img src="assets/m2_07_geometry2/intro.png" alt="Background" class="panel-image">
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
            <img src="assets/m2_07_geometry2/outro.png" alt="Ending" class="panel-image">
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
        "qtext": "<strong>Q1.</strong> 한 도형을 일정한 비율로 확대하거나 축소한 도형이 다른 도형과 합동이 될 때, 두 도형은 서로 ( ? )인 관계에 있다고 한다.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '닮음'"
    },
    {
        "qnum": 2,
        "title": "스테이지 2",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q2.</strong> 서로 닮은 두 평면도형에서 대응하는 선분의 길이의 비를 무엇이라 하는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '닮음비'"
    },
    {
        "qnum": 3,
        "title": "스테이지 3",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q3.</strong> 두 원은 항상 닮은 도형인가? ( O / X )",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'O'"
    },
    {
        "qnum": 4,
        "title": "스테이지 4",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q4.</strong> 닮음비가 2:3인 두 직사각형이 있다. 작은 직사각형의 가로가 4cm일 때, 큰 직사각형의 가로는 몇 cm인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '6cm'"
    },
    {
        "qnum": 5,
        "title": "스테이지 5",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q5.</strong> 모든 정사각형은 항상 서로 닮은 도형인가? ( O / X )",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'O'"
    },
    {
        "qnum": 6,
        "title": "스테이지 6",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q6.</strong> 삼각형의 세 쌍의 대응하는 변의 길이의 비가 같을 때의 닮음 조건을 쓰시오. (기호로)",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'SSS'"
    },
    {
        "qnum": 7,
        "title": "스테이지 7",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q7.</strong> 삼각형의 두 쌍의 대응하는 변의 길이의 비가 같고, 그 끼인각의 크기가 같을 때의 닮음 조건을 쓰시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'SAS'"
    },
    {
        "qnum": 8,
        "title": "스테이지 8",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q8.</strong> 삼각형의 두 쌍의 대응하는 각의 크기가 같을 때의 닮음 조건을 쓰시오.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'AA'"
    },
    {
        "qnum": 9,
        "title": "스테이지 9",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q9.</strong> 한 각이 60도인 두 정삼각형은 무조건 어떤 닮음 조건에 의해 닮음인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'AA닮음'"
    },
    {
        "qnum": 10,
        "title": "스테이지 10",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q10.</strong> 직각삼각형 내부에서 직각인 꼭짓점에서 빗변에 수선을 내렸을 때 만들어지는 두 개의 작은 직각삼각형은 서로 ( ? ) 관계이다.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '닮음'"
    },
    {
        "qnum": 11,
        "title": "스테이지 11",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q11.</strong> 삼각형 ABC에서 변 AB의 중점 M, 변 AC의 중점 N을 이은 선분 MN은 변 BC와 어떤 위치 관계에 있는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '평행'"
    },
    {
        "qnum": 12,
        "title": "스테이지 12",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q12.</strong> 위 Q11의 삼각형 중점 연결 정리에서 선분 MN의 길이는 선분 BC의 길이의 ( 몇 분의 몇 ) 인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '1/2'"
    },
    {
        "qnum": 13,
        "title": "스테이지 13",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q13.</strong> 삼각형의 한 변에 평행한 선분을 그어 다른 두 변과 만나게 하면, 새로 만들어진 작은 삼각형은 원래 삼각형과 ( ? ) 관계이다.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '닮음'"
    },
    {
        "qnum": 14,
        "title": "스테이지 14",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q14.</strong> 평행한 세 직선이 두 직선과 만날 때, 잘린 대응하는 선분의 길이의 비는 서로 ( 같다 / 다르다 ).",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '같다'"
    },
    {
        "qnum": 15,
        "title": "스테이지 15",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q15.</strong> 삼각형의 무게중심은 세 중선의 길이를 꼭짓점으로부터 각각 ( ? ) : ( ? ) 의 비율로 나눈다.",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '2'"
    },
    {
        "qnum": 16,
        "title": "스테이지 16",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q16.</strong> 두 평면도형의 닮음비가 $m:n$ 일 때, 넓이의 비는 얼마인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'm2'"
    },
    {
        "qnum": 17,
        "title": "스테이지 17",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q17.</strong> 두 정육면체의 닮음비가 1:2 일 때, 넓이(겉넓이)의 비는 얼마인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '1'"
    },
    {
        "qnum": 18,
        "title": "스테이지 18",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q18.</strong> 두 입체도형의 닮음비가 $m:n$ 일 때, 부피의 비는 얼마인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === 'm3'"
    },
    {
        "qnum": 19,
        "title": "스테이지 19",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q19.</strong> 닮음비가 1:3 인 두 구슬의 부피의 비는 얼마인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '1'"
    },
    {
        "qnum": 20,
        "title": "스테이지 20",
        "story": "단서를 찾아 문제를 해결하세요.",
        "qtext": "<strong>Q20.</strong> 작은 컵의 부피가 10mL이다. 닮음비가 2:3인 큰 컵이 있다면, 큰 컵의 부피를 구하기 위한 비례식을 세워보시오. (계산 불필요, 식만 작성)",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 다시 시도해보세요.",
        "ans_check": "ans === '8'"
    }
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
            <img src="assets/m2_07_geometry2/q{qnum}.png" alt="Background" class="panel-image">
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
                    <button class="btn btn-hint" onclick="alert('💡 힌트: {q['hint']}')" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>
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

print("app_m2_07_escape_room.html generated successfully.")
