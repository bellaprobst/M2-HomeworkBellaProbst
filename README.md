# M2 Homework: MAcc 2024 Course Ranking Workflow

This repository answers the research question:

> **"Rank order the programs or courses based on student ratings or preferences for that year."**

using one year of MAcc exit survey data (2024), in a deterministic and repeatable way.

## Data source

- Expected input file: `data/Grad Program Exit Survey Data 2024 (1).xlsx`
- Excel sheet: `MAcc Exit Survey - April 2024_M`
- Qualtrics export structure used by the script:
  - Row 1 (index 0): human-readable question text
  - Row 2 (index 1): `ImportId` metadata
  - Real survey responses start on Row 3 (index 2)

## What the analysis does

`src/rank_courses.py`:

1. Loads the Excel sheet.
2. Extracts course labels from the first data row (question text), with fallback to column names.
3. Drops the first two non-response rows.
4. Uses these rating columns:
   - `Q76_1`, `Q77_2`, `Q78_3`, `Q83_4`, `Q82_5`, `Q80_6`, `Q81_9`, `Q79_7`
5. Converts ratings to numeric with coercion to `NaN`.
6. Computes per-course:
   - `score_mean` (mean rating, ignoring `NaN`)
   - `n_responses` (non-`NaN` count)
7. Applies deterministic ranking:
   1. Higher `score_mean`
   2. Higher `n_responses`
   3. Alphabetical `course_label`

## Outputs

Generated files are written to `outputs/`:

- `outputs/rank_order.csv` — ranked table with columns:
  - `rank`, `course_label`, `score_mean`, `n_responses`
- `outputs/rank_order.png` — horizontal bar chart of mean ratings

## Run locally

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/rank_courses.py
```

## GitHub Actions automation

Workflow file: `.github/workflows/run_analysis.yml`

On every `push` and manual `workflow_dispatch`, GitHub Actions will:

1. Set up Python 3.11
2. Install dependencies from `requirements.txt`
3. Run `python src/rank_courses.py`
4. Upload the `outputs/` directory as an artifact named **outputs**
