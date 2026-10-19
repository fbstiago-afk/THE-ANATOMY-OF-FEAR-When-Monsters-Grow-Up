# -*- coding: utf-8 -*-
"""The Anatomy of Fear - rebuilds the PBIP (model + report) on top of the
official starter project, and writes a quick HTML mock-up of the layout.

Usage (from the project folder):
    python Documentacao/scripts/build.py pbip Assets/Background/AnatomyOfFear_Background.jpg
"""
import json, os, re, shutil, sys, uuid, hashlib, html
sys.path.insert(0, os.path.dirname(__file__))
from measures import M
import html_parts as HP

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('AOF_ROOT', os.path.abspath(os.path.join(_HERE, '..', '..')))
STARTER = 'Halloween Contest 2026 - Starter File'
OUT = os.environ.get('AOF_OUT', ROOT)
NAME = 'TheAnatomyOfFear'
VIZ = os.environ.get('AOF_SPECS', os.path.join(ROOT, 'Assets', 'Deneb'))
PAGE_ID = 'a602c84c5fe643e1debd'   # the starter's portrait page (1357 x 1920)
PW, PH_ = 1357, 1920

def uid(seed):
    return hashlib.md5(seed.encode()).hexdigest()[:20]
def guid(seed):
    return str(uuid.UUID(hex=hashlib.md5(('lt-' + seed).encode()).hexdigest(), version=4))

# ---------------------------------------------------------------- layout
BONE, BONE2, VIOLET, MINT, CANDLE, BLOOD, LAV = '#F4EBDD', '#D9CDBD', '#BD9AF7', '#B4F2C4', '#FFB886', '#FF858E', '#C9B8E0'
L = 56            # left margin
CW = PW - 2 * L   # content width 1245

def run(text, size, color=BONE, font='Segoe UI', bold=False, italic=False):
    return dict(text=text, size=size, color=color, font=font, bold=bold, italic=italic)

EL = []
def text(key, x, y, w, h, paras, align='left', tab=None):
    EL.append(dict(kind='text', key=key, x=x, y=y, w=w, h=h, paras=paras, align=align, tab=tab))
def card(key, x, y, w, h, measure, size, color=BONE, font='Segoe UI', bold=False, alt=None, tab=None):
    EL.append(dict(kind='card', key=key, x=x, y=y, w=w, h=h, measure=measure, size=size, color=color, font=font, bold=bold, alt=alt, tab=tab))
def deneb(key, x, y, w, h, spec, fields, alt, sample, tab=None):
    EL.append(dict(kind='deneb', key=key, x=x, y=y, w=w, h=h, spec=spec, fields=fields, alt=alt, sample=sample, tab=tab))
def htmlv(key, x, y, w, h, measure, tpl, alt=None, alt_text=None, tab=None):
    EL.append(dict(kind='html', key=key, x=x, y=y, w=w, h=h, measure=measure, tpl=tpl, alt=alt, alt_text=alt_text, tab=tab))

MID = '   ·   '
# --- header
text('kicker', L, 58, 900, 34, [[run('THE ANATOMY OF FEAR' + MID + 'WHEN MONSTERS GROW UP', 12, VIOLET, bold=True)]], tab=1)
text('title', L, 92, 1010, 196, [
    [run('We outgrew the monsters.', 47, BONE, 'Georgia')],
    [run('Not the fear.', 47, BLOOD, 'Georgia', italic=True)]], tab=2)
text('subtitle', L, 290, 930, 66, [
    [run('As children, we feared what was hiding in the dark. As adults, we fear what the future is hiding from us. '
         'Here is what the data community told us about both.', 14, BONE2, 'Georgia', italic=True)]], tab=3)
card('strip', L, 356, 930, 40, 'Text Survey Strip', 11, VIOLET, bold=True, tab=4)
htmlv('ghost', 1000, 64, 215, 290, 'HTML Ghost', HP.GHOST, alt_text='Decorative illustration: a ghost holding a candle in front of the moon.', tab=-9999)

# --- Acts I & II : the spine
text('sec12', L, 434, CW, 74, [
    [run('I – II', 12, VIOLET, bold=True), run('     THE MONSTERS CHANGED SHAPE', 20, BONE, 'Georgia')],
    [run('Respondents who named each fear as children (left) and today (right). Shown: every fear in the top 5 of either period, '
         'ordered from the fear that grew most to the one that faded most. Optional: hover a fear for its dossier.', 11, LAV)]], tab=5)
