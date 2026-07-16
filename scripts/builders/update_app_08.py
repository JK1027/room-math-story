# -*- coding: utf-8 -
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
            
            <div class="info-box" style="background: rgba(220, 38, 38, 0.2); border-left: 4px solid #ef4444; padding: 0.8rem 1.2rem; margin-top: 1.5rem; border-radius: 0 12px 12px 0; color: #f87171; font-size: 0.95rem; line-height: 1.6; text-align: left;">
                ⚠️ <b>주의사항</b><br>
                문제는 총 20문제이며, 한 문제에서 3번 틀릴 경우 해당 구역의 처음으로 되돌아갑니다. <br>
                또한 <b>오답을 제출할 때마다 제한 시간이 1분씩 단축</b>되니 신중하게 도전해 주세요!
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
    {'qnum': 1, "options": ["3,4,7", "3,4,7 아님", "알 수 없음", "해 없음"], 'title': '잎의 복원', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "크하하! 런던 통계국의 모든 차분기관 톱니바퀴 동력 장치는 내 손안에 있다! 셜록 홈즈의 풋내기 조수 녀석들이 감히 장부 보호 빗장을 뚫으려 하다니! 장부를 찢어 흩뜨려 놓겠다!"<br><br><i>치이이- 스팀파이프에서 연기가 뿜어 나오며 통계 스크린에 깨진 데이터 테이블이 노출됩니다. 소매치기 발생 장부에서 줄기가 2인 잎의 목록을 순서대로 정렬해 전송해야 락이 해제됩니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "조사관님! 차분 기어의 수치가 엉키고 있습니다. 줄기가 2인 잎 데이터를 신속히 나열하여 정렬 다이얼을 가동해 주십시오!"''', 'qtext': '<strong>Q1. [줄기와 잎 그림]</strong><br>위 자료를 줄기와 잎 그림으로 나타낼 때, 줄기가 2인 잎을 쉼표(,)로 구분하여 크기 순으로 모두 적으시오.', 'placeholder': '예: 3, 4, 7', 'error': '장부 판독 실패! 잎을 다시 세십시오.', 'ans_check': "ans === '3,4,7' || ans === '3, 4, 7' || ans === '347'", 'hint': '줄기가 2인 데이터 변량들의 일의 자리 숫자들을 차례대로 나열해 줍니다.'},
    {'qnum': 2, "options": ["8", "10", "20", "12"], 'title': '변량 개수', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "장부 데이터 왜곡 흔적을 겨우 한 줄 찾았을 뿐이다! 수집된 장부 상의 전체 변량 표본 개수가 어긋나면 차분기관의 놋쇠 기어가 역회전해 폭발하리라!"<br><br><i>드르륵- 놋쇠 크랭크가 고속으로 맞물리며 마모 진동이 전달됩니다. 전체 변량 데이터 개수를 산출하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "놋쇠 기어가 과열되고 있습니다! 수집된 진짜 변량 표본의 개수를 구해 압력 방출 다이얼에 입력해 주십시오!"''', 'qtext': '<strong>Q2. [변량의 개수]</strong><br>위 자료에서 전체 변량의 개수는 몇 개인가?', 'placeholder': '숫자 또는 개수 입력', 'error': '변량 개수 불일치! 장부의 줄 수가 다릅니다.', 'ans_check': "ans === '10' || ans === '10개'", 'hint': '수집된 전체 데이터 샘플의 개수가 모두 몇 개인지 직접 세어 봅니다.'},
    {'qnum': 3, "options": ["2와3", "2와3 아님", "알 수 없음", "해 없음"], 'title': '최대 분포 줄기', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "오답 제출 시 밸브가 막히도록 세팅했다. 잎이 가장 집중 분포된 줄기 번호를 찾아내지 못한다면 증기 고압 가스가 방 안을 가득 메우리라!"<br><br><i>쉬이이익- 증기 통제구 틈새로 뜨겁고 탁한 한증 기포가 새어 나오기 시작합니다. 잎의 밀도가 최고치인 줄기 번호들을 입력하여 차단하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "증기 가리개를 전개했습니다! 잎이 가장 많이 분포하는 핵심 줄기 코드를 입력하여 밸브를 격리 차단해 주십시오!"''', 'qtext': '<strong>Q3. [최다 잎 줄기]</strong><br>위 자료에서 잎이 가장 많은 줄기는 무엇인가?', 'placeholder': '예: 2, 3', 'error': '탐색 실패! 잎의 최대 개수가 매칭되지 않습니다.', 'ans_check': "ans === '2와3' || ans === '2,3' || ans === '2, 3'", 'hint': '줄기와 잎 그림에서 잎(오른쪽 숫자)의 개수가 가장 많이 늘어선 줄기 번호를 찾습니다.'},
    {'qnum': 4, "options": ["10", "3", "7", "5"], 'title': '우범 구역 식별', 'story': '''<strong>[차분 기어 조작 노이즈 발생]</strong><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "치지직... 조사관님! 모리아티가 차분 기어를 조작하여 계산 종이 회전축을 비틀었습니다! 소매치기 다발 30건 이상 구역 개수를 식별해 제어용 수치 카드를 대입해야 합니다!"''', 'qtext': '<strong>Q4. [조건 필터링]</strong><br>소매치기 발생 건수가 30건 이상인 지역은 몇 곳인가?', 'placeholder': '숫자 또는 곳 입력', 'error': '구역 필터링 개수가 달라 통신 오류가 발생합니다!', 'ans_check': "ans === '5' || ans === '5곳'", 'hint': '30 이상인 숫자(31, 31, 35, 42, 45)가 모두 몇 개인지 개수를 셉니다.'},
    {'qnum': 5, "options": ["21", "23", "46", "25"], 'title': '경미 지역 추적', 'story': '''🚨 <strong>[비상 로그: 동력 기판 과부하 위험]</strong> 🚨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "과부하 경보 발생! 발생 건수가 하위 3번째에 위치한 표본 데이터를 확인하여, 동력 기판의 압력 제어 상수를 맞춰 주십시오!"<br><br><i>파지직- 구리 연결판 주변에 불꽃이 튀며 경보 사이렌이 방 안을 난타합니다.</i>''', 'qtext': '<strong>Q5. [순위 데이터]</strong><br>소매치기 발생 건수가 적은 쪽에서 3번째인 지역의 건수는 얼마인가?', 'placeholder': '숫자 또는 건 입력', 'error': '수치 불일치! 정렬 순서가 꼬였습니다.', 'ans_check': "ans === '23' || ans === '23건'", 'hint': '데이터를 크기 순서대로 정렬했을 때 세 번째로 작은 건수 값을 찾습니다.'},
    {'qnum': 6, "options": ["계급", "계급 아님", "알 수 없음", "해 없음"], 'title': '제2구역: 계급 분류', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "놋쇠 동력 연결관을 수리하다니 성가신 녀석들! 하지만 용의자 연령 데이터를 일정한 단위로 토막 내어 숨겨둔 이 통계학적 구간의 명칭을 알고 있느냐?"<br><br><i>철컥-! 콘솔 보드 상단에 슬롯 회전식 판독기가 조작 장치에서 솟아오릅니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "용의자 연령을 나누는 데이터 구간 용어를 입력해 슬롯 드럼을 회전시켜야 합니다!"''', 'qtext': '<strong>Q6. [계급의 정의]</strong><br>자료를 몇 개의 구간으로 나눌 때, 이 구간을 무엇이라 하는가?', 'placeholder': '한글 단어 입력', 'error': '기초 통계 용어 오류! 결계가 열리지 않습니다.', 'ans_check': "ans === '계급'", 'hint': '수집된 변량을 일정한 간격으로 나눈 구간을 가리키는 통계 용어입니다.'},
    {'qnum': 7, "options": ["도수", "도수 아님", "알 수 없음", "해 없음"], 'title': '도수의 정의', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "계급 드럼을 돌렸나? 그렇다면 각 계급 세그먼트에 분류 매핑된 순수 용의자 머릿수(변량 수)를 지칭하는 진짜 통계 값을 대봐라!"<br><br><i>드럼 슬롯이 빠른 기어 소리와 함께 다시 멈춰 서며 한글 암호 키 입력을 요합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "각 계급 구간에 분포하는 표본의 수를 의미하는 핵심 한글 용어를 입력하십시오!"''', 'qtext': '<strong>Q7. [도수의 정의]</strong><br>각 계급에 속하는 변량의 개수를 무엇이라 하는가?', 'placeholder': '한글 단어 입력', 'error': '회전 기운 조절 오류! 올바른 한글 용어를 쓰십시오.', 'ans_check': "ans === '도수'", 'hint': '각 계급 구간에 속해 있는 자료(변량)의 개수를 의미하는 용어입니다.'},
    {'qnum': 8, "options": ["8", "10", "20", "12"], 'title': '계급의 폭', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "나이 띠별 구간의 너비를 비틀었다. 용의자 연령대가 10대, 20대 등으로 묶여 있을 때, 이 통계 구조의 구간폭 크기는 얼마인지 산출해 기계 축을 고정해라!"<br><br><i>기어 샤프트가 회전하며 흔들리고 있습니다. 정확한 구간 너비를 입력해 회전 진동을 축 상쇄해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "기어 축 손상 방지 가동! 계급 구간 크기의 숫자 수치를 빠르게 주입해 주십시오!"''', 'qtext': '<strong>Q8. [계급의 크기]</strong><br>계급의 너비(크기)는 얼마인가? (자료: 10대, 20대 식일 때의 너비)', 'placeholder': '숫자만 입력', 'error': '너비 부조화! 구간 세그먼트가 틀어졌습니다.', 'ans_check': "ans === '10' || ans === '10세'", 'hint': '한 계급 구간의 너비(끝값 - 시작값)를 계산하여 단위를 포함하지 않은 값을 적습니다.'},
    {'qnum': 9, "options": ["20대", "20대 아님", "알 수 없음", "해 없음"], 'title': '최대 나이 도수', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "나이 분포를 흔들어 스파이의 소속 연령을 숨겼다. 가장 많은 스파이 혐의자들이 분포한 다발적 나이대 계급을 검출해 봐라!"<br><br><i>화면에 붉은색 막대 그래프 노이즈들이 급등락을 보이며 춤을 춥니다. 도수 분포가 압도적으로 높은 연령대 구간을 지명해야 합니다.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "모리아티 측 용의자들이 최다 포진한 연령대 계급 명칭을 입력 창에 전송하십시오!"''', 'qtext': '<strong>Q9. [최대 도수 계급]</strong><br>도수가 가장 큰 계급은 어느 연령대인가? (자료: 10대: 4명, 20대: 8명, 30대: 5명, 40대: 3명)', 'placeholder': '예: 20대', 'error': '용의자 타겟팅 오류!', 'ans_check': "ans === '20대'", 'hint': '도수(인원수)가 8명으로 가장 많이 몰려 있는 나이대 계급을 찾습니다.'},
    {'qnum': 10, "options": ["120", "62", "60", "58"], 'title': '청년 용의자 비율', 'story': '''💥 <strong>[비상 경보: 보일러 증기압 폭발 시작!]</strong> 💥<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "내 계산 엔진을 이렇게 깊이 헤집어 놓다니! 런던 통계국 지하의 원동기 보일러를 강제 자폭시키겠다! 5분 뒤 모두 증기 속에서 질식해 흩어지리라!"<br><br><i>쿠구구궁- 압력 밸브 바늘이 위험 수치인 적색 대역으로 휘어지며 증기가 대량 분출됩니다. 30세 미만 용의자들의 백분율 비율 수치를 긴급 도출해 점화를 차단하십시오.</i><br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "비상! 증기압 해제 밸브 가동! 30세 미만 인원이 차지하는 전체 대비 백분율(%) 상수를 입력하십시오! 제가 압력 차단 패널로 폭발을 억제하고 있겠습니다!"''', 'qtext': '<strong>Q10. [백분율 계산]</strong><br>나이가 30세 미만인 용의자는 전체의 몇 %인가? (단위 생략)', 'placeholder': '숫자만 입력', 'error': '백분율 오차 발생! 차단 셔터 압력 증가!', 'ans_check': "ans === '60' || ans === '60%'", 'hint': '30세 미만 인원수(4명 + 8명 = 12명)가 전체 20명 중에서 차지하는 비율을 백분율(%)로 계산합니다.', "extra_class": "glitch-bg"},
    {'qnum': 11, 'title': '제3구역: 히스토그램', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "보일러 폭발 지연 성공! 하지만 배출용 증기 노즐이 아직 불완전하게 동축 얽혀 있습니다! ⚙️ [기둥형 장부 그림 정렬]"<br><br><i>가로축에 계급, 세로축에 도수를 세워 설계한 고대 차분기관의 정밀 분포 직사각형 그래프 명칭을 입력해 필터를 여십시오.</i>''', 'qtext': '<strong>Q11. [히스토그램]</strong><br>도수분포표를 바탕으로 가로축에 계급, 세로축에 도수를 나타내어 직사각형 모양으로 그린 그래프를 무엇이라 하는가?', 'placeholder': '한글 그래프 이름 입력', 'error': '그래프 타입 인식 불가능!', 'ans_check': "ans === '히스토그램'", 'hint': '도수분포표를 바탕으로 가로에 계급, 세로에 도수를 매칭해 그린 직사각형 모양의 그래프 명칭입니다.'},
    {'qnum': 12, 'title': '가로폭의 속성', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "좋습니다, 그래프 채널을 잡았으나 기둥들의 밑바닥 폭 너비 비례값이 뒤흔들리고 있습니다! ⚙️ [가로폭 눈금 보정]"<br><br><i>지지직- 모니터 상의 직사각형 가로폭 수치가 고유 통계적 물리 속성을 나타내도록 해당 물리 명칭을 입력창에 정확히 기술해 주십시오.</i>''', 'qtext': '<strong>Q12. [히스토그램 가로]</strong><br>히스토그램에서 직사각형의 가로의 길이는 무엇을 의미하는가?', 'placeholder': '예: 계급의 크기', 'error': '가로 기둥 정렬 에러!', 'ans_check': "ans === '계급의크기' || ans === '계급의 크기' || ans === '계급의너비' || ans === '계급의 너비'", 'hint': '도수분포표의 각 직사각형의 가로폭이 나타내는 계급의 간격 크기를 의미합니다.'},
    {'qnum': 13, 'title': '넓이의 총합', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "동력원 85% 결합 도달! 이제 모든 직사각형 넓이의 면적 총합을 연산하여 기어 조율기 수치에 대입해야 합니다!"<br><br><i>직사각형 넓이의 총합 공식을 정의하기 위해, 계급의 크기에 곱해져야 하는 핵심 통계 합산 단어를 밸런서에 전송하십시오.</i>''', 'qtext': '<strong>Q13. [히스토그램 넓이 공식]</strong><br>히스토그램에서 직사각형의 넓이의 합은 (계급의 크기) × ( ? ) 이다. ?에 들어갈 알맞은 말은?', 'placeholder': '한글 단어 입력', 'error': '넓이 총합 불일치! 차분기관 가동 정지 경보!', 'ans_check': "ans === '도수의총합' || ans === '도수의 총합' || ans === '도수의합' || ans === '도수의 합'", 'hint': '모든 직사각형의 넓이 합 공식은 (계급의 크기) * (도수의 총합) 입니다.'},
    {'qnum': 14, 'title': '다각형 그래프', 'story': '''<span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "훌륭합니다! 이제 윗변의 중점들을 모조리 꺾은선으로 팽팽하게 당겨 묶어 잔류 궤적 노이즈를 완벽하게 격리 통제해야 합니다!"<br><br><i>중점들을 이은 녹색 다각형 선분 그래프가 생성됩니다. 이 통계 그래프의 풀 네임을 새겨 넣어 기어를 동기화하십시오.</i>''', 'qtext': '<strong>Q14. [도수분포다각형]</strong><br>히스토그램의 각 직사각형 윗변의 중점을 차례로 선분으로 연결한 그래프를 무엇이라 하는가?', 'placeholder': '한글 그래프 이름 입력', 'error': '꺾은선 궤적 연결 오류!', 'ans_check': "ans === '도수분포다각형'", 'hint': '히스토그램의 각 직사각형 윗변의 중점들을 선분으로 이어 꺾은선 모양으로 만든 다각형 그래프입니다.'},
    {'qnum': 15, 'title': '넓이의 동등성', 'story': '''✨ <strong><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[차분기관 작동 권한 100% 완전 환수]</span></strong> ✨<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "해독 대조 완료! 런던 통계국 차분기관의 작동 권한을 제가 완벽히 장악했습니다! 이제 모리아티의 조작 수치 카드들을 차분기관에서 제거하겠습니다. 다각형과 히스토그램의 면적 비례 관계를 입력하십시오!"<br><br><i>스팀 콘솔 화면들이 일제히 차분하고 투명한 민트색 황동 프레임 조명으로 돌아옵니다.</i><br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "말도 안 돼... 내 조작 장치들이 연산 기어에서 모조리 제거당하다니... 상대도수 균형 빗장으로 마지막 저지를 시도하겠다!"''', 'qtext': '<strong>Q15. [넓이의 성질]</strong><br>도수분포다각형과 가로축으로 둘러싸인 부분의 넓이는 히스토그램의 직사각형들의 넓이의 합과 어떠한가?', 'placeholder': '같다 또는 다르다 입력', 'error': '면적 불균형! 공간 붕괴 위험!', 'ans_check': "ans === '같다'", 'hint': '도수분포다각형과 가로축이 만드는 면적은 히스토그램 전체 직사각형 넓이의 합과 항상 같은 성질을 가집니다.', "extra_class": "glitch-bg"},
    {'qnum': 16, 'title': '제4구역: 상대도수', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "상대도수 비율 빗장이다! 전체 총합에서 특정 계급 도수가 차지하는 물리적 상대적 비율 값을 뜻하는 용어를 해독해 봐라!"<br><br><i>가동 판독기 스크린에 비율 환산 다이얼 판 필드가 활성화되며 한글 키워드를 스캔하기 시작합니다.</i>''', 'qtext': '<strong>Q16. [상대도수의 정의]</strong><br>각 계급의 도수를 도수의 총합으로 나눈 비율을 무엇이라 하는가?', 'placeholder': '한글 단어 입력', 'error': '가중치 데이터 로드 불가!', 'ans_check': "ans === '상대도수'", 'hint': '각 계급의 도수가 전체 도수 총합 중에서 차지하는 상대적인 비율을 뜻하는 용어입니다.'},
    {'qnum': 17, 'title': '상대도수 계산', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "용의자 도수 15명, 도수 총합 50명일 때 해당하는 비율 소수 눈금 수치를 계산해 전송해라!"<br><br><i>지이잉- 차분 기어가 흔들리며 미세 전압의 조정을 위해 정확한 소수 해를 놋쇠 눈금 창에 입력해야 합니다.</i>''', 'qtext': '<strong>Q17. [상대도수 계산]</strong><br>어떤 계급의 도수가 15, 도수의 총합이 50일 때, 이 계급의 상대도수를 구하시오. (소수로 기재)', 'placeholder': '예: 0.5', 'error': '오차 발생! 기계 증기가 더 짙어집니다.', 'ans_check': "ans === '0.3'", 'hint': '특정 계급 도(15)를 전체 도수(50)로 나눈 비율을 소수 값으로 계산합니다.'},
    {'qnum': 18, 'title': '상대도수의 총합', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "상대적인 비율 조각들을 모두 주워 모아 봤자, 그 총합의 한계 상수는 정해져 있을 터!"<br><br><i>보안 격벽의 수량 안전 레버 센서가 작동을 대기합니다. 모든 상대도수를 합쳐 나오는 고정 불변의 총합 상수를 입력하십시오.</i>''', 'qtext': '<strong>Q18. [상대도수 총합]</strong><br>상대도수의 총합은 항상 얼마인가?', 'placeholder': '숫자만 입력', 'error': '한계선 수치 초과! 시스템 잠금!', 'ans_check': "ans === '1'", 'hint': '상대적인 비율들의 총합은 항상 전체를 뜻하는 고정된 자연수 값이 나옵니다.'},
    {'qnum': 19, 'title': '분포 상태 비교', 'story': '''<span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "총합 규모가 상이한 두 용의자 집단의 분포 비교를 비율 없이 단순 머릿수(도수)로 감당할 수 있겠느냐!"<br><br><i>두 표본 집단의 크기가 어긋나 스크린에 경고 문구가 교차 점멸합니다. 상대도수가 비교 분석 도구로써 갖는 실질적 활용성 선언을 입력해 분석 엔진을 가동하십시오.</i>''', 'qtext': '<strong>Q19. [상대도수의 활용]</strong><br>상대도수는 도수의 총합이 다른 두 집단의 분포 상태를 비교할 때 어떠한가? (유용하다 / 불필요하다)', 'placeholder': '유용하다 또는 불필요하다 입력', 'error': '비교 기어 작동 불능!', 'ans_check': "ans === '유용하다'", 'hint': '조사 대상의 전체 총인원수가 서로 다른 두 집단의 성적이나 선호도를 비율로 공평하게 비교할 때의 유용성 여부를 생각합니다.'},
    {'qnum': 20, 'title': '범인 도수 산출', 'story': '''🔮 <strong>[최종 보안 격벽 전면 해제 작동]</strong> 🔮<br><br><span style="color: #60a5fa; text-shadow: 0 0 5px #3b82f6;">[존 H. 왓슨 - 왓슨]</span>: "조사관님! 이제 눈앞의 런던 통계국 메인 탈출용 비밀 나선 계단만 남았습니다! 제 마지막 백업 기어 동력을 계단 개방에 집중하겠습니다! 전체 40명의 통계 요원 중 상대도수 비율이 0.2를 기록한 진범 스파이 도수(인원수)를 정확히 지목해 락을 해제하십시오! 스파이를 검거할 시간입니다!"<br><br><span class="glitch-text" style="color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;">[범죄의 지배자 - 모리아티]</span>: "이럴 수가... 내 완벽한 조작 장부 수치 카드 조각들이... 전면 소거 정지당하다니... 끄아아앗!"''', 'qtext': '<strong>Q20. [도수 구하기]</strong><br>상대도수가 0.2이고 전체 도수가 40명일 때, 이 계급의 도수를 구하시오.', 'placeholder': '숫자만 입력', 'error': '지목 실패! 스파이가 안개 속으로 도망칩니다!', 'ans_check': "ans === '8' || ans === '8명'", 'hint': '(전체 인원 40명) * (상대도수 비율 0.2)를 곱하여 해당 계급의 실제 인원수를 계산합니다.', "extra_class": "glitch-bg"}
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
