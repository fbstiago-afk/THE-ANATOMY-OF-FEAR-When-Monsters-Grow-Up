# -*- coding: utf-8 -*-
"""HTML Content components. Templates use {{DAX expression}} placeholders.
to_dax() turns a template into a DAX string concatenation; render() fills
placeholders with sample values for the design preview only."""
import re

GHOST = """<style>
.fg{width:100%;height:100%;display:flex;align-items:center;justify-content:center;overflow:hidden}
.fg svg{width:88%;height:auto;filter:drop-shadow(0 0 16px rgba(189,154,247,.55));animation:fgfloat 7s ease-in-out infinite}
.fg .eye{animation:fgblink 6s infinite;transform-origin:center;transform-box:fill-box}
.fg .flame{animation:fgflick 1.8s ease-in-out infinite;transform-origin:50% 100%;transform-box:fill-box}
@keyframes fgfloat{0%,100%{transform:translateY(4px)}50%{transform:translateY(-10px)}}
@keyframes fgblink{0%,90%,100%{transform:scaleY(1)}93%{transform:scaleY(.08)}96%{transform:scaleY(1)}}
@keyframes fgflick{0%,100%{transform:scale(1,1);opacity:1}50%{transform:scale(.88,1.12);opacity:.85}}
@media (prefers-reduced-motion: reduce){.fg svg,.fg .eye,.fg .flame{animation:none}}
</style>
<div class='fg'><svg viewBox='0 0 220 260' aria-hidden='true' focusable='false'>
<defs>
<linearGradient id='fgb' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#F4EBDD' stop-opacity='.92'/><stop offset='.55' stop-color='#D9CDE8' stop-opacity='.62'/><stop offset='1' stop-color='#BD9AF7' stop-opacity='0'/></linearGradient>
<radialGradient id='fgf' cx='.5' cy='.6' r='.5'><stop offset='0' stop-color='#FFF3D6'/><stop offset='.55' stop-color='#FFB886'/><stop offset='1' stop-color='#FF858E' stop-opacity='0'/></radialGradient>
</defs>
<path d='M112 18 C74 18 56 50 54 92 C51 138 44 176 24 218 C42 212 54 222 64 240 C74 226 86 228 98 244 C108 230 120 230 130 244 C140 230 152 228 164 238 C172 206 176 166 172 118 C168 58 150 18 112 18 Z' fill='url(#fgb)'/>
<path d='M60 150 C70 170 66 196 50 214' stroke='#F4EBDD' stroke-opacity='.25' stroke-width='3' fill='none'/>
<path d='M150 112 C158 150 160 188 154 226' stroke='#BD9AF7' stroke-opacity='.30' stroke-width='3' fill='none'/>
<ellipse class='eye' cx='95' cy='88' rx='7' ry='12' fill='#151020' transform='rotate(-8 95 88)'/>
<ellipse class='eye' cx='129' cy='88' rx='7' ry='12' fill='#151020' transform='rotate(8 129 88)'/>
<path d='M168 132 C182 136 190 144 194 154' stroke='#E3D8EC' stroke-width='9' fill='none' stroke-linecap='round' opacity='.75'/>
<rect x='189' y='154' width='12' height='30' rx='2' fill='#F4EBDD'/>
<path d='M195 154 L195 149' stroke='#151020' stroke-width='2'/>
<ellipse cx='195' cy='150' rx='24' ry='26' fill='url(#fgf)' opacity='.35'/>
<path class='flame' d='M195 132 C201 140 202 145 195 150 C188 145 189 140 195 132 Z' fill='url(#fgf)'/>
</svg></div>"""

