# Medidas DAX — The Anatomy of Fear

Todas na tabela `_Measures`, pasta **Anatomy of Fear** (medidas HTML em `Assets/HTML`).

## Responses
*Pasta:* `Anatomy of Fear\1 Core`

Survey responses (one row per ResponseKey in Respondent). Denominator for every share on the poster.

```dax
Responses =
COUNTROWS ( Respondent )
```

## Childhood Fear Mentions
*Pasta:* `Anatomy of Fear\1 Core`

Fear selections in the childhood list. A respondent could select several fears, so this is NOT a count of people.

```dax
Childhood Fear Mentions =
CALCULATE (
    COUNTROWS ( FactFearSelection ),
    KEEPFILTERS ( FactFearSelection[LifeStage] = "Childhood" )
)
```

## Current Fear Mentions
*Pasta:* `Anatomy of Fear\1 Core`

Fear selections in the current (adult) list. A respondent could select several fears, so this is NOT a count of people.

```dax
Current Fear Mentions =
CALCULATE (
    COUNTROWS ( FactFearSelection ),
    KEEPFILTERS ( FactFearSelection[LifeStage] = "Adult" )
)
```

## Max Fears per List
*Pasta:* `Anatomy of Fear\1 Core`

Largest number of fears any respondent selected in one list (childhood or current).

```dax
Max Fears per List =
MAX ( MAX ( Respondent[ChildhoodFearCount] ), MAX ( Respondent[CurrentFearCount] ) )
```

## Respondents by Fear
*Pasta:* `Anatomy of Fear\2 Fears by period`

Distinct respondents who selected the fear(s) in context, in any period (respects a LifeStage filter if present).

```dax
Respondents by Fear =
DISTINCTCOUNT ( FactFearSelection[ResponseKey] )
```

## Childhood Respondents
*Pasta:* `Anatomy of Fear\2 Fears by period`

Distinct respondents who selected the fear in their childhood list.

```dax
Childhood Respondents =
CALCULATE (
    DISTINCTCOUNT ( FactFearSelection[ResponseKey] ),
    KEEPFILTERS ( FactFearSelection[LifeStage] = "Childhood" )
)
```

## Now Respondents
*Pasta:* `Anatomy of Fear\2 Fears by period`

Distinct respondents who selected the fear in their current (adult) list.

```dax
Now Respondents =
CALCULATE (
    DISTINCTCOUNT ( FactFearSelection[ResponseKey] ),
    KEEPFILTERS ( FactFearSelection[LifeStage] = "Adult" )
)
```

## Kept Respondents
*Pasta:* `Anatomy of Fear\2 Fears by period`

Distinct respondents who selected exactly the same fear in BOTH lists (IsRetained). Not a causal or continuous-fear claim.

```dax
Kept Respondents =
CALCULATE (
    DISTINCTCOUNT ( FactFearSelection[ResponseKey] ),
    KEEPFILTERS ( FactFearSelection[IsRetained] = TRUE () )
)
```

## Fear Share
*Pasta:* `Anatomy of Fear\2 Fears by period`

Respondents selecting the fear in context divided by all respondents.

```dax
Fear Share =
DIVIDE ( [Respondents by Fear], [Responses] )
```

## Childhood Fear Share
*Pasta:* `Anatomy of Fear\2 Fears by period`

Childhood respondents for the fear divided by all respondents.

```dax
Childhood Fear Share =
DIVIDE ( [Childhood Respondents], [Responses] )
```

## Now Fear Share
*Pasta:* `Anatomy of Fear\2 Fears by period`

Current respondents for the fear divided by all respondents.

```dax
Now Fear Share =
DIVIDE ( [Now Respondents], [Responses] )
```

## Fear Change
*Pasta:* `Anatomy of Fear\2 Fears by period`

Current respondents minus childhood respondents for the fear. Difference between two aggregate counts, NOT individual transitions.

```dax
Fear Change =
COALESCE ( [Now Respondents], 0 ) - COALESCE ( [Childhood Respondents], 0 )
```

