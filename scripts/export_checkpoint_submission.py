"""Export a Starter Kit-aligned test submission from a saved trial checkpoint.

This script never evaluates test labels. It only restores the selected model,
encodes the frozen test split, writes scores, and applies the alignment checks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.trial_lab_core import (
    FM,
    encode_history,
    encode_official,
    load_official_modules,
    validate_predictions,
    write_predictions,
)


def export_submission(data_dir: str, starter_dir: str, checkpoint_path: str,
                      config_path: str, output_path: str) -> dict:
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    encoder_mode = config.get("encoder_mode")
    official_data, _ = load_official_modules(starter_dir)
    if encoder_mode == "history":
        splits, encoded, dim, feature_names = encode_history(data_dir)
    elif encoder_mode == "official":
        splits, encoded, dim, feature_names = encode_official(data_dir, official_data)
    else:
        raise ValueError("unsupported encoder_mode in config: %r" % encoder_mode)

    model = FM(
        dim,
        k=int(config["k"]),
        lr=float(config["lr"]),
        l2=float(config["l2"]),
        seed=int(config["seed"]),
    )
    with np.load(checkpoint_path) as saved:
        required = {"V", "W", "b"}
        if not required.issubset(saved.files):
            raise ValueError("checkpoint is missing required model arrays")
        state = {name: saved[name] for name in saved.files}
    if state["V"].shape != (dim, int(config["k"])) or state["W"].shape != (dim,):
        raise ValueError("checkpoint shape does not match encoded feature dimensions")
    model.restore(state)

    X_test = encoded["test"][0]
    scores = model.predict(X_test)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_predictions(output, splits["test"], scores)
    # csv.writer uses CRLF by default. Normalize the public artifact so Git's
    # whitespace checks and cross-platform checksum reproduction stay clean.
    output.write_bytes(output.read_bytes().replace(b"\r\n", b"\n"))
    validate_predictions(output, splits["test"])
    return {
        "rows": len(scores),
        "schema": ["row_id", "user_id", "video_id", "score"],
        "encoder_mode": encoder_mode,
        "features": feature_names,
        "test_labels_used_for_scoring": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export a test submission without scoring test labels"
    )
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--starter-dir", default=".")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = export_submission(
        args.data_dir, args.starter_dir, args.checkpoint, args.config, args.output,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
