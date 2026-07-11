import re

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, 'apps')
html_file = os.path.join(apps_dir, 'app_m1_07_escape_room.html')

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# ?ㅽ????뺤씤 諛?二쇱엯
css = """
        .panel-image {
            width: 100%;
            max-height: 250px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
"""
if '.panel-image {' not in content:
    content = content.replace('</style>', css + '</style>')

# intro ?⑤꼸???쇰씪誘몃뱶 ?뚮쭏濡?援먯껜
intro_pattern = r'<div id="intro" class="glass-panel active">[\s\S]*?</div>\s*</div>\s*<!-- Q1 -->'
intro_replacement = '''<div id="intro" class="glass-panel active">
            <h1>?쇰씪誘몃뱶??鍮꾨?</h1>
            <img src="assets/m1_07_solid_geometry/intro.png" alt="Background" class="panel-image">
            <div class="story-box">
                ?щ윭遺꾩? ?댁쭛???щ쭑 ?쒓??대뜲 ?④꺼???덈뜕 誘몄???嫄곕? ?쇰씪誘몃뱶瑜??먯궗 以묒엯?덈떎. ?뺤쓽 臾대뜡???ㅼ뼱???쒓컙, 諛붾떏??爰쇱?硫?源딆? 吏??誘멸턿?쇰줈 ?⑥뼱議뚯뒿?덈떎!<br><br>
                ??誘멸턿? ?낆껜?꾪삎??留덈쾿?쇰줈 蹂댄샇諛쏄퀬 ?덉뒿?덈떎. ?ㅻ㈃泥댁? ?뚯쟾泥댁쓽 ?깆쭏???댁슜???⑥젙???쇳븯怨? 媛곸쥌 ?꾪삎??寃됰꼻?댁? 遺?쇰? 怨꾩궛?섏뿬 20媛쒖쓽 ?뷀샇瑜???댁빞留?吏?곸쑝濡??щ씪媛????덉뒿?덈떎.<br><br>
                ?곗냼????45遺??⑥븯?듬땲?? ?섑븰??吏?쒕? 諛쒗쐶?섏뿬 ?쇰씪誘몃뱶瑜??덉텧?섏꽭??
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('intro', 'panel_q1', 0)">?쒖뒪??蹂듦뎄 ?쒖옉</button>
            </div>
        </div>
        <!-- Q1 -->'''

content = re.sub(intro_pattern, intro_replacement, content)

