"""Iteration 00: reproduce the official five-field pointwise FM.

This version adds evidence files and checkpointing but keeps the official
feature set and pointwise logloss.
"""

from experiment_core import make_parser, run_experiment


if __name__ == "__main__":
    parser = make_parser(
        "Iteration 00 - official pointwise FM with logs/checkpoint",
        "runs/iteration_00_official_pointwise",
    )
    args = parser.parse_args()
    run_experiment(args, training_mode="pointwise", encoder_mode="official")