text('then', L, 512, 420, 34, [[run('◀  THEN  ·  AS CHILDREN', 13, VIOLET, bold=True)]], tab=6)
text('spinehdr', L + 420, 512, 405, 34, [[run('THE SPINE OF FEAR', 11, '#9A86B5', bold=True)]], align='center', tab=7)
text('now', L + 825, 512, 420, 34, [[run('NOW  ·  AS ADULTS  ▶', 13, CANDLE, bold=True)]], align='right', tab=8)
SPINE_FIELDS = [('col', 'DimFear', 'Fear'),
                ('m', '_Measures', 'Childhood Respondents'), ('m', '_Measures', 'Now Respondents'),
                ('m', '_Measures', 'Kept Respondents'), ('m', '_Measures', 'Childhood Rank'),
                ('m', '_Measures', 'Now Rank'), ('m', '_Measures', 'Spine Include')]
deneb('spine', L, 548, CW, 590, 'spine', SPINE_FIELDS, 'Alt Spine', 'spine', tab=9); EL[-1]['tooltip'] = 'fear'
text('legend', L, 1140, CW, 30, [[
    run('Bar length = respondents   ·   ', 10.5, LAV),
    run('▬', 10.5, MINT, bold=True),
    run(' mint stripe = the same respondents named that exact fear in both lists   ·   #1–#3 = rank in that period   ·   ▲▼ = change in respondents, not individual journeys', 10.5, LAV)]],
    align='center', tab=10)
# insight trio
tw = (CW - 2 * 24) / 3
for i, (k, lab, meas, col) in enumerate([
        ('rise', 'GREW THE MOST', 'Text Biggest Rise', CANDLE),
        ('fall', 'FADED THE MOST', 'Text Biggest Fall', VIOLET),
        ('adult', 'NO ONE NAMED IT AS A CHILD', 'Text Adult Only', BLOOD)]):
    x = L + i * (tw + 24)
    text('lab_' + k, x, 1172, tw, 28, [[run(lab, 10.5, col, bold=True)]], align='center', tab=11 + 2 * i)
    card('val_' + k, x, 1196, tw, 44, meas, 15, BONE, 'Segoe UI', bold=True, tab=12 + 2 * i)

# --- Act III : persistence
text('sec3', L, 1262, CW, 40, [[run('III', 12, MINT, bold=True), run('     THE FEARS THAT NEVER LEFT', 20, BONE, 'Georgia')]], tab=17)
card('pct', L, 1300, 420, 110, 'Text Persistent %', 60, MINT, 'Georgia', alt='Alt Persistent', tab=18); EL[-1]['tooltip'] = 'persist'
card('pctof', L, 1408, 420, 40, 'Text Persistent Count', 15, BONE, bold=True, tab=19); EL[-1]['tooltip'] = 'persist'
text('pcttxt', L, 1448, 420, 92, [[run('named the exact same fear as a child', 12.5, BONE2)], [run('and again as an adult.', 12.5, BONE2)],
                                  [run('Some monsters never left.', 14, MINT, 'Georgia', italic=True)]], align='center', tab=20)
GH_FIELDS = [('col', 'Respondent', 'ResponseKey'), ('col', 'Respondent', 'FearsKept'), ('col', 'Respondent', 'PersonOrder'), ('col', 'Respondent', 'KeptFears')]
deneb('ghosts', 500, 1300, 800, 206, 'ghosts', GH_FIELDS, 'Alt Ghosts', 'people', tab=21); EL[-1]['tooltip'] = 'ghost'
card('loyal', 500, 1504, 800, 38, 'Text Most Loyal', 12, MINT, bold=True, tab=22); EL[-1]['tooltip'] = 'persist'

# --- Act IV : data nightmares
text('sec4', L, 1568, CW, 64, [
    [run('IV', 12, BLOOD, bold=True), run('     EVEN DATA HAS MONSTERS', 20, BONE, 'Georgia')],
    [run('We asked: what is your worst data nightmare? One answer per respondent.', 11, LAV)]], tab=23)
htmlv('nmcard', L, 1630, 470, 170, 'HTML Data Nightmare', HP.NIGHTMARE, alt='Alt Nightmares', tab=24)
NM_FIELDS = [('col', 'Respondent', 'Nightmare'), ('m', '_Measures', 'Responses'),
             ('m', '_Measures', 'Nightmare Share'), ('m', '_Measures', 'Nightmare Rank')]
deneb('nightmares', L + 490, 1628, CW - 490, 168, 'nightmare', NM_FIELDS, 'Alt Nightmares', 'nightmare', tab=25); EL[-1]['tooltip'] = 'nightmare'

# --- punchline + footer
text('punch', L, 1814, CW, 66, [
    [run('The monsters didn’t disappear. ', 21, BONE, 'Georgia', italic=True),
     run('They learned to use spreadsheets.', 21, MINT, 'Georgia', italic=True)]], align='center', tab=26)
text('footer', L, 1864, CW, 48, [
    [run('Source: official Halloween Data Visualization Contest 2026 survey (survey_responses.csv)  \u00B7  voluntary respondents from the data community, not a population sample', 8.5, LAV)],
    [run('Counts are respondents unless noted  \u00B7  fear lists allowed several answers  \u00B7  \u201Cidentical\u201D = the same answer in both lists  \u00B7  ranks exclude None of these, Prefer not to answer, Something else', 8.5, LAV)]],
    align='center', tab=27)

