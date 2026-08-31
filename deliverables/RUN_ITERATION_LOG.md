# Run & Iteration Log

- Run ID: `gpt56-evidence-20260831-01`
- Iterations: **15 / 50**
- Total LLM tokens (input + output): **209035**
- End-to-end agent wall-clock: **563.895 seconds**
- GPU-hours: **0.0**
- Manual interventions: **0**
- Guarded deterministic planner fallbacks: **1**

Each non-baseline experiment applied a run-scoped variant marker through the controlled patcher. Rejected markers were rolled back; accepted markers were retained. Parameter changes are recorded in full in the JSONL companion file.

| Iteration | Status | Hypothesis / intended change | Applied code diff | GAUC | nDCG@5 | Primary | Error / recovery |
|---:|---|---|---|---:|---:|---:|---|
| 0 | accepted | establish the official five-field pointwise FM baseline — The integrated implementation should reproduce the official validation baseline. | No code diff (baseline) | 0.667133 | 0.535806 | 0.601470 | None |
| 1 | accepted | replace pointwise logloss with within-user pairwise BPR — A ranking-aligned pairwise loss should improve valid primary over the accepted pointwise FM baseline. | create `experiments/configs/gpt56-evidence-20260831-01/E001-active-variant.json` | 0.669711 | 0.537082 | 0.603396 | None |
| 2 | accepted | add leakage-safe historical and time fields to pairwise BPR — Adding leakage-safe historical and time fields to the accepted pairwise BPR configuration should improve validation ranking under temporal drift. | create `experiments/configs/gpt56-evidence-20260831-01/E002-active-variant.json` | 0.669704 | 0.537571 | 0.603638 | None |
| 3 | accepted | decrease learning rate from 0.001 to 0.0007 — A modestly lower learning rate will reduce post-checkpoint validation degradation and improve the validation primary of the history-enhanced pairwise model. | create `experiments/configs/gpt56-evidence-20260831-01/E003-active-variant.json` | 0.670724 | 0.537445 | 0.604085 | None |
| 4 | rejected | decrease learning rate from 0.0007 to 0.0005 — A further modest learning-rate reduction from 0.0007 to 0.0005 may reduce post-checkpoint validation degradation and improve the validation primary of the history-enhanced pairwise model. | create `experiments/configs/gpt56-evidence-20260831-01/E004-active-variant.json` | 0.670194 | 0.537249 | 0.603721 | None |
| 5 | rejected | increase learning rate from 0.0007 to 0.0015 — A modest learning-rate increase from 0.0007 to 0.0015 may improve optimization enough to exceed the accepted validation primary without changing model capacity or features. | create `experiments/configs/gpt56-evidence-20260831-01/E005-active-variant.json` | 0.670102 | 0.537634 | 0.603868 | None |
| 6 | accepted | increase L2 regularization from 1e-6 to 1e-5 — Increasing L2 regularization from 1e-6 to 1e-5 may reduce post-checkpoint validation degradation and improve the validation primary of the accepted history-enhanced pairwise model. | create `experiments/configs/gpt56-evidence-20260831-01/E006-active-variant.json` | 0.670884 | 0.537625 | 0.604255 | None |
| 7 | accepted | increase L2 regularization from 1e-5 to 1e-4 — Increasing L2 regularization from 1e-5 to 1e-4 may further reduce post-checkpoint validation degradation and improve the validation primary of the accepted history-enhanced pairwise model. | create `experiments/configs/gpt56-evidence-20260831-01/E007-active-variant.json` | 0.670871 | 0.538381 | 0.604626 | None |
| 8 | rejected | increase L2 regularization from 1e-4 to 1e-3 — Increasing L2 regularization from 1e-4 to 1e-3 may further control overfitting and improve the validation primary of the accepted history-enhanced pairwise model. | create `experiments/configs/gpt56-evidence-20260831-01/E008-active-variant.json` | 0.667427 | 0.536428 | 0.601928 | None |
| 9 | rejected | increase negative samples per positive from 1 to 2 — Reducing L2 regularization from 1e-4 to 1e-5 was worse, while increasing it to 1e-3 caused underfitting; the untried weaker declared neighbor 1e-5 is already tested, so reducing L2 to 1e-5 is unavailable and testing 1e-5 would duplicate prior work. Instead, increasing negative samples per positive from 1 to 2 may improve within-user ranking discrimination while retaining the accepted regularization and optimization settings. | create `experiments/configs/gpt56-evidence-20260831-01/E009-active-variant.json` | 0.670628 | 0.537728 | 0.604178 | None |
| 10 | accepted | increase batch size from 8192 to 16384 — Increasing the training batch size from 8192 to 16384 may reduce gradient noise and improve validation ranking while preserving the accepted history-enhanced pairwise model, learning rate, and regularization. | create `experiments/configs/gpt56-evidence-20260831-01/E010-active-variant.json` | 0.671803 | 0.538556 | 0.605179 | None |
| 11 | rejected | increase batch size from 16384 to 32768 — Increasing batch size from 16384 to 32768 may further reduce gradient noise and improve validation ranking while preserving the accepted history-enhanced pairwise model and all other settings. | create `experiments/configs/gpt56-evidence-20260831-01/E011-active-variant.json` | 0.671035 | 0.538564 | 0.604800 | None |
| 12 | rejected | decrease batch size from 16384 to 4096 — Reducing batch size from the accepted 16384 setting to 4096 may add beneficial gradient noise and improve validation ranking, given that the larger 32768 neighbor underperformed. | create `experiments/configs/gpt56-evidence-20260831-01/E012-active-variant.json` | 0.669665 | 0.537506 | 0.603585 | None |
| 13 | rejected | tune lr from 0.0007 to 0.0003 around validation-best run_history_pairwise — Changing only lr from 0.0007 to 0.0003 may improve the accepted validation best. | create `experiments/configs/gpt56-evidence-20260831-01/E013-active-variant.json` | 0.671266 | 0.538203 | 0.604735 | Planner validation rejected proposal; deterministic fallback used |
| 14 | rejected | set max_pairs_per_epoch from 0 to 1200000 — Increasing the maximum number of sampled pairs per epoch from unlimited/default to 1200000 may improve ranking signal coverage and validation primary while retaining the accepted history-enhanced pairwise configuration. | create `experiments/configs/gpt56-evidence-20260831-01/E014-active-variant.json` | 0.671803 | 0.538556 | 0.605179 | None |

## Autonomy summary

The run required **0 manual interventions**. All 15 training experiments completed on their first execution attempt. At iteration 13, the LLM proposed a non-canonical model-variant combination; local plan validation blocked it before execution and the deterministic planner supplied a legal one-parameter neighbor. No unsafe command or invalid experiment was run.

The machine-readable record is [`run_iteration_log.jsonl`](run_iteration_log.jsonl).
