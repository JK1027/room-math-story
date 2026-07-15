import re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m3_03_escape_room.html")
html_path = html_file

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>시간의 이차방정식 톱니바퀴 탑: 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #060f1e;
            --glass-bg: rgba(10, 20, 35, 0.75);
            --glass-border: rgba(37, 99, 243, 0.25);
            --accent: #2563eb;
            --accent-hover: #60a5fa;
            --text-main: #fbfbf3;
            --text-muted: #cbbba0;
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
                radial-gradient(circle at 10% 20%, rgba(37, 99, 235, 0.08) 0%, transparent 40%),
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
            border-top: 1px solid rgba(37, 99, 235, 0.4);
            border-left: 1px solid rgba(37, 99, 235, 0.4);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(37, 99, 235, 0.15), inset 0 0 20px rgba(37, 99, 235, 0.02);
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
            text-shadow: 0 0 30px rgba(37, 99, 235, 0.3);
            letter-spacing: 2px;
        }

        h2 {
            font-size: 1.4rem;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(37, 99, 235, 0.15);
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
            border: 1px solid rgba(37, 99, 235, 0.15);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            position: relative;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .story-box:hover {
            background: rgba(15, 23, 42, 0.7);
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
            background: rgba(37, 99, 235, 0.05);
            border: 1px dashed rgba(37, 99, 235, 0.3);
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
            border: 1px solid rgba(37, 99, 235, 0.3);
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
            box-shadow: 0 0 10px rgba(37, 99, 235, 0.3);
        }

        .btn-group {
            display: flex;
            justify-content: center;
        }

        .btn {
            background: linear-gradient(135deg, var(--accent) 0%, #1a2a3a 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.85rem 2.5rem;
            font-size: 1.05rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
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

        .progress-container {
            width: 100%;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(37, 99, 235, 0.2);
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
            box-shadow: 0 0 10px rgba(37, 99, 235, 0.3);
        }

        .info-panel {
            position: fixed;
            top: 20px;
            left: 20px;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            padding: 0.5rem 1rem;
            border-radius: 50px;
            z-index: 100;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .log-modal {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            display: none;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(5px);
        }
        
        .log-content {
            background: var(--bg-main);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            width: 90%;
            max-width: 500px;
            max-height: 70vh;
            padding: 2rem;
            overflow-y: auto;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .close-log {
            position: absolute;
            top: 15px; right: 15px;
            background: none; border: none; color: #fff;
            font-size: 1.2rem; cursor: pointer;
        }
        
        .log-list {
            margin-top: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .log-item {
            padding: 0.75rem;
            background: rgba(255,255,255,0.03);
            border-left: 3px solid var(--accent);
            font-size: 0.9rem;
            line-height: 1.5;
            border-radius: 4px;
        }
        
        .log-content h2 {
            border-bottom: 1px solid rgba(37, 99, 235, 0.2);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }

        @media (max-width: 600px) {
            .container { padding: 1rem; }
            .glass-panel { padding: 1.5rem; border-radius: 16px; }
            h1 { font-size: 1.8rem; }
            h2 { font-size: 1.1rem; }
            .story-text { font-size: 0.9rem; min-height: 140px; }
            .btn { width: 100%; }
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
</head>
<body>
    <button class="sound-ctrl" onclick="toggleMute()">
        <span id="soundIcon">🔊</span> <span id="soundText">Sound ON</span>
    </button>
    
    <div class="info-panel" id="infoPanel" style="display: none;">
        <span id="displayStudentId">학번: -</span>
        <span id="displayName">이름: -</span>
    </div>

    <div class="container">
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <!-- Intro Panel -->
        <div id="intro" class="glass-panel active">
            <h1>시간의 이차방정식 톱니바퀴 탑</h1>
            <h2>이차방정식</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_03/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [시계탑 태엽장치 크로노스-C]: "멈춰버린 거대한 '시간의 탑'의 제어실에 들어섰습니다. 탑의 거대한 톱니바퀴들은 '이차방정식'의 동력 에너지 수식 결계로 고정되어 움직이지 않습니다. 톱니바퀴들의 맞물림 관계와 회전 주기를 나타내는 이차방정식의 근들을 정확하게 찾아내어 제한시간 45분 내에 시계탑을 다시 가동시키고 시간의 봉인에서 탈출하십시오!"
            </div>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 0)">탈출 시도 개시</button>
            </div>
        </div>

        {{panels_placeholder}}

        <!-- Outro Panel -->
        <div id="outro" class="glass-panel">
            <h1>미션 완료!</h1>
            <h2>최종 봉인 탈출 성공</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_03/outro.png" alt="Ending" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                [시계탑 태엽장치 크로노스-C]: "째깍- 째깍-! 톱니바퀴들이 마침내 제자리를 찾아 회전하며 시간의 봉인이 풀립니다. 탑의 육중한 청동 문이 열리고 영광의 서광이 비추기 시작합니다. 시간의 지배자가 된 탑의 가동을 선포합니다!"
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

        function toggleMute() {
            isMuted = !isMuted;
            document.getElementById('soundIcon').innerText = isMuted ? "🔇" : "🔊";
            document.getElementById('soundText').innerText = isMuted ? "Sound OFF" : "Sound ON";
        }

        function playBeep(freq, type, duration) {
            if (isMuted) return;
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }

        function playSuccess() {
            playBeep(523.25, 'triangle', 0.15); // C5
            setTimeout(() => playBeep(659.25, 'triangle', 0.15), 100); // E5
            setTimeout(() => playBeep(783.99, 'triangle', 0.3), 200); // G5
        }

        function playFail() {
            playBeep(220.00, 'sawtooth', 0.25); // A3
        }

        function playClick() {
            playBeep(440.00, 'sine', 0.05); // A4
        }
    </script>

    <script>
        let studentId = "";
        let studentName = "";
        let recordRow = null;
        let wrongCount = 0;
        const UNIT_ID = "m3_03";

        function cleanString(str) {
            return str.replace(/\s+/g, '').toUpperCase();
        }

        function nextStage(currentId, nextId, progressPercent) {
            try { playClick(); } catch(e) {}
            
            // Record registration at the start of stage 1
            if (currentId === 'intro') {
                studentId = prompt("학번을 입력하세요 (예: 20101):");
                studentName = prompt("이름을 입력하세요:");
                if (!studentId || !studentName) {
                    alert("학번과 이름을 반드시 입력해야 진행할 수 있습니다.");
                    return;
                }
                
                document.getElementById('displayStudentId').innerText = "학번: " + studentId;
                document.getElementById('displayName').innerText = "이름: " + studentName;
                document.getElementById('infoPanel').style.display = "flex";
                document.getElementById('progressContainer').style.display = "block";
                
                try {
                    google.script.run
                        .withSuccessHandler(function(row) {
                            recordRow = row;
                        })
                        .recordStart(studentId, studentName, UNIT_ID);
                } catch (err) {
                    console.log("GAS Not Connected");
                }
            }

            const currentPanel = document.getElementById(currentId);
            const nextPanel = document.getElementById(nextId);

            currentPanel.classList.remove('active');
            setTimeout(() => {
                currentPanel.style.display = 'none';
                nextPanel.style.display = 'block';
                setTimeout(() => {
                    nextPanel.classList.add('active');
                    const storyBox = nextPanel.querySelector('.story-box');
                    if (storyBox) {
                        const textElement = storyBox.querySelector('.story-text');
                        if (textElement && !textElement.dataset.typed) {
                            typeWriterHTML(textElement, 25);
                            textElement.dataset.typed = "true";
                        }
                    }
                }, 50);
            }, 500);

            // Update Progress Bar
            document.getElementById('progressBar').style.width = progressPercent + '%';

            // Completion check at Outro
            if (nextId === 'outro') {
                try {
                    google.script.run.recordEnd(recordRow, UNIT_ID);
                } catch (err) {
                    console.log("GAS Not Connected");
                }
            }
        }

        function showError(panelId, errorId) {
            try { playFail(); } catch(e) {}
            const errorMsg = document.getElementById(errorId);
            errorMsg.style.display = 'block';
            
            const panel = document.getElementById(panelId);
            panel.style.transform = 'translateX(10px)';
            setTimeout(() => panel.style.transform = 'translateX(-10px)', 100);
            setTimeout(() => panel.style.transform = 'translateX(5px)', 200);
            setTimeout(() => panel.style.transform = 'translateX(-5px)', 300);
            setTimeout(() => panel.style.transform = 'translateX(0)', 400);

            setTimeout(() => {
                errorMsg.style.display = 'none';
            }, 3000);
        }

        function typeWriterHTML(element, speed) {
            const htmlContent = element.innerHTML.strip ? element.innerHTML.strip() : element.innerHTML;
            element.innerHTML = "";
            element.style.visibility = "visible";
            
            let progress = 0;
            let currentHTML = "";
            
            // Extract dialog speaker prefix
            const speakerMatch = htmlContent.match(/^(\[[^\]]+\]|【[^】]+】|[^:]+:)/);
            let speakerPrefix = "";
            let remainingHTML = htmlContent;
            
            if (speakerMatch) {
                speakerPrefix = speakerMatch[0];
                remainingHTML = htmlContent.slice(speakerPrefix.length);
                element.innerHTML = speakerPrefix;
            }

            const tokens = [];
            let i = 0;
            while (i < remainingHTML.length) {
                if (remainingHTML[i] === '<') {
                    let endIdx = remainingHTML.indexOf('>', i);
                    if (endIdx !== -1) {
                        tokens.push({ type: 'tag', content: remainingHTML.slice(i, endIdx + 1) });
                        i = endIdx + 1;
                        continue;
                    }
                }
                tokens.push({ type: 'text', content: remainingHTML[i] });
                i++;
            }

            function type() {
                if (progress < tokens.length) {
                    const token = tokens[progress];
                    if (token.type === 'tag') {
                        element.innerHTML += token.content;
                    } else {
                        element.innerHTML += token.content;
                    }
                    progress++;
                    setTimeout(type, speed);
                }
            }
            
            type();
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

        // Q1 Load setup
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
    {'qnum': 1, 'title': '스테이지 1', 'story': '[시간의-방랑자]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q1.</strong> 다음 보기 중 이차방정식인 것의 번호를 쓰시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === ''", 'hint': '주어진 등식을 모두 한 변(좌변)으로 이항하여 정리했을 때, (x에 대한 2차식) = 0 꼴이 되는 식을 찾게 합니다.'},
    {'qnum': 2, 'title': '스테이지 2', 'story': '[시간의-방랑자]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q2.</strong> 이차방정식 x² - 4 = 0 의 두 근을 구하시오. (± 기호를 사용하여 구하시오. 예: ±2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '±2' || ans === '+-2' || ans === '2,-2' || ans === '-2,2'", 'hint': '미지수의 제곱이 상수항과 같음을 이용해, 제곱근의 정의를 활용해 해를 구하도록 안내합니다.'},
    {'qnum': 3, 'title': '스테이지 3', 'story': '[시간의-방랑자]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q3.</strong> x=2 가 이차방정식 x² - ax + 6 = 0 의 한 근일 때, 상수 a의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '5'", 'hint': '이차방정식의 한 근이 주어지면, 그 근의 값을 방정식의 미지수 자리에 대입하여 성립함을 활용하게 지도합니다.'},
    {'qnum': 4, 'title': '스테이지 4', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[크로노스-C]: \\"치지직... 들리십니까...? 시간의-방랑자의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q4.</strong> 이차방정식 (x-3)(x+2) = 0 의 두 근을 구하시오. (작은 수부터 쉼표로 구분하여 적으시오. 예: -2, 3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '-2,3'", 'hint': '두 일차식의 곱이 0이 되기 위해서는 각각의 일차식이 0이 되어야 한다는 방정식을 세우게 합니다.'},
    {'qnum': 5, 'title': '스테이지 5', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[크로노스-C]: \\"치지직... 들리십니까...? 시간의-방랑자의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q5.</strong> 이차방정식 x² - 5x + 6 = 0 의 두 근을 구하시오. (작은 수부터 적으시오. 예: 2, 3)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2,3'", 'hint': '우변을 0으로 만든 뒤 좌변을 인수분해하여 두 일차식의 곱이 0이 되는 원리로 해를 구하게 유도합니다.'},
    {'qnum': 6, 'title': '스테이지 6', 'story': '[시간의-방랑자]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q6.</strong> 이차방정식 x² - 8x + 16 = 0 의 근을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '4'", 'hint': '좌변이 동일한 두 일차식의 곱(완전제곱식)으로 인수분해될 때 발생하는 중복된 근(중근)의 성질을 설명합니다.'},
    {'qnum': 7, 'title': '스테이지 7', 'story': '[시간의-방랑자]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q7.</strong> 이차방정식 x² + ax + 9 = 0 이 중근을 가질 때, 양수 a의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '6'", 'hint': '이차방정식이 중근을 가질 조건은 상수항이 1차항 계수의 반의 제곱과 같아야 한다는 공식을 적용하게 합니다.'},
    {'qnum': 8, 'title': '스테이지 8', 'story': '[시간의-방랑자]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q8.</strong> 이차방정식 (x-2)² = 5 의 근을 구하시오. (기호 ±와 루트를 사용하여 나타내시오. 예: 2±√5)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '±2√5' || ans === '+-2√5' || ans === '2√5,-2√5' || ans === '-2√5,2√5'", 'hint': '완전제곱식을 이용해 제곱근의 정의를 활용하여 미지수 값의 범위를 구하도록 지도합니다.'},
    {'qnum': 9, 'title': '스테이지 9', 'story': '[시간의-방랑자]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q9.</strong> 이차방정식 x² - 6x + 2 = 0 을 (x-p)² = q 꼴로 고칠 때, 두 상수 p, q에 대하여 p+q의 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '8'", 'hint': '상수항을 먼저 우변으로 이항한 후, 좌변을 완전제곱식으로 만들기 위해 양변에 필요한 상수를 더해주는 과정을 안내합니다.'},
    {'qnum': 10, 'title': '스테이지 10', 'story': '🚨 <strong>[비상 경보: 강제 자폭 시스템 작동]</strong> 🚨<br><br>[시간의-방랑자]: \\"더는 참을 수 없군! 모든 데이터를 자폭 폭파하겠다! 5분 내로 전부 잿더미로 만들어주지!\\"<br><br>[크로노스-C]: \\"경고! 시스템 온도 상승 중! 제가 방화벽을 전개할 동안 긴급 수치 입력을 끝내십시오!\\"', 'qtext': '<strong>Q10.</strong> 근의 공식을 사용하여 이차방정식 x² - 3x + 1 = 0 의 근을 구할 때, 분모에 들어갈 값을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2'", 'hint': '이차방정식의 근의 공식 분모 부분을 구하는 문제로, 분모는 x² 계수의 2배가 됨을 상기시킵니다.', "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '스테이지 11', 'story': '[크로노스-C]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q11.</strong> 이차방정식 x² - 4x - 1 = 0 의 근을 구하시오. (근의 공식을 활용하여 나타내시오. 예: 2±√5)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '±2√5' || ans === '+-2√5' || ans === '2√5,-2√5' || ans === '-2√5,2√5'", 'hint': '인수분해가 되지 않는 경우 근의 공식을 사용하여 해를 대입하여 계산하게 가이드합니다.'},
    {'qnum': 12, 'title': '스테이지 12', 'story': '[크로노스-C]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q12.</strong> 이차방정식 2x² + 5x - 3 = 0 의 두 근을 구하시오. (작은 수부터 적으시오. 분수는 슬래시로 표현하시오. 예: -3, 1/2)', 'placeholder': '수식 입력 (예: 1/2 또는 8:27=10:x)', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '-3,1/2'", 'hint': '대각선 곱셈 인수분해 기법을 활용해 좌변을 두 일차식의 곱으로 유도한 후 해를 구하게 합니다.'},
    {'qnum': 13, 'title': '스테이지 13', 'story': '[크로노스-C]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q13.</strong> 이차방정식 (x-1)(x-2) = 6 의 두 근을 구하시오. (작은 수부터 적으시오. 예: -1, 4)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '-1,4'", 'hint': '괄호 식을 먼저 모두 전개한 후 모든 항을 한 변으로 이항해 정리하여 이차방정식 기본 형태로 바꾸어 풀게 합니다.'},
    {'qnum': 14, 'title': '스테이지 14', 'story': '[크로노스-C]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q14.</strong> 두 근이 -2와 5 이고 x²의 계수가 1인 이차방정식을 구하시오. (예: x²-3x-10=0)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === 'X²-3X-10=0'", 'hint': '두 근이 주어졌을 때 이차방정식의 작성 공식인 (x-a)(x-b) = 0 을 이용하여 전개하도록 지도합니다.'},
    {'qnum': 15, 'title': '스테이지 15', 'story': '✨ <strong><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\"><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\"><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\">[조력자 시스템 권한 100% 완전 복구]</span></span></span></strong> ✨<br><br>[크로노스-C]: \\"연산 데이터 대조 성공! 이제 시스템 통제권을 제가 절반 확보했습니다. 가자, 복수의 시간입니다!\\"<br><br>[시간의-방랑자]: \\"크으으윽... 하찮은 인간 녀석들이 내 서버까지 잠식해 들어오다니!\\"', 'qtext': '<strong>Q15.</strong> 이차방정식 x² + 4x - 5 = 0 의 두 근 중 양수인 근을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '1'", 'hint': '방정식의 해를 구한 후 얻어진 근 중에서 조건에 부합하는 양수 값을 선택하게 안내합니다.', "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '스테이지 16', 'story': '[시간의-방랑자]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q16.</strong> 이차방정식 x² - 2x = 0 의 두 근을 구하시오. (작은 수부터 적으시오. 예: 0, 2)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '0,2'", 'hint': '상수항이 0인 경우, 공통인수 x를 묶어내어 간단히 인수분해하여 해를 구하게 유도합니다.'},
    {'qnum': 17, 'title': '스테이지 17', 'story': '[시간의-방랑자]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q17.</strong> 이차방정식 3x² - 7x + 2 = 0 의 두 근 중 정수인 근을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2'", 'hint': '인수분해를 통해 근을 도출하고, 그 중에서 정수 형태를 가진 근만 선별하도록 가이드합니다.'},
    {'qnum': 18, 'title': '스테이지 18', 'story': '[시간의-방랑자]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q18.</strong> 이차방정식 x² - 6x + 9 = 0 의 중근을 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '3'", 'hint': '좌변이 완전제곱식이 되어 한 개의 중근을 가지게 되는 식을 판별하게 유도합니다.'},
    {'qnum': 19, 'title': '스테이지 19', 'story': '[시간의-방랑자]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! 주어진 단서를 해결하여 방의 봉인을 해제하세요.\\"', 'qtext': '<strong>Q19.</strong> 연속하는 두 자연수의 곱이 56일 때, 두 자연수 중 큰 수를 구하시오.', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '8'", 'hint': '두 연속하는 자연수를 x와 x+1 로 두고 곱을 나타내는 방정식을 세워 이차방정식으로 해결하게 유도합니다.'},
    {'qnum': 20, 'title': '스테이지 20', 'story': '🔮 <strong>[최종 방화벽 락다운 해제]</strong> 🔮<br><br>[크로노스-C]: \\"제 모든 에너지를 출구 개방에 전념하겠습니다. 당신이라면 저 장벽을 해독해 낼 것입니다. 마지막 답을 입력하세요!\\"<br><br>[시간의-방랑자]: \\"안 돼... 내 제어권이... 소멸한다아아!\\"', 'qtext': '<strong>Q20.</strong> 지면에서 초속 30m로 똑바로 쏘아 올린 물체의 t초 후의 높이가 30t - 5t² (m)이다. 이 물체의 높이가 40m가 되는 시점은 몇 초 후인지 모두 구하시오. (오름차순으로 적으시오. 예: 2, 4)', 'placeholder': '정답 입력', 'error': '정답이 올바르지 않습니다. 다시 계산해보세요.', 'ans_check': "ans === '2,4'", 'hint': '높이 식과 목표 수치가 같다는 방정식을 세운 뒤 최고차항의 계수를 간단히 정리하여 해를 구하도록 안내합니다.', "extra_class": "glitch-bg"}
]

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
    
    # Year 3 unit 1 specific hints
    elif '제곱근' in qtext_clean: return "어떤 수 x를 제곱하여 a가 될 때, x를 a의 제곱근(±)이라고 부릅니다."
    elif '유리화' in qtext_clean: return "분모와 분자에 분모에 있는 루트 기호와 똑같은 무리수를 곱해서 분모를 유리수로 만들어 보세요."
    elif '무리수' in qtext_clean: return "순환하지 않는 무한소수를 찾으세요. 루트 기호가 완전히 안 벗겨지는 수가 무리수입니다."
    elif '삼각비' in qtext_clean or '사인' in qtext_clean or '코사인' in qtext_clean or '탄젠트' in qtext_clean: return "직각삼각형에서 대변과 빗변, 밑변 간의 삼각비 공식(sin, cos, tan)을 확인하세요."
    elif '이차방정식' in qtext_clean: return "방정식을 ax² + bx + c = 0 꼴로 정리한 후 인수분해하거나 근의 공식을 사용하세요."
    elif '이차함수' in qtext_clean: return "이차함수 y = a(x-p)² + q 꼴로 고치면 꼭짓점의 좌표가 (p, q)가 됨을 활용해 보세요."
    
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
            <h2>제 {qnum}구역: {title}</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m3_03/q{qnum}.png" alt="Background" class="panel-image">
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
                
                // Add current dialogue story to history log
                const currentStory = document.querySelector('#panel_q{qnum} .story-text').innerText;
                storyHistory.push("🔊 제 {qnum}구역: " + currentStory);
                
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
"""

final_html = base_html.replace("{{panels_placeholder}}", panels_html) + "\n<script>\n" + js_checks + "\n</script>"


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

print("app_m3_03_escape_room.html generated successfully.")
