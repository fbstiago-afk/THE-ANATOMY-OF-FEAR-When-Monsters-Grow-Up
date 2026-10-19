# -*- coding: utf-8 -*-
# Single source of truth for every DAX measure added to the model.
# (name, folder, formatString or None, description, expression)

LIFE_CHILD = '"Childhood"'
LIFE_NOW = '"Adult"'

RANKABLE = '''CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    )'''

M = []
def m(name, folder, fmt, desc, expr):
    M.append((name, folder, fmt, desc, expr.strip('\n')))

F_CORE = "Anatomy of Fear\\1 Core"
F_FEAR = "Anatomy of Fear\\2 Fears by period"
F_PERS = "Anatomy of Fear\\3 Persistence"
F_NM = "Anatomy of Fear\\4 Data nightmares"
F_TXT = "Anatomy of Fear\\5 Poster text"
F_A11Y = "Anatomy of Fear\\6 Accessibility"
F_HTML = "Anatomy of Fear\\7 HTML"
F_QA = "Anatomy of Fear\\9 QA"

# ---------- core ----------
m("Responses", F_CORE, "#,0",
  "Survey responses (one row per ResponseKey in Respondent). Denominator for every share on the poster.",
  "COUNTROWS ( Respondent )")
m("Childhood Fear Mentions", F_CORE, "#,0",
  "Fear selections in the childhood list. A respondent could select several fears, so this is NOT a count of people.",
  f"""CALCULATE (
    COUNTROWS ( FactFearSelection ),
    KEEPFILTERS ( FactFearSelection[LifeStage] = {LIFE_CHILD} )
)""")
m("Current Fear Mentions", F_CORE, "#,0",
  "Fear selections in the current (adult) list. A respondent could select several fears, so this is NOT a count of people.",
  f"""CALCULATE (
    COUNTROWS ( FactFearSelection ),
    KEEPFILTERS ( FactFearSelection[LifeStage] = {LIFE_NOW} )
)""")
m("Max Fears per List", F_CORE, "0",
  "Largest number of fears any respondent selected in one list (childhood or current).",
  "MAX ( MAX ( Respondent[ChildhoodFearCount] ), MAX ( Respondent[CurrentFearCount] ) )")

# ---------- fears by period ----------
m("Respondents by Fear", F_FEAR, "#,0",
  "Distinct respondents who selected the fear(s) in context, in any period (respects a LifeStage filter if present).",
  "DISTINCTCOUNT ( FactFearSelection[ResponseKey] )")
m("Childhood Respondents", F_FEAR, "#,0",
  "Distinct respondents who selected the fear in their childhood list.",
  f"""CALCULATE (
    DISTINCTCOUNT ( FactFearSelection[ResponseKey] ),
    KEEPFILTERS ( FactFearSelection[LifeStage] = {LIFE_CHILD} )
)""")
m("Now Respondents", F_FEAR, "#,0",
  "Distinct respondents who selected the fear in their current (adult) list.",
  f"""CALCULATE (
    DISTINCTCOUNT ( FactFearSelection[ResponseKey] ),
    KEEPFILTERS ( FactFearSelection[LifeStage] = {LIFE_NOW} )
)""")
m("Kept Respondents", F_FEAR, "#,0",
  "Distinct respondents who selected exactly the same fear in BOTH lists (IsRetained). Not a causal or continuous-fear claim.",
  """CALCULATE (
    DISTINCTCOUNT ( FactFearSelection[ResponseKey] ),
    KEEPFILTERS ( FactFearSelection[IsRetained] = TRUE () )
)""")
m("Fear Share", F_FEAR, "0.0%",
  "Respondents selecting the fear in context divided by all respondents.",
  "DIVIDE ( [Respondents by Fear], [Responses] )")
m("Childhood Fear Share", F_FEAR, "0.0%",
  "Childhood respondents for the fear divided by all respondents.",
  "DIVIDE ( [Childhood Respondents], [Responses] )")
m("Now Fear Share", F_FEAR, "0.0%",
  "Current respondents for the fear divided by all respondents.",
  "DIVIDE ( [Now Respondents], [Responses] )")