# ---------------------------------------------------------------- tooltip pages (hidden, complementary)
MAIN_EL = EL
TT_PAGES = {}
TT_IDS = {}
TTW = 440
def tt_page(key, display, h):
    global EL
    EL = []
    TT_PAGES[key] = dict(id=uid('ttpage-' + key), name=display, w=TTW, h=h, els=EL)
    TT_IDS[key] = TT_PAGES[key]['id']
    return EL
def tt_labels(prefix, y, items):
    w = (TTW - 24 - 16) / 3
    for i, (lab, col, meas) in enumerate(items):
        x = 12 + i * (w + 8)
        text(f'{prefix}_l{i}', x, y, w, 22, [[run(lab, 8.5, col, bold=True)]], align='center')
        card(f'{prefix}_v{i}', x, y + 20, w, 30, meas, 12, BONE, bold=True)

tt_page('fear', 'TT Fear dossier', 340)
htmlv('ttf_eyes', 8, 6, 70, 56, 'HTML TT Eyes', HP.TT_EYES, alt_text='Decorative animation: eyes blinking in the dark.')
htmlv('ttf_spider', 362, 0, 70, 66, 'HTML TT Spider', HP.TT_SPIDER, alt_text='Decorative animation: a spider dropping on its thread.')
card('ttf_name', 80, 8, TTW - 160, 34, 'TT Fear Name', 14, BONE, bold=True)
card('ttf_cat', 80, 40, TTW - 160, 22, 'TT Fear Category', 9, LAV)
tt_labels('ttf', 68, [('AS A CHILD', VIOLET, 'TT Childhood Text'), ('TODAY', CANDLE, 'TT Now Text'), ('IN BOTH LISTS', MINT, 'TT Kept Text')])
text('ttf_note', 12, 124, TTW - 24, 24, [[run('Respondents by age group (age when answering the survey)', 9, LAV)]], align='center')
deneb('ttf_age', 12, 148, TTW - 24, 184, 'tt_age_fear',
      [('col', 'DimAgeGroup', 'AgeGroup'), ('m', '_Measures', 'Childhood Respondents'), ('m', '_Measures', 'Now Respondents')],
      None, None)

tt_page('persist', 'TT Persistence', 380)
htmlv('ttp_tomb', 6, 2, 84, 64, 'HTML TT Tomb', HP.TT_TOMB, alt_text='Decorative animation: a ghost peeking from a tombstone that reads STILL HERE.')
htmlv('ttp_candle', 384, 4, 46, 60, 'HTML TT Candle', HP.TT_CANDLE, alt_text='Decorative animation: a flickering candle.')
text('ttp_t', 92, 6, TTW - 184, 58, [[run('WHICH FEARS STAYED?', 12, MINT, bold=True)],
     [run('Same answer in both lists, of childhood respondents', 8, LAV)]], align='center')
deneb('ttp_kept', 12, 56, TTW - 24, 156, 'tt_kept',
      [('col', 'DimFear', 'Fear'), ('m', '_Measures', 'Kept Respondents'), ('m', '_Measures', 'Childhood Respondents')], None, None)
text('ttp_n', 12, 214, TTW - 24, 24, [[run('Kept at least one identical fear, by age group (small groups: read with care)', 8.5, LAV)]], align='center')
deneb('ttp_age', 12, 238, TTW - 24, 136, 'tt_age_share',
      [('col', 'Respondent', 'AgeGroup'), ('m', '_Measures', 'TT Persist Count'), ('m', '_Measures', 'TT Persist Size')], None, None)
EL[-1]['subs'] = {'TT Group Count': 'TT Persist Count', 'TT Group Size': 'TT Persist Size'}

tt_page('nightmare', 'TT Data nightmare', 300)
htmlv('ttn_sheet', 6, 6, 72, 56, 'HTML TT Sheet', HP.TT_SHEET, alt_text='Decorative animation: a haunted spreadsheet with a blinking eye.')
htmlv('ttn_bat', 362, 4, 72, 52, 'HTML TT Bat', HP.TT_BAT, alt_text='Decorative animation: a bat flying across.')
card('ttn_name', 80, 8, TTW - 160, 34, 'TT Nightmare Name', 14, BLOOD, bold=True)
card('ttn_det', 80, 40, TTW - 160, 22, 'TT Nightmare Detail', 9.5, LAV)
card('ttn_cnt', 12, 64, TTW - 24, 30, 'TT Nightmare Text', 12, BONE, bold=True)
text('ttn_n', 12, 100, TTW - 24, 24, [[run('Share of each age group choosing it (age when answering; small groups)', 8.5, LAV)]], align='center')
deneb('ttn_age', 12, 124, TTW - 24, 168, 'tt_age_share',
      [('col', 'Respondent', 'AgeGroup'), ('m', '_Measures', 'TT NM Count'), ('m', '_Measures', 'TT NM Size')], None, None)