NIGHTMARE = """<style>
.nm{font-family:'Segoe UI',sans-serif;color:#F4EBDD;display:flex;gap:14px;align-items:center;height:100%;padding:10px 16px;box-sizing:border-box;border:1px solid #6B5590;border-radius:16px;background:linear-gradient(160deg,#2A1B37 0%,#1A1124 100%);box-shadow:inset 0 0 28px rgba(255,133,142,.14)}
.nm .ic{flex:0 0 104px}
.nm .num{font-family:Georgia,serif;font-size:62px;line-height:.95;color:#FF858E;letter-spacing:-1px}
.nm .of{font-size:14px;font-weight:600;margin-top:2px}
.nm .q{font-family:Georgia,serif;font-style:italic;font-size:19px;margin:5px 0 1px;color:#F4EBDD}
.nm .d{font-size:12.5px;line-height:1.25;color:#C9B8E0}
.nm .err{animation:nmflick 3.4s infinite}
.nm .drip{animation:nmdrip 4s ease-in infinite}
@keyframes nmflick{0%,46%,54%,100%{opacity:1}50%{opacity:.25}}
@keyframes nmdrip{0%{transform:translateY(0);opacity:1}80%{transform:translateY(16px);opacity:1}100%{transform:translateY(20px);opacity:0}}
@media (prefers-reduced-motion: reduce){.nm .err,.nm .drip{animation:none}}
</style>
<div class='nm'>
<svg class='ic' width='104' height='132' viewBox='0 0 118 150' aria-hidden='true' focusable='false'>
<rect x='6' y='14' width='106' height='122' rx='6' fill='#151020' stroke='#BD9AF7' stroke-width='2'/>
<rect x='6' y='14' width='106' height='20' rx='6' fill='#FF858E'/>
<path d='M20 34 C20 44 26 44 26 34 Z M52 34 C52 50 60 50 60 34 Z M88 34 C88 41 93 41 93 34 Z' fill='#FF858E'/>
<circle class='drip' cx='23' cy='42' r='3' fill='#FF858E'/>
<g stroke='#5A4775' stroke-width='1'><line x1='6' y1='60' x2='112' y2='60'/><line x1='6' y1='85' x2='112' y2='85'/><line x1='6' y1='110' x2='112' y2='110'/><line x1='42' y1='34' x2='42' y2='136'/><line x1='77' y1='34' x2='77' y2='136'/></g>
<rect x='12' y='44' width='24' height='7' rx='3' fill='#F4EBDD'/>
<rect x='83' y='44' width='22' height='7' rx='3' fill='#F4EBDD'/>
<rect class='err' x='47' y='40' width='25' height='15' rx='2' fill='none' stroke='#FF858E' stroke-width='1.6' stroke-dasharray='3 2'/>
<rect x='12' y='69' width='24' height='7' rx='3' fill='#B4F2C4'/>
<rect x='50' y='66' width='22' height='7' rx='3' fill='#B4F2C4' opacity='.45'/>
<rect x='47' y='70' width='24' height='7' rx='3' fill='#B4F2C4'/>
<rect x='83' y='69' width='24' height='7' rx='3' fill='#B4F2C4'/>
<rect x='12' y='94' width='12' height='7' rx='3' fill='#FFB886'/>
<rect x='55' y='94' width='17' height='7' rx='3' fill='#FFB886'/>
<g fill='#FFB886'><circle cx='87' cy='97.5' r='2.4'/><circle cx='94' cy='97.5' r='2.4'/><circle cx='101' cy='97.5' r='2.4'/></g>
<path d='M10 124 L28 116 L40 128 L58 114 L72 127 L90 117 L108 126' fill='none' stroke='#FF858E' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/>
<line x1='100' y1='0' x2='100' y2='16' stroke='#C9B8E0' stroke-width='1'/>
<g fill='#151020' stroke='#C9B8E0' stroke-width='1'><ellipse cx='100' cy='9' rx='4' ry='3.4'/></g>
</svg>
<div>
<div class='num'>{{FORMAT ( [Data Nightmare Respondents], "#,0" )}}</div>
<div class='of'>of {{FORMAT ( [Responses], "#,0" )}} respondents &#183; {{FORMAT ( [Data Nightmare %], "0.0%" )}}</div>
<div class='q'>&#8220;{{[Top Data Nightmare]}}&#8221;</div>
<div class='d'>{{[Top Data Nightmare Detail]}}</div>
</div>
</div>"""