m("Fear Change", F_FEAR, "+0;-0;0",
  "Current respondents minus childhood respondents for the fear. Difference between two aggregate counts, NOT individual transitions.",
  "COALESCE ( [Now Respondents], 0 ) - COALESCE ( [Childhood Respondents], 0 )")
m("Fear Share Difference", F_FEAR, "+0.0%;-0.0%;0.0%",
  "Current share minus childhood share (percentage points of all respondents).",
  "COALESCE ( [Now Fear Share], 0 ) - COALESCE ( [Childhood Fear Share], 0 )")
m("Childhood Rank", F_FEAR, "0",
  "Rank of the fear by childhood respondents (1 = most selected, ties share a rank, SKIP). Excludes non-fear answers (Other Responses category).",
  f"""VAR _value = [Childhood Respondents]
VAR _isFear = SELECTEDVALUE ( DimFear[Category] ) <> "Other Responses"
RETURN
    IF (
        HASONEVALUE ( DimFear[Fear] ) && _isFear && _value > 0,
        RANKX ( {RANKABLE}, [Childhood Respondents], _value, DESC, SKIP )
    )""")
m("Now Rank", F_FEAR, "0",
  "Rank of the fear by current respondents (1 = most selected, ties share a rank, SKIP). Excludes non-fear answers.",
  f"""VAR _value = [Now Respondents]
VAR _isFear = SELECTEDVALUE ( DimFear[Category] ) <> "Other Responses"
RETURN
    IF (
        HASONEVALUE ( DimFear[Fear] ) && _isFear && _value > 0,
        RANKX ( {RANKABLE}, [Now Respondents], _value, DESC, SKIP )
    )""")
m("Fear Rank", F_FEAR, "0",
  "Rank of the fear by respondents in the current filter context (for example a LifeStage filter).",
  f"""VAR _value = [Respondents by Fear]
VAR _isFear = SELECTEDVALUE ( DimFear[Category] ) <> "Other Responses"
RETURN
    IF (
        HASONEVALUE ( DimFear[Fear] ) && _isFear && _value > 0,
        RANKX ( {RANKABLE}, [Respondents by Fear], _value, DESC, SKIP )
    )""")
m("Spine Top N", F_FEAR, "0",
  "Display rule (not data): a fear appears on the spine chart when it ranks within this Top N in either period.",
  "5")
m("Spine Include", F_FEAR, "0",
  "1 when the fear ranks within [Spine Top N] in childhood OR today; otherwise 0. Used by the Deneb spine chart.",
  """VAR _c = [Childhood Rank]
VAR _n = [Now Rank]
VAR _top = [Spine Top N]
RETURN
    IF (
        ( NOT ISBLANK ( _c ) && _c <= _top ) || ( NOT ISBLANK ( _n ) && _n <= _top ),
        1,
        0
    )""")
m("Top Childhood Fear", F_FEAR, None,
  "Most selected childhood fear (ties broken alphabetically).",
  f"""VAR _t = TOPN ( 1, {RANKABLE}, [Childhood Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )""")
m("Top Childhood Fear Respondents", F_FEAR, "#,0",
  "Respondents who selected the top childhood fear.",
  'CALCULATE ( [Childhood Respondents], TREATAS ( { [Top Childhood Fear] }, DimFear[Fear] ) )')
m("Top Current Fear", F_FEAR, None,
  "Most selected current fear (ties broken alphabetically).",
  f"""VAR _t = TOPN ( 1, {RANKABLE}, [Now Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )""")
m("Top Current Fear Respondents", F_FEAR, "#,0",
  "Respondents who selected the top current fear.",
  'CALCULATE ( [Now Respondents], TREATAS ( { [Top Current Fear] }, DimFear[Fear] ) )')
m("Biggest Rise Fear", F_FEAR, None,
  "Fear with the largest positive [Fear Change] (ties: more current respondents, then alphabetical).",
  f"""VAR _t = TOPN ( 1, {RANKABLE}, [Fear Change], DESC, [Now Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )""")