## Fear Share Difference
*Pasta:* `Anatomy of Fear\2 Fears by period`

Current share minus childhood share (percentage points of all respondents).

```dax
Fear Share Difference =
COALESCE ( [Now Fear Share], 0 ) - COALESCE ( [Childhood Fear Share], 0 )
```

## Childhood Rank
*Pasta:* `Anatomy of Fear\2 Fears by period`

Rank of the fear by childhood respondents (1 = most selected, ties share a rank, SKIP). Excludes non-fear answers (Other Responses category).

```dax
Childhood Rank =
VAR _value = [Childhood Respondents]
VAR _isFear = SELECTEDVALUE ( DimFear[Category] ) <> "Other Responses"
RETURN
    IF (
        HASONEVALUE ( DimFear[Fear] ) && _isFear && _value > 0,
        RANKX ( CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), [Childhood Respondents], _value, DESC, SKIP )
    )
```

## Now Rank
*Pasta:* `Anatomy of Fear\2 Fears by period`

Rank of the fear by current respondents (1 = most selected, ties share a rank, SKIP). Excludes non-fear answers.

```dax
Now Rank =
VAR _value = [Now Respondents]
VAR _isFear = SELECTEDVALUE ( DimFear[Category] ) <> "Other Responses"
RETURN
    IF (
        HASONEVALUE ( DimFear[Fear] ) && _isFear && _value > 0,
        RANKX ( CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), [Now Respondents], _value, DESC, SKIP )
    )
```

## Fear Rank
*Pasta:* `Anatomy of Fear\2 Fears by period`

Rank of the fear by respondents in the current filter context (for example a LifeStage filter).

```dax
Fear Rank =
VAR _value = [Respondents by Fear]
VAR _isFear = SELECTEDVALUE ( DimFear[Category] ) <> "Other Responses"
RETURN
    IF (
        HASONEVALUE ( DimFear[Fear] ) && _isFear && _value > 0,
        RANKX ( CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), [Respondents by Fear], _value, DESC, SKIP )
    )
```

## Spine Top N
*Pasta:* `Anatomy of Fear\2 Fears by period`

Display rule (not data): a fear appears on the spine chart when it ranks within this Top N in either period.

```dax
Spine Top N =
5
```

## Spine Include
*Pasta:* `Anatomy of Fear\2 Fears by period`

1 when the fear ranks within [Spine Top N] in childhood OR today; otherwise 0. Used by the Deneb spine chart.

```dax
Spine Include =
VAR _c = [Childhood Rank]
VAR _n = [Now Rank]
VAR _top = [Spine Top N]
RETURN
    IF (
        ( NOT ISBLANK ( _c ) && _c <= _top ) || ( NOT ISBLANK ( _n ) && _n <= _top ),
        1,
        0
    )
```

## Top Childhood Fear
*Pasta:* `Anatomy of Fear\2 Fears by period`

Most selected childhood fear (ties broken alphabetically).

```dax
Top Childhood Fear =
VAR _t = TOPN ( 1, CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), [Childhood Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )
```

## Top Childhood Fear Respondents
*Pasta:* `Anatomy of Fear\2 Fears by period`

Respondents who selected the top childhood fear.

```dax
Top Childhood Fear Respondents =
CALCULATE ( [Childhood Respondents], TREATAS ( { [Top Childhood Fear] }, DimFear[Fear] ) )
```

## Top Current Fear
*Pasta:* `Anatomy of Fear\2 Fears by period`

Most selected current fear (ties broken alphabetically).

```dax
Top Current Fear =
VAR _t = TOPN ( 1, CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), [Now Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )
```

## Top Current Fear Respondents
*Pasta:* `Anatomy of Fear\2 Fears by period`

Respondents who selected the top current fear.

```dax
Top Current Fear Respondents =
CALCULATE ( [Now Respondents], TREATAS ( { [Top Current Fear] }, DimFear[Fear] ) )
```