EL[-1]['subs'] = {'TT Group Count': 'TT NM Count', 'TT Group Size': 'TT NM Size', '"value": "#B4F2C4"': '"value": "#FF858E"'}
tt_page('ghost', 'TT Ghost case file', 300)
htmlv('ttg_card', 0, 0, TTW, 300, 'HTML TT Ghost Case File', HP.GHOST_CARD, alt='HTML TT Ghost Alt')
EL[-1]['sample'] = 'ghostcard'
EL = MAIN_EL

# ---------------------------------------------------------------- theme
THEME = {
  "name": "AnatomyOfFear",
  "dataColors": ["#8463BF", "#B8622F", "#B4F2C4", "#FF858E", "#BD9AF7", "#FFB886", "#C9B8E0", "#9A86B5"],
  "background": "#151020", "foreground": BONE, "tableAccent": VIOLET,
  "good": MINT, "neutral": CANDLE, "bad": BLOOD,
  "maximum": BLOOD, "center": CANDLE, "minimum": "#8463BF",
  "textClasses": {
    "callout": {"fontFace": "Georgia", "fontSize": 40, "color": BONE},
    "title": {"fontFace": "Georgia", "fontSize": 16, "color": BONE},
    "header": {"fontFace": "Segoe UI Semibold", "fontSize": 13, "color": BONE},
    "label": {"fontFace": "Segoe UI", "fontSize": 11, "color": BONE}
  },
  "visualStyles": {
    "*": {"*": {
      "background": [{"show": False, "transparency": 100}],
      "border": [{"show": False}],
      "dropShadow": [{"show": False}],
      "visualHeader": [{"show": False}],
      "title": [{"show": False}],
      "padding": [{"top": 0, "bottom": 0, "left": 0, "right": 0}]
    }},
    "page": {"*": {
      "outspace": [{"color": {"solid": {"color": "#0D0913"}}}],
      "background": [{"color": {"solid": {"color": "#151020"}}, "transparency": 0}]
    }}
  }
}

# ---------------------------------------------------------------- helpers
def lit(v):
    if isinstance(v, bool):
        return {"expr": {"Literal": {"Value": "true" if v else "false"}}}
    if isinstance(v, (int, float)):
        return {"expr": {"Literal": {"Value": f"{v}D"}}}
    return {"expr": {"Literal": {"Value": "'" + str(v).replace("'", "''") + "'"}}}
def color(c):
    return {"solid": {"color": lit(c)}}
