import re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_05_escape_room.html")
base_dir = apps_dir
html_path = os.path.join(base_dir, html_file)

base_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>(중1) 방탈출 게임</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbit&family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;900&display=swap" rel="stylesheet">
    <style>
@keyframes shake{0%, 100%{transform:translate(0, 0) rotate(0deg);}10%{transform:translate(-2px, -1px) rotate(-0.5deg);}20%{transform:translate(-3px, 0px) rotate(1deg);}30%{transform:translate(0px, 2px) rotate(0deg);}40%{transform:translate(1px, -1px) rotate(1deg);}50%{transform:translate(-1px, 2px) rotate(-1deg);}60%{transform:translate(-3px, 1px) rotate(0deg);}70%{transform:translate(2px, 1px) rotate(-0.5deg);}80%{transform:translate(-1px, -1px) rotate(1deg);}90%{transform:translate(2px, 2px) rotate(0deg);}}.shake-effect{animation:shake 0.3s ease-in-out;}.laser-flash-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255, 0, 0, 0);pointer-events:none;z-index:9999;transition:background 0.15s ease-out;}.laser-flash-active{background:rgba(255, 0, 0, 0.15);transition:none;}:root{--bg-main:#201A15;--glass-bg:rgba(35, 28, 22, 0.75);--glass-border:rgba(205, 133, 63, 0.25);--accent:#CD853F;--accent-hover:#D2B48C;--text-main:#FDF5E6;--text-muted:#D3C2B0;}*{box-sizing:border-box;margin:0;padding:0;}body{font-family:'Noto Sans KR', sans-serif;background-color:var(--bg-main);color:var(--text-main);min-height:100vh;display:flex;justify-content:center;align-items:center;overflow-x:hidden;position:relative;}body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(circle at 20% 30%, rgba(205, 133, 63, 0.1) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(139, 92, 26, 0.12) 0%, transparent 40%);z-index:-2;}.container{width:100%;max-width:800px;padding:2rem;position:relative;z-index:10;}.glass-panel{background:var(--glass-bg);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid var(--glass-border);border-top:1px solid rgba(205, 133, 63, 0.4);border-left:1px solid rgba(205, 133, 63, 0.4);border-radius:24px;padding:3rem;box-shadow:0 0 40px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(205, 133, 63, 0.05);display:none;opacity:0;transform:translateY(20px);transition:all 0.5s cubic-bezier(0.4, 0, 0.2, 1);}.glass-panel.active{display:block;opacity:1;transform:translateY(0);}h1{font-family:'Orbit', sans-serif;font-size:2.5rem;font-weight:900;text-align:center;margin-bottom:0.5rem;background:linear-gradient(135deg, #FFF 30%, var(--accent) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:0 0 30px rgba(205, 133, 63, 0.3);letter-spacing:2px;}h2{font-size:1.4rem;color:var(--text-main);text-align:center;margin-bottom:2rem;font-weight:500;letter-spacing:1px;}.panel-image{width:100%;height:auto;max-height:250px;object-fit:cover;border-radius:8px;margin-bottom:1rem;}.story-box{position:relative;background:linear-gradient(90deg, rgba(60, 45, 30, 0.5) 0%, rgba(0,0,0,0.3) 100%);border-left:4px solid var(--accent);padding:0.8rem 1.2rem;margin-bottom:1.5rem;border-radius:0 12px 12px 0;box-shadow:0 4px 15px rgba(0,0,0,0.4);height:90px;max-height:90px;overflow:hidden;box-sizing:border-box;}.story-text{width:100%;height:100%;overflow:hidden;line-height:1.6;font-size:1.02rem;color:var(--text-main);text-align:justify;}.story-log-trigger{position:absolute;bottom:4px;right:8px;background:rgba(16, 185, 129, 0.25);border:1px solid rgba(16, 185, 129, 0.5);color:#34D399;padding:2px 6px;font-size:0.7rem;border-radius:4px;cursor:pointer;transition:all 0.2s;font-weight:bold;z-index:10;}.story-log-trigger:hover{background:rgba(16, 185, 129, 0.5);color:white;}.question-box{background:rgba(255, 255, 255, 0.02);border:1px solid rgba(255, 255, 255, 0.05);border-radius:16px;padding:1.5rem;margin-bottom:1.5rem;position:relative;box-shadow:inset 0 0 20px rgba(255, 255, 255, 0.02);}.question-box::before{content:'Q';position:absolute;font-family:'Share Tech Mono', monospace;font-size:4rem;color:rgba(205, 133, 63, 0.05);top:-10px;right:10px;font-weight:bold;pointer-events:none;}.question-content{font-size:1.15rem;line-height:1.8;margin-bottom:1rem;}.input-group{margin-top:1rem;}input[type="text"]{width:100%;padding:1rem 1.2rem;background:rgba(15, 23, 42, 0.8);border:1px solid rgba(205, 133, 63, 0.3);border-radius:12px;color:white;font-size:1.1rem;font-family:'Share Tech Mono', monospace, 'Noto Sans KR';transition:all 0.3s;box-shadow:inset 0 2px 4px rgba(0,0,0,0.5);}input[type="text"]:focus{outline:none;border-color:var(--accent);box-shadow:0 0 15px rgba(205, 133, 63, 0.4), inset 0 2px 4px rgba(0,0,0,0.5);}.error-msg{color:#EF4444;font-size:0.95rem;margin-top:0.5rem;display:none;text-align:center;font-weight:bold;text-shadow:0 0 10px rgba(239, 68, 68, 0.3);animation:shake 0.5s ease;}@keyframes shake{0%, 100%{transform:translateX(0);}20%, 60%{transform:translateX(-5px);}40%, 80%{transform:translateX(5px);}}.progress-container{width:100%;height:6px;background:rgba(255, 255, 255, 0.05);border-radius:3px;margin-bottom:2rem;overflow:hidden;display:none;border:1px solid rgba(255, 255, 255, 0.02);}.progress-bar{height:100%;width:0%;background:linear-gradient(90deg, #B45309, var(--accent));border-radius:3px;box-shadow:0 0 10px var(--accent);transition:width 0.8s cubic-bezier(0.4, 0, 0.2, 1);}.btn-group{display:flex;gap:1rem;margin-top:2rem;}.btn{background:linear-gradient(135deg, #B45309, #78350F);color:white;border:1px solid #D97706;padding:0.6rem 1.5rem;font-size:1.1rem;font-weight:900;border-radius:8px;cursor:pointer;transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);text-transform:uppercase;letter-spacing:3px;width:100%;box-shadow:0 10px 25px rgba(120, 53, 15, 0.5), inset 0 2px 5px rgba(255,255,255,0.3);text-shadow:0 2px 4px rgba(0,0,0,0.5);position:relative;overflow:hidden;}.btn::after{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);transition:all 0.6s;}.btn:hover::after{left:100%;}.btn:hover{transform:translateY(-2px);box-shadow:0 15px 30px rgba(205, 133, 63, 0.5), inset 0 2px 5px rgba(255,255,255,0.5);border-color:#F59E0B;}.btn-hint{display:inline-block;background:rgba(16, 185, 129, 0.2);border:1px solid rgba(16, 185, 129, 0.5);color:#34D399;padding:4px 10px;font-size:0.85rem;font-weight:700;border-radius:6px;cursor:pointer;transition:all 0.2s ease;vertical-align:middle;margin-left:10px;letter-spacing:0.5px;text-transform:none;box-shadow:0 2px 5px rgba(0, 0, 0, 0.2);}.btn-hint:hover{background:rgba(16, 185, 129, 0.4);color:#fff;box-shadow:0 0 10px rgba(52, 211, 153, 0.4);}.btn:active{transform:translateY(1px);}.sound-toggle{position:fixed;top:20px;right:20px;background:rgba(35, 28, 22, 0.6);border:1px solid var(--glass-border);padding:8px 16px;border-radius:20px;color:white;cursor:pointer;z-index:100;backdrop-filter:blur(10px);font-size:0.9rem;transition:all 0.3s;font-weight:bold;}.sound-toggle:hover{background:var(--accent);border-color:white;box-shadow:0 0 15px var(--accent);}@keyframes blink{0%, 100%{opacity:1;}50%{opacity:0;}}@media (max-width:600px){body{overflow-y:auto;}.container{padding:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;box-sizing:border-box;min-height:100vh;}.glass-panel{width:100%;max-height:94vh;max-height:94dvh;height:auto;padding:1.2rem;border-radius:16px;box-sizing:border-box;display:none;flex-direction:column;justify-content:flex-start;overflow-y:auto;}.glass-panel.active{display:flex;}.story-box{padding:0.6rem 1rem;margin-bottom:0.5rem;height:80px;max-height:80px;overflow:hidden;flex:0 0 auto;}.story-text{font-size:0.85rem;line-height:1.5;}h1{font-size:1.6rem;letter-spacing:1px;}h2{font-size:1rem;margin-bottom:1rem;}.panel-image{max-height:180px;margin-bottom:1rem;}.question-box{padding:0.8rem;margin-bottom:1rem;}.question-box::before{font-size:3rem;top:-5px;right:-5px;}input[type="text"]{font-size:1rem;padding:0.8rem;}.btn{font-size:0.9rem;padding:0.5rem;letter-spacing:1px;border-radius:6px;}.btn-group{flex-direction:column;gap:0.6rem;}.sound-toggle{top:10px;right:10px;font-size:0.8rem;padding:6px 12px;}}.log-modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0, 0, 0, 0.85);z-index:1000;justify-content:center;align-items:center;backdrop-filter:blur(10px);}.log-content{background:#231B15;border:2px solid var(--accent);border-radius:20px;width:90%;max-width:600px;max-height:80vh;padding:2rem;position:relative;display:flex;flex-direction:column;}.log-content h2{font-family:'Orbit', sans-serif;color:var(--accent);margin-bottom:1rem;text-align:left;}#logContainer{overflow-y:auto;flex-grow:1;margin-bottom:1.5rem;padding-right:10px;font-size:0.95rem;line-height:1.8;color:#cbd5e1;}#logContainer strong{color:var(--accent);}.close-log{position:absolute;top:15px;right:15px;background:transparent;border:none;color:#ef4444;font-size:1.5rem;cursor:pointer;transition:scale 0.2s;}.close-log:hover{scale:1.2;}
</style>
</head>
<body>
    <div class="laser-flash-overlay" id="laserFlash"></div>


    <button id="soundToggle" class="sound-toggle" onclick="toggleSound()">🔊 소리 켜짐</button>

    <div class="container">
        
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <!-- 0. 인트로 -->
        <div id="intro" class="glass-panel active">
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_05_basic_geometry/intro.png" alt="Background" class="panel-image">
            <h1>다빈치의 비밀 작업실</h1>
            <h2>르네상스 기하학의 수수께끼</h2>
            <div class="story-box">
                <div class="story-text">
                    르네상스 시대의 천재, 레오나르도 다빈치의 숨겨진 비밀 작업실에 도달했습니다.<br><br>
                    하지만 이 작업실은 침입자를 막기 위해 복잡한 기하학적 장치들로 굳게 봉인되어 있습니다.<br><br>
                    설계도의 점, 선, 각도, 그리고 삼각형의 비밀을 풀어 20개의 수수께끼 결계를 해결하고 걸작을 공개하세요!
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            
            <div class="info-box" style="background: rgba(220, 38, 38, 0.2); border-left: 4px solid #ef4444; padding: 0.8rem 1.2rem; margin-bottom: 1.5rem; border-radius: 0 12px 12px 0; color: #f87171; font-size: 0.95rem; line-height: 1.6;">
                ⚠️ <b>주의사항</b><br>
                문제는 총 20문제이며, 한 문제에서 3번 틀릴 경우 해당 구역의 처음으로 되돌아갑니다. 신중하게 도전하세요!
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
                <button class="btn" onclick="tryStartGame('m1_05')">수수께끼 해독 가동</button>
            </div>
        </div>

        <!-- Q1 -->

    </div>

    <!-- Audio Elements -->
    <audio id="bgm" loop>
        <source src="https://assets.mixkit.co/music/preview/mixkit-space-ambient-tension-905.mp3" type="audio/mp3">
    </audio>
    <audio id="sndClick">
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-mechanical-switch-key-2980.wav" type="audio/wav">
    </audio>
    <audio id="sndTick">
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-mechanical-keyboard-clicks-2266.wav" type="audio/wav">
    </audio>
    <audio id="sndSuccess">
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-digital-quick-bypass-2255.wav" type="audio/wav">
    </audio>
    <audio id="sndError">
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-ambient-dark-error-sound-2985.wav" type="audio/wav">
    </audio>
    <audio id="sndVictory">
        <source src="https://assets.mixkit.co/music/preview/mixkit-uplifting-creative-technology-groove-911.mp3" type="audio/mp3">
    </audio>

    <script>
        function tryStartGame(unitId) {
            const sid = document.getElementById('studentId');
            const sname = document.getElementById('studentName');
            if(sid && sname) {
                if(!sid.value.trim() || !sname.value.trim()) {
                    alert('학번과 이름을 모두 입력해주세요!');
                    return;
                }
                // GAS 로직
                try {
                    if(typeof google !== 'undefined' && google.script && google.script.run) {
                        google.script.run
                            .withSuccessHandler(function(row) { window.userRecordRow = row; })
                            .recordStart(sid.value.trim(), sname.value.trim(), unitId);
                    }
                } catch(e) { console.warn('GAS 연동 안됨:', e); }
            }
            
            // 브라우저 오디오 엔진 시작 (외부 링크 의존 없음)
            try {
                if (!isMuted) {
                    initAudio();
                    startBGM();
                }
            } catch(e) {}
            
            nextStage('intro', 'panel_q1', 5);
        }

        

        

        

        

        

        


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

        let isMuted = false;
        let audioCtx = null;
        let bgmOsc = null;
        let bgmGain = null;
        let bgmLfo = null;

        function initAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function playSynth(freq, type, duration, vol) {
            if (isMuted) return;
            try {
                initAudio();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(vol, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration);
            } catch(e){}
        }

        function stopBGM() {
            try {
                if(bgmOsc) { bgmOsc.stop(); bgmOsc.disconnect(); bgmOsc = null; }
                if(bgmLfo) { bgmLfo.stop(); bgmLfo.disconnect(); bgmLfo = null; }
            } catch(e){}
        }

        function startBGM() {
            if (isMuted) return;
            try {
                initAudio();
                if(bgmOsc) return;
                bgmOsc = audioCtx.createOscillator();
                bgmGain = audioCtx.createGain();
                bgmOsc.type = 'triangle';
                bgmOsc.frequency.setValueAtTime(55.00, audioCtx.currentTime);
                bgmGain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                bgmOsc.connect(bgmGain);
                bgmGain.connect(audioCtx.destination);
                bgmOsc.start();
                
                bgmLfo = audioCtx.createOscillator();
                bgmLfo.type = 'sine';
                bgmLfo.frequency.setValueAtTime(0.15, audioCtx.currentTime); 
                const lfoGain = audioCtx.createGain();
                lfoGain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                bgmLfo.connect(lfoGain);
                lfoGain.connect(bgmGain.gain);
                bgmLfo.start();
            } catch(e) {}
        }

        function toggleSound() {
            isMuted = !isMuted;
            const btn = document.getElementById('soundToggle');
            if (isMuted) {
                if(btn) btn.innerText = '🔇 소리 꺼짐';
                stopBGM();
            } else {
                if(btn) btn.innerText = '🔊 소리 켜짐';
                startBGM();
            }
        }

        function playClick() { playSynth(800, 'sine', 0.1, 0.5); }
        function playTick() { playSynth(1500, 'square', 0.04, 0.15); }
        function playSuccess() { 
            playSynth(523.25, 'sine', 0.15, 0.7); 
            setTimeout(()=>playSynth(659.25, 'sine', 0.15, 0.7), 150); 
            setTimeout(()=>playSynth(783.99, 'sine', 0.3, 0.7), 300); 
        }
        function playError() {
            playSynth(150, 'sawtooth', 0.3, 0.6);
            setTimeout(()=>playSynth(100, 'sawtooth', 0.4, 0.6), 200);
        }
        function playVictory() {
            stopBGM();
            [523.25, 659.25, 783.99, 1046.50].forEach((f, i) => {
                setTimeout(()=>playSynth(f, 'square', 0.2, 0.6), i*150);
            });
        }

        let wrongCount = 0;
function cleanString(str) {
            return str.replace(/\\s+/g, '').toLowerCase();
        }

        // 엔터키 정답 제출 바인딩
        document.addEventListener('keydown', function(e) {
            if (e.target && e.target.id.startsWith('ans') && e.key === 'Enter') {
                const qnum = e.target.id.replace('ans', '');
                const activePanel = e.target.closest('.glass-panel');
                if (activePanel) {
                    const btn = activePanel.querySelector('.btn-group .btn');
                    if (btn) btn.click();
                }
            }
        });


        window.addEventListener('DOMContentLoaded', () => {
            const audios = [
                document.getElementById('bgm'),
                document.getElementById('sndClick'),
                document.getElementById('sndTick'),
                document.getElementById('sndSuccess'),
                document.getElementById('sndError'),
                document.getElementById('sndVictory')
            ];
            audios.forEach(audio => {
                if (audio) {
                    audio.addEventListener('error', (e) => {
                        console.warn(`사운드 리소스 로드 실패: ${audio.id}`);
                    });
                }
            });
        });

        
        function triggerLockdownAlert() {
    
            const flash = document.getElementById('laserFlash');
            if (flash) {
                flash.classList.add('laser-flash-active');
                setTimeout(() => {
                    flash.classList.remove('laser-flash-active');
                }, 150);
            }
            
    
            const activePanel = document.querySelector('.glass-panel.active');
            if (activePanel) {
                activePanel.classList.add('shake-effect');
                setTimeout(() => {
                    activePanel.classList.remove('shake-effect');
                }, 300);
            }
        }

function showError(panelId, errorId, currentWrongCount) {
            triggerLockdownAlert();

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

        let storyHistory = [];
        function openLog() {
            try { playClick(); } catch(e) {}
            const modal = document.getElementById('storyLogModal');
            const container = document.getElementById('logContainer');
            if (storyHistory.length === 0) {
                container.innerHTML = "기록이 존재하지 않습니다.";
            } else {
                container.innerHTML = storyHistory.join("<br><br>");
            }
            modal.style.display = 'flex';
        }
        function closeLog() {
            try { playClick(); } catch(e) {}
            document.getElementById('storyLogModal').style.display = 'none';
        }

        let typeWriterTimeout;
        
        function splitSentences(text) {
            let result = [];
            let start = 0;
            for (let i = 0; i < text.length; i++) {
                const char = text.charAt(i);
                if (char === '.' || char === '!' || char === '?') {
                    const nextChar = text.charAt(i + 1);
                    if (!nextChar || nextChar === ' ' || nextChar === '\\n' || nextChar === '<') {
                        result.push(text.substring(start, i + 1).trim());
                        start = i + 1;
                    }
                }
            }
            const finalChunk = text.substring(start).trim();
            if (finalChunk) {
                result.push(finalChunk);
            }
            return result;
        }

        function typeWriterHTML(element, speed = 25, onComplete = null) {
            let isComplete = false;
            let currentChunkIndex = 0;
            let chunks = [];
            const textEl = element.querySelector('.story-text');
            if(!textEl) {
                if(onComplete) onComplete();
                return;
            }

            function triggerComplete() {
                if(!isComplete) {
                    isComplete = true;
                    element.style.cursor = 'default';
                    if(onComplete) onComplete();
                }
            }
            if (typeWriterTimeout) clearTimeout(typeWriterTimeout);
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
            let typingFinished = false;
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
                    if(currentChunkIndex === chunks.length - 1) triggerComplete();
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
            <h2>📜 지나온 기하학 기록</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>

</body>
</html>
"""

qs = [
    {
        "qnum": 1,
        "title": "코덱스-L의 위협",
        "story": "[코덱스-L]: \"어리석은 침입자여! 난 다빈치 님께서 설계하신 기계 비서 코덱스-L이다. 보안 트랩이 기동되어 작업실이 폐쇄된다! 묘실이 완전히 잠기기 전에 기하학 기초 요소 점, 선, 그리고 마지막을 입력해 능력을 증명해라!\"",
        "qtext": "<strong>Q1.</strong> 도형을 구성하는 가장 기본이 되는 요소 세 가지는 점, 선, 그리고 무엇인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 점이 모여 선이 되고, 선이 모여 이것이 됩니다.",
        "ans_check": "ans === '면'"
    },
    {
        "qnum": 2,
        "title": "궤적의 고유성",
        "story": "[코덱스-L]: \"호오, 기본은 아는군. 그럼 서로 다른 두 개의 고정 핀 A, B를 일직선으로 잇는 로프(직선)는 오직 몇 개만 설치할 수 있는지 말해봐라!\"",
        "qtext": "<strong>Q2.</strong> 서로 다른 두 점 A, B를 지나는 직선은 모두 몇 개인가?",
        "placeholder": "예: 1개",
        "error": "틀렸습니다. 두 점을 동시에 관통하는 직선은 세상에 오직 하나뿐입니다.",
        "ans_check": "ans === '1' || ans === '1개'"
    },
    {
        "qnum": 3,
        "title": "레이저 방향 지정",
        "story": "[코덱스-L]: \"점 A에서 시작해서 점 B 방향으로 곧장 발사되어 끝없이 뻗어 나가는 파괴 레이저(선)를 기하학 용어로 무엇이라 부르는가?\"",
        "qtext": "<strong>Q3.</strong> 점 A에서 시작하여 점 B 방향으로 끝없이 뻗어 나가는 선분을 기호로 나타낼 때, 이를 무엇이라 부르는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 한쪽으로만 끝없이 뻗어 나가는 직선의 절반입니다.",
        "ans_check": "ans.includes('반직선')"
    },
    {
        "qnum": 4,
        "title": "수평의 바닥",
        "story": "[코덱스-L]: \"바닥이 완전히 평평하게 펼쳐져 180도 일직선을 이루는 이 성스러운 각도의 이름을 대라. 머리가 굳었다면 힌트 단추를 눌러보든가!\"",
        "qtext": "<strong>Q4.</strong> 180도인 각을 무엇이라 부르는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 평평한 각을 뜻하는 명칭입니다.",
        "ans_check": "ans === '평각'"
    },
    {
        "qnum": 5,
        "title": "경보 태엽의 각도",
        "story": "[코덱스-L]: \"시계 기어의 시침과 분침이 4시 정각을 가리키며 톱니 락이 걸렸다. 두 침 사이의 좁은 쪽 각도를 연산하여 기어 압력을 해제하라!\"",
        "qtext": "<strong>Q5.</strong> 시계가 4시 정각을 가리킬 때, 시침과 분침이 이루는 작은 쪽의 각의 크기를 구하시오.",
        "placeholder": "단위 없이 숫자만 입력 또는 '120도' 입력",
        "error": "틀렸습니다. 시계의 1시간 간격은 30도입니다. 4시간의 각도를 계산해보세요.",
        "ans_check": "ans === '120' || ans === '120도'"
    },
    {
        "qnum": 6,
        "title": "제 2구역: 교차하는 빛줄기",
        "story": "[코덱스-L]: \"2구역 진입을 환영한다! 교차하는 두 광학 센서가 그물처럼 얽혀 있군. 교차하는 두 선이 마주 보며 똑같은 크기로 대치하는 각을 무엇이라 하는가?\"",
        "qtext": "<strong>Q6.</strong> 두 직선이 교차할 때 생기는 교각 중, 마주 보는 두 각을 무엇이라 하는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 마주 보고 솟은 꼭지점을 공유하는 각입니다.",
        "ans_check": "ans === '맞꼭지각'"
    },
    {
        "qnum": 7,
        "title": "광선의 대칭성",
        "story": "[코덱스-L]: \"마주 보는 그 두 각(맞꼭지각)의 크기 관계가 서로 '같다'와 '다르다' 중 무엇에 해당하는지 입력 장치에 송신해라!\"",
        "qtext": "<strong>Q7.</strong> 맞꼭지각의 크기는 서로 어떠한가? (예: 같다, 다르다)",
        "placeholder": "같다 또는 다르다 입력",
        "error": "틀렸습니다. 마주 보는 각은 기하학적으로 항상 동일한 크기를 가집니다.",
        "ans_check": "ans === '같다'"
    },
    {
        "qnum": 8,
        "title": "평행 레이저의 동위",
        "story": "[코덱스-L]: \"나란한 두 평행 레이저 l, m을 하나의 대각선 빔이 뚫고 지나갈 때, 같은 방향의 고유 수신 포트(동위각)의 크기 관계는?\"",
        "qtext": "<strong>Q8.</strong> 직선 l과 m이 평행하고 한 직선 n과 만날 때, 동위각의 크기는 서로 어떠한가?",
        "placeholder": "같다 또는 다르다 입력",
        "error": "틀렸습니다. 평행할 때 동위각의 크기는 항상 대칭 일치합니다.",
        "ans_check": "ans === '같다'"
    },
    {
        "qnum": 9,
        "title": "엇갈린 반사각",
        "story": "[코덱스-L]: \"좋아, 그럼 평행선 장벽 내부에서 지그재그로 엇갈리게 꺾이는 반사 빔(엇각)의 크기 관계는 어떻게 설계되겠나?\"",
        "qtext": "<strong>Q9.</strong> 평행한 두 직선 사이를 가로지르는 선이 있을 때, 엇각의 크기는 서로 어떠한가?",
        "placeholder": "같다 또는 다르다 입력",
        "error": "틀렸습니다. 평행한 직선 사이에서 엇각의 크기는 언제나 일치합니다.",
        "ans_check": "ans === '같다'"
    },
    {
        "qnum": 10,
        "title": "위치 정렬 빔",
        "story": "[코덱스-L]: \"두 도선이 나란하게(평행) 배열되도록 강제하기 위해선, 동위각의 크기가 같거나 무엇의 크기가 서로 같아야 하는가?\"",
        "qtext": "<strong>Q10.</strong> 두 직선이 평행할 조건 중 하나는 동위각의 크기가 같거나 무엇의 크기가 같은 경우인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 엇갈린 위치에 있는 각도입니다.",
        "ans_check": "ans === '엇각'"
    },
    {
        "qnum": 11,
        "title": "제 3구역: 작도의 방",
        "story": "[코덱스-L]: \"3구역이다! 다빈치 님의 순수한 기하학 법칙에 따라, 오직 '눈금 없는 자'와 '컴퍼스'만으로 모형을 그리는 이 성스러운 행위를 무엇이라 하는가?\"",
        "qtext": "<strong>Q11.</strong> 눈금 없는 자와 컴퍼스만을 사용하여 도형을 그리는 것을 무엇이라 하는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 두 글자 기하학 용어입니다.",
        "ans_check": "ans === '작도'"
    },
    {
        "qnum": 12,
        "title": "길이 복제기",
        "story": "[코덱스-L]: \"특정 석재 선분의 폭을 정확히 계측해 설계도 위로 옮겨 복제할 때 주로 쓰는 양다리 금속 기구의 이름을 입력하라!\"",
        "qtext": "<strong>Q12.</strong> 길이가 주어진 선분을 다른 직선 위로 옮길 때 주로 사용하는 도구는 무엇인가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 원을 그리거나 길이를 재어 옮기는 도구입니다.",
        "ans_check": "ans === '컴퍼스'"
    },
    {
        "qnum": 13,
        "title": "삼각 지지대의 성립 조건",
        "story": "[코덱스-L]: \"삼각형 지지대를 만들 때, 가장 긴 변 c는 나머지 두 변의 합(a+b)보다 무조건 ( 커야 / 작아야 ) 조립이 되는가?\"",
        "qtext": "<strong>Q13.</strong> 삼각형의 세 변의 길이가 a, b, c (c가 가장 긴 변)일 때, c는 a+b보다 ( 커야 / 작아야 ) 삼각형이 만들어진다. 알맞은 말은?",
        "placeholder": "커야 또는 작아야 입력",
        "error": "틀렸습니다. 한 변이 너무 길면 양쪽에서 닫히지 않고 벌어집니다.",
        "ans_check": "ans === '작아야'"
    },
    {
        "qnum": 14,
        "title": "목재 조립 테스트",
        "story": "[코덱스-L]: \"자, 3cm, 4cm, 7cm 길이의 나무 막대 세 개를 주지. 이 막대들로 삼각형 구조물을 세울 수 있는지 '있다'와 '없다' 중 답해라!\"",
        "qtext": "<strong>Q14.</strong> 다음 세 선분의 길이로 삼각형을 만들 수 있는가? (3cm, 4cm, 7cm) (예: 있다, 없다)",
        "placeholder": "있다 또는 없다 입력",
        "error": "틀렸습니다. 가장 긴 변이 나머지 두 변의 합과 같으므로 겹쳐져 무너집니다.",
        "ans_check": "ans === '없다'"
    },
    {
        "qnum": 15,
        "title": "설계 완성 가능 여부",
        "story": "[코덱스-L]: \"삼각형의 두 변의 길이와 그 사이의 끼인각의 크기를 안다면, 이 설계도면 위에 완벽한 삼각형을 결정해서 그려낼 수 있는가? (있다/없다)\"",
        "qtext": "<strong>Q15.</strong> 두 변의 길이와 그 끼인각의 크기가 주어졌을 때, 삼각형을 작도할 수 있는가? (예: 있다, 없다)",
        "placeholder": "있다 또는 없다 입력",
        "error": "틀렸습니다. 두 변과 사잇각은 삼각형을 고정하는 완벽한 조건입니다.",
        "ans_check": "ans === '있다'"
    },
    {
        "qnum": 16,
        "title": "제 4구역: 잃어버린 걸작 복원",
        "story": "[코덱스-L]: \"마지막 4구역이다! 모양과 크기가 거울처럼 완벽하게 동일하여 서로 포갰을 때 100% 빈틈없이 일치하는 두 도형의 기하학적 관계는?\"",
        "qtext": "<strong>Q16.</strong> 모양과 크기가 완전히 같아서 포개었을 때 완전히 겹쳐지는 두 도형을 서로 무엇이라 하는가?",
        "placeholder": "정답 입력",
        "error": "틀렸습니다. 두 글자 수학적 명칭입니다.",
        "ans_check": "ans === '합동'"
    },
    {
        "qnum": 17,
        "title": "세 기둥의 합동 락",
        "story": "[코덱스-L]: \"삼각형 보석판의 세 변의 길이가 모두 똑같아 완전히 합동임을 지시하는 조건 기호(영문 3글자)를 입력하여 락을 가동해라!\"",
        "qtext": "<strong>Q17.</strong> 삼각형의 합동 조건 중 세 변의 길이가 각각 같을 때의 합동을 기호로 무엇이라 하는가? (예: SSS, SAS, ASA)",
        "placeholder": "영문 대문자 세 글자 입력",
        "error": "틀렸습니다. 변(Side) 세 개를 뜻하는 기호입니다.",
        "ans_check": "ans === 'SSS' || ans === 'SSS합동'"
    },
    {
        "qnum": 18,
        "title": "두 변과 사잇각의 락",
        "story": "[코덱스-L]: \"두 변의 길이와 그 사이에 끼인각이 각각 같을 때의 삼각형 합동 조건 기호(영문 3글자)를 정밀하게 송신해라!\"",
        "qtext": "<strong>Q18.</strong> 삼각형의 두 변의 길이와 그 끼인각의 크기가 각각 같을 때의 합동 조건을 무엇이라 하는가?",
        "placeholder": "영문 대문자 세 글자 입력",
        "error": "틀렸습니다. 변(Side) 두 개와 각(Angle) 하나가 끼어 있는 기호입니다.",
        "ans_check": "ans === 'SAS' || ans === 'SAS합동'"
    },
    {
        "qnum": 19,
        "title": "한 변과 양 끝각의 락",
        "story": "[코덱스-L]: \"한 변의 길이와 그 변의 양쪽 끝에 걸려 있는 두 모퉁이 각도(양 끝각)가 같을 때의 합동 조건 기호(영문 3글자)는?\"",
        "qtext": "<strong>Q19.</strong> 삼각형의 한 변의 길이와 그 양 끝각의 크기가 각각 같을 때의 합동 조건을 무엇이라 하는가?",
        "placeholder": "영문 대문자 세 글자 입력",
        "error": "틀렸습니다. 각(Angle) 두 개 사이에 변(Side)이 끼어 있는 기호입니다.",
        "ans_check": "ans === 'ASA' || ans === 'ASA합동'"
    },
    {
        "qnum": 20,
        "title": "최종 마스터 봉인",
        "story": "[코덱스-L]: \"마지막 경고다! 두 직각삼각형 락의 빗변 길이와 한 예각의 크기가 동일하다면, 두 락은 서로 어떤 관계인가? ('합동이다' 또는 '합동')\"",
        "qtext": "<strong>Q20.</strong> 직각삼각형에서 빗변의 길이와 한 예각의 크기가 같을 때의 합동 조건을 무엇이라 하는가?",
        "placeholder": "합동이다 또는 합동 입력",
        "error": "틀렸습니다. 빗변과 예각이 같으면 무조건 합동이 성립됩니다.",
        "ans_check": "ans === '합동' || ans === '합동이다'"
    }
]

import re
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
    q['hint'] = q.get('hint') or generate_hint(q['qtext'], q.get('ans_check', ''))

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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_05_basic_geometry/q{qnum}.png" alt="Background" class="panel-image">
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
                <button class="btn" onclick="checkQ{qnum}()">{'작도 활성화 시작' if qnum==1 else '다음으로'}</button>

            </div>
        </div>
'''
    panels_html += panel

outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>봉인 해제!</h1>
            <h2>다빈치의 잃어버린 걸작 복원</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_05_basic_geometry/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">마지막 패스코드 '합동이다'를 누르고 수수께끼판을 맞추자, 요란하게 회전하는 기계 톱니소리와 함께 다빈치의 작업실 숨겨진 벽면이 서서히 열립니다! 
                그 안에는 현대의 헬리콥터와 낙하산 원형이 담긴 다빈치의 실제 설계 스케치와 걸작 유화 판넬이 화려한 금빛 조명 속에서 웅장하게 서 있습니다. 
                눈금 없는 자와 컴퍼스, 그리고 기하학의 완전한 합동 조건을 이해해 르네상스의 가장 깊은 비밀을 파헤친 요원들, 탈출 완벽 성공입니다!</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

js_checks = ""
for q in qs:
    qnum = q['qnum']
    ans_check = q.get('ans_check', 'false')
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    victory_call = 'try { playVictory(); } catch(e) {}' if qnum == 20 else 'try { playSuccess(); } catch(e) {}'
    
    if qnum <= 5:
        reset_qnum = 1
        reset_prog = 0
        zone_name = "1구역"
    elif qnum <= 10:
        reset_qnum = 6
        reset_prog = 25
        zone_name = "2구역"
    elif qnum <= 15:
        reset_qnum = 11
        reset_prog = 50
        zone_name = "3구역"
    else:
        reset_qnum = 16
        reset_prog = 75
        zone_name = "4구역"
        
    # GAS 종료 호출 로직 추가 (Q20)
    gas_end_call = ""
    if qnum == 20:
        gas_end_call = '''
                // GAS 기록 종료 호출
                try {
                    if (window.userRecordRow && typeof google !== 'undefined' && google.script && google.script.run) {
                        google.script.run.recordEnd(window.userRecordRow, 'm1_05');
                    }
                } catch(e) {
                    console.warn("구글 시트 종료 기록 실패(로컬 테스트 모드):", e);
                }'''

    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace('(','').replace(')','');
            if ({ans_check}) {{
                wrongCount = 0;
                {victory_call} {gas_end_call}
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                wrongCount++;
                if (wrongCount >= 3) {{
                    alert("🚨 3회 오답 패널티! {zone_name} 처음으로 이동됩니다.");
                    wrongCount = 0;
                    document.getElementById('ans{reset_qnum}').value = '';
                    nextStage('panel_q{qnum}', 'panel_q{reset_qnum}', {reset_prog});
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}', wrongCount);
                }}
            }}
        }}
'''
    js_checks += js

# Compile
new_content = re.sub(r'<!-- Q1.*?-->', lambda m: '<!-- Q1 -->\n' + panels_html + '\n    ', base_html, flags=re.DOTALL)
new_content = re.sub(r'// Q1[\s\S]*?(?=window\.onload = \(\) => \{)', lambda m: '// Q1\n' + js_checks + '\n        ', new_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("app_m1_05_escape_room.html created successfully.")