## Biggest Rise Fear
*Pasta:* `Anatomy of Fear\2 Fears by period`

Fear with the largest positive [Fear Change] (ties: more current respondents, then alphabetical).

```dax
Biggest Rise Fear =
VAR _t = TOPN ( 1, CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), [Fear Change], DESC, [Now Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )
```

## Biggest Fall Fear
*Pasta:* `Anatomy of Fear\2 Fears by period`

Fear with the most negative [Fear Change] (ties: more childhood respondents, then alphabetical).

```dax
Biggest Fall Fear =
VAR _t = TOPN ( 1, CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), [Fear Change], ASC, [Childhood Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )
```

## Adult Only Top Fear
*Pasta:* `Anatomy of Fear\2 Fears by period`

Most selected current fear that NO respondent selected in the childhood list.

```dax
Adult Only Top Fear =
VAR _candidates =
    FILTER ( CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), ISBLANK ( [Childhood Respondents] ) && [Now Respondents] > 0 )
VAR _t = TOPN ( 1, _candidates, [Now Respondents], DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )
```

## Most Loyal Fear
*Pasta:* `Anatomy of Fear\2 Fears by period`

Fear selected in both lists by the most respondents (ties: higher share of childhood respondents kept, then alphabetical).

```dax
Most Loyal Fear =
VAR _t =
    TOPN ( 1, CALCULATETABLE (
        VALUES ( DimFear[Fear] ),
        DimFear[Category] <> "Other Responses",
        REMOVEFILTERS ( DimFear )
    ), [Kept Respondents], DESC, DIVIDE ( [Kept Respondents], [Childhood Respondents] ), DESC, DimFear[Fear], ASC )
RETURN MAXX ( _t, DimFear[Fear] )
```

## Persistent Fear Respondents
*Pasta:* `Anatomy of Fear\3 Persistence`

Respondents who selected at least one identical fear in their childhood and current lists.

```dax
Persistent Fear Respondents =
CALCULATE ( [Responses], KEEPFILTERS ( Respondent[FearsKept] > 0 ) )
```

## Persistent Fear %
*Pasta:* `Anatomy of Fear\3 Persistence`

[Persistent Fear Respondents] / [Responses].

```dax
Persistent Fear % =
DIVIDE ( [Persistent Fear Respondents], [Responses] )
```

## No Fear Kept Respondents
*Pasta:* `Anatomy of Fear\3 Persistence`

Respondents with no identical fear in both lists.

```dax
No Fear Kept Respondents =
CALCULATE ( [Responses], KEEPFILTERS ( Respondent[FearsKept] = 0 ) )
```

## Persistent Fear Respondents (Fact check)
*Pasta:* `Anatomy of Fear\9 QA`

Independent re-computation of persistence from FactFearSelection[IsRetained]; must equal [Persistent Fear Respondents].

```dax
Persistent Fear Respondents (Fact check) =
CALCULATE (
    DISTINCTCOUNT ( FactFearSelection[ResponseKey] ),
    FactFearSelection[IsRetained] = TRUE (),
    REMOVEFILTERS ( DimFear )
)
```

## Top Data Nightmare
*Pasta:* `Anatomy of Fear\4 Data nightmares`

Most chosen data nightmare (short label; single-choice question).

```dax
Top Data Nightmare =
VAR _t = TOPN ( 1, ALL ( Respondent[Nightmare] ), [Responses], DESC, Respondent[Nightmare], ASC )
RETURN MAXX ( _t, Respondent[Nightmare] )
```

## Top Data Nightmare Detail
*Pasta:* `Anatomy of Fear\4 Data nightmares`

Text in brackets of the original answer for the top data nightmare.

```dax
Top Data Nightmare Detail =
VAR _top = [Top Data Nightmare]
RETURN
    MAXX ( FILTER ( ALL ( Respondent[Nightmare], Respondent[NightmareDetail] ), Respondent[Nightmare] = _top ), Respondent[NightmareDetail] )
```

