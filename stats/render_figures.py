"""Render the showcase figures from stats/stats.json.

Usage (from the repo root):  python3 stats/render_figures.py

Stdlib only. Writes figures/funnel.svg and figures/levers.svg. Every number
comes from stats.json; nothing is computed from the eval questions themselves.
"""

import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
STATS_PATH = REPO_ROOT / "stats" / "stats.json"
FIGURES_DIR = REPO_ROOT / "figures"

FIGURE_WIDTH = 800
TOP_MARGIN = 92
LABEL_COLUMN_WIDTH = 270
BAR_AREA_WIDTH = 300
BAR_HEIGHT = 14
BAR_GAP = 4
ROW_GAP = 16
MINIMUM_BAR_WIDTH = 3
LEFT_MARGIN = 20

# Fonts with their fallback stacks; no font is fetched, so a viewer
# without Inter or JetBrains Mono simply gets the next font in the stack.
TEXT_FONT = "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
NUMBER_FONT = "'JetBrains Mono', ui-monospace, monospace"

THEME_STYLE = f"""
  .bg {{ fill: #ffffff; }}
  .series-0 {{ fill: #2f6f9f; }}
  .series-1 {{ fill: #2a8a86; }}
  .track {{ fill: #eef1f4; }}
  .label {{ fill: #1f2328; font: 14px {TEXT_FONT}; }}
  .label-strong {{ fill: #1f2328; font: 600 14px {TEXT_FONT}; }}
  .count {{ fill: #1f2328; font: 12px {NUMBER_FONT}; }}
  .title {{ fill: #1f2328; font: 600 16px {TEXT_FONT}; }}
  .legend {{ fill: #1f2328; font: 13px {TEXT_FONT}; }}
  .note {{ fill: #59636e; font: 12px {TEXT_FONT}; }}
  @media (prefers-color-scheme: dark) {{
    .bg {{ fill: #0d1117; }}
    .series-0 {{ fill: #4f9bd1; }}
    .series-1 {{ fill: #4fbdb8; }}
    .track {{ fill: #1c232c; }}
    .label, .label-strong, .count, .title, .legend {{ fill: #e6edf3; }}
    .note {{ fill: #9198a1; }}
  }}
"""


def proportional_bar_width(count, total):
    """Linear scale on the share of the set, so 20 of 24 and 10 of 12 read alike."""
    if total <= 0:
        raise ValueError(f"a set total must be positive, got {total}")
    if count < 0 or count > total:
        raise ValueError(f"count {count} is outside 0..{total}")
    if count == 0:
        return 0
    return max(MINIMUM_BAR_WIDTH, round(count / total * BAR_AREA_WIDTH))


