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


def extract_course_label(raw_text: object, fallback: str) -> str:
    if not isinstance(raw_text, str):
        return fallback

    label = raw_text.strip()
    if not label:
        return fallback

    label = re.sub(r"^Rate\s+", "", label, flags=re.IGNORECASE)
    label = re.split(r"\s+on\s+a\b", label, maxsplit=1, flags=re.IGNORECASE)[0].strip()

    return label or fallback


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME, engine="openpyxl")

    missing_columns = [col for col in RATING_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected rating columns: {missing_columns}")

    label_row = df.iloc[0]

    ratings_df = df.iloc[2:].copy()
    label_map = {
        col: extract_course_label(label_row.get(col), fallback=col) for col in RATING_COLUMNS
    }

    long_df = ratings_df[RATING_COLUMNS].melt(
        value_vars=RATING_COLUMNS,
        var_name="course_column",
        value_name="rating",
    )
    long_df["course_label"] = long_df["course_column"].map(label_map)
    long_df["rating"] = pd.to_numeric(long_df["rating"], errors="coerce")

    summary_df = (
        long_df.groupby(["course_column", "course_label"], as_index=False)
        .agg(score_mean=("rating", "mean"), n_responses=("rating", "count"))
        .sort_values(
            by=["score_mean", "n_responses", "course_label"],
            ascending=[False, False, True],
            kind="mergesort",
        )
        .reset_index(drop=True)
    )

    ranking_df = summary_df[["course_label", "score_mean", "n_responses"]].copy()
    ranking_df.insert(0, "rank", range(1, len(ranking_df) + 1))

    ranking_df.to_csv(OUTPUT_CSV, index=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(ranking_df["course_label"], ranking_df["score_mean"])
    ax.set_title("MAcc 2024 Course Ratings Rank Order")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Course")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