## Data Nightmare Respondents
*Pasta:* `Anatomy of Fear\4 Data nightmares`

Respondents who chose the top data nightmare.

```dax
Data Nightmare Respondents =
CALCULATE ( [Responses], TREATAS ( { [Top Data Nightmare] }, Respondent[Nightmare] ) )
```

## Data Nightmare %
*Pasta:* `Anatomy of Fear\4 Data nightmares`

[Data Nightmare Respondents] / all respondents.

```dax
Data Nightmare % =
DIVIDE ( [Data Nightmare Respondents], CALCULATE ( [Responses], REMOVEFILTERS ( Respondent ) ) )
```

## Nightmare Share
*Pasta:* `Anatomy of Fear\4 Data nightmares`

Respondents choosing the nightmare in context / all respondents.

```dax
Nightmare Share =
DIVIDE ( [Responses], CALCULATE ( [Responses], REMOVEFILTERS ( Respondent ) ) )
```

## Nightmare Rank
*Pasta:* `Anatomy of Fear\4 Data nightmares`

Rank of the nightmare answer by respondents (1 = most chosen).

```dax
Nightmare Rank =
IF (
    HASONEVALUE ( Respondent[Nightmare] ),
    RANKX ( ALL ( Respondent[Nightmare] ), [Responses], , DESC, SKIP )
)
```

## Text Survey Strip
*Pasta:* `Anatomy of Fear\5 Poster text`

Method strip under the headline.

```dax
Text Survey Strip =
FORMAT ( [Responses], "#,0" ) & " respondents   " & UNICHAR ( 183 ) & "   "
    & FORMAT ( [Childhood Fear Mentions], "#,0" ) & " childhood + "
    & FORMAT ( [Current Fear Mentions], "#,0" ) & " current fear selections   " & UNICHAR ( 183 ) & "   up to "
    & [Max Fears per List] & " fears per list" 
```

## Text Biggest Rise
*Pasta:* `Anatomy of Fear\5 Poster text`

e.g. War: 5 -> 19 (respondents, childhood -> today).

```dax
Text Biggest Rise =
VAR _f = [Biggest Rise Fear]
VAR _c = CALCULATE ( COALESCE ( [Childhood Respondents], 0 ), TREATAS ( { _f }, DimFear[Fear] ) )
VAR _n = CALCULATE ( COALESCE ( [Now Respondents], 0 ), TREATAS ( { _f }, DimFear[Fear] ) )
RETURN _f & ":  " & _c & "  " & UNICHAR ( 8594 ) & "  " & _n
```

## Text Biggest Fall
*Pasta:* `Anatomy of Fear\5 Poster text`

e.g. The dark: 11 -> 2 (respondents, childhood -> today).

```dax
Text Biggest Fall =
VAR _f = [Biggest Fall Fear]
VAR _c = CALCULATE ( COALESCE ( [Childhood Respondents], 0 ), TREATAS ( { _f }, DimFear[Fear] ) )
VAR _n = CALCULATE ( COALESCE ( [Now Respondents], 0 ), TREATAS ( { _f }, DimFear[Fear] ) )
RETURN _f & ":  " & _c & "  " & UNICHAR ( 8594 ) & "  " & _n
```

## Text Adult Only
*Pasta:* `Anatomy of Fear\5 Poster text`

Top fear that no respondent named as a child, childhood -> today.

```dax
Text Adult Only =
VAR _f = [Adult Only Top Fear]
VAR _c = CALCULATE ( COALESCE ( [Childhood Respondents], 0 ), TREATAS ( { _f }, DimFear[Fear] ) )
VAR _n = CALCULATE ( COALESCE ( [Now Respondents], 0 ), TREATAS ( { _f }, DimFear[Fear] ) )
RETURN _f & ":  " & _c & "  " & UNICHAR ( 8594 ) & "  " & _n
```

## Text Persistent %
*Pasta:* `Anatomy of Fear\5 Poster text`

Hero number for Act III.