SAMPLE = {
    'FORMAT ( [Data Nightmare Respondents], "#,0" )': '23',
    'FORMAT ( [Responses], "#,0" )': '105',
    'FORMAT ( [Data Nightmare %], "0.0%" )': '21.9%',
    '[Top Data Nightmare]': 'It arrives a mess',
    '[Top Data Nightmare Detail]': 'missing values, duplicates, inconsistent formats',
}

PH = re.compile(r"\{\{(.+?)\}\}", re.S)

def to_dax(tpl):
    parts = []
    pos = 0
    for mm in PH.finditer(tpl):
        lit = tpl[pos:mm.start()]
        lit = lit.replace('\n', '')
        if lit:
            parts.append('"' + lit.replace('"', '""') + '"')
        parts.append(mm.group(1).strip())
        pos = mm.end()
    lit = tpl[pos:].replace('\n', '')
    if lit:
        parts.append('"' + lit.replace('"', '""') + '"')
    return "\n    & ".join(parts)

def render(tpl):
    return PH.sub(lambda mm: SAMPLE[mm.group(1).strip()], tpl)

# =====================================================================
# Tooltip-page animations (decorative, CSS only, reduced-motion aware)
# =====================================================================
_RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

TT_EYES = """<style>
.ey{width:100%;height:100%;display:flex;align-items:center;justify-content:center}
.ey svg{width:92%;height:auto}
.ey .lid{animation:eyblink 4.2s infinite;transform-origin:center;transform-box:fill-box}
.ey .pu{animation:eylook 5s ease-in-out infinite}
.ey .glow{animation:eyglow 3s ease-in-out infinite}
@keyframes eyblink{0%,44%,50%,100%{transform:scaleY(1)}47%{transform:scaleY(.05)}}
@keyframes eylook{0%,20%{transform:translateX(0)}30%,45%{transform:translateX(-4px)}60%,75%{transform:translateX(4px)}90%,100%{transform:translateX(0)}}
@keyframes eyglow{0%,100%{opacity:.35}50%{opacity:.7}}
""" + _RM + """</style>
<div class='ey'><svg viewBox='0 0 80 52' aria-hidden='true' focusable='false'>
<ellipse class='glow' cx='40' cy='26' rx='38' ry='20' fill='#FFB886' opacity='.4' style='filter:blur(8px)'/>
<g class='lid'><ellipse cx='24' cy='26' rx='12' ry='8' fill='#FFE7C2'/><ellipse cx='56' cy='26' rx='12' ry='8' fill='#FFE7C2'/>
<g class='pu'><circle cx='24' cy='26' r='4.2' fill='#151020'/><circle cx='56' cy='26' r='4.2' fill='#151020'/><circle cx='25.5' cy='24.5' r='1.2' fill='#F4EBDD'/><circle cx='57.5' cy='24.5' r='1.2' fill='#F4EBDD'/></g></g>
</svg></div>"""

TT_SPIDER = """<style>
.sp{width:100%;height:100%;overflow:hidden;position:relative}
.sp svg{width:100%;height:100%}
.sp .bob{animation:spdrop 4.5s ease-in-out infinite;transform-origin:40px 0}
.sp .leg{animation:spwig .5s ease-in-out infinite alternate;transform-origin:center;transform-box:fill-box}
.sp .eye{animation:spblink 3s infinite}
@keyframes spdrop{0%{transform:translateY(-26px) rotate(0)}35%{transform:translateY(4px) rotate(6deg)}55%{transform:translateY(0) rotate(-6deg)}75%{transform:translateY(3px) rotate(3deg)}100%{transform:translateY(-26px) rotate(0)}}
@keyframes spwig{from{transform:rotate(-6deg)}to{transform:rotate(6deg)}}
@keyframes spblink{0%,90%,100%{opacity:1}94%{opacity:.1}}
""" + _RM + """</style>
<div class='sp'><svg viewBox='0 0 80 80' aria-hidden='true' focusable='false'><g class='bob'>
<line x1='40' y1='0' x2='40' y2='44' stroke='#C9B8E0' stroke-width='1'/>
<g class='leg' stroke='#BD9AF7' stroke-width='2' fill='none' stroke-linecap='round'>
<path d='M34 50 L22 42 L16 48'/><path d='M34 53 L20 52 L14 58'/><path d='M34 56 L22 62 L18 70'/><path d='M35 58 L28 68 L26 76'/>
<path d='M46 50 L58 42 L64 48'/><path d='M46 53 L60 52 L66 58'/><path d='M46 56 L58 62 L62 70'/><path d='M45 58 L52 68 L54 76'/></g>
<ellipse cx='40' cy='54' rx='9' ry='10' fill='#24172F' stroke='#BD9AF7' stroke-width='1.5'/>
<circle cx='40' cy='44' r='6' fill='#24172F' stroke='#BD9AF7' stroke-width='1.5'/>
<g class='eye' fill='#FF858E'><circle cx='37.6' cy='43.5' r='1.6'/><circle cx='42.4' cy='43.5' r='1.6'/></g>
<path d='M36 57 L44 57 M38 53 L42 53' stroke='#FF858E' stroke-width='1.2'/></g></svg></div>"""

