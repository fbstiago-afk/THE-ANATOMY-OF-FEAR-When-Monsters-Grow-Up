# The Anatomy of Fear — When Monsters Grow Up

<!-- portfolio-link:start -->
[![View the poster in Power BI](https://img.shields.io/badge/View%20the%20poster-Power%20BI-6C3BAA?style=for-the-badge)](https://app.powerbi.com/view?r=eyJrIjoiMGViN2ZkYmMtOGUwNy00NGFmLTg2YTItNjBiYmY3MTI0MWEyIiwidCI6IjMxYzJjZDk3LWE3MGItNDgwYy1iZTM1LTBhMGRiMzgwZTNlNCJ9)
[![More projects](https://img.shields.io/badge/More%20projects-bocardidata.com.br-24172F?style=for-the-badge)](https://bocardidata.com.br)

> 🔗 **Live report (Publish to web):** [https://app.powerbi.com/view?r=eyJrIjoiMGViN2…](https://app.powerbi.com/view?r=eyJrIjoiMGViN2ZkYmMtOGUwNy00NGFmLTg2YTItNjBiYmY3MTI0MWEyIiwidCI6IjMxYzJjZDk3LWE3MGItNDgwYy1iZTM1LTBhMGRiMzgwZTNlNCJ9)
> 📂 **More Power BI projects:** **[bocardidata.com.br](https://bocardidata.com.br)**
<!-- portfolio-link:end -->

My entry for the **Halloween Data Visualization Contest 2026** (Microsoft Fabric / Power BI Community). One A4 portrait page, built in Power BI, telling how our fears change from childhood to adulthood, using only the 105 responses of the official survey.

> *We outgrew the monsters. Not the fear.*

🇧🇷 [Versão em português](README.pt-BR.md)

## What's in the repo

- `TheAnatomyOfFear_Submission.pbix` → the file for submission (`TheAnatomyOfFear.pbix` is identical).
- `TheAnatomyOfFear.pbip` + `.Report` and `.SemanticModel` folders → the open project (PBIR + TMDL), where I work.
- `Assets/` → background (SVG and exported JPG), theme, Deneb specs, HTML/CSS for the animations, PNG preview.
- `Documentacao/` → DAX measures, the `Respondent` query, layout notes, contest checklist and my helper scripts.
- `survey_responses.csv` → the official dataset, untouched.
- `STATUS.md` → where I am and what is left (in Portuguese).

## The story

The poster reads top to bottom in four parts:

1. **The monsters changed shape (I–II).** A "spine" chart: childhood on one side, today on the other. As kids, people feared *Being trapped / small spaces* (14), *Heights* (13), *Snakes* and *The dark* (11). Today: *War* (19), *Uncertainty about the future* (14), *Death* (12), *Financial insecurity* (11). Below it, three highlights: War 5 → 19, The dark 11 → 2 and Financial insecurity 0 → 11 (nobody named it as a child).
2. **The fears that never left (III).** 45 of 105 people (42.9%) named the exact same fear in both lists. Each person is a little ghost; the lit ones still carry an old fear. The most loyal monster is *Snakes*: 6 of the 11 who feared them as kids still do.
3. **Even data has monsters (IV).** The worst nightmare for people who work with data: *It arrives a mess*, 23 of 105 (21.9%).
4. Closing line: *The monsters didn't disappear. They learned to use spreadsheets.*

A few caveats are written on the poster itself: counts are people, not selections; respondents could pick several fears; it is a voluntary community sample, not the general population; and the ▲▼ arrows compare totals, they don't show each person's trajectory.

## Model

I kept the whole starter model (same source, same JSON parser, tables `FactFearSelection`, `DimFear`, `DimAgeGroup`, `DimGender`, `DimCountry`) and added:

- a **`Respondent`** table, one row per response, with the original `dataNightmare`, short labels (`Nightmare`, `NightmareDetail`), `AgeGroup`, how many fears were kept (`FearsKept`) and which ones (`KeptFears`);
- a `Respondent[ResponseKey]` 1 → * `FactFearSelection[ResponseKey]` relationship, single direction;
- measures in the **Anatomy of Fear** folder (see `Documentacao/DAX_Measures.md`). No number on the poster is typed by hand; everything comes from measures. Rankings leave out *None of these*, *Prefer not to answer* and *Something else*.

## Visuals

- **Deneb (Vega-Lite):** the fear spine, the 105 ghosts and the data-nightmare ranking.
- **HTML Content:** the ghost with a candle (decorative) and the data-nightmare card. The card icon is only an illustration: empty cell = missing value, repeated bars = duplicates, misaligned bars = mixed formats.
- **Native:** titles, text and key numbers are text boxes and cards, which behave better with screen readers.
- The background (gothic frame, moon, bats, web, skyline) is a single image with no information in it.

### Tooltips

The contest allows tooltip pages for extra detail as long as the story works without them, so everything essential is on the main page. I made four hidden ones:

| Tooltip | Shows up on | What it shows |
|---|---|---|
| Fear dossier | any fear in the spine | category, people and % in childhood and today, how many kept it, chart by age group |
| Persistence | 42.9%, "45 of 105", *Most loyal monster* | the fears that stayed most, and % keeping any fear by age group |
| Data nightmare | nightmare bars | answer detail, n and %, % by age group |
| Ghost case file | each ghost | the response "file": childhood and current fears, kept ones highlighted, age group and data nightmare |

Each one has a small CSS animation (eyes in the dark and a spider, a ghost peeking from a tombstone and a candle, a haunted spreadsheet and a bat, a floating ghost on the file). They are decoration only and stop when the system asks for reduced motion.

I did not use bookmarks: they added nothing to the story and complicated keyboard navigation.

## Accessibility

- Contrast checked against the `#151020` background: text between 8:1 and 15.8:1; bars above 4:1; the mint band above 3:1 over the bars.
- Nothing relies on color alone: written values, ▲▼, ranks #1–#3, filled vs hollow ghosts with numbers.
- Alt text comes from measures and states the finding with its total (e.g. "45 of 105 respondents, 42.9%…").
- Tab order follows reading order; the decorative ghost is outside it.

## Opening it

Open the `.pbix` directly. To refresh, the source is the official contest blob (anonymous access). Marketplace visuals used: **Deneb** and **HTML Content**, both embedded in the PBIX.

The scripts in `Documentacao/scripts` rebuild the project and the background when I change the layout (`python Documentacao/scripts/build.py pbip Assets/Background/AnatomyOfFear_Background.jpg`).