```dax
Text Persistent % =
FORMAT ( [Persistent Fear %], "0.0%" )
```

## Text Persistent Count
*Pasta:* `Anatomy of Fear\5 Poster text`

45 of 105 respondents.

```dax
Text Persistent Count =
FORMAT ( [Persistent Fear Respondents], "#,0" ) & " of " & FORMAT ( [Responses], "#,0" ) & " respondents"
```

## Text Most Loyal
*Pasta:* `Anatomy of Fear\5 Poster text`

Most loyal monster sentence.

```dax
Text Most Loyal =
VAR _f = [Most Loyal Fear]
VAR _k = CALCULATE ( [Kept Respondents], TREATAS ( { _f }, DimFear[Fear] ) )
VAR _c = CALCULATE ( [Childhood Respondents], TREATAS ( { _f }, DimFear[Fear] ) )
RETURN
    "Most loyal monster:  " & _f & "  " & UNICHAR ( 8212 ) & "  " & _k & " of the " & _c
        & " who named it as children still name it today" 
```

## Alt Spine
*Pasta:* `Anatomy of Fear\6 Accessibility`

Alt text for the Deneb spine chart.

```dax
Alt Spine =
VAR _tc = [Top Childhood Fear]
VAR _tn = [Top Current Fear]
RETURN
    "Fears then and now, in respondents out of " & [Responses] & ". As children, the most named fear was "
        & _tc & " (" & [Top Childhood Fear Respondents] & "). Today it is " & _tn & " (" & [Top Current Fear Respondents]
        & "). Biggest rise: " & SUBSTITUTE ( [Text Biggest Rise], ":  ", " from " ) & ". Biggest fall: " & SUBSTITUTE ( [Text Biggest Fall], ":  ", " from " )
        & ". Nobody named " & [Adult Only Top Fear] & " as a child; " & CALCULATE ( [Now Respondents], TREATAS ( { [Adult Only Top Fear] }, DimFear[Fear] ) )
        & " name it today." 
```

## Alt Ghosts
*Pasta:* `Anatomy of Fear\6 Accessibility`

Alt text for the 105 ghosts unit chart.

```dax
Alt Ghosts =
"One ghost per respondent. " & [Persistent Fear Respondents] & " of " & [Responses] & " ("
    & FORMAT ( [Persistent Fear %], "0.0%" ) & ") named at least one identical fear as a child and today: "
    & CALCULATE ( [Responses], Respondent[FearsKept] = 1 ) & " kept one, "
    & CALCULATE ( [Responses], Respondent[FearsKept] = 2 ) & " kept two, "
    & CALCULATE ( [Responses], Respondent[FearsKept] = 3 ) & " kept three. "
    & [No Fear Kept Respondents] & " kept none. " & [Text Most Loyal] & "." 
```

## Alt Nightmares
*Pasta:* `Anatomy of Fear\6 Accessibility`

Alt text for the data nightmare chart and card.

```dax
Alt Nightmares =
"Worst data nightmare, one answer per respondent: " & [Top Data Nightmare] & " ("
    & [Top Data Nightmare Detail] & ") was chosen by " & [Data Nightmare Respondents] & " of " & [Responses]
    & " respondents (" & FORMAT ( [Data Nightmare %], "0.0%" ) & "), the most common answer." 
```

## Alt Persistent
*Pasta:* `Anatomy of Fear\6 Accessibility`

Alt text for the persistence hero number.

```dax
Alt Persistent =
[Persistent Fear Respondents] & " of " & [Responses] & " respondents, " & FORMAT ( [Persistent Fear %], "0.0%" )
    & ", named at least one identical fear as a child and as an adult." 
```

## TT Fear Name
*Pasta:* `Anatomy of Fear\8 Tooltips`

Hovered fear (tooltip page).

```dax
TT Fear Name =
SELECTEDVALUE ( DimFear[Fear], "Several fears" )
```

## TT Fear Category
*Pasta:* `Anatomy of Fear\8 Tooltips`