TT_TOMB = """<style>
.tb{width:100%;height:100%;overflow:hidden}
.tb svg{width:100%;height:100%}
.tb .gh{animation:tbpeek 4s ease-in-out infinite}
.tb .arm{animation:tbwave .6s ease-in-out infinite alternate;transform-origin:62px 30px}
.tb .fog{animation:tbfog 6s ease-in-out infinite}
@keyframes tbpeek{0%,15%{transform:translateY(30px)}35%,70%{transform:translateY(0)}90%,100%{transform:translateY(30px)}}
@keyframes tbwave{from{transform:rotate(-14deg)}to{transform:rotate(14deg)}}
@keyframes tbfog{0%,100%{transform:translateX(-6px);opacity:.35}50%{transform:translateX(6px);opacity:.6}}
""" + _RM + """</style>
<div class='tb'><svg viewBox='0 0 90 70' aria-hidden='true' focusable='false'>
<g class='gh'><path d='M30 60 L30 26 C30 10 60 10 60 26 L60 60 Z' fill='#B4F2C4'/>
<circle cx='40' cy='26' r='3' fill='#151020'/><circle cx='50' cy='26' r='3' fill='#151020'/><ellipse cx='45' cy='35' rx='3' ry='4' fill='#151020'/>
<path class='arm' d='M60 34 C66 30 68 26 70 20' stroke='#B4F2C4' stroke-width='5' fill='none' stroke-linecap='round'/></g>
<path d='M18 70 L18 44 C18 30 72 30 72 44 L72 70 Z' fill='#3A2D4B' stroke='#5A4775' stroke-width='1.5'/>
<text x='45' y='53' text-anchor='middle' font-family='Georgia' font-size='8' fill='#F4EBDD'>STILL</text>
<text x='45' y='63' text-anchor='middle' font-family='Georgia' font-size='8' fill='#F4EBDD'>HERE</text>
<ellipse class='fog' cx='45' cy='68' rx='42' ry='5' fill='#BD9AF7' opacity='.4'/></svg></div>"""

TT_CANDLE = """<style>
.cd{width:100%;height:100%;display:flex;align-items:flex-end;justify-content:center}
.cd svg{width:70%;height:auto}
.cd .fl{animation:cdflick 1.3s ease-in-out infinite;transform-origin:50% 100%;transform-box:fill-box}
.cd .halo{animation:cdhalo 2.6s ease-in-out infinite}
.cd .drip{animation:cddrip 5s ease-in infinite}
@keyframes cdflick{0%,100%{transform:scale(1,1) skewX(0)}30%{transform:scale(.9,1.12) skewX(4deg)}60%{transform:scale(1.05,.92) skewX(-4deg)}}
@keyframes cdhalo{0%,100%{opacity:.25}50%{opacity:.5}}
@keyframes cddrip{0%,60%{transform:translateY(0)}100%{transform:translateY(14px)}}
""" + _RM + """</style>
<div class='cd'><svg viewBox='0 0 50 70' aria-hidden='true' focusable='false'>
<circle class='halo' cx='25' cy='20' r='18' fill='#FFB886'/>
<path class='fl' d='M25 6 C31 15 31 21 25 26 C19 21 19 15 25 6 Z' fill='#FFB886'/>
<path d='M25 14 C27 18 27 21 25 23 C23 21 23 18 25 14 Z' fill='#FFF3D6'/>
<line x1='25' y1='26' x2='25' y2='31' stroke='#151020' stroke-width='1.5'/>
<rect x='16' y='30' width='18' height='36' rx='2' fill='#F4EBDD'/>
<path class='drip' d='M19 30 L19 38 C19 41 22 41 22 38 L22 30 Z' fill='#F4EBDD'/></svg></div>"""

