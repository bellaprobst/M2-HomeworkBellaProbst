from __future__ import annotations

from pathlib import Path
import re

import matplotlib.pyplot as plt
import pandas as pd


DATA_PATH = Path("data/Grad Program Exit Survey Data 2024 (1).xlsx")
SHEET_NAME = "MAcc Exit Survey - April 2024_M"
OUTPUT_DIR = Path("outputs")
OUTPUT_CSV = OUTPUT_DIR / "rank_order.csv"
OUTPUT_PNG = OUTPUT_DIR / "rank_order.png"

RATING_COLUMNS = [
    "Q76_1",
    "Q77_2",
    "Q78_3",
    "Q83_4",
    "Q82_5",
    "Q80_6",
    "Q81_9",
    "Q79_7",
]


def parse_course_label(raw_value: object, fallback: str) -> str:
    """Extract readable course label from Qualtrics question text row."""
    if raw_value is None or (isinstance(raw_value, float) and pd.isna(raw_value)):
        return fallback

    text = str(raw_value).strip()
    if not text:
        return fallback

    # Remove leading "Rate " when present.
    text = re.sub(r"^\s*Rate\s+", "", text, flags=re.IGNORECASE)

    # Keep text before " on a..." for concise course title.
    text = re.split(r"\s+on\s+a\b", text, maxsplit=1, flags=re.IGNORECASE)[0].strip(" .:-")

    return text or fallback


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME, engine="openpyxl")

    missing_cols = [c for c in RATING_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected rating columns: {missing_cols}")

    # Qualtrics export:
    # row index 0 -> human-readable question text
    # row index 1 -> ImportId metadata
    # real responses start at index 2
    label_row = df.iloc[0]
    response_df = df.iloc[2:].copy()

    course_map = {
        col: parse_course_label(label_row.get(col), col)
        for col in RATING_COLUMNS
    }

    # Long-format ratings table (deterministic column selection order).
    long_df = response_df[RATING_COLUMNS].melt(
        value_vars=RATING_COLUMNS,
        var_name="course_column",
        value_name="rating",
    )
    long_df["course_label"] = long_df["course_column"].map(course_map)
    long_df["rating"] = pd.to_numeric(long_df["rating"], errors="coerce")

    summary = (
        long_df.groupby(["course_column", "course_label"], dropna=False)
        .agg(
            score_mean=("rating", "mean"),
            n_responses=("rating", "count"),
        )
        .reset_index()
    )

    # Deterministic ranking:
    # 1) score_mean descending
    # 2) n_responses descending
    # 3) course_label alphabetical ascending
    ranking = (
        summary.sort_values(
            by=["score_mean", "n_responses", "course_label"],
            ascending=[False, False, True],
            kind="mergesort",
        )
        .reset_index(drop=True)
    )
    ranking.insert(0, "rank", ranking.index + 1)

    output_ranking = ranking[["rank", "course_label", "score_mean", "n_responses"]].copy()
    output_ranking.to_csv(OUTPUT_CSV, index=False)

    # Horizontal bar chart: best course at the top.
    plt.figure(figsize=(10, 6))
    plt.barh(output_ranking["course_label"], output_ranking["score_mean"])
    plt.gca().invert_yaxis()
    plt.title("MAcc 2024 Course Rankings by Mean Student Rating")
    plt.xlabel("Mean Rating")
    plt.ylabel("Course")
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150)
    plt.close()

    print(f"Saved ranking CSV to: {OUTPUT_CSV}")
    print(f"Saved ranking chart to: {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
