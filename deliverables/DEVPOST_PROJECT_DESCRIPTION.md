# Evidence-Aware Autonomous Research Agent for KuaiRand

## Project overview

Recommendation research is usually a slow manual loop: inspect a baseline, form a hypothesis, edit a configuration, train, evaluate, decide whether to keep the change, and repeat. Our project turns that loop into a controlled autonomous research agent for the KuaiRand-Pure within-user ranking benchmark.

The system uses an LLM only as a planner. It cannot run arbitrary shell commands, edit unrestricted files, inspect test metrics, or bypass experiment controls. Every proposal is normalized into a typed `ExperimentPlan`, checked against a registered tool and parameter allowlist, executed through a bounded runner, evaluated on the official validation split, and recorded in append-only ledgers. Accepted experiments become the new search anchor; rejected changes are rolled back exactly. API, JSON, or plan-validation failures automatically fall back to a deterministic evidence-driven planner.

## How the solution addresses the problem

The official pointwise Factorization Machine optimizes log loss even though the benchmark evaluates within-user ranking using GAUC and nDCG@5. Our agent first reproduced that baseline, then isolated a ranking-aligned BPR objective, added leakage-safe historical and time features, and optimized one hyperparameter at a time around the validation-best configuration.

The key improvement is an evidence-aware planner context. Instead of sending raw data or large artifacts to the LLM, the local runtime computes compact summaries of:

- dataset size, positive rate, cardinality, missingness, and cold-start rates;
- feature dimensions, coverage, sparsity, and unseen-value rates;
- best epoch, actual epochs, early-stop cause, and loss/Primary trends;
- prediction distributions, baseline correlation, exposure-group metrics, and ranking-error rates;
- bounded embedding/weight norms and feature-group importance proxies.

This prevented wasted searches such as increasing the epoch budget after training had already early-stopped. The enhanced planner found the useful `lr=0.0007`, `l2=1e-4`, and `batch_size=16384` combination within the 15-iteration run.

## Results

On KuaiRand-Pure validation, the selected model achieved:

| Model | GAUC | nDCG@5 | Primary |
|---|---:|---:|---:|
| Official FM baseline | 0.667400 | 0.535700 | 0.601600 |
| Evidence-aware agent best | **0.671803** | **0.538556** | **0.605179** |
| Absolute delta | **+0.004403** | **+0.002856** | **+0.003579** |

Against the exact seed-0 pointwise baseline rerun inside the same study (`0.601470` Primary), the gain was `+0.003710`. The final run used 15 of the 50 allowed iterations, 209,035 total LLM tokens, 563.895 seconds of end-to-end agent wall-clock, 0 GPU-hours, and 0 manual interventions.

## Development tools

- VS Code for repository inspection and editing
- Codex desktop for code review, implementation, terminal execution, and experiment auditing
- macOS Terminal / zsh for reproducible command-line runs
- Git and GitHub for versioning and public delivery

## APIs

- OpenAI Responses API
- `gpt-5.6-sol` as the planning model with structured JSON output

The LLM received only aggregate evidence and registered search constraints. Raw CSV rows, concrete user/video identifiers, local data paths, prediction files, checkpoints, and model tensors were not sent to the API.

## Libraries and frameworks

- Python 3.9+
- NumPy for feature encoding, Factorization Machine training, BPR optimization, checkpointing, and inference
- Python standard library for the agent state machine, JSON Schema-compatible contracts, HTTP requests, subprocess isolation, CSV handling, hashing, and append-only logging

The final implementation does not require PyTorch, TensorFlow, pandas, or scikit-learn.

## Dataset and assets

- KuaiRand-Pure public recommendation dataset
- Official Starter Kit split definitions, immutable evaluator, submission checker, and baseline configuration
- Training window: 2022-04-08 through 2022-04-21
- Validation window: 2022-04-22 through 2022-04-28
- Test window: 2022-04-29 through 2022-05-08
- Target: binary `long_view`
- Metrics: GAUC and nDCG@5; Primary is their mean

The repository does not redistribute the source dataset. The final model checkpoint and schema-valid prediction file are included in the deliverables.

## Autonomy and safety

The final run required no manual intervention. All 15 experiments completed on their first training attempt. In iteration 13, the LLM proposed an unsupported non-canonical variant combination. Local validation rejected it before execution and the deterministic planner selected a legal alternative. This event is preserved in the public per-iteration log.

## Limitations and future improvements

- The reported gains are validation results; hidden-test performance is not claimed.
- The study uses one seed during dynamic search. Multi-seed confirmation would better quantify variance.
- Planner evidence increased LLM token usage; future work should retain full diagnostics only for the baseline, current best, and latest run.
- The tool registry does not yet expose a combined history-plus-hard-negative variant, even though the planner identified it as a plausible direction.
- KuaiRand-1k and KuaiRand-27k bonus benchmarks were not attempted.
- Future work would add listwise objectives, multi-task watch-time signals, and automated multi-seed confirmation within the same safety boundary.

## Repository

<https://github.com/jiexinzhang2-code/TK-techjam-2026/tree/feature/bpr-fm>