def measure_ref(name):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": name}}
def column_ref(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}
def projection(kind, entity, prop):
    f = column_ref(entity, prop) if kind == 'col' else measure_ref(prop)
    return {"field": f, "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}

def container_objects(alt_measure=None, alt_text=None, tooltip=None):
    gen = {}
    if alt_measure:
        gen["altText"] = {"expr": measure_ref(alt_measure)}
    elif alt_text:
        gen["altText"] = lit(alt_text)
    o = {
        "background": [{"properties": {"show": lit(False)}}],
        "border": [{"properties": {"show": lit(False)}}],
        "title": [{"properties": {"show": lit(False)}}],
        "visualHeader": [{"properties": {"show": lit(False)}}],
        "dropShadow": [{"properties": {"show": lit(False)}}],
        "padding": [{"properties": {"top": lit(0), "bottom": lit(0), "left": lit(0), "right": lit(0)}}],
    }
    if gen:
        o["general"] = [{"properties": gen}]
    if tooltip:
        o["visualTooltip"] = [{"properties": {"show": lit(True), "type": lit("Canvas"), "section": lit(TT_IDS[tooltip])}}]
    return o

VC_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json"

def spec_text(name, subs=None):
    s = json.load(open(f'{VIZ}/{name}.vl.json', encoding='utf-8'))
    t = json.dumps(s, indent=2, ensure_ascii=False)
    for a, c in (subs or {}).items():
        t = t.replace(a, c)
    return t

def visual_json(e, z):
    pos = {"x": e['x'], "y": e['y'], "z": z, "height": e['h'], "width": e['w'], "tabOrder": e['tab'] * 1000 if e['tab'] is not None else z}
    v = {"$schema": VC_SCHEMA, "name": uid(e['key']), "position": pos}
    if e['kind'] == 'text':
        paras = []
        for p in e['paras']:
            runs = []
            for r in p:
                st = {"fontFamily": r['font'], "fontSize": f"{r['size']}pt", "color": r['color']}
                if r['bold']: st["fontWeight"] = "bold"
                if r['italic']: st["fontStyle"] = "italic"
                runs.append({"value": r['text'], "textStyle": st})
            para = {"textRuns": runs}
            if e['align'] != 'left':
                para["horizontalTextAlignment"] = e['align']
            paras.append(para)
        v["visual"] = {"visualType": "textbox",
                       "objects": {"general": [{"properties": {"paragraphs": paras}}]},
                       "visualContainerObjects": container_objects(None, None, e.get('tooltip')),
                       "drillFilterOtherVisuals": True}
    elif e['kind'] == 'card':
        v["visual"] = {
            "visualType": "card",
            "query": {"queryState": {"Values": {"projections": [projection('m', '_Measures', e['measure'])]}}},
            "objects": {
                "labels": [{"properties": {"color": color(e['color']), "fontSize": lit(e['size']),
                                            "fontFamily": lit(e['font']), "bold": lit(e['bold'])}}],
                "categoryLabels": [{"properties": {"show": lit(False)}}]},
            "visualContainerObjects": container_objects(e.get('alt') or e['measure'], tooltip=e.get('tooltip')),
            "drillFilterOtherVisuals": True}
    elif e['kind'] == 'deneb':
        v["visual"] = {
            "visualType": "deneb7E15AEF80B9E4D4F8E12924291ECE89A",
            "query": {"queryState": {"dataset": {"projections": [projection(k, en, p) for k, en, p in e['fields']]}}},
            "objects": {"vega": [{"properties": {
                "provider": lit('vegaLite'),
                "jsonSpec": lit(spec_text(e['spec'], e.get('subs'))),
                "jsonConfig": lit('{}'),
                "renderMode": lit('svg'),
                "enableTooltips": lit(True),
                "enableContextMenu": lit(True),
                "enableSelection": lit(False),
                "enableHighlight": lit(False)}}]},
            "visualContainerObjects": container_objects(e['alt'], tooltip=e.get('tooltip')),
            "drillFilterOtherVisuals": True}
    elif e['kind'] == 'html':
        v["visual"] = {
            "visualType": "htmlContent443BE3AD55E043BF878BED274D3A6855",
            "query": {"queryState": {"content": {"projections": [projection('m', '_Measures', e['measure'])]}}},
            "objects": {"contentFormatting": [{"properties": {
                "showRawHtml": lit(False), "fontFamily": lit('Segoe UI'), "fontColour": color(BONE),
                "fontSize": lit(11), "userSelect": lit(False), "hyperlinks": lit(False)}}]},
            "visualContainerObjects": container_objects(e.get('alt'), e.get('alt_text'), e.get('tooltip')),
            "drillFilterOtherVisuals": True}
    return v

def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')

# ---------------------------------------------------------------- semantic model
def tmdl_measure(name, folder, fmt, desc, expr):
    lines = [f"\t/// {d}" for d in desc.split('\n')]
    q = name if all(c.isalnum() or c == '_' for c in name) else "'" + name.replace("'", "''") + "'"
    body = expr.split('\n')
    lines.append(f"\tmeasure {q} =")
    for b in body:
        lines.append("\t\t\t" + b if b.strip() else "")
    if fmt:
        lines.append(f"\t\tformatString: {fmt}")
    lines.append(f"\t\tdisplayFolder: {folder}")
    lines.append(f"\t\tlineageTag: {guid('m-' + name)}")
    lines.append("")
    return "\n".join(lines)

RESPONDENT_M = r'''let
	    // Same parser as the starter tables: JSON array -> distinct trimmed list (never split on commas).
	    Parse = (v as any) as list => if v = null or Text.Trim(Text.From(v)) = "" then {} else let j = Json.Document(v) in if not Value.Is(j, type list) then error "Fear JSON must be a list" else List.Distinct(List.Select(List.Transform(j, each if _ = null then "" else Text.Trim(Text.From(_))), each _ <> "")),
	    Clean = (v as any) as text => if v = null or Text.Trim(Text.From(v)) = "" then "(Unknown)" else Text.Trim(Text.From(v)),
	    Source = raw_survey_responses,
	    Checked = if Table.RowCount(Source) <> List.Count(List.Distinct(Source[ResponseKey])) then error "ResponseKey must be unique" else Source,
	    WithLists = Table.AddColumn(Checked, "Lists", each [C = Parse([childhoodFearsJson]), N = Parse([currentFearsJson])]),
	    WithKept = Table.AddColumn(WithLists, "FearsKept", each List.Count(List.Intersect({[Lists][C], [Lists][N]})), Int64.Type),
	    WithKeptList = Table.AddColumn(WithKept, "KeptFears", each let k = List.Intersect({[Lists][C], [Lists][N]}) in if List.IsEmpty(k) then "none" else Text.Combine(k, ", "), type text),
	    WithAge = Table.AddColumn(WithKeptList, "AgeGroup", each Clean([ageGroup]), type text),
	    WithChildCount = Table.AddColumn(WithAge, "ChildhoodFearCount", each List.Count([Lists][C]), Int64.Type),
	    WithNowCount = Table.AddColumn(WithChildCount, "CurrentFearCount", each List.Count([Lists][N]), Int64.Type),
	    // Derived display labels. The original answer stays untouched in dataNightmare.
	    WithShort = Table.AddColumn(WithNowCount, "Nightmare", each let t = Clean([dataNightmare]) in if Text.Contains(t, " (") then Text.Trim(Text.BeforeDelimiter(t, " (")) else t, type text),
	    WithDetail = Table.AddColumn(WithShort, "NightmareDetail", each let t = Clean([dataNightmare]) in if Text.Contains(t, " (") then Text.Trim(Text.BeforeDelimiter(Text.AfterDelimiter(t, " ("), ")", {0, RelativePosition.FromEnd})) else "", type text),
	    Sorted = Table.Sort(WithDetail, {{"FearsKept", Order.Descending}, {"ResponseKey", Order.Ascending}}),
	    Indexed = Table.AddIndexColumn(Sorted, "PersonOrder", 1, 1, Int64.Type),
	    Result = Table.SelectColumns(Indexed, {"ResponseKey", "dataNightmare", "Nightmare", "NightmareDetail", "AgeGroup", "FearsKept", "KeptFears", "ChildhoodFearCount", "CurrentFearCount", "PersonOrder"}),
	    Typed = Table.TransformColumnTypes(Result, {{"ResponseKey", Int64.Type}, {"dataNightmare", type text}})
	in
	    Typed'''

def respondent_tmdl():
    cols = [("ResponseKey", "int64", None, "Survey response identifier (one row per response)."),
            ("dataNightmare", "string", None, "Original, unmodified answer to the data nightmare question."),
            ("Nightmare", "string", None, "Short label: text of dataNightmare before the bracket. Derived, for display."),
            ("NightmareDetail", "string", None, "Text inside the bracket of dataNightmare. Derived, for display."),
            ("AgeGroup", "string", None, "Age group when answering the survey (not childhood age)."),
            ("FearsKept", "int64", None, "Number of identical fears in the childhood and current lists of this response."),
            ("KeptFears", "string", None, "The identical fears of this response, comma separated (\"none\" if none). Derived, for tooltips."),
            ("ChildhoodFearCount", "int64", None, "Number of distinct fears in the childhood list."),
            ("CurrentFearCount", "int64", None, "Number of distinct fears in the current list."),
            ("PersonOrder", "int64", None, "Display order for the 105-ghost chart: most identical fears first, then ResponseKey.")]
    out = ["/// One row per survey response. Derived from raw_survey_responses; original values are not modified.",
           "table Respondent", f"\tlineageTag: {guid('t-Respondent')}", ""]
    for c, t, _, d in cols:
        out += [f"\t/// {d}", f"\tcolumn {c}", f"\t\tdataType: {t}"]
        if t == 'int64':
            out.append("\t\tformatString: 0")
        out += [f"\t\tlineageTag: {guid('c-Respondent-' + c)}", "\t\tsummarizeBy: none", f"\t\tsourceColumn: {c}", "",
                "\t\tannotation SummarizationSetBy = User", ""]
    out += ["\tpartition Respondent = m", "\t\tmode: import", "\t\tsource ="]
    out += ["\t\t\t\t" + l.replace("\t", "", 1) if l.startswith("\t") else "\t\t\t\t" + l for l in RESPONDENT_M.split("\n")]
    out += ["", "\tannotation PBI_ResultType = Table", ""]
    return "\n".join(out)

def build_model(dst):
    src = f'{ROOT}/{STARTER}.SemanticModel'
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('cache.abf', 'localSettings.json'))
    d = f'{dst}/definition'
    # model.tmdl : add Respondent table + query order
    mt = open(f'{d}/model.tmdl', encoding='utf-8').read()
    mt = mt.replace('"FactFearSelection","_Measures"]', '"FactFearSelection","Respondent","_Measures"]')
    mt = re.sub(r'annotation PBI_ProTooling = .*', 'annotation PBI_ProTooling = ["DevMode"]', mt)
    mt = mt.replace("ref table _Measures", "ref table Respondent\nref table _Measures")
    open(f'{d}/model.tmdl', 'w', encoding='utf-8', newline='\n').write(mt)
    open(f'{d}/tables/Respondent.tmdl', 'w', encoding='utf-8', newline='\n').write(respondent_tmdl())
    rel = open(f'{d}/relationships.tmdl', encoding='utf-8').read().rstrip('\n')
    rel += "\n\nrelationship Respondent_FactFearSelection\n\tfromColumn: FactFearSelection.ResponseKey\n\ttoColumn: Respondent.ResponseKey\n"
    open(f'{d}/relationships.tmdl', 'w', encoding='utf-8', newline='\n').write(rel)
    # measures: insert before the hidden Column1 of _Measures
    mm = open(f'{d}/tables/_Measures.tmdl', encoding='utf-8').read()
    html_measures = [
        ("HTML Ghost", "Anatomy of Fear\\7 HTML", None, "Decorative animated ghost for the HTML Content visual (static SVG + CSS, no script).",
         HP.to_dax(HP.GHOST)),
        ("HTML Data Nightmare", "Anatomy of Fear\\7 HTML", None, "Data nightmare card for the HTML Content visual; numbers come from measures.",
         HP.to_dax(HP.NIGHTMARE)),
        ("HTML TT Eyes", "Anatomy of Fear\\7 HTML", None, "Tooltip animation: blinking eyes in the dark (decorative).", HP.to_dax(HP.TT_EYES)),
        ("HTML TT Spider", "Anatomy of Fear\\7 HTML", None, "Tooltip animation: spider dropping on its thread (decorative).", HP.to_dax(HP.TT_SPIDER)),
        ("HTML TT Tomb", "Anatomy of Fear\\7 HTML", None, "Tooltip animation: ghost peeking from a STILL HERE tombstone (decorative).", HP.to_dax(HP.TT_TOMB)),
        ("HTML TT Candle", "Anatomy of Fear\\7 HTML", None, "Tooltip animation: flickering candle (decorative).", HP.to_dax(HP.TT_CANDLE)),
        ("HTML TT Sheet", "Anatomy of Fear\\7 HTML", None, "Tooltip animation: haunted spreadsheet with a blinking eye (decorative).", HP.to_dax(HP.TT_SHEET)),
        ("HTML TT Bat", "Anatomy of Fear\\7 HTML", None, "Tooltip animation: bat flying across (decorative).", HP.to_dax(HP.TT_BAT)),
        ("HTML TT Ghost Case File", "Anatomy of Fear\\7 HTML", None, "Tooltip case file for one respondent (hovered ghost): childhood and current fears, identical fears highlighted, age group and data nightmare. Values from the model.", HP.ghost_card_dax()),
    ]
    block = "\n".join(tmdl_measure(*x) for x in list(M) + html_measures)
    anchor = "\tcolumn Column1"
    assert anchor in mm
    mm = mm.replace(anchor, block + "\n" + anchor, 1)
    open(f'{d}/tables/_Measures.tmdl', 'w', encoding='utf-8', newline='\n').write(mm)
    # platform display name
    p = json.load(open(f'{dst}/.platform', encoding='utf-8'))
    p['metadata']['displayName'] = NAME
    p['config']['logicalId'] = guid('sm-' + NAME)
    dump(f'{dst}/.platform', p)

