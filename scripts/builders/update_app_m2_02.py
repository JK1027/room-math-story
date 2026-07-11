import re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m2_02_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>기계 도시 기어즈의 폭주: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #1e1a17;
            --glass-bg: rgba(40, 30, 25, 0.75);
            --glass-border: rgba(212, 118, 55, 0.25);
            --accent: #d47637;
            --accent-hover: #f28f4f;
            --text-main: #fdf8f4;
            --text-muted: #b09c91;
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
                radial-gradient(circle at 10% 20%, rgba(212, 118, 55, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 26, 0.08) 0%, transparent 40%);
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
            border-top: 1px solid rgba(212, 118, 55, 0.4);
            border-left: 1px solid rgba(212, 118, 55, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(212, 118, 55, 0.1), inset 0 0 20px rgba(212, 118, 55, 0.02);
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
            text-shadow: 0 0 30px rgba(212, 118, 55, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(212, 118, 55, 0.15);
            padding-bottom: 0.75rem;
        }

        .panel-image {
            width: 100%;
            height: 220px;
            object-fit: cover;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(212, 118, 55, 0.15);
        }

        .story-box {
            background: rgba(20, 15, 12, 0.5);
            border: 1px solid rgba(212, 118, 55, 0.15);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            position: relative;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .story-box:hover {
            background: rgba(20, 15, 12, 0.7);
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
            background: rgba(212, 118, 55, 0.05);
            border: 1px dashed rgba(212, 118, 55, 0.3);
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
            background: rgba(20, 15, 12, 0.8);
            border: 1px solid rgba(212, 118, 55, 0.3);
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
            box-shadow: 0 0 10px rgba(212, 118, 55, 0.3);
        }

        .btn-group {
            display: flex;
            justify-content: center;
        }

        .btn {
            background: linear-gradient(135deg, var(--accent) 0%, #a45320 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.85rem 2.5rem;
            font-size: 1.05rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(212, 118, 55, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(212, 118, 55, 0.5);
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
            background: rgba(20, 15, 12, 0.6);
            border: 1px solid rgba(212, 118, 55, 0.2);
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
            box-shadow: 0 0 10px rgba(212, 118, 55, 0.2);
        }

        /* Log Modal */
        .log-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10, 8, 7, 0.85);
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
            border-bottom: 1px solid rgba(212, 118, 55, 0.2);
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
            background: rgba(20, 15, 12, 0.4);
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
            <h1>기계 도시 기어즈의 폭주</h1>
            <h2>지수법칙과 다항식의 연산</h2>
            <img src="assets/m2_02_expressions/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">거대한 기계 도시 '기어즈'를 제어하는 중앙 메인프레임이 폭주하기 시작했습니다! 톱니바퀴들이 무질서하게 맞물려 도시 전체가 붕괴되기까지 남은 시간은 단 45분! 시스템을 안정화하려면 기계어의 기초인 지수법칙과 다항식 연산 20개를 완벽하게 계산해 코드를 덮어씌워야 합니다.</div>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 0)">시스템 복구 가동</button>
            </div>
        </div>

        {panels_placeholder}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>기계 도시 안정화 성공</h2>
            <img src="assets/m2_02_expressions/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text">입력한 코드가 마지막 톱니바퀴에 완벽하게 맞물려 돌아가며, 굉음을 내던 기계 도시 기어즈가 평온을 되찾습니다! 여러분은 지수법칙과 다항식의 계산으로 도시의 붕괴를 성공적으로 막아냈습니다!</div>
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
        "title": "동력 기어 복구",
        "story": "⚙️ <strong>[장치 동기화 시작]</strong><br><br>기어즈의 입구 기어들이 멈춰 섰습니다. 기본적인 지수 결합 수식을 해결하여 첫 번째 동력 기어를 물려주십시오.<br> $a^3 \\times a^4$ 를 지수를 사용하여 간단히 나타내십시오.",
        "qtext": "<strong>Q1. [지수의 곱셉]</strong><br>$a^3 \\times a^4$ 를 간단히 하시오.",
        "placeholder": "예: a^7",
        "error": "기어 치합 실패! 동력 결합음이 끊어집니다.",
        "ans_check": "ans === 'A^7' || ans === 'A**7'"
    },
    {
        "qnum": 2,
        "title": "제어 축 부스트",
        "story": "⚙️ <strong>[동력 증폭]</strong><br><br>기어가 회전하면서 지수 증폭이 일어납니다. $(x^2)^5$ 의 팽창 수치를 계산해 다음 동력 축으로 연결하십시오.",
        "qtext": "<strong>Q2. [지수의 거듭제곱]</strong><br>$(x^2)^5$ 를 간단히 하시오.",
        "placeholder": "예: x^10",
        "error": "축 토크 부족! 기어가 공전합니다.",
        "ans_check": "ans === 'X^10' || ans === 'X**10'"
    },
    {
        "qnum": 3,
        "title": "압력 밸브 배출",
        "story": "⚙️ <strong>[기압 조절]</strong><br><br>스팀 실린더 내부의 지수 압력을 낮춰야 합니다. $2^5 \\div 2^2$ 의 몫을 구하여 배출 밸브를 여십시오.",
        "qtext": "<strong>Q3. [지수의 나눗셈]</strong><br>$2^5 \\div 2^2$ 를 간단히 하시오.",
        "placeholder": "예: 2^3 또는 8",
        "error": "압력 임계치 돌파! 스팀이 누출됩니다!",
        "ans_check": "ans === '2^3' || ans === '2**3' || ans === '8'"
    },
    {
        "qnum": 4,
        "title": "다축 조인트 스케일",
        "story": "⚙️ <strong>[조인트 회전 반경]</strong><br><br>다축 조인트 기어의 크기가 곱의 거듭제곱 형태로 주어집니다. $(3a)^2$ 를 괄호를 풀어 완성하십시오.",
        "qtext": "<strong>Q4. [곱의 거듭제곱]</strong><br>$(3a)^2$ 를 간단히 하시오.",
        "placeholder": "예: 9a^2",
        "error": "조인트 크기 불일치! 톱니바퀴 마찰음이 발생합니다.",
        "ans_check": "ans === '9A^2' || ans === '9A**2'"
    },
    {
        "qnum": 5,
        "title": "기압 실린더 압축",
        "story": "⚙️ <strong>[최종 기압 균형]</strong><br><br>1구역의 마지막 동력 압축 기압 장치입니다. $\\left(\\frac{b}{a^2}\\right)^3$ 의 분수 기압 공식을 정밀하게 정리하십시오.",
        "qtext": "<strong>Q5. [분수의 거듭제곱]</strong><br>$\\left(\\frac{b}{a^2}\\right)^3$ 을 간단히 하시오.",
        "placeholder": "예: b^3/a^6",
        "error": "압축 밸브 기밀 누설! 압축이 중단됩니다.",
        "ans_check": "ans === 'B^3/A^6' || ans === 'B**3/A**6' || ans === '(B^3)/(A^6)'"
    },
    {
        "qnum": 6,
        "title": "단항 전선 연결",
        "story": "🔌 <strong>[단항식 전류 공급]</strong><br><br>2구역 단항식 회로망에 도달했습니다. 끊어진 도선 2개를 연결하기 위해 $3a^2$ 와 $4ab$ 의 결합 에너지를 계산하십시오.",
        "qtext": "<strong>Q6. [단항식의 곱셈]</strong><br>$3a^2 \\times 4ab$ 를 간단히 하시오.",
        "placeholder": "예: 12a^3b",
        "error": "스파크 발생! 전류 전송 효율이 급감합니다.",
        "ans_check": "ans === '12A^3B' || ans === '12A**3B' || ans === '12(A^3)B'"
    },
    {
        "qnum": 7,
        "title": "콘덴서 역방향 충전",
        "story": "🔌 <strong>[음전하 축전]</strong><br><br>음의 부호 전하를 가진 콘덴서 $(-2x^2y)^3$ 를 활성화하여 임시 배터리에 전하를 완충시켜 주십시오.",
        "qtext": "<strong>Q7. [음수 항의 거듭제곱]</strong><br>$(-2x^2y)^3$ 을 간단히 하시오.",
        "placeholder": "예: -8x^6y^3",
        "error": "콘덴서 과부하! 퓨즈가 끊어집니다.",
        "ans_check": "ans === '-8X^6Y^3' || ans === '-8X**6Y**3' || ans === '-8(X^6)(Y^3)'"
    },
    {
        "qnum": 8,
        "title": "신호 분배기 해제",
        "story": "🔌 <strong>[신호 분기 전압]</strong><br><br>단항 전류 전압 $12x^4y^2$ 를 $3x^2y$ 로 나눠 신호 분배 주파수를 획득하십시오.",
        "qtext": "<strong>Q8. [단항식의 나눗셈]</strong><br>$12x^4y^2 \\div 3x^2y$ 를 간단히 하시오.",
        "placeholder": "예: 4x^2y",
        "error": "신호 감쇄! 모니터 화면이 흐려집니다.",
        "ans_check": "ans === '4X^2Y' || ans === '4X**2Y' || ans === '4(X^2)Y'"
    },
    {
        "qnum": 9,
        "title": "역전류 필터 우회",
        "story": "🔌 <strong>[역전압 제거]</strong><br><br>전압이 분수 형태로 꺾인 역전류 필터 구역입니다. $8a^3b^2 \\div \\frac{2}{3}ab$ 의 필터 저항값을 계산해 전류를 우회시키십시오.",
        "qtext": "<strong>Q9. [분수 단항식 나눗셈]</strong><br>$8a^3b^2 \\div \\frac{2}{3}ab$ 를 간단히 하시오.",
        "placeholder": "예: 12a^2b",
        "error": "필터 막힘! 역전류가 역류합니다!",
        "ans_check": "ans === '12A^2B' || ans === '12A**2B'"
    },
    {
        "qnum": 10,
        "title": "메인 퓨즈 충방전",
        "story": "🔌 <strong>[안정화 최종 루프]</strong><br><br>2구역의 메인 퓨즈 전류 제어 수식입니다. $4x^2 \\times (-3xy) \\div 2x^2y$ 의 복합 연산을 처리해 메인 퓨즈를 봉인하십시오.",
        "qtext": "<strong>Q10. [단항식 곱셈과 나눗셈]</strong><br>$4x^2 \\times (-3xy) \\div 2x^2y$ 를 간단히 하시오.",
        "placeholder": "예: -6x",
        "error": "전원 차단! 회로망 전체가 암전됩니다.",
        "ans_check": "ans === '-6X'"
    },
    {
        "qnum": 11,
        "title": "다항 압력 밸브 합산",
        "story": "🏭 <strong>[제어 밸브 1단계]</strong><br><br>3구역 다항식 제어 장치로 진입했습니다. 분산된 압력 배관 $(2x + 3y)$ 와 $(4x - y)$ 를 결합하여 단일 관으로 정렬하십시오.",
        "qtext": "<strong>Q11. [다항식의 덧셈]</strong><br>$(2x + 3y) + (4x - y)$ 를 간단히 하시오.",
        "placeholder": "예: 6x+2y",
        "error": "밸브 누수! 기압 유실 경보가 울립니다.",
        "ans_check": "ans === '6X+2Y' || ans === '2Y+6X'"
    },
    {
        "qnum": 12,
        "title": "음압 실린더 차감",
        "story": "🏭 <strong>[제어 밸브 2단계]</strong><br><br>반대 방향 음압 실린더 배관 수식 $(5a - 2b) - (3a - 4b)$ 를 계산하여 음압 밸브의 압력을 조정하십시오. 부호 변화에 주의하십시오.",
        "qtext": "<strong>Q12. [다항식의 뺄셈]</strong><br>$(5a - 2b) - (3a - 4b)$ 를 간단히 하시오.",
        "placeholder": "예: 2a+2b",
        "error": "부호 오류! 실린더 피스톤이 급제동합니다.",
        "ans_check": "ans === '2A+2B' || ans === '2B+2A'"
    },
    {
        "qnum": 13,
        "title": "배율 실린더 동조",
        "story": "🏭 <strong>[배율 증폭 축]</strong><br><br>배율 기어에 의해 3배와 2배로 각각 커진 실린더 식 $3(x - 2y) + 2(2x + y)$ 의 합산 회전비를 도출하십시오.",
        "qtext": "<strong>Q13. [괄호가 있는 다항식 계산]</strong><br>$3(x - 2y) + 2(2x + y)$ 를 간단히 하시오.",
        "placeholder": "예: 7x-4y",
        "error": "증폭비 불일치! 기어 이가 맞지 않습니다.",
        "ans_check": "ans === '7X-4Y' || ans === '-4Y+7X'"
    },
    {
        "qnum": 14,
        "title": "다항식 분류 장치",
        "story": "🏭 <strong>[특성 포트 분류]</strong><br><br>문자와 차수가 같은 항들끼리만 모아 처리해야 포트 분류가 가능합니다. 이러한 특성을 가진 항을 한글 3글자로 무엇이라 합니까?",
        "qtext": "<strong>Q14. [다항식의 기초 용어]</strong><br>다항식의 덧셈에서 문자와 차수가 각각 같은 항을 무엇이라 하는가?",
        "placeholder": "한글 3글자 입력",
        "error": "분류 장치 걸림! 이물질 배출구가 작동합니다.",
        "ans_check": "ans === '동류항'"
    },
    {
        "qnum": 15,
        "title": "이차 압축 제어판",
        "story": "🏭 <strong>[이차 제어 장치 작동]</strong><br><br>이차 압축 시스템을 통과하려면 차수가 2인 다항식 연산 $(3x^2 - 2x + 1) + (-x^2 + 5x - 3)$ 을 올바르게 연산하십시오.",
        "qtext": "<strong>Q15. [이차식의 덧셈]</strong><br>$(3x^2 - 2x + 1) + (-x^2 + 5x - 3)$ 을 간단히 하시오.",
        "placeholder": "예: 2x^2+3x-2",
        "error": "이차 기어 마모 발생! 윤활유를 긴급 공급하십시오.",
        "ans_check": "ans === '2X^2+3X-2' || ans === '2X**2+3X-2' || ans === '-2+3X+2X^2'"
    },
    {
        "qnum": 16,
        "title": "메인보드 단다항 곱셈",
        "story": "🚨 <strong>[메인프레임 코어 1단계]</strong><br><br>4구역 메인보드 과부하 구역에 진입했습니다! 단항식과 다항식의 곱셉 결합 수식 $2x(3x - 4y)$ 의 과부하 계수를 분배 계산하여 주입하십시오.",
        "qtext": "<strong>Q16. [단항식과 다항식의 곱셈]</strong><br>$2x(3x - 4y)$ 를 간단히 하시오.",
        "placeholder": "예: 6x^2-8xy",
        "error": "코드 에러! 메인보드 발열이 시작됩니다.",
        "ans_check": "ans === '6X^2-8XY' || ans === '6X**2-8XY' || ans === '-8XY+6X^2'"
    },
    {
        "qnum": 17,
        "title": "신호 세기 분배 감쇠",
        "story": "🚨 <strong>[메인프레임 코어 2단계]</strong><br><br>다항식 전력을 단항식 포트로 나눈 $(6a^2b - 3ab^2) \\div 3ab$ 의 신호 세기를 계산해 전압 폭주를 막으십시오.",
        "qtext": "<strong>Q17. [다항식과 단항식의 나눗셈]</strong><br>$(6a^2b - 3ab^2) \\div 3ab$ 를 간단히 하시오.",
        "placeholder": "예: 2a-b",
        "error": "전압 과충전! 경고부저가 울립니다.",
        "ans_check": "ans === '2A-B' || ans === '-B+2A'"
    },
    {
        "qnum": 18,
        "title": "코어 분배 합성",
        "story": "🚨 <strong>[메인프레임 코어 3단계]</strong><br><br>전원 차단 수치 $-3x(2x - 5) + 4x^2$ 을 정밀하게 병합하여 중앙 해제 코드를 전송하십시오.",
        "qtext": "<strong>Q18. [분배법칙 복합 계산]</strong><br>$-3x(2x - 5) + 4x^2$ 을 간단히 하시오.",
        "placeholder": "예: -2x^2+15x",
        "error": "신호 전송 차단! 연결 유실 경고 발생.",
        "ans_check": "ans === '-2X^2+15X' || ans === '-2X**2+15X' || ans === '15X-2X^2'"
    },
    {
        "qnum": 19,
        "title": "음의 다항 신호 분기",
        "story": "🚨 <strong>[메인프레임 코어 4단계]</strong><br><br>코어 온도가 계속 올라갑니다! 음의 포트 전송 수식 $(4x^2y - 8xy^2) \\div (-2xy)$ 를 계산하여 긴급 냉각 밸브를 여십시오.",
        "qtext": "<strong>Q19. [음수로 나누는 다항식 나눗셈]</strong><br>$(4x^2y - 8xy^2) \\div (-2xy)$ 를 간단히 하시오.",
        "placeholder": "예: -2x+4y",
        "error": "냉각수 밸브 고착! 발열이 임계치를 위협합니다.",
        "ans_check": "ans === '-2X+4Y' || ans === '4Y-2X'"
    },
    {
        "qnum": 20,
        "title": "최종 제어 코드 입력",
        "story": "🚨 <strong>[안정화 마스터 키]</strong><br><br>마지막 순간입니다! 복합 연산식 $(15x^3 - 10x^2) \\div 5x^2 + 3(x - 2)$ 의 최종 통합 결과를 도출해 도시의 메인프레임을 구원하십시오.",
        "qtext": "<strong>Q20. [식의 계산 최종 복합형]</strong><br>$(15x^3 - 10x^2) \\div 5x^2 + 3(x - 2)$ 를 간단히 하시오.",
        "placeholder": "예: 6x-8",
        "error": "마스터 키 불일치! 기계도시 전체가 비상 셧다운 모드로 돌입합니다!",
        "ans_check": "ans === '6X-8' || ans === '-8+6X'"
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
            <img src="assets/m2_02_expressions/q{qnum}.png" alt="Background" class="panel-image">
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
                nextStage('panel_q{qnum}', {next_stage}, {progress});
            }} else {{
                showError('panel_q{qnum}', 'error{qnum}');
            }}
        }}
'''
    js_checks += check_fn

# Common JS functions boilerplate
js_boilerplate = """
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

print("app_m2_02_escape_room.html generated successfully.")
