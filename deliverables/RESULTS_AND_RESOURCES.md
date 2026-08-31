# Final Submission & Results Summary

## Selected result

- Benchmark: **KuaiRand-Pure**
- Run: `gpt56-evidence-20260831-01`
- Selected iteration: **E010**
- Model: history/time Factorization Machine trained with within-user pairwise BPR
- Seed: `0`
- Selected parameters: `k=16`, `lr=0.0007`, `l2=0.0001`, `batch_size=16384`, `epochs=40`, `patience=4`, `negative_per_positive=1`, `max_pairs_per_epoch=0`

## Validation results

| Benchmark | Model | GAUC | nDCG@5 | Primary | Primary delta vs official baseline |
|---|---|---:|---:|---:|---:|
| KuaiRand-Pure | Official FM baseline | 0.667400 | 0.535700 | 0.601600 | — |
| KuaiRand-Pure | Final selected model | **0.671803** | **0.538556** | **0.605179** | **+0.003579** |
| KuaiRand-1k | Not attempted | — | — | — | — |
| KuaiRand-27k | Not attempted | — | — | — | — |

Metric-level absolute deltas over the official validation baseline are `+0.004403` GAUC and `+0.002856` nDCG@5. Against the exact seed-0 pointwise FM rerun in iteration E000 (`GAUC=0.667133`, `nDCG@5=0.535806`, `Primary=0.601470`), the selected model improved Primary by `+0.003710`.

These are validation-only model-selection results. Test labels were not evaluated by the agent or by the final export script.

## Resource usage to convergence

| Resource | Reported usage |
|---|---:|
| LLM model | `gpt-5.6-sol` |
| Total LLM tokens (input + output) | **209,035** |
| End-to-end agent wall-clock | **563.895 seconds (9m 23.895s)** |
| Iterations | **15 / 50** |
| GPU-hours | **0.0** |
| Manual interventions | **0** |
| Training attempts requiring retry | **0** |
| Guarded deterministic planner fallbacks | **1** |

The internal training/evaluation timer recorded 484.648 seconds. The required agent wall-clock is larger because it also includes the 15 LLM planning calls, validation, persistence, and orchestration overhead. It was measured from creation to final write of the append-only phase-event ledger.

After iteration 14, the convergence counter was 12 with `convergence_patience=12`. The CLI recorded `max_iterations` because the 15-iteration guard is evaluated before the convergence guard; no additional experiment would have run under the larger 50-iteration ceiling.

## Final files

- [`final/submission.csv`](final/submission.csv): Starter Kit schema `row_id,user_id,video_id,score`, test split, no test scoring.
- [`final/best_model.npz`](final/best_model.npz): selected NumPy FM checkpoint.
- [`final/config.json`](final/config.json): exact selected configuration.
- [`final/validation_summary.json`](final/validation_summary.json): validation metrics and bounded diagnostic evidence.
- [`final/SHA256SUMS`](final/SHA256SUMS): integrity hashes.

Use [`../scripts/export_checkpoint_submission.py`](../scripts/export_checkpoint_submission.py) to regenerate the test submission from the checkpoint.