# ---------------------------------------------------------------- report
def build_report(dst, bg_png):
    src = f'{ROOT}/{STARTER}.Report'
    os.makedirs(dst)
    shutil.copy(f'{src}/definition.pbir', f'{dst}/definition.pbir')
    pb = json.load(open(f'{dst}/definition.pbir'))
    pb['datasetReference']['byPath']['path'] = f'../{NAME}.SemanticModel'
    dump(f'{dst}/definition.pbir', pb)
    p = json.load(open(f'{src}/.platform', encoding='utf-8'))
    p['metadata']['displayName'] = NAME
    p['config']['logicalId'] = guid('rp-' + NAME)
    dump(f'{dst}/.platform', p)
    shutil.copytree(f'{src}/StaticResources/SharedResources', f'{dst}/StaticResources/SharedResources')
    rr = f'{dst}/StaticResources/RegisteredResources'
    os.makedirs(rr)
    dump(f'{rr}/AnatomyOfFear.json', THEME)
    shutil.copy(bg_png, f'{rr}/AnatomyOfFear_Background.jpg')
    rep = json.load(open(f'{src}/definition/report.json', encoding='utf-8'))
    rep['themeCollection']['customTheme']['name'] = 'AnatomyOfFear.json'
    for pk in rep['resourcePackages']:
        if pk['name'] == 'RegisteredResources':
            pk['items'] = [
                {"name": "AnatomyOfFear_Background.jpg", "path": "AnatomyOfFear_Background.jpg", "type": "Image"},
                {"name": "AnatomyOfFear.json", "path": "AnatomyOfFear.json", "type": "CustomTheme"}]
    rep['publicCustomVisuals'] = ["deneb7E15AEF80B9E4D4F8E12924291ECE89A", "htmlContent443BE3AD55E043BF878BED274D3A6855"]
    rep['settings']['exportDataMode'] = 'AllowSummarized'
    dump(f'{dst}/definition/report.json', rep)
    shutil.copy(f'{src}/definition/version.json', f'{dst}/definition/version.json')
    dump(f'{dst}/definition/pages/pages.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [PAGE_ID] + [p['id'] for p in TT_PAGES.values()], "activePageName": PAGE_ID})
    page = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": PAGE_ID, "displayName": "The Anatomy of Fear", "displayOption": "FitToPage",
        "height": PH_, "width": PW,
        "objects": {
            "background": [{"properties": {
                "image": {"image": {
                    "name": lit("AnatomyOfFear_Background.jpg"),
                    "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": "AnatomyOfFear_Background.jpg"}}},
                    "scaling": lit("Fit")}},
                "transparency": lit(0)}}],
            "outspace": [{"properties": {"color": color("#0D0913")}}]}}
    dump(f'{dst}/definition/pages/{PAGE_ID}/page.json', page)
    for z, e in enumerate(EL):
        dump(f'{dst}/definition/pages/{PAGE_ID}/visuals/{uid(e["key"])}/visual.json', visual_json(e, z * 1000))
    for key, tp in TT_PAGES.items():
        dump(f'{dst}/definition/pages/{tp["id"]}/page.json', {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
            "name": tp['id'], "displayName": tp['name'], "displayOption": "FitToPage",
            "height": tp['h'], "width": tp['w'],
            "pageBinding": {"name": uid('ttbind-' + key), "type": "Tooltip"},
            "type": "Tooltip", "visibility": "HiddenInViewMode",
            "objects": {"background": [{"properties": {"color": color("#1E142B"), "transparency": lit(0)}}],
                        "outspace": [{"properties": {"color": color("#1E142B")}}]}})
        for z, e in enumerate(tp['els']):
            e['tab'] = z + 1
            dump(f'{dst}/definition/pages/{tp["id"]}/visuals/{uid(e["key"])}/visual.json', visual_json(e, z * 1000))