TT_SHEET = """<style>
.hs{width:100%;height:100%;display:flex;align-items:center;justify-content:center}
.hs svg{width:94%;height:auto}
.hs .lid{animation:hsopen 3.6s infinite;transform-origin:center;transform-box:fill-box}
.hs .pu{animation:hslook 3.6s ease-in-out infinite}
.hs .rowshake{animation:hsshake 2.4s infinite}
@keyframes hsopen{0%,25%{transform:scaleY(.08)}35%,80%{transform:scaleY(1)}90%,100%{transform:scaleY(.08)}}
@keyframes hslook{0%,40%{transform:translateX(0)}55%{transform:translateX(-2px)}70%{transform:translateX(2px)}100%{transform:translateX(0)}}
@keyframes hsshake{0%,88%,100%{transform:translateX(0)}91%{transform:translateX(-2px)}94%{transform:translateX(2px)}97%{transform:translateX(-1px)}}
""" + _RM + """</style>
<div class='hs'><svg viewBox='0 0 80 60' aria-hidden='true' focusable='false'>
<rect x='4' y='6' width='72' height='50' rx='4' fill='#151020' stroke='#BD9AF7' stroke-width='1.6'/>
<rect x='4' y='6' width='72' height='11' rx='4' fill='#FF858E'/>
<g stroke='#5A4775' stroke-width='1'><line x1='4' y1='30' x2='76' y2='30'/><line x1='4' y1='43' x2='76' y2='43'/><line x1='28' y1='17' x2='28' y2='56'/><line x1='52' y1='17' x2='52' y2='56'/></g>
<g class='rowshake'><rect x='9' y='21' width='14' height='5' rx='2' fill='#F4EBDD'/><rect x='57' y='21' width='14' height='5' rx='2' fill='#F4EBDD'/></g>
<g class='lid'><ellipse cx='40' cy='23.5' rx='9' ry='5' fill='#FFE7C2'/><circle class='pu' cx='40' cy='23.5' r='2.6' fill='#151020'/></g>
<rect x='9' y='34' width='14' height='5' rx='2' fill='#B4F2C4'/><rect x='33' y='34' width='14' height='5' rx='2' fill='#B4F2C4'/><rect x='57' y='34' width='14' height='5' rx='2' fill='#B4F2C4' opacity='.5'/>
<rect x='9' y='47' width='7' height='5' rx='2' fill='#FFB886'/><rect x='40' y='47' width='7' height='5' rx='2' fill='#FFB886'/><circle cx='61' cy='49.5' r='1.6' fill='#FFB886'/><circle cx='66' cy='49.5' r='1.6' fill='#FFB886'/></svg></div>"""

TT_BAT = """<style>
.bt{width:100%;height:100%;overflow:hidden;position:relative}
.bt svg{position:absolute;top:30%;left:0;width:46%;height:auto;animation:btfly 4.8s linear infinite}
.bt .w{animation:btflap .22s ease-in-out infinite alternate;transform-origin:50% 50%;transform-box:fill-box}
@keyframes btfly{0%{transform:translate(-110%,10px)}25%{transform:translate(20%,-8px)}50%{transform:translate(70%,12px)}75%{transform:translate(130%,-6px)}100%{transform:translate(230%,8px)}}
@keyframes btflap{from{transform:scaleY(1)}to{transform:scaleY(.35)}}
""" + _RM + """</style>
<div class='bt'><svg viewBox='0 0 40 20' aria-hidden='true' focusable='false'>
<g class='w'><path d='M20 10 C16 4 10 2 2 4 C6 7 7 10 5 14 C9 12 13 12 15 15 C16 12 18 11 20 12 C22 11 24 12 25 15 C27 12 31 12 35 14 C33 10 34 7 38 4 C30 2 24 4 20 10 Z' fill='#BD9AF7'/></g>
<circle cx='18.5' cy='9.5' r='.9' fill='#FF858E'/><circle cx='21.5' cy='9.5' r='.9' fill='#FF858E'/></svg></div>"""