Survey category of the hovered fear.

```dax
TT Fear Category =
"Survey category:  " & SELECTEDVALUE ( DimFear[Category], "-" )
```

## TT Childhood Text
*Pasta:* `Anatomy of Fear\8 Tooltips`

Respondents and share, childhood list.

```dax
TT Childhood Text =
FORMAT ( COALESCE ( [Childhood Respondents], 0 ), "0" ) & "   " & UNICHAR ( 183 ) & "   " & FORMAT ( COALESCE ( [Childhood Fear Share], 0 ), "0.0%" )
```

## TT Now Text
*Pasta:* `Anatomy of Fear\8 Tooltips`

Respondents and share, current list.

```dax
TT Now Text =
FORMAT ( COALESCE ( [Now Respondents], 0 ), "0" ) & "   " & UNICHAR ( 183 ) & "   " & FORMAT ( COALESCE ( [Now Fear Share], 0 ), "0.0%" )
```

## TT Kept Text
*Pasta:* `Anatomy of Fear\8 Tooltips`

Same respondents in both lists, out of childhood respondents.

```dax
TT Kept Text =
FORMAT ( COALESCE ( [Kept Respondents], 0 ), "0" ) & " of " & FORMAT ( COALESCE ( [Childhood Respondents], 0 ), "0" )
```

## TT Persist Count
*Pasta:* `Anatomy of Fear\8 Tooltips`

Respondents with at least one identical fear (for the age-group tooltip chart).

```dax
TT Persist Count =
[Persistent Fear Respondents]
```

## TT Persist Size
*Pasta:* `Anatomy of Fear\8 Tooltips`

Respondents in the group (for the age-group tooltip chart).

```dax
TT Persist Size =
[Responses]
```

## TT Nightmare Name
*Pasta:* `Anatomy of Fear\8 Tooltips`

Hovered data nightmare.

```dax
TT Nightmare Name =
SELECTEDVALUE ( Respondent[Nightmare], "All data nightmares" )
```

## TT Nightmare Detail
*Pasta:* `Anatomy of Fear\8 Tooltips`

Bracketed detail of the hovered data nightmare.

```dax
TT Nightmare Detail =
SELECTEDVALUE ( Respondent[NightmareDetail], "" )
```

## TT Nightmare Text
*Pasta:* `Anatomy of Fear\8 Tooltips`

Respondents choosing the hovered nightmare, of all respondents.

```dax
TT Nightmare Text =
FORMAT ( [Responses], "0" ) & " of " & FORMAT ( CALCULATE ( [Responses], REMOVEFILTERS ( Respondent ) ), "0" ) & " respondents   " & UNICHAR ( 183 ) & "   " & FORMAT ( [Nightmare Share], "0.0%" )
```

## TT NM Count
*Pasta:* `Anatomy of Fear\8 Tooltips`

Respondents in the age group choosing the hovered nightmare.

```dax
TT NM Count =
[Responses]
```

## TT NM Size
*Pasta:* `Anatomy of Fear\8 Tooltips`

All respondents in the age group, regardless of nightmare.

```dax
TT NM Size =
CALCULATE ( [Responses], REMOVEFILTERS ( Respondent[Nightmare], Respondent[NightmareDetail], Respondent[dataNightmare] ) )
```

## HTML TT Ghost Alt
*Pasta:* `Anatomy of Fear\8 Tooltips`

Alt text for the ghost case-file tooltip.

```dax
HTML TT Ghost Alt =
VAR _rk = SELECTEDVALUE ( Respondent[ResponseKey] )
RETURN "Case file for response " & _rk & ": " & SELECTEDVALUE ( Respondent[FearsKept] ) & " identical fear(s) - " & SELECTEDVALUE ( Respondent[KeptFears] ) & ". Age group " & SELECTEDVALUE ( Respondent[AgeGroup] ) & ". Worst data nightmare: " & SELECTEDVALUE ( Respondent[Nightmare] ) & "."
```
