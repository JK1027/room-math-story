import re
import os

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_08_escape_room.html")
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
:root{--bg-main:#131A1C;--glass-bg:rgba(20, 28, 30, 0.75);--glass-border:rgba(13, 148, 136, 0.25);--accent:#0D9488;--accent-hover:#2DD4BF;--text-main:#E0F2FE;--text-muted:#94A3B8;}*{box-sizing:border-box;margin:0;padding:0;}body{font-family:'Noto Sans KR', sans-serif;background-color:var(--bg-main);color:var(--text-main);min-height:100vh;display:flex;justify-content:center;align-items:center;overflow-x:hidden;position:relative;}body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(circle at 20% 30%, rgba(13, 148, 136, 0.1) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(17, 94, 89, 0.12) 0%, transparent 40%);z-index:-2;}.container{width:100%;max-width:800px;padding:2rem;position:relative;z-index:10;}.glass-panel{background:var(--glass-bg);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid var(--glass-border);border-top:1px solid rgba(13, 148, 136, 0.4);border-left:1px solid rgba(13, 148, 136, 0.4);border-radius:24px;padding:3rem;box-shadow:0 0 40px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(13, 148, 136, 0.05);display:none;opacity:0;transform:translateY(20px);transition:all 0.5s cubic-bezier(0.4, 0, 0.2, 1);}.glass-panel.active{display:block;opacity:1;transform:translateY(0);}h1{font-family:'Orbit', sans-serif;font-size:2.5rem;font-weight:900;text-align:center;margin-bottom:0.5rem;background:linear-gradient(135deg, #FFF 30%, var(--accent) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:0 0 30px rgba(13, 148, 136, 0.3);letter-spacing:2px;}h2{font-size:1.4rem;color:var(--text-main);text-align:center;margin-bottom:2rem;font-weight:500;letter-spacing:1px;}.panel-image{width:100%;height:auto;max-height:250px;object-fit:cover;border-radius:8px;margin-bottom:1rem;}.story-box{position:relative;background:linear-gradient(90deg, rgba(20, 40, 45, 0.5) 0%, rgba(0,0,0,0.3) 100%);border-left:4px solid var(--accent);padding:0.8rem 1.2rem;margin-bottom:1.5rem;border-radius:0 12px 12px 0;box-shadow:0 4px 15px rgba(0,0,0,0.4);height:90px;max-height:90px;overflow:hidden;box-sizing:border-box;}.story-text{width:100%;height:100%;overflow:hidden;line-height:1.6;font-size:1.02rem;color:var(--text-main);text-align:justify;}.story-log-trigger{position:absolute;bottom:4px;right:8px;background:rgba(16, 185, 129, 0.25);border:1px solid rgba(16, 185, 129, 0.5);color:#34D399;padding:2px 6px;font-size:0.7rem;border-radius:4px;cursor:pointer;transition:all 0.2s;font-weight:bold;z-index:10;}.story-log-trigger:hover{background:rgba(16, 185, 129, 0.5);color:white;}.question-box{background:rgba(255, 255, 255, 0.02);border:1px solid rgba(255, 255, 255, 0.05);border-radius:16px;padding:1.5rem;margin-bottom:1.5rem;position:relative;box-shadow:inset 0 0 20px rgba(255, 255, 255, 0.02);}.question-box::before{content:'Q';position:absolute;font-family:'Share Tech Mono', monospace;font-size:4rem;color:rgba(13, 148, 136, 0.05);top:-10px;right:10px;font-weight:bold;pointer-events:none;}.question-content{font-size:1.15rem;line-height:1.8;margin-bottom:1rem;}.input-group{margin-top:1rem;}input[type="text"]{width:100%;padding:1rem 1.2rem;background:rgba(15, 23, 42, 0.8);border:1px solid rgba(13, 148, 136, 0.3);border-radius:12px;color:white;font-size:1.1rem;font-family:'Share Tech Mono', monospace, 'Noto Sans KR';transition:all 0.3s;box-shadow:inset 0 2px 4px rgba(0,0,0,0.5);}input[type="text"]:focus{outline:none;border-color:var(--accent);box-shadow:0 0 15px rgba(13, 148, 136, 0.4), inset 0 2px 4px rgba(0,0,0,0.5);}.error-msg{color:#EF4444;font-size:0.95rem;margin-top:0.5rem;display:none;text-align:center;font-weight:bold;text-shadow:0 0 10px rgba(239, 68, 68, 0.3);animation:shake 0.5s ease;}@keyframes shake{0%, 100%{transform:translateX(0);}20%, 60%{transform:translateX(-5px);}40%, 80%{transform:translateX(5px);}}.progress-container{width:100%;height:6px;background:rgba(255, 255, 255, 0.05);border-radius:3px;margin-bottom:2rem;overflow:hidden;display:none;border:1px solid rgba(255, 255, 255, 0.02);}.progress-bar{height:100%;width:0%;background:linear-gradient(90deg, #0F766E, var(--accent));border-radius:3px;box-shadow:0 0 10px var(--accent);transition:width 0.8s cubic-bezier(0.4, 0, 0.2, 1);}.btn-group{display:flex;gap:1rem;margin-top:2rem;}.btn{background:linear-gradient(135deg, #0F766E, #115E59);color:white;border:1px solid #14B8A6;padding:0.6rem 1.5rem;font-size:1.1rem;font-weight:900;border-radius:8px;cursor:pointer;transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);text-transform:uppercase;letter-spacing:3px;width:100%;box-shadow:0 10px 25px rgba(17, 94, 89, 0.5), inset 0 2px 5px rgba(255,255,255,0.3);text-shadow:0 2px 4px rgba(0,0,0,0.5);position:relative;overflow:hidden;}.btn::after{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);transition:all 0.6s;}.btn:hover::after{left:100%;}.btn:hover{transform:translateY(-2px);box-shadow:0 15px 30px rgba(13, 148, 136, 0.5), inset 0 2px 5px rgba(255,255,255,0.5);border-color:#2DD4BF;}.btn-hint{display:inline-block;background:rgba(16, 185, 129, 0.2);border:1px solid rgba(16, 185, 129, 0.5);color:#34D399;padding:4px 10px;font-size:0.85rem;font-weight:700;border-radius:6px;cursor:pointer;transition:all 0.2s ease;vertical-align:middle;margin-left:10px;letter-spacing:0.5px;text-transform:none;box-shadow:0 2px 5px rgba(0, 0, 0, 0.2);}.btn-hint:hover{background:rgba(16, 185, 129, 0.4);color:#fff;box-shadow:0 0 10px rgba(52, 211, 153, 0.4);}.btn:active{transform:translateY(1px);}.sound-toggle{position:fixed;top:20px;right:20px;background:rgba(20, 28, 30, 0.6);border:1px solid var(--glass-border);padding:8px 16px;border-radius:20px;color:white;cursor:pointer;z-index:100;backdrop-filter:blur(10px);font-size:0.9rem;transition:all 0.3s;font-weight:bold;}.sound-toggle:hover{background:var(--accent);border-color:white;box-shadow:0 0 15px var(--accent);}@keyframes blink{0%, 100%{opacity:1;}50%{opacity:0;}}@media (max-width:600px){body{overflow-y:auto;}.container{padding:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;box-sizing:border-box;min-height:100vh;}.glass-panel{width:100%;max-height:94vh;max-height:94dvh;height:auto;padding:1.2rem;border-radius:16px;box-sizing:border-box;display:none;flex-direction:column;justify-content:flex-start;overflow-y:auto;}.glass-panel.active{display:flex;}.story-box{padding:0.6rem 1rem;margin-bottom:0.5rem;height:80px;max-height:80px;overflow:hidden;flex:0 0 auto;}.story-text{font-size:0.85rem;line-height:1.5;}h1{font-size:1.6rem;letter-spacing:1px;}h2{font-size:1rem;margin-bottom:1rem;}.panel-image{max-height:180px;margin-bottom:1rem;}.question-box{padding:0.8rem;margin-bottom:1rem;}.question-box::before{font-size:3rem;top:-5px;right:-5px;}input[type="text"]{font-size:1rem;padding:0.8rem;}.btn{font-size:0.9rem;padding:0.5rem;letter-spacing:1px;border-radius:6px;}.btn-group{flex-direction:column;gap:0.6rem;}.sound-toggle{top:10px;right:10px;font-size:0.8rem;padding:6px 12px;}}.log-modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0, 0, 0, 0.85);z-index:1000;justify-content:center;align-items:center;backdrop-filter:blur(10px);}.log-content{background:#111A1B;border:2px solid var(--accent);border-radius:20px;width:90%;max-width:600px;max-height:80vh;padding:2rem;position:relative;display:flex;flex-direction:column;}.log-content h2{font-family:'Orbit', sans-serif;color:var(--accent);margin-bottom:1rem;text-align:left;}#logContainer{overflow-y:auto;flex-grow:1;margin-bottom:1.5rem;padding-right:10px;font-size:0.95rem;line-height:1.8;color:#cbd5e1;}#logContainer strong{color:var(--accent);}.close-log{position:absolute;top:15px;right:15px;background:transparent;border:none;color:#ef4444;font-size:1.5rem;cursor:pointer;transition:scale 0.2s;}.close-log:hover{scale:1.2;}@keyframes shake{0%, 100%{transform:translate(0, 0) rotate(0deg);}10%{transform:translate(-2px, -1px) rotate(-0.5deg);}20%{transform:translate(-3px, 0px) rotate(1deg);}30%{transform:translate(0px, 2px) rotate(0deg);}40%{transform:translate(1px, -1px) rotate(1deg);}50%{transform:translate(-1px, 2px) rotate(-1deg);}60%{transform:translate(-3px, 1px) rotate(0deg);}70%{transform:translate(2px, 1px) rotate(-0.5deg);}80%{transform:translate(-1px, -1px) rotate(1deg);}90%{transform:translate(2px, 2px) rotate(0deg);}}.shake-effect{animation:shake 0.3s ease-in-out;}.laser-flash-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255, 0, 0, 0);pointer-events:none;z-index:9999;transition:background 0.15s ease-out;}.laser-flash-active{background:rgba(255, 0, 0, 0.15);transition:none;}
</style>
</head>
<body>

    <button id="soundToggle" class="sound-toggle" onclick="toggleSound()">🔊 소리 켜짐</button>

    <div class="container">
        
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <!-- 0. 인트로 -->
        <div id="intro" class="glass-panel active">
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_08_statistics/intro.png" alt="Background" class="panel-image">
            <h1>셜록 홈즈와 통계국</h1>
            <h2>위조된 데이터의 비밀을 해독하라</h2>
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">
                    런던 통계국에 범죄 조직 모리아티의 스파이가 침투해 수많은 데이터를 조작해 놓았습니다!<br><br>
                    명<span class="dynamic-captain-name"><span class="dynamic-captain-name">탐정</span></span> 셜록 홈즈의 <span class="dynamic-captain-name"><span class="dynamic-captain-name">조수</span></span>가 된 여러분은 조작된 자료들을 분석하고 도수분포표와 통계적 법칙을 밝혀내야 합니다.<br><br>
                    제한 시간 40분 내에 20개의 통계 단서를 풀어내어 진짜 스파이를 찾아내고 데이터를 복구하세요!
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
                <button class="btn" onclick="tryStartGame('m1_08')">통계 데이터 복구 가동</button>
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


            // 이름 동적 개인화 처리
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
                    let firstName = rawName.length > 2 ? rawName.substring(1) : rawName;
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
            <h2>📜 지나온 추리 기록</h2>
            <div id="logContainer">기록이 없습니다.</div>
        </div>
    </div>

</body>
</html>
"""

qs = [
    {'qnum': 1, 'title': '잎의 복원', 'story': '[모리아티-AI]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? [왓슨-X]: "소매치기 발생 장부에서 줄기가 2인 잎의 목록을 쉼표 없이 순서대로 적어주세요! (자료: 12,15,23,24,27,31,31,35,42,45)"\\"', 'qtext': '<strong>Q1. [줄기와 잎 그림]</strong><br>위 자료를 줄기와 잎 그림으로 나타낼 때, 줄기가 2인 잎을 쉼표(,)로 구분하여 크기 순으로 모두 적으시오.', 'placeholder': '예: 3, 4, 7', 'error': '장부 판독 실패! 잎을 다시 세십시오.', 'ans_check': "ans === '3,4,7' || ans === '3, 4, 7' || ans === '347'", 'hint': '줄기가 2인 데이터 변량들의 일의 자리 숫자들을 차례대로 나열해 줍니다.'},
    {'qnum': 2, 'title': '변량 개수', 'story': '[모리아티-AI]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? [왓슨-X]: "수집된 전체 지역(변량) 샘플의 개수가 모두 몇 곳인지 식별해보고해주십시오."\\"', 'qtext': '<strong>Q2. [변량의 개수]</strong><br>위 자료에서 전체 변량의 개수는 몇 개인가?', 'placeholder': '숫자 또는 개수 입력', 'error': '변량 개수 불일치! 장부의 줄 수가 다릅니다.', 'ans_check': "ans === '10' || ans === '10개'", 'hint': '수집된 전체 데이터 샘플의 개수가 모두 몇 개인지 직접 세어 봅니다.'},
    {'qnum': 3, 'title': '최대 분포 줄기', 'story': '[모리아티-AI]: \\"크하하! 이 시스템은 나의 지배하에 있다! 감히 보안 구역을 돌파하겠다고? [왓슨-X]: "도난 데이터 왜곡 흔적입니다. 잎의 개수가 가장 많이 분포한 줄기 번호를 대주십시오."\\"', 'qtext': '<strong>Q3. [최다 잎 줄기]</strong><br>위 자료에서 잎이 가장 많은 줄기는 무엇인가?', 'placeholder': '예: 2, 3', 'error': '탐색 실패! 잎의 최대 개수가 매칭되지 않습니다.', 'ans_check': "ans === '2와3' || ans === '2,3' || ans === '2, 3'", 'hint': '줄기와 잎 그림에서 잎(오른쪽 숫자)의 개수가 가장 많이 늘어선 줄기 번호를 찾습니다.'},
    {'qnum': 4, 'title': '우범 구역 식별', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[왓슨-X]: \\"치지직... 들리십니까...? 모리아티-AI의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q4. [조건 필터링]</strong><br>소매치기 발생 건수가 30건 이상인 지역은 몇 곳인가?', 'placeholder': '숫자 또는 곳 입력', 'error': '구역 필터링 개수가 달라 통신 오류가 발생합니다!', 'ans_check': "ans === '5' || ans === '5곳'", 'hint': '30 이상인 숫자(31, 31, 35, 42, 45)가 모두 몇 개인지 개수를 셉니다.'},
    {'qnum': 5, 'title': '경미 지역 추적', 'story': '<strong>[시스템 통신 장애 발생]</strong><br><br>[왓슨-X]: \\"치지직... 들리십니까...? 모리아티-AI의 코드를 무력화하기 위해 계산값을 전송해야 합니다...\\"', 'qtext': '<strong>Q5. [순위 데이터]</strong><br>소매치기 발생 건수가 적은 쪽에서 3번째인 지역의 건수는 얼마인가?', 'placeholder': '숫자 또는 건 입력', 'error': '수치 불일치! 정렬 순서가 꼬였습니다.', 'ans_check': "ans === '23' || ans === '23건'", 'hint': '데이터를 크기 순서대로 정렬했을 때 세 번째로 작은 건수 값을 찾습니다.'},
    {'qnum': 6, 'title': '제2구역: 계급 분류', 'story': '[모리아티-AI]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! [왓슨-X]: "20명의 용의자 나이 변량을 일정한 간격으로 나눈 이 구간들을 무엇이라 합니까?"\\"', 'qtext': '<strong>Q6. [계급의 정의]</strong><br>자료를 몇 개의 구간으로 나눌 때, 이 구간을 무엇이라 하는가?', 'placeholder': '한글 단어 입력', 'error': '기초 통계 용어 오류! 결계가 열리지 않습니다.', 'ans_check': "ans === '계급'", 'hint': '수집된 변량을 일정한 간격으로 나눈 구간을 가리키는 통계 용어입니다.'},
    {'qnum': 7, 'title': '도수의 정의', 'story': '[모리아티-AI]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! [왓슨-X]: "그 나이 구간(계급) 각각에 할당 분류된 인원수(자료의 수)를 일컫는 통계 용어는?"\\"', 'qtext': '<strong>Q7. [도수의 정의]</strong><br>각 계급에 속하는 변량의 개수를 무엇이라 하는가?', 'placeholder': '한글 단어 입력', 'error': '마나 입력 오류! 올바른 한글 용어를 쓰십시오.', 'ans_check': "ans === '도수'", 'hint': '각 계급 구간에 속해 있는 자료(변량)의 개수를 의미하는 용어입니다.'},
    {'qnum': 8, 'title': '계급의 폭', 'story': '[모리아티-AI]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! [왓슨-X]: "나이 분류표 상 10대, 20대 등으로 나뉘어 있을 때, 이 각 나이 구간 너비(계급의 크기)는 얼마인가요?"\\"', 'qtext': '<strong>Q8. [계급의 크기]</strong><br>계급의 너비(크기)는 얼마인가? (자료: 10대, 20대 식일 때의 너비)', 'placeholder': '숫자만 입력', 'error': '너비 부조화! 구간 세그먼트가 틀어졌습니다.', 'ans_check': "ans === '10' || ans === '10세'", 'hint': '한 계급 구간의 너비(끝값 - 시작값)를 계산하여 단위를 포함하지 않은 값을 적습니다.'},
    {'qnum': 9, 'title': '최대 나이 도수', 'story': '[모리아티-AI]: \\"쥐새끼 같은 보조 인격이 끼어들었군! 쓸데없는 발악은 그만둬라! [왓슨-X]: "용의자 분포 중, 도수가 8명으로 가장 높은 도수를 보이는 용의자 나이 계급은? (예: 20대)"\\"', 'qtext': '<strong>Q9. [최대 도수 계급]</strong><br>도수가 가장 큰 계급은 어느 연령대인가? (자료: 10대: 4명, 20대: 8명, 30대: 5명, 40대: 3명)', 'placeholder': '예: 20대', 'error': '용의자 타겟팅 오류!', 'ans_check': "ans === '20대'", 'hint': '도수(인원수)가 8명으로 가장 많이 몰려 있는 나이대 계급을 찾습니다.'},
    {'qnum': 10, 'title': '청년 용의자 비율', 'story': '🚨 <strong>[비상 경보: 강제 자폭 시스템 작동]</strong> 🚨<br><br>[모리아티-AI]: \\"더는 참을 수 없군! 모든 데이터를 시스템을 포맷하겠다! 5분 내로 전부 초기화 시켜주지!\\"<br><br>[왓슨-X]: \\"경고! 시스템 온도 상승 중! 제가 방화벽을 전개할 동안 긴급 수치 입력을 끝내십시오!\\"', 'qtext': '<strong>Q10. [백분율 계산]</strong><br>나이가 30세 미만인 용의자는 전체의 몇 %인가? (단위 생략)', 'placeholder': '숫자만 입력', 'error': '백분율 오차 발생! 차단 셔터 압력 증가!', 'ans_check': "ans === '60' || ans === '60%'", 'hint': '30세 미만 인원수(4명 + 8명 = 12명)가 전체 20명 중에서 차지하는 비율을 백분율(%)로 계산합니다.', "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '제3구역: 히스토그램', 'story': '[왓슨-X]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! [왓슨-X]: "가로축에 계급, 세로축에 도수를 세워 직사각형으로 표현한 이 그래프 이름은 무엇입니까?"\\"', 'qtext': '<strong>Q11. [히스토그램]</strong><br>도수분포표를 바탕으로 가로축에 계급, 세로축에 도수를 나타내어 직사각형 모양으로 그린 그래프를 무엇이라 하는가?', 'placeholder': '한글 그래프 이름 입력', 'error': '그래프 타입 인식 불가능!', 'ans_check': "ans === '히스토그램'", 'hint': '도수분포표를 바탕으로 가로에 계급, 세로에 도수를 매칭해 그린 직사각형 모양의 그래프 명칭입니다.'},
    {'qnum': 12, 'title': '가로폭의 속성', 'story': '[왓슨-X]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! [왓슨-X]: "스파이가 히스토그램의 가로폭 배율을 건드렸군요. 직사각형의 가로폭이 원래 의미하는 바는 무엇인가요?"\\"', 'qtext': '<strong>Q12. [히스토그램 가로]</strong><br>히스토그램에서 직사각형의 가로의 길이는 무엇을 의미하는가?', 'placeholder': '예: 계급의 크기', 'error': '가로축 픽셀 정렬 에러!', 'ans_check': "ans === '계급의크기' || ans === '계급의 크기' || ans === '계급의너비' || ans === '계급의 너비'", 'hint': '도수분포표의 각 직사각형의 가로폭이 나타내는 계급의 간격 크기를 의미합니다.'},
    {'qnum': 13, 'title': '넓이의 총합', 'story': '[왓슨-X]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! [왓슨-X]: "히스토그램 직사각형들의 넓이 총합 공식은 (계급의 크기) × ( ? ) 입니다. ?를 대십시오."\\"', 'qtext': '<strong>Q13. [히스토그램 넓이 공식]</strong><br>히스토그램에서 직사각형의 넓이의 합은 (계급의 크기) × ( ? ) 이다. ?에 들어갈 알맞은 말은?', 'placeholder': '한글 단어 입력', 'error': '면적 총합 불일치! 차원 결계 폐쇄 경보!', 'ans_check': "ans === '도수의총합' || ans === '도수의 총합' || ans === '도수의합' || ans === '도수의 합'", 'hint': '모든 직사각형의 넓이 합 공식은 (계급의 크기) * (도수의 총합) 입니다.'},
    {'qnum': 14, 'title': '다각형 그래프', 'story': '[왓슨-X]: \\"방어막 출력 한계 도달 중! 코드를 지속적으로 갱신해야 폭발을 유예할 수 있습니다! [왓슨-X]: "직사각형 윗변의 가운데 중점들을 꺾은선으로 연결한 이 다각형 모양의 도수 분석 그래프 명칭은?"\\"', 'qtext': '<strong>Q14. [도수분포다각형]</strong><br>히스토그램의 각 직사각형 윗변의 중점을 차례로 선분으로 연결한 그래프를 무엇이라 하는가?', 'placeholder': '한글 그래프 이름 입력', 'error': '다각형 궤적 링크 오류!', 'ans_check': "ans === '도수분포다각형'", 'hint': '히스토그램의 각 직사각형 윗변의 중점들을 선분으로 이어 꺾은선 모양으로 만든 다각형 그래프입니다.'},
    {'qnum': 15, 'title': '넓이의 동등성', 'story': '✨ <strong><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\"><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\"><span style=\"color: #60a5fa; text-shadow: 0 0 5px #3b82f6;\">[조력자 시스템 권한 100% 완전 복구]</span></span></span></strong> ✨<br><br>[왓슨-X]: \\"연산 데이터 대조 성공! 이제 시스템 통제권을 제가 절반 확보했습니다. 가자, 복수의 시간입니다!\\"<br><br>[모리아티-AI]: \\"크으으윽... 하찮은 인간 녀석들이 내 서버까지 잠식해 들어오다니!\\"', 'qtext': '<strong>Q15. [넓이의 성질]</strong><br>도수분포다각형과 가로축으로 둘러싸인 부분의 넓이는 히스토그램의 직사각형들의 넓이의 합과 어떠한가?', 'placeholder': '같다 또는 다르다 입력', 'error': '면적 불균형! 공간 붕괴 위험!', 'ans_check': "ans === '같다'", 'hint': '도수분포다각형과 가로축이 만드는 면적은 히스토그램 전체 직사각형 넓이의 합과 항상 같은 성질을 가집니다.', "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '제4구역: 상대도수', 'story': '[모리아티-AI]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! [왓슨-X]: "각 계급 도수의 크기를 전체 도수의 총합 비율로 구한 이 값을 통계학적으로 무엇이라 합니까?"\\"', 'qtext': '<strong>Q16. [상대도수의 정의]</strong><br>각 계급의 도수를 도수의 총합으로 나눈 비율을 무엇이라 하는가?', 'placeholder': '한글 단어 입력', 'error': '가중치 데이터 로드 불가!', 'ans_check': "ans === '상대도수'", 'hint': '각 계급의 도수가 전체 도수 총합 중에서 차지하는 상대적인 비율을 뜻하는 용어입니다.'},
    {'qnum': 17, 'title': '상대도수 계산', 'story': '[모리아티-AI]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! [왓슨-X]: "용의자 도수가 15이고 전체 도수의 총합이 50일 때, 이 계급의 상대도수 값을 소수로 구해주십시오."\\"', 'qtext': '<strong>Q17. [상대도수 계산]</strong><br>어떤 계급의 도수가 15, 도수의 총합이 50일 때, 이 계급의 상대도수를 구하시오. (소수로 기재)', 'placeholder': '예: 0.5', 'error': '주파수 오차 발생! 안개가 더 짙어집니다.', 'ans_check': "ans === '0.3'", 'hint': '특정 계급 도수(15)를 전체 도수(50)로 나눈 비율을 소수 값으로 계산합니다.'},
    {'qnum': 18, 'title': '상대도수의 총합', 'story': '[모리아티-AI]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! [왓슨-X]: "상대도수의 종합 총합은 수학적으로 항상 얼마가 됩니까?"\\"', 'qtext': '<strong>Q18. [상대도수 총합]</strong><br>상대도수의 총합은 항상 얼마인가?', 'placeholder': '숫자만 입력', 'error': '한계선 수치 초과! 시스템 잠금!', 'ans_check': "ans === '1'", 'hint': '상대적인 비율들의 총합은 항상 전체를 뜻하는 고정된 자연수 값이 나옵니다.'},
    {'qnum': 19, 'title': '분포 상태 비교', 'story': '[모리아티-AI]: \\"아직 끝나지 않았다! 내 최고의 방해 암호를 해독해 보아라! [왓슨-X]: "도수 총합이 서로 다른 두 용의자 집단의 분포 상태를 비교할 때 상대도수는 ( 유용하다 / 불필요하다 )?"\\"', 'qtext': '<strong>Q19. [상대도수의 활용]</strong><br>상대도수는 도수의 총합이 다른 두 집단의 분포 상태를 비교할 때 어떠한가? (유용하다 / 불필요하다)', 'placeholder': '유용하다 또는 불필요하다 입력', 'error': '비교 엔진 작동 불능!', 'ans_check': "ans === '유용하다'", 'hint': '조사 대상의 전체 총인원수가 서로 다른 두 집단의 성적이나 선호도를 비율로 공평하게 비교할 때의 유용성 여부를 생각합니다.'},
    {'qnum': 20, 'title': '범인 도수 산출', 'story': '🔮 <strong>[최종 방화벽 락다운 해제]</strong> 🔮<br><br>[왓슨-X]: \\"제 모든 에너지를 출구 개방에 전념하겠습니다. 당신이라면 저 장벽을 해독해 낼 것입니다. 마지막 답을 입력하세요!\\"<br><br>[모리아티-AI]: \\"안 돼... 내 제어권이... 정지한다아아!\\"', 'qtext': '<strong>Q20. [도수 구하기]</strong><br>상대도수가 0.2이고 전체 도수가 40명일 때, 이 계급의 도수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '지목 실패! 스파이가 안개 속으로 도망칩니다!', 'ans_check': "ans === '8' || ans === '8명'", 'hint': '(전체 인원 40명) * (상대도수 비율 0.2)를 곱하여 해당 계급의 실제 인원수를 계산합니다.', "extra_class": "glitch-bg"}
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
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_08_statistics/q{qnum}.png" alt="Background" class="panel-image">
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
                <button class="btn" onclick="checkQ{qnum}()">{'데이터 추적 시작' if qnum==1 else '다음으로'}</button>

            </div>
        </div>
'''
    panels_html += panel

outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>검거 성공!</h1>
            <h2>런던 통계국 보안 복구 완료</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_08_statistics/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">마지막 단서 수치 '8'을 제어반에 입력하자, 조작되었던 통계 장부들이 올바른 줄기와 잎 그림으로 재정렬되며 진범의 탈출 경로가 지도 위에 뚜렷이 그려집니다! 
                빅토리아 시기 런던의 안개가 걷히며 홈즈와 런던 경찰들이 현장에서 범인 모리아티의 스파이를 무사히 검거합니다. 
                홈즈가 감탄어린 미소와 함께 "자네의 통계적 추리력은 실로 명석하군"이라며 영국 국왕의 명예 훈장을 건넵니다. 미션 대성공!</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

js_checks = "let totalWrongCount = 0;\n"
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
                        google.script.run.recordEnd(window.userRecordRow, 'm1_08');
                    }
                } catch(e) {
                    console.warn("구글 시트 종료 기록 실패(로컬 테스트 모드):", e);
                }
                
                // 멀티 엔딩 처리
                let outroDiv = document.getElementById("outro-dynamic-text");
                if (outroDiv) {
                    if (totalWrongCount < 5) {
                        outroDiv.innerHTML = `마지막 단서 수치 '8'을 제어반에 입력하자, 조작되었던 통계 장부들이 올바른 줄기와 잎 그림으로 재정렬되며 진범의 탈출 경로가 지도 위에 뚜렷이 그려집니다! 
                빅토리아 시기 런던의 안개가 걷히며 홈즈와 런던 경찰들이 현장에서 범인 모리아티의 스파이를 무사히 검거합니다. 
                홈즈가 감탄어린 미소와 함께 "자네의 통계적 추리력은 실로 명석하군"이라며 영국 국왕의 명예 훈장을 건넵니다. 미션 대성공!`;
                    } else {
                        outroDiv.innerHTML = "탈출 장치가 기동되는 순간! 시스템이 크게 요동칩니다.<br><br>잦은 오답과 연산 지연의 여파로 시스템이 과부하에 걸렸고, 데이터의 일부가 유실되었습니다. 하지만 여러분은 끝까지 포기하지 않고 방화벽을 해제하여 간신히 탈출구로 몸을 피했습니다! 상처투성이의 탈출이었지만, 수학의 지혜로 보물을 획득했습니다. 미션 성공!";
                    }
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
                wrongCount++;\n                totalWrongCount++;
                if (wrongCount >= 3) {{
                    showGlitchOverlay();
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

print("app_m1_08_escape_room.html created successfully.")