# ---------------------------------------------------------------------
# Ghost case file (one respondent) - DAX built around a template.
# ---------------------------------------------------------------------
GHOST_CARD = """<style>
.gc{font-family:'Segoe UI',sans-serif;color:#F4EBDD;height:100%;box-sizing:border-box;padding:10px 14px 8px;position:relative;overflow:hidden;
background:radial-gradient(circle at 88% 6%,rgba(189,154,247,.28),rgba(30,20,43,0) 42%),#1E142B}
.gc .hd{display:flex;gap:12px;align-items:center}
.gc .gs{flex:0 0 74px;height:86px}
.gc .gs svg{width:74px;height:86px;animation:gcfloat 3.8s ease-in-out infinite}
.gc .eye{animation:gcblink 4s infinite;transform-origin:center;transform-box:fill-box}
.gc .kick{font-size:10px;letter-spacing:1.6px;color:#BD9AF7;font-weight:700}
.gc .ttl{font-family:Georgia,serif;font-size:21px;line-height:1.15;margin:2px 0}
.gc .sub{font-size:11px;color:#C9B8E0}
.gc .cols{display:flex;gap:12px;margin-top:8px}
.gc .col{flex:1;border-top:1px solid #4A3860;padding-top:5px}
.gc .h{font-size:10px;font-weight:700;letter-spacing:1.4px;margin-bottom:3px}
.gc .then{color:#BD9AF7}.gc .now{color:#FFB886}
.gc ul{list-style:none;margin:0;padding:0}
.gc li{font-size:12px;line-height:1.5;color:#F4EBDD}
.gc li.k{color:#151020;background:#B4F2C4;border-radius:4px;padding:0 5px;margin:1px 0;font-weight:700;animation:gcpulse 2.8s ease-in-out infinite}
.gc li.k:before{content:'\\2726  '}
.gc .lg{margin-top:8px;font-size:11px;color:#B4F2C4;font-style:italic}
.gc .ft{margin-top:6px;font-size:11px;color:#C9B8E0;border-top:1px dashed #4A3860;padding-top:5px}
.gc .ft b{color:#FF858E;font-family:Georgia,serif;font-style:italic;font-weight:400;font-size:13px}
.gc .bat{position:absolute;top:8px;right:-40px;width:34px;animation:gcbat 7s linear infinite}
.gc .bat .w{animation:gcflap .22s ease-in-out infinite alternate;transform-origin:50% 50%;transform-box:fill-box}
@keyframes gcfloat{0%,100%{transform:translateY(3px)}50%{transform:translateY(-6px)}}
@keyframes gcblink{0%,90%,100%{transform:scaleY(1)}94%{transform:scaleY(.1)}}
@keyframes gcpulse{0%,100%{box-shadow:0 0 0 rgba(180,242,196,0)}50%{box-shadow:0 0 10px rgba(180,242,196,.65)}}
@keyframes gcbat{0%,55%{transform:translate(0,0)}75%{transform:translate(-260px,18px)}100%{transform:translate(-520px,-4px)}}
@keyframes gcflap{from{transform:scaleY(1)}to{transform:scaleY(.35)}}
""" + _RM + """</style>
<div class='gc'>
<svg class='bat' viewBox='0 0 40 20' aria-hidden='true'><g class='w'><path d='M20 10 C16 4 10 2 2 4 C6 7 7 10 5 14 C9 12 13 12 15 15 C16 12 18 11 20 12 C22 11 24 12 25 15 C27 12 31 12 35 14 C33 10 34 7 38 4 C30 2 24 4 20 10 Z' fill='#BD9AF7'/></g></svg>
<div class='hd'><div class='gs'><svg viewBox='0 0 74 86' aria-hidden='true'>
<path d='M10 82 L10 34 C10 6 64 6 64 34 L64 82 L55 74 L46 82 L37 74 L28 82 L19 74 Z' fill='{{_fill}}' stroke='#B4F2C4' stroke-width='2.5' stroke-dasharray='{{_dash}}' style='filter:drop-shadow(0 0 {{_glow}}px #B4F2C4)'/>
<ellipse class='eye' cx='28' cy='38' rx='5' ry='7' fill='{{_eye}}'/><ellipse class='eye' cx='46' cy='38' rx='5' ry='7' fill='{{_eye}}'/>
<ellipse cx='37' cy='54' rx='4' ry='5.5' fill='{{_eye}}'/></svg></div>
<div><div class='kick'>CASE FILE &#183; RESPONSE #{{_rk}}</div>
<div class='ttl'>{{_title}}</div>
<div class='sub'>Age group {{_age}} (when answering) &#183; {{_kept}} identical fear(s)</div></div></div>
<div class='cols'><div class='col'><div class='h then'>&#9664; THEN &#183; AS A CHILD</div><ul>{{_child}}</ul></div>
<div class='col'><div class='h now'>NOW &#183; TODAY &#9654;</div><ul>{{_now}}</ul></div></div>
<div class='lg'>{{_explain}}</div>
<div class='ft'>Worst data nightmare: <b>&#8220;{{_nm}}&#8221;</b></div>
</div>"""

