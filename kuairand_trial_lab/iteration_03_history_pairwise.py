"""Iteration 03: pairwise BPR plus leakage-safe history and time features."""

from experiment_core import make_parser, run_experiment


if __name__ == "__main__":
    parser = make_parser(
        "Iteration 03 - pairwise BPR with time-safe history features",
        "runs/iteration_03_history_pairwise",
    )
    args = parser.parse_args()
    run_experiment(
        args,
        training_mode="pairwise",
        encoder_mode="history",
        negative_strategy="random",
    )

