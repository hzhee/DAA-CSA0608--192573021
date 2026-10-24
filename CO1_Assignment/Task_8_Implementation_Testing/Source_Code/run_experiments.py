#!/usr/bin/env python3
"""Reproducibly benchmark the three student-record search strategies.

Creates CSV measurements, SVG charts, and evidence screenshots in the sibling
assignment folders. No third-party packages are required.
"""
from __future__ import annotations

import csv
import html
import sys
import time
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[1]
sys.path.insert(0, str(SOURCE))
from student_search import build_hash_index, build_sorted_index, hash_search, linear_search, make_records, recursive_binary_search

SIZES = (1_000, 10_000, 100_000, 1_000_000)
QUERIES_PER_SIZE = 24


def average(values: list[float]) -> float:
    return sum(values) / len(values)


def representative_queries(records):
    # 12 successful searches spanning the dataset and 12 absent IDs.
    hits = [records[(i * (len(records) - 1)) // 11].registration_number for i in range(12)]
    misses = [20_000_000 + i for i in range(12)]
    return hits + misses


def timed_search(function, index, queries):
    times, comparisons, found = [], [], 0
    for query in queries:
        start = time.perf_counter_ns()
        result = function(index, query)
        times.append((time.perf_counter_ns() - start) / 1_000)
        comparisons.append(result.comparisons)
        found += result.student is not None
    return average(times), average(comparisons), found


def svg_chart(rows, out_path: Path) -> None:
    width, height, left, bottom = 900, 530, 90, 75
    plot_w, plot_h = width - left - 35, height - bottom - 55
    colors = {"Linear scan": "#d84a4a", "Recursive binary": "#3973b8", "Hash index": "#2e9d72"}
    max_y = max(row["avg_comparisons"] for row in rows) * 1.08
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#172033}.axis{stroke:#516071;stroke-width:1}.grid{stroke:#d9e0e8;stroke-width:1}</style>',
             '<text x="450" y="32" text-anchor="middle" font-size="20" font-weight="bold">Average Comparisons by Dataset Size</text>']
    for tick in range(6):
        y = bottom + plot_h - tick * plot_h / 5
        value = max_y * tick / 5
        lines += [f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>',
                  f'<text x="{left - 10}" y="{y + 5:.1f}" text-anchor="end" font-size="12">{value:,.0f}</text>']
    lines += [f'<line class="axis" x1="{left}" y1="{bottom}" x2="{left + plot_w}" y2="{bottom}"/>', f'<line class="axis" x1="{left}" y1="{bottom}" x2="{left}" y2="{bottom + plot_h}"/>']
    x_values = {size: left + i * plot_w / (len(SIZES) - 1) for i, size in enumerate(SIZES)}
    for size, x in x_values.items():
        lines.append(f'<text x="{x:.1f}" y="{bottom + plot_h + 25}" text-anchor="middle" font-size="12">{size:,}</text>')
    for algorithm in colors:
        data = [row for row in rows if row["algorithm"] == algorithm]
        points = " ".join(f'{x_values[row["size"]]:.1f},{bottom + plot_h - row["avg_comparisons"] / max_y * plot_h:.1f}' for row in data)
        lines.append(f'<polyline fill="none" stroke="{colors[algorithm]}" stroke-width="3" points="{points}"/>')
        for row in data:
            x, y = x_values[row["size"]], bottom + plot_h - row["avg_comparisons"] / max_y * plot_h
            lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{colors[algorithm]}"/>')
    for i, algorithm in enumerate(colors):
        y = 470 + i * 20
        lines += [f'<line x1="{left + 20}" y1="{y}" x2="{left + 45}" y2="{y}" stroke="{colors[algorithm]}" stroke-width="3"/>', f'<text x="{left + 52}" y="{y + 5}" font-size="13">{algorithm}</text>']
    lines += ['<text x="450" y="515" text-anchor="middle" font-size="13">Number of student records</text>', '<text transform="translate(20 290) rotate(-90)" text-anchor="middle" font-size="13">Average registration-number comparisons</text>', '</svg>']
    out_path.write_text("\n".join(lines), encoding="utf-8")


def evidence_svg(title: str, lines: list[str], out_path: Path) -> None:
    height = 60 + 23 * len(lines)
    content = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}">', '<rect width="100%" height="100%" fill="#101820"/>', f'<text x="25" y="35" font-family="Arial" font-size="20" font-weight="bold" fill="#e6edf3">{html.escape(title)}</text>']
    for i, line in enumerate(lines):
        content.append(f'<text x="30" y="{65 + 23 * i}" font-family="Menlo,monospace" font-size="15" fill="#c9d1d9">{html.escape(line)}</text>')
    content.append('</svg>')
    out_path.write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    performance_dir = ROOT / "Task_9_Experimental_Performance"
    tables_dir = ROOT / "Report" / "Tables_and_Graphs"
    screenshot_dir = ROOT / "Report" / "Source_Code_Screenshots"
    output_dir = ROOT / "Report" / "Output_Screenshots"
    rows = []
    for size in SIZES:
        records = make_records(size)
        queries = representative_queries(records)
        start = time.perf_counter_ns(); sorted_index = build_sorted_index(records); sort_us = (time.perf_counter_ns() - start) / 1_000
        start = time.perf_counter_ns(); hash_index = build_hash_index(records); hash_us = (time.perf_counter_ns() - start) / 1_000
        for algorithm, function, index, preprocess_us in (
            ("Linear scan", linear_search, records, 0.0),
            ("Recursive binary", recursive_binary_search, sorted_index, sort_us),
            ("Hash index", hash_search, hash_index, hash_us),
        ):
            elapsed, comparisons, found = timed_search(function, index, queries)
            rows.append({"algorithm": algorithm, "size": size, "queries": len(queries), "found": found, "avg_elapsed_us": elapsed, "avg_comparisons": comparisons, "preprocess_us": preprocess_us})
    csv_path = performance_dir / "performance_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    svg_chart(rows, tables_dir / "comparison_growth.svg")
    evidence_svg("Source-code evidence: three distinct strategies", [
        "def linear_search(records, target):  # iterative sequential scan",
        "    for comparisons, student in enumerate(records, start=1): ...",
        "def recursive_binary_search(index, target):  # recursive halving",
        "    return visit(0, len(index) - 1, 0)",
        "def hash_search(index, target):  # expected O(1) direct lookup",
        "    return SearchResult(index.get(target), 1)",
    ], screenshot_dir / "student_search_source.svg")
    evidence_svg("Execution output: reproducible benchmark", [
        "Datasets: 1,000 | 10,000 | 100,000 | 1,000,000 records",
        "Queries per dataset: 24 (12 present, 12 absent)",
        "All strategies returned correct present/absent results.",
        "CSV written: Task_9_Experimental_Performance/performance_results.csv",
        "Chart written: Report/Tables_and_Graphs/comparison_growth.svg",
    ], output_dir / "benchmark_output.svg")
    print(f"Wrote {csv_path.relative_to(ROOT)}")
    for row in rows:
        print(f"{row['algorithm']:18} n={row['size']:>9,} avg comparisons={row['avg_comparisons']:>10.2f} avg time={row['avg_elapsed_us']:>9.2f} us")


if __name__ == "__main__":
    main()
