# Final KuaiRand-Pure Artifacts

Selected run: `gpt56-evidence-20260831-01-E010`.

| File | Purpose |
|---|---|
| `submission.csv` | Test predictions in the Starter Kit schema `row_id,user_id,video_id,score` |
| `best_model.npz` | NumPy FM checkpoint selected using validation only |
| `config.json` | Exact training and feature configuration |
| `validation_summary.json` | Validation metrics and aggregate diagnostics |
| `SHA256SUMS` | Integrity hashes for all final artifacts |

The test prediction file was produced without evaluating test labels. To verify alignment after downloading KuaiRand-Pure:

```bash
python3 submit.py \
  --data_dir /path/to/KuaiRand-Pure/data \
  --split test \
  --check deliverables/final/submission.csv
```

To regenerate it from the checkpoint:

```bash
python3 scripts/export_checkpoint_submission.py \
  --data-dir /path/to/KuaiRand-Pure/data \
  --starter-dir . \
  --checkpoint deliverables/final/best_model.npz \
  --config deliverables/final/config.json \
  --output /tmp/kuairand-final-submission.csv
```