m("Biggest Fall Fear", F_FEAR, None,
  "Fear with the most negative [Fear Change] (ties: more childhood respondents, then alphabetical).",
  f"""VAR _t = TOPN ( 1, {RANKABLE}, [Fear Change], ASC, [Childhood Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )""")
m("Adult Only Top Fear", F_FEAR, None,
  "Most selected current fear that NO respondent selected in the childhood list.",
  f"""VAR _candidates =
    FILTER ( {RANKABLE}, ISBLANK ( [Childhood Respondents] ) && [Now Respondents] > 0 )
VAR _t = TOPN ( 1, _candidates, [Now Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )""")
m("Most Loyal Fear", F_FEAR, None,
  "Fear selected in both lists by the most respondents (ties: higher share of childhood respondents kept, then alphabetical).",
  f"""VAR _t =
    TOPN ( 1, {RANKABLE}, [Kept Respondents], DESC, DIVIDE ( [Kept Respondents], [Childhood Respondents] ), DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )""")

# ---------- persistence ----------
m("Persistent Fear Respondents", F_PERS, "#,0",
  "Respondents who selected at least one identical fear in their childhood and current lists.",
  "CALCULATE ( [Responses], KEEPFILTERS ( Respondent[FearsKept] > 0 ) )")
m("Persistent Fear %", F_PERS, "0.0%",
  "[Persistent Fear Respondents] / [Responses].",
  "DIVIDE ( [Persistent Fear Respondents], [Responses] )")
m("No Fear Kept Respondents", F_PERS, "#,0",
  "Respondents with no identical fear in both lists.",
  "CALCULATE ( [Responses], KEEPFILTERS ( Respondent[FearsKept] = 0 ) )")
m("Persistent Fear Respondents (Fact check)", F_QA, "#,0",
  "Independent re-computation of persistence from FactFearSelection[IsRetained]; must equal [Persistent Fear Respondents].",
  """CALCULATE (
    DISTINCTCOUNT ( FactFearSelection[ResponseKey] ),
    FactFearSelection[IsRetained] = TRUE (),
    REMOVEFILTERS ( DimFear )
)""")

# ---------- data nightmares ----------
m("Top Data Nightmare", F_NM, None,
  "Most chosen data nightmare (short label; single-choice question).",
  """VAR _t = TOPN ( 1, ALL ( Respondent[Nightmare] ), [Responses], DESC, Respondent[Nightmare], ASC )
RETURN MAXX ( _t, Respondent[Nightmare] )""")
m("Top Data Nightmare Detail", F_NM, None,
  "Text in brackets of the original answer for the top data nightmare.",
  """VAR _top = [Top Data Nightmare]
RETURN
    MAXX ( FILTER ( ALL ( Respondent[Nightmare], Respondent[NightmareDetail] ), Respondent[Nightmare] = _top ), Respondent[NightmareDetail] )""")
m("Data Nightmare Respondents", F_NM, "#,0",
  "Respondents who chose the top data nightmare.",
  "CALCULATE ( [Responses], TREATAS ( { [Top Data Nightmare] }, Respondent[Nightmare] ) )")
m("Data Nightmare %", F_NM, "0.0%",
  "[Data Nightmare Respondents] / all respondents.",
  "DIVIDE ( [Data Nightmare Respondents], CALCULATE ( [Responses], REMOVEFILTERS ( Respondent ) ) )")
m("Nightmare Share", F_NM, "0.0%",
  "Respondents choosing the nightmare in context / all respondents.",
  "DIVIDE ( [Responses], CALCULATE ( [Responses], REMOVEFILTERS ( Respondent ) ) )")
m("Nightmare Rank", F_NM, "0",
  "Rank of the nightmare answer by respondents (1 = most chosen).",
  """IF (
    HASONEVALUE ( Respondent[Nightmare] ),
    RANKX ( ALL ( Respondent[Nightmare] ), [Responses], , DESC, SKIP )
)""")