def build_pbip(out):
    dump(f'{out}/{NAME}.pbip', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0", "artifacts": [{"report": {"path": f"{NAME}.Report"}}], "settings": {"enableAutoRecovery": True}})

# ---------------------------------------------------------------- preview
def preview(out_html, bg_png):
    parts = []
    for e in EL:
        st = f"left:{e['x']}px;top:{e['y']}px;width:{e['w']}px;height:{e['h']}px"
        if e['kind'] == 'text':
            ps = []
            for p in e['paras']:
                rs = ''.join(
                    f"<span style=\"font-family:'{r['font']}';font-size:{r['size']*4/3:.2f}px;color:{r['color']};"
                    f"font-weight:{700 if r['bold'] else 400};font-style:{'italic' if r['italic'] else 'normal'}\">{html.escape(r['text'])}</span>"
                    for r in p)
                ps.append(f"<p style='margin:0;text-align:{e['align']};line-height:1.25'>{rs}</p>")
            parts.append(f"<div class='v' style='{st}'>{''.join(ps)}</div>")
        elif e['kind'] == 'card':
            sample = SAMPLES.get(e['measure'], e['measure'])
            parts.append(f"<div class='v card' style='{st};font-family:\"{e['font']}\";font-size:{e['size']*4/3:.1f}px;color:{e['color']};font-weight:{700 if e['bold'] else 400}'>{html.escape(sample)}</div>")
        elif e['kind'] == 'deneb':
            parts.append(f"<div class='v' style='{st}'><img src='{e['spec']}.svg' style='width:100%;height:100%'></div>")
        elif e['kind'] == 'html':
            parts.append(f"<div class='v' style='{st}'>{HP.render(e['tpl'])}</div>")
    doc = f"""<!doctype html><html><head><meta charset='utf-8'><style>
body{{margin:0;background:#0D0913}} .page{{position:relative;width:{PW}px;height:{PH_}px;background:url('{os.path.basename(bg_png)}') no-repeat;background-size:100% 100%}}
.v{{position:absolute;overflow:hidden;box-sizing:border-box}} .card{{display:flex;align-items:center;justify-content:center;text-align:center;white-space:nowrap}}
</style></head><body><div class='page'>{''.join(parts)}</div></body></html>"""
    open(out_html, 'w', encoding='utf-8').write(doc)

SAMPLES = {}

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'samples':
        print(json.dumps([e['key'] for e in EL]))
    elif mode == 'preview':
        SAMPLES.update(json.load(open(sys.argv[3], encoding='utf-8')))
        preview(sys.argv[2], sys.argv[4])
    elif mode == 'pbip':
        for part in (f'{NAME}.Report', f'{NAME}.SemanticModel'):
            if os.path.exists(f'{OUT}/{part}'):
                shutil.rmtree(f'{OUT}/{part}')
        os.makedirs(OUT, exist_ok=True)
        build_model(f'{OUT}/{NAME}.SemanticModel')
        build_report(f'{OUT}/{NAME}.Report', sys.argv[2])
        build_pbip(OUT)
        print('built', OUT)
