# MAcc Exit Survey 2024 Course Ranking Workflow

This repository contains a deterministic, repeatable data workflow that answers the research question:

**“Rank order the programs or courses based on student ratings or preferences for that year (2024).”**

The analysis uses one year of survey data from:

- `data/Grad Program Exit Survey Data 2024 (1).xlsx`
- Sheet: `MAcc Exit Survey - April 2024_M`

## What the workflow does

The script in `src/rank_courses.py`:

1. Loads the Excel file and reads the specified worksheet.
2. Uses Qualtrics layout assumptions:
   - Row 1 in the worksheet body (index 0 in pandas) has human-readable question text.
   - Row 2 in the worksheet body (index 1 in pandas) has ImportId metadata.
   - Real responses begin at row index 2.
3. Uses these rating columns:
   - `Q76_1`, `Q77_2`, `Q78_3`, `Q83_4`, `Q82_5`, `Q80_6`, `Q81_9`, `Q79_7`
4. Extracts readable course labels from the first row text (with fallback to column names).
5. Converts ratings to numeric (`errors='coerce'`) and computes per-course:
   - `score_mean` = mean rating ignoring missing values
   - `n_responses` = non-missing rating count
6. Ranks courses deterministically by:
   1. Higher `score_mean`
   2. Higher `n_responses`
   3. Alphabetical `course_label`
7. Writes outputs:
   - `outputs/rank_order.csv`
   - `outputs/rank_order.png`

## Run locally

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/rank_courses.py
```

After running, check:

- `outputs/rank_order.csv`
- `outputs/rank_order.png`

## GitHub Actions automation

The workflow `.github/workflows/run_analysis.yml` runs on:

- `push`
- `workflow_dispatch`

It performs the following steps on `ubuntu-latest`:

1. Checks out the repository
2. Sets up Python 3.11
3. Installs dependencies from `requirements.txt`
4. Runs `python src/rank_courses.py`
5. Uploads the `outputs/` directory as an artifact named **outputs**