GHOST_CARD_SAMPLE = {'_fill': '#B4F2C4', '_dash': '0', '_glow': '8', '_eye': '#151020', '_rk': '12', '_title': 'Still haunted by 2 fears',
    '_age': '35–44', '_kept': '2',
    '_child': "<li class='k'>Heights</li><li class='k'>Snakes</li><li>The dark</li>",
    '_now': "<li>Financial insecurity/poverty</li><li class='k'>Heights</li><li class='k'>Snakes</li>",
    '_nm': 'It arrives a mess', '_explain': '&#10022; = the very same answer in both lists: a monster that grew up with them.'}

def ghost_card_dax():
    def li(stage):
        return f'''CONCATENATEX (
        CALCULATETABLE (
            SUMMARIZE ( FactFearSelection, DimFear[Fear], FactFearSelection[IsRetained] ),
            FactFearSelection[LifeStage] = "{stage}"
        ),
        IF ( FactFearSelection[IsRetained], "<li class='k'>", "<li>" ) & DimFear[Fear] & "</li>",
        "",
        FactFearSelection[IsRetained], DESC, DimFear[Fear], ASC
    )'''
    body = to_dax(GHOST_CARD)
    return f'''VAR _rk = SELECTEDVALUE ( Respondent[ResponseKey] )
VAR _keptN = SELECTEDVALUE ( Respondent[FearsKept] )
VAR _kept = FORMAT ( _keptN, "0" )
VAR _age = SELECTEDVALUE ( Respondent[AgeGroup] )
VAR _nm = SELECTEDVALUE ( Respondent[Nightmare] )
VAR _title = IF ( _keptN > 0, "Still haunted by " & _keptN & IF ( _keptN = 1, " old fear", " old fears" ), "Escaped every childhood fear" )
VAR _fill = IF ( _keptN > 0, "#B4F2C4", "none" )
VAR _dash = IF ( _keptN > 0, "0", "5 4" )
VAR _glow = IF ( _keptN > 0, "8", "0" )
VAR _eye = IF ( _keptN > 0, "#151020", "#9A86B5" )
VAR _explain = IF ( _keptN > 0, "&#10022; = the very same answer in both lists: a monster that grew up with them.", "None of the childhood answers appears in today&#8217;s list: these monsters stayed under the bed." )
VAR _child = {li("Childhood")}
VAR _now = {li("Adult")}
RETURN
    IF (
        ISBLANK ( _rk ),
        "<div style='font-family:Segoe UI;color:#C9B8E0;padding:20px'>Hover a single ghost to open its case file.</div>",
        {body}
    )'''