qs = [
    {"qnum": 1, "title": "?ㅻ㈃泥댁쓽 諛?, "story": "?슚 <strong>[?앹긽???二?</strong><br><br>諛⑹쓽 踰쎈㈃??議곗뿬?듬땲?? ?ㅻ㈃泥댁쓽 紐⑥꽌由ъ? 瑗?쭞???섎? ?뺥솗???몄뼱??踰쎌씠 硫덉땅?덈떎!", "qtext": "<strong>Q1. [?ㅻ㈃泥댁쓽 ?댄빐]</strong><br>?녿㈃??紐⑤몢 吏곸궗媛곹삎???ㅻ㈃泥대? 臾댁뾿?대씪 遺瑜대뒗媛? (?뚰듃: 湲곕뫁)", "placeholder": "?? 媛곷퓭", "error": "?꾪삎 ?대쫫 ?ㅻ쪟!", "ans_check": "ans === '媛곴린??"},
    {"qnum": 2, "title": "?ㅻ㈃泥댁쓽 諛?, "story": "?슚 <strong>[瑗?쭞??移댁슫??</strong><br><br>湲곕뫁??瑗?쭞?먯쓣 ?몄뼱???⑸땲??", "qtext": "<strong>Q2. [瑗?쭞?먯쓽 媛쒖닔]</strong><br>諛묐㈃???ㅺ컖?뺤씤 ?ㅺ컖湲곕뫁??瑗?쭞?먯쓽 媛쒖닔瑜?援ы븯?쒖삤.", "placeholder": "?レ옄留??낅젰", "error": "媛쒖닔 ?ㅻ쪟!", "ans_check": "ans === '10'"},
    {"qnum": 3, "title": "?ㅻ㈃泥댁쓽 諛?, "story": "?슚 <strong>[紐⑥꽌由??뺤씤]</strong><br><br>?대쾲?먮뒗 肉붿쓽 紐⑥꽌由ъ엯?덈떎.", "qtext": "<strong>Q3. [紐⑥꽌由ъ쓽 媛쒖닔]</strong><br>諛묐㈃???↔컖?뺤씤 ?↔컖肉붿쓽 紐⑥꽌由ъ쓽 媛쒖닔瑜?援ы븯?쒖삤.", "placeholder": "?レ옄留??낅젰", "error": "媛쒖닔 ?ㅻ쪟!", "ans_check": "ans === '12'"},
    {"qnum": 4, "title": "?ㅻ㈃泥댁쓽 諛?, "story": "?슚 <strong>[肉붾???硫?</strong><br><br>肉붾???硫댁쓽 媛쒖닔瑜??뚯븘???⑥젙??硫덉땅?덈떎.", "qtext": "<strong>Q4. [硫댁쓽 媛쒖닔]</strong><br>?ш컖肉붾???硫댁쓽 媛쒖닔瑜?援ы븯?쒖삤.", "placeholder": "?レ옄留??낅젰", "error": "媛쒖닔 ?ㅻ쪟!", "ans_check": "ans === '6'"},
    {"qnum": 5, "title": "?ㅻ㈃泥댁쓽 諛?, "story": "?슚 <strong>[?뺣떎硫댁껜??留덈쾿]</strong><br><br>踰쎌씠 嫄곗쓽 ?ㅺ??붿뒿?덈떎! ?뺣떎硫댁껜???대쫫??留욎텛?몄슂.", "qtext": "<strong>Q5. [?뺣떎硫댁껜]</strong><br>媛?硫댁씠 紐⑤몢 ?⑸룞???뺤궪媛곹삎?닿퀬 ??瑗?쭞?먯뿉 紐⑥씠??硫댁쓽 媛쒖닔媛 3媛쒖씤 ?뺣떎硫댁껜???대쫫??援ы븯?쒖삤.", "placeholder": "?? ?뺤쑁硫댁껜", "error": "?뺣떎硫댁껜 ?대쫫 ?ㅻ쪟!", "ans_check": "ans === '?뺤궗硫댁껜'"},
    {"qnum": 6, "title": "?뚮씪?ㅼ쓽 ?꾩옄湲?, "story": "?뤊 <strong>[?꾩옄湲?蹂듭썝]</strong><br><br>?뚯뇙???뚮씪?ㅼ쓽 ??븘由щ? 蹂듭썝?섎젮硫??뚯쟾泥댁쓽 ?⑤㈃???뚯븘???⑸땲??", "qtext": "<strong>Q6. [?뚯쟾泥댁쓽 ?댄빐]</strong><br>?됰㈃?꾪삎????吏곸꽑??異뺤쑝濡??섏뿬 1?뚯쟾 ?쒗궗 ???앷린???낆껜?꾪삎??臾댁뾿?대씪 遺瑜대뒗媛?", "placeholder": "?? ?ㅻ㈃泥?, "error": "?꾪삎 醫낅쪟 ?ㅻ쪟!", "ans_check": "ans === '?뚯쟾泥?"},
    {"qnum": 7, "title": "?뚮씪?ㅼ쓽 ?꾩옄湲?, "story": "?뤊 <strong>[?먭린?μ쓽 ?⑤㈃]</strong><br><br>?먭린??紐⑥뼇 ?꾩옄湲곗쓽 議곌컖??留욎땅?덈떎.", "qtext": "<strong>Q7. [?뚯쟾異뺢낵 ?⑤㈃ 1]</strong><br>?먭린?μ쓣 ?뚯쟾異뺤쓣 ?ы븿?섎뒗 ?됰㈃?쇰줈 ?먮? ???앷린???⑤㈃??紐⑥뼇? 臾댁뾿?멸??", "placeholder": "?? ?ш컖??, "error": "?⑤㈃ 紐⑥뼇 ?ㅻ쪟!", "ans_check": "ans === '吏곸궗媛곹삎'"},
    {"qnum": 8, "title": "?뚮씪?ㅼ쓽 ?꾩옄湲?, "story": "?뤊 <strong>[?먮퓭???⑤㈃]</strong><br><br>?먮퓭 紐⑥뼇 ?쒓퍚???⑤㈃?낅땲??", "qtext": "<strong>Q8. [?뚯쟾異뺢낵 ?⑤㈃ 2]</strong><br>?먮퓭???뚯쟾異뺤뿉 ?섏쭅???됰㈃?쇰줈 ?먮? ???앷린???⑤㈃??紐⑥뼇? 臾댁뾿?멸??", "placeholder": "?? ???, "error": "?⑤㈃ 紐⑥뼇 ?ㅻ쪟!", "ans_check": "ans === '??"},
    {"qnum": 9, "title": "?뚮씪?ㅼ쓽 ?꾩옄湲?, "story": "?뤊 <strong>[?뚯쟾泥??앹꽦]</strong><br><br>吏곴컖?쇨컖??紐⑥뼇???꾧뎄瑜??뚯쟾?쒖폒???⑸땲??", "qtext": "<strong>Q9. [?뚯쟾泥댁쓽 醫낅쪟]</strong><br>吏곴컖?쇨컖?뺤쓣 吏곴컖??? ??蹂??異뺤쑝濡??섏뿬 1?뚯쟾 ?쒗궎硫??앷린???꾪삎? 臾댁뾿?멸??", "placeholder": "?? ?먭린??, "error": "?꾪삎 ?대쫫 ?ㅻ쪟!", "ans_check": "ans === '?먮퓭'"},
    {"qnum": 10, "title": "?뚮씪?ㅼ쓽 ?꾩옄湲?, "story": "?뤊 <strong>[援ъ쓽 ?⑤㈃]</strong><br><br>媛???꾨꼍???꾪삎, 援ъ쓽 ?깆쭏?낅땲??", "qtext": "<strong>Q10. [援ъ쓽 ?깆쭏]</strong><br>援щ? ?대뼡 ?됰㈃?쇰줈 ?먮Ⅴ?붾씪??洹??⑤㈃? ??긽 ?대뼡 紐⑥뼇?멸??", "placeholder": "?? ???, "error": "?⑤㈃ ?ㅻ쪟!", "ans_check": "ans === '??"},
    {"qnum": 11, "title": "?⑷툑 ?곸옄??寃됰꼻??, "story": "?截?<strong>[?⑷툑 ?꾧툑]</strong><br><br>?뚮씪?ㅼ쓽 ?곸옄瑜??⑷툑?쇰줈 ?꾧툑?댁빞 ?⑸땲?? ?꾧툑??寃됰꼻?대? ?뺥솗??怨꾩궛?섏꽭??", "qtext": "<strong>Q11. [媛곴린?μ쓽 寃됰꼻??</strong><br>諛묐㈃??媛濡?3cm, ?몃줈 4cm??吏곸궗媛곹삎?닿퀬, ?믪씠媛 5cm??吏곸쑁硫댁껜??寃됰꼻?대? 援ы븯?쒖삤.", "placeholder": "?レ옄留??낅젰", "error": "?꾧툑 硫댁쟻 ?ㅻ쪟!", "ans_check": "ans === '94'"},
    {"qnum": 12, "title": "?⑷툑 ?곸옄??寃됰꼻??, "story": "?截?<strong>[?먰넻 ?꾧툑]</strong><br><br>?대쾲?먮뒗 ?먰넻 紐⑥뼇 ?곸옄?낅땲?? (?먯＜?⑥? ?濡?怨꾩궛, ?쒓? '?뚯씠'濡??낅젰)", "qtext": "<strong>Q12. [?먭린?μ쓽 寃됰꼻??</strong><br>諛묐㈃??諛섏?由꾩씠 2cm?닿퀬 ?믪씠媛 6cm???먭린?μ쓽 寃됰꼻?대? 援ы븯?쒖삤.", "placeholder": "?? 10?뚯씠", "error": "?꾧툑 硫댁쟻 ?ㅻ쪟!", "ans_check": "ans === '32?뚯씠'"},
    {"qnum": 13, "title": "?⑷툑 ?곸옄??寃됰꼻??, "story": "?截?<strong>[?쇰씪誘몃뱶 ?꾧툑]</strong><br><br>?뺤궗媛곷퓭 紐⑥뼇 ?쒓퍚???꾧툑?댁빞 ?⑸땲??", "qtext": "<strong>Q13. [?ш컖肉붿쓽 寃됰꼻??</strong><br>諛묐㈃????蹂??湲몄씠媛 4cm???뺤궗媛곹삎?닿퀬, ?녿㈃???쇨컖?뺤쓽 ?믪씠媛 5cm???뺤궗媛곷퓭??寃됰꼻?대? 援ы븯?쒖삤.", "placeholder": "?レ옄留??낅젰", "error": "?꾧툑 硫댁쟻 ?ㅻ쪟!", "ans_check": "ans === '56'"},
    {"qnum": 14, "title": "?⑷툑 ?곸옄??寃됰꼻??, "story": "?截?<strong>[?먮퓭 ?꾧툑]</strong><br><br>?먮퓭 紐⑥뼇 ?쒕떒???꾧툑?⑸땲??", "qtext": "<strong>Q14. [?먮퓭??寃됰꼻??</strong><br>諛묐㈃??諛섏?由꾩씠 3cm?닿퀬, 紐⑥꽑??湲몄씠媛 5cm???먮퓭??寃됰꼻?대? 援ы븯?쒖삤.", "placeholder": "?? 10?뚯씠", "error": "?꾧툑 硫댁쟻 ?ㅻ쪟!", "ans_check": "ans === '24?뚯씠'"},
    {"qnum": 15, "title": "?⑷툑 ?곸옄??寃됰꼻??, "story": "?截?<strong>[?⑷툑 援ъ뒳]</strong><br><br>?μ떇??援ъ뒳???꾩쟾???꾧툑?댁빞 ?⑸땲??", "qtext": "<strong>Q15. [援ъ쓽 寃됰꼻??</strong><br>諛섏?由꾩쓽 湲몄씠媛 3cm??援ъ쓽 寃됰꼻?대? 援ы븯?쒖삤.", "placeholder": "?? 10?뚯씠", "error": "?꾧툑 硫댁쟻 ?ㅻ쪟!", "ans_check": "ans === '36?뚯씠'"},
    {"qnum": 16, "title": "?앸챸??臾?梨꾩슦湲?, "story": "?뵎 <strong>[留덉?留?愿臾?</strong><br><br>?덉텧 ?μ튂瑜?媛?숉븯?ㅻ㈃ ?щ윭 ?낆껜?꾪삎 紐⑥뼇???섏“???앸챸??臾쇱쓣 ?뺥솗??遺?쇰쭔??梨꾩썙???⑸땲??", "qtext": "<strong>Q16. [媛곴린?μ쓽 遺??</strong><br>諛묐㈃???볦씠媛 20cm짼?닿퀬 ?믪씠媛 8cm??媛곴린?μ쓽 遺?쇰? 援ы븯?쒖삤.", "placeholder": "?レ옄留??낅젰", "error": "?섏븬 議곗젅 ?ㅽ뙣!", "ans_check": "ans === '160'"},
    {"qnum": 17, "title": "?앸챸??臾?梨꾩슦湲?, "story": "?뵎 <strong>[?먭린???섏“]</strong><br><br>媛?????먰넻 ?섏“??臾쇱쓣 梨꾩썎?덈떎.", "qtext": "<strong>Q17. [?먭린?μ쓽 遺??</strong><br>諛묐㈃??諛섏?由꾩씠 4cm?닿퀬 ?믪씠媛 5cm???먭린?μ쓽 遺?쇰? 援ы븯?쒖삤.", "placeholder": "?? 10?뚯씠", "error": "臾쇱씠 ?섏묩?덈떎!", "ans_check": "ans === '80?뚯씠'"},
    {"qnum": 18, "title": "?앸챸??臾?梨꾩슦湲?, "story": "?뵎 <strong>[?먮퓭 ?섏“]</strong><br><br>?먮퓭 ?섏“??臾쇱쓣 議곗떖?ㅻ읇寃?梨꾩썎?덈떎.", "qtext": "<strong>Q18. [?먮퓭??遺??</strong><br>諛묐㈃??諛섏?由꾩씠 3cm?닿퀬 ?믪씠媛 4cm???먮퓭??遺?쇰? 援ы븯?쒖삤.", "placeholder": "?? 10?뚯씠", "error": "臾쇱씠 ?섏묩?덈떎!", "ans_check": "ans === '12?뚯씠'"},
    {"qnum": 19, "title": "?앸챸??臾?梨꾩슦湲?, "story": "?뵎 <strong>[?κ렐 ?섏“]</strong><br><br>援?紐⑥뼇 ?섏“??遺?쇰? 怨꾩궛?섏꽭??", "qtext": "<strong>Q19. [援ъ쓽 遺??</strong><br>諛섏?由꾩쓽 湲몄씠媛 3cm??援ъ쓽 遺?쇰? 援ы븯?쒖삤.", "placeholder": "?? 10?뚯씠", "error": "臾쇱씠 遺議깊빀?덈떎!", "ans_check": "ans === '36?뚯씠'"},
    {"qnum": 20, "title": "?앸챸??臾?梨꾩슦湲?, "story": "?뵎 <strong>[理쒖쥌 鍮꾨? 肄붾뱶]</strong><br><br>紐⑤뱺 ?섏“??臾쇱씠 李쇱뒿?덈떎! 留덉?留?鍮꾨? 肄붾뱶瑜??낅젰?섏꽭??", "qtext": "<strong>Q20. [遺?쇱쓽 鍮?</strong><br>諛묐㈃??諛섏?由꾧낵 ?믪씠媛 紐⑤몢 媛숈? ?먮퓭, 援? ?먭린?μ쓽 遺?쇱쓽 鍮꾨? 援ы븯?쒖삤.", "placeholder": "?? 1:2:3", "error": "肄붾뱶媛 ??몄뒿?덈떎!", "ans_check": "ans === '1:2:3'"}
]

# Generate panels
panels_html = ""
for i, q in enumerate(qs):
    qnum = q['qnum']
    title = q['title']
    story = q['story']
    qtext = q['qtext']
    placeholder = q['placeholder']
    error = q['error']
    
    prev_stage = f"'panel_q{qnum-1}'" if qnum > 1 else "'intro'"
    prev_progress = (qnum-1)*5
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    
    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel">
            <h2>??{qnum}援ъ뿭: {title}</h2>
            <img src="assets/m1_07_solid_geometry/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">?뱶 ?댁쟾 ???/button>
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
                <button class="btn" onclick="checkQ{qnum}()">{'?좏빆 ?쒖옉' if qnum==1 and "update_app_07.py"=="update_app_04.py" else '誘멸턿 吏꾩엯' if qnum==1 and "update_app_07.py"=="update_app_06.py" else '?쒖뒪??蹂듦뎄 ?쒖옉' if qnum==1 else '?ㅼ쓬?쇰줈' if qnum < 20 else '?덉텧?섍린'}</button>
            </div>
        </div>
'''
    panels_html += panel

# Outro panel
outro_html = '''
        <!-- ?꾩썐?몃줈 -->
        <div id="outro" class="glass-panel">
            <h1>?덉텧 ?깃났!</h1>
            <h2>?쇰씪誘몃뱶??鍮꾨?</h2>
            <img src="assets/m1_07_solid_geometry/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">?щ윭遺꾨뱾??留덉?留??뷀샇 '1:2:3'???낅젰?섏옄, 援녠쾶 ?ロ? ?덈뜕 ?쇰씪誘몃뱶??泥쒖옣???대━硫??잛븘吏??紐⑤옒 ?ъ씠濡???以꾧린 ?덈????뉗궡???ㅼ뼱?듬땲?? 
                留덈쾿??紐⑤옒?쒓퀎媛 硫덉텛怨? ?щ윭遺꾩? 遺?쇱쓽 鍮꾩쑉??留욎떠 李⑥삤瑜??앸챸??臾쇨린?μ쓣 ?怨?吏?곸쑝濡?臾댁궗???좎삤由낅땲?? 
                ?ㅻ㈃泥댁? ?뚯쟾泥댁쓽 ?깆쭏, 洹몃━怨?寃됰꼻?댁? 遺?쇱쓽 鍮꾨????꾨꼍?섍쾶 ?뚰뿤移??щ윭遺? 怨좊? ?댁쭛??誘멸턿 ?덉텧????깃났?덉뒿?덈떎!</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">?뱶 ?댁쟾 ???/button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">?ㅼ떆 ?꾩쟾?섍린</button>
        </div>
'''
panels_html += outro_html

# Generate JS checks
js_checks = ""
for q in qs:
    qnum = q['qnum']
    ans_check = q['ans_check']
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    victory_call = 'playVictory();' if qnum == 20 else 'playSuccess();'
    
    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace(/\\s+/g, '');
            if ({ans_check}) {{
                {victory_call} 
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                showError('panel_q{qnum}', 'error{qnum}');
            }}
        }}
'''
    js_checks += js

# Replace in content
start_panel_idx = content.find('<!-- Q1 -->')
end_panel_idx = content.find('        <script>', start_panel_idx)

if start_panel_idx != -1 and end_panel_idx != -1:
    content = content[:start_panel_idx] + panels_html + content[end_panel_idx:]

start_js_idx = content.find('        // Q1\n')
if start_js_idx == -1:
    start_js_idx = content.find('        // Q1\r\n')
end_js_idx = content.find('        window.onload = () => {', start_js_idx)

if start_js_idx != -1 and end_js_idx != -1:
    content = content[:start_js_idx] + js_checks + content[end_js_idx:]

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("App 07 updated successfully with images.")

