"""Iteration 02: warm up, then mix random and mined hard negatives."""

from experiment_core import make_parser, run_experiment


if __name__ == "__main__":
    parser = make_parser(
        "Iteration 02 - pairwise BPR FM with hard negatives",
        "runs/iteration_02_hard_negative_bpr",
    )
    args = parser.parse_args()
    run_experiment(
        args,
        training_mode="pairwise",
        encoder_mode="official",
        negative_strategy="hard",
    )