# ---------- poster text ----------
ARROW = 'UNICHAR ( 8594 )'
m("Text Survey Strip", F_TXT, None,
  "Method strip under the headline.",
  f"""FORMAT ( [Responses], "#,0" ) & " respondents   " & UNICHAR ( 183 ) & "   "
    & FORMAT ( [Childhood Fear Mentions], "#,0" ) & " childhood + "
    & FORMAT ( [Current Fear Mentions], "#,0" ) & " current fear selections   " & UNICHAR ( 183 ) & "   up to "
    & [Max Fears per List] & " fears per list" """)
def arrow_text(name, fear_measure, desc):
    m(name, F_TXT, None, desc,
      f"""VAR _f = [{fear_measure}]
VAR _c = CALCULATE ( COALESCE ( [Childhood Respondents], 0 ), TREATAS ( {{ _f }}, DimFear[Fear] ) )
VAR _n = CALCULATE ( COALESCE ( [Now Respondents], 0 ), TREATAS ( {{ _f }}, DimFear[Fear] ) )
RETURN _f & ":  " & _c & "  " & {ARROW} & "  " & _n""")
arrow_text("Text Biggest Rise", "Biggest Rise Fear", "e.g. War: 5 -> 19 (respondents, childhood -> today).")
arrow_text("Text Biggest Fall", "Biggest Fall Fear", "e.g. The dark: 11 -> 2 (respondents, childhood -> today).")
arrow_text("Text Adult Only", "Adult Only Top Fear", "Top fear that no respondent named as a child, childhood -> today.")
m("Text Persistent %", F_TXT, None, "Hero number for Act III.",
  'FORMAT ( [Persistent Fear %], "0.0%" )')
m("Text Persistent Count", F_TXT, None, "45 of 105 respondents.",
  'FORMAT ( [Persistent Fear Respondents], "#,0" ) & " of " & FORMAT ( [Responses], "#,0" ) & " respondents"')
m("Text Most Loyal", F_TXT, None, "Most loyal monster sentence.",
  """VAR _f = [Most Loyal Fear]
VAR _k = CALCULATE ( [Kept Respondents], TREATAS ( { _f }, DimFear[Fear] ) )
VAR _c = CALCULATE ( [Childhood Respondents], TREATAS ( { _f }, DimFear[Fear] ) )
RETURN
    "Most loyal monster:  " & _f & "  " & UNICHAR ( 8212 ) & "  " & _k & " of the " & _c
        & " who named it as children still name it today" """)

# ---------- accessibility (alt text) ----------
m("Alt Spine", F_A11Y, None, "Alt text for the Deneb spine chart.",
  """VAR _tc = [Top Childhood Fear]
VAR _tn = [Top Current Fear]
RETURN
    "Fears then and now, in respondents out of " & [Responses] & ". As children, the most named fear was "
        & _tc & " (" & [Top Childhood Fear Respondents] & "). Today it is " & _tn & " (" & [Top Current Fear Respondents]
        & "). Biggest rise: " & SUBSTITUTE ( [Text Biggest Rise], ":  ", " from " ) & ". Biggest fall: " & SUBSTITUTE ( [Text Biggest Fall], ":  ", " from " )
        & ". Nobody named " & [Adult Only Top Fear] & " as a child; " & CALCULATE ( [Now Respondents], TREATAS ( { [Adult Only Top Fear] }, DimFear[Fear] ) )
        & " name it today." """)
m("Alt Ghosts", F_A11Y, None, "Alt text for the 105 ghosts unit chart.",
  """"One ghost per respondent. " & [Persistent Fear Respondents] & " of " & [Responses] & " ("
    & FORMAT ( [Persistent Fear %], "0.0%" ) & ") named at least one identical fear as a child and today: "
    & CALCULATE ( [Responses], Respondent[FearsKept] = 1 ) & " kept one, "
    & CALCULATE ( [Responses], Respondent[FearsKept] = 2 ) & " kept two, "
    & CALCULATE ( [Responses], Respondent[FearsKept] = 3 ) & " kept three. "
    & [No Fear Kept Respondents] & " kept none. " & [Text Most Loyal] & "." """)
