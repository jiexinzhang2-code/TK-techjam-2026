"""Iteration 01: keep the official FM scorer, change training to pairwise BPR."""

from experiment_core import make_parser, run_experiment


if __name__ == "__main__":
    parser = make_parser(
        "Iteration 01 - pairwise BPR FM with random negatives",
        "runs/iteration_01_pairwise_bpr",
    )
    args = parser.parse_args()
    run_experiment(
        args,
        training_mode="pairwise",
        encoder_mode="official",
        negative_strategy="random",
    )