def render_grouped_bars(title, series_labels, rows, notes, strong_row_index=None):
    """rows: list of (row label, [(count, total, value text) per series])."""
    if not rows:
        raise ValueError("no rows to draw")
    row_height = len(series_labels) * (BAR_HEIGHT + BAR_GAP) + ROW_GAP
    figure_height = TOP_MARGIN + row_height * len(rows) + 22 * len(notes) + 16
    bar_left = LEFT_MARGIN + LABEL_COLUMN_WIDTH

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{FIGURE_WIDTH}" '
        f'height="{figure_height}" viewBox="0 0 {FIGURE_WIDTH} {figure_height}" '
        f'role="img" aria-label="{escape(title)}">',
        f"<style>{THEME_STYLE}</style>",
        f'<rect class="bg" width="{FIGURE_WIDTH}" height="{figure_height}" rx="8"/>',
        f'<text class="title" x="{LEFT_MARGIN}" y="34">{escape(title)}</text>',
    ]
    legend_x = LEFT_MARGIN
    for series_index, series_label in enumerate(series_labels):
        parts.append(
            f'<rect class="series-{series_index}" x="{legend_x}" y="52" width="14" height="14" rx="3"/>'
        )
        parts.append(f'<text class="legend" x="{legend_x + 20}" y="64">{escape(series_label)}</text>')
        legend_x += 30 + 8 * len(series_label)

    for row_index, (row_label, values) in enumerate(rows):
        row_top = TOP_MARGIN + row_index * row_height
        label_class = "label-strong" if row_index == strong_row_index else "label"
        parts.append(
            f'<text class="{label_class}" x="{LEFT_MARGIN}" y="{row_top + BAR_HEIGHT + 6}">'
            f"{escape(row_label)}</text>"
        )
        for series_index, (count, total, value_text) in enumerate(values):
            bar_top = row_top + series_index * (BAR_HEIGHT + BAR_GAP)
            bar_width = proportional_bar_width(count, total)
            parts.append(
                f'<rect class="track" x="{bar_left}" y="{bar_top}" width="{BAR_AREA_WIDTH}" '
                f'height="{BAR_HEIGHT}" rx="3"/>'
            )
            if bar_width:
                parts.append(
                    f'<rect class="series-{series_index}" x="{bar_left}" y="{bar_top}" '
                    f'width="{bar_width}" height="{BAR_HEIGHT}" rx="3"/>'
                )
            parts.append(
                f'<text class="count" x="{bar_left + BAR_AREA_WIDTH + 10}" '
                f'y="{bar_top + BAR_HEIGHT - 2}">{escape(value_text)}</text>'
            )

    note_top = TOP_MARGIN + row_height * len(rows) + 8
    for note_index, note in enumerate(notes):
        parts.append(
            f'<text class="note" x="{LEFT_MARGIN}" y="{note_top + note_index * 22}">{escape(note)}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_funnel_svg(funnel):
    labels = funnel["step_labels"]
    sets = funnel["sets"]
    for one_set in sets:
        if len(one_set["counts"]) != len(labels):
            raise ValueError(f"set {one_set['label']!r} has {len(one_set['counts'])} counts for {len(labels)} steps")
        counts = one_set["counts"]
        if any(later > earlier for earlier, later in zip(counts, counts[1:])):
            raise ValueError(f"set {one_set['label']!r} is not a funnel: {counts}")
    rows = []
    for step_index, step_label in enumerate(labels):
        values = []
        for one_set in sets:
            total = one_set["counts"][0]
            count = one_set["counts"][step_index]
            values.append((count, total, f"{count} of {total}"))
        rows.append((step_label, values))
    series_labels = [f"{one_set['label']} ({one_set['counts'][0]} questions)" for one_set in sets]
    return render_grouped_bars(
        title="Where the answer is lost",
        series_labels=series_labels,
        rows=rows,
        notes=[
            "Candidates: the run with translation on, before the review fixes.",
            "Last step: the current iteration, after the review fixes, reranker off.",
        ],
        strong_row_index=len(labels) - 1,
    )


def render_levers_svg(levers):
    tuned_total = levers["tuned_questions"]
    heldout_total = levers["heldout_questions"]
    rows = []
    for step in levers["steps"]:
        rows.append((
            step["label"],
            [
                (step["tuned_right"], tuned_total,
                 f"{step['tuned_right']} of {tuned_total}, false {step['tuned_false']} of {levers['tuned_negatives']}"),
                (step["heldout_right"], heldout_total,
                 f"{step['heldout_right']} of {heldout_total}, false {step['heldout_false']} of {levers['heldout_negatives']}"),
            ],
        ))
    return render_grouped_bars(
        title="The right note inserted, step by step",
        series_labels=[f"Tuning set ({tuned_total} questions)", f"Check set ({heldout_total} questions)"],
        rows=rows,
        notes=[
            "False = something inserted into an ordinary prompt where nothing belonged.",
            "The reranker is switched off for its memory cost; its gain was on the tuning set only.",
            "The review fixes to the insert rule took the tuning set from 12 to 11 right and from 1 to 0 false.",
        ],
        strong_row_index=len(rows) - 1,
    )


def main():
    if not STATS_PATH.exists():
        sys.exit(f"FAILED: {STATS_PATH} not found; run from a checkout of the showcase repo")
    stats = json.loads(STATS_PATH.read_text(encoding="utf-8"))
    FIGURES_DIR.mkdir(exist_ok=True)
    outputs = {
        "funnel.svg": render_funnel_svg(stats["funnel"]),
        "levers.svg": render_levers_svg(stats["levers"]),
    }
    for name, svg in outputs.items():
        path = FIGURES_DIR / name
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