m("Alt Nightmares", F_A11Y, None, "Alt text for the data nightmare chart and card.",
  """"Worst data nightmare, one answer per respondent: " & [Top Data Nightmare] & " ("
    & [Top Data Nightmare Detail] & ") was chosen by " & [Data Nightmare Respondents] & " of " & [Responses]
    & " respondents (" & FORMAT ( [Data Nightmare %], "0.0%" ) & "), the most common answer." """)
m("Alt Persistent", F_A11Y, None, "Alt text for the persistence hero number.",
  """[Persistent Fear Respondents] & " of " & [Responses] & " respondents, " & FORMAT ( [Persistent Fear %], "0.0%" )
    & ", named at least one identical fear as a child and as an adult." """)

# ---------- tooltip pages (complementary detail only) ----------
F_TT = "Anatomy of Fear\\8 Tooltips"
m("TT Fear Name", F_TT, None, "Hovered fear (tooltip page).", 'SELECTEDVALUE ( DimFear[Fear], "Several fears" )')
m("TT Fear Category", F_TT, None, "Survey category of the hovered fear.", '"Survey category:  " & SELECTEDVALUE ( DimFear[Category], "-" )')
m("TT Childhood Text", F_TT, None, "Respondents and share, childhood list.",
  'FORMAT ( COALESCE ( [Childhood Respondents], 0 ), "0" ) & "   " & UNICHAR ( 183 ) & "   " & FORMAT ( COALESCE ( [Childhood Fear Share], 0 ), "0.0%" )')
m("TT Now Text", F_TT, None, "Respondents and share, current list.",
  'FORMAT ( COALESCE ( [Now Respondents], 0 ), "0" ) & "   " & UNICHAR ( 183 ) & "   " & FORMAT ( COALESCE ( [Now Fear Share], 0 ), "0.0%" )')
m("TT Kept Text", F_TT, None, "Same respondents in both lists, out of childhood respondents.",
  'FORMAT ( COALESCE ( [Kept Respondents], 0 ), "0" ) & " of " & FORMAT ( COALESCE ( [Childhood Respondents], 0 ), "0" )')
m("TT Persist Count", F_TT, "#,0", "Respondents with at least one identical fear (for the age-group tooltip chart).", "[Persistent Fear Respondents]")
m("TT Persist Size", F_TT, "#,0", "Respondents in the group (for the age-group tooltip chart).", "[Responses]")
m("TT Nightmare Name", F_TT, None, "Hovered data nightmare.", 'SELECTEDVALUE ( Respondent[Nightmare], "All data nightmares" )')
m("TT Nightmare Detail", F_TT, None, "Bracketed detail of the hovered data nightmare.", 'SELECTEDVALUE ( Respondent[NightmareDetail], "" )')
m("TT Nightmare Text", F_TT, None, "Respondents choosing the hovered nightmare, of all respondents.",
  'FORMAT ( [Responses], "0" ) & " of " & FORMAT ( CALCULATE ( [Responses], REMOVEFILTERS ( Respondent ) ), "0" ) & " respondents   " & UNICHAR ( 183 ) & "   " & FORMAT ( [Nightmare Share], "0.0%" )')
m("TT NM Count", F_TT, "#,0", "Respondents in the age group choosing the hovered nightmare.", "[Responses]")
m("TT NM Size", F_TT, "#,0", "All respondents in the age group, regardless of nightmare.",
  "CALCULATE ( [Responses], REMOVEFILTERS ( Respondent[Nightmare], Respondent[NightmareDetail], Respondent[dataNightmare] ) )")
m("HTML TT Ghost Alt", F_TT, None, "Alt text for the ghost case-file tooltip.",
  '''VAR _rk = SELECTEDVALUE ( Respondent[ResponseKey] )
RETURN "Case file for response " & _rk & ": " & SELECTEDVALUE ( Respondent[FearsKept] ) & " identical fear(s) - " & SELECTEDVALUE ( Respondent[KeptFears] ) & ". Age group " & SELECTEDVALUE ( Respondent[AgeGroup] ) & ". Worst data nightmare: " & SELECTEDVALUE ( Respondent[Nightmare] ) & "."''')
