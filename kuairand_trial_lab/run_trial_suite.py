"""Run all four experiments and create a validation leaderboard.

Use --smoke first.  Full runs can take several minutes in total.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "iteration_00_official_pointwise.py",
    "iteration_01_pairwise_bpr.py",
    "iteration_02_hard_negative_bpr.py",
    "iteration_03_history_pairwise.py",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir", default="/Users/xixi/Downloads/KuaiRand-Pure/data"
    )
    parser.add_argument(
        "--starter-dir", default="/Users/xixi/Downloads/kuairand-starter-kit"
    )
    parser.add_argument("--runs-dir", default="runs/suite")
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--score-test", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    runs_dir = Path(args.runs_dir).expanduser().resolve()
    runs_dir.mkdir(parents=True, exist_ok=True)
    leaderboard = []
    for script_name in SCRIPTS:
        name = Path(script_name).stem
        output_dir = runs_dir / name
        command = [
            sys.executable,
            str(root / script_name),
            "--data-dir",
            args.data_dir,
            "--starter-dir",
            args.starter_dir,
            "--output-dir",
            str(output_dir),
            "--epochs",
            str(2 if args.smoke else args.epochs),
            "--seed",
            str(args.seed),
        ]
        if args.smoke:
            command += [
                "--max-train-rows",
                "50000",
                "--max-eval-rows",
                "20000",
                "--max-pairs-per-epoch",
                "20000",
            ]
        if args.score_test:
            command.append("--score-test")
        print("\nRUN:", " ".join(command), flush=True)
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            leaderboard.append(
                {"experiment": name, "status": "failed", "returncode": completed.returncode}
            )
            continue
        with (output_dir / "summary.json").open(encoding="utf-8") as fh:
            summary = json.load(fh)
        leaderboard.append(
            {
                "experiment": name,
                "status": summary["status"],
                **summary["valid"],
                "runtime_seconds": summary["runtime_seconds"],
            }
        )

    leaderboard.sort(
        key=lambda row: row.get("primary", float("-inf")), reverse=True
    )
    with (runs_dir / "leaderboard.json").open("w", encoding="utf-8") as fh:
        json.dump(leaderboard, fh, ensure_ascii=False, indent=2)
    print("\nVALIDATION LEADERBOARD")
    for row in leaderboard:
        if "primary" in row:
            print(
                f"{row['experiment']:38s} primary={row['primary']:.4f} "
                f"GAUC={row['GAUC']:.4f} nDCG@5={row['nDCG@5']:.4f}"
            )
        else:
            print(f"{row['experiment']:38s} FAILED")
    print(f"\nSaved: {runs_dir / 'leaderboard.json'}")


if __name__ == "__main__":
    main()
