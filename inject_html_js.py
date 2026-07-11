import os
import glob

timer_js = """
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
"""

next_stage_replacement = """function nextStage(currentId, nextId, progressPercent) {
            if (currentId === 'intro') startTimer();
            if (nextId === 'outro') clearInterval(timerId);"""

apps = glob.glob('apps/app_*.html')
for app_path in apps:
    with open(app_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if "function startTimer()" not in html:
        # inject just before function nextStage
        html = html.replace('function nextStage', timer_js + '\n        function nextStage')
        html = html.replace('function nextStage(currentId, nextId, progressPercent) {', next_stage_replacement)
        
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Injected JS logic into all 16 HTML files!")
