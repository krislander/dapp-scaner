from pathlib import Path
from typing import Iterable, List

import pandas as pd


def write_md(path: Path, lines: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def df_to_markdown_table(df: pd.DataFrame, max_rows: int = 50) -> str:
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in view.iterrows():
        cells = [str(row[c]).replace("|", "\\|")[:300] for c in cols]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def bullet_list(items: List[str], prefix: str = "- ") -> List[str]:
    return [prefix + i for i in items]
