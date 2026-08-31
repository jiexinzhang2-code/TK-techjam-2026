import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from models.trial_lab_core import FM
from scripts.export_checkpoint_submission import export_submission
from scripts.export_run_log import markdown_report, public_records


class DeliverableScriptTests(unittest.TestCase):
    def test_checkpoint_export_writes_aligned_test_without_scoring(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = {
                "encoder_mode": "history", "k": 2, "lr": 0.001,
                "l2": 1e-6, "seed": 0,
            }
            (root / "config.json").write_text(json.dumps(config), encoding="utf-8")
            model = FM(6, k=2, seed=0)
            np.savez_compressed(root / "model.npz", **model.state())
            rows = [
                (20220429, "u1", "v1", "a1", "1", 10.0, 0),
                (20220429, "u2", "v2", "a2", "1", 20.0, 1),
            ]
            encoded = {
                "test": (
                    np.asarray([[0, 3], [1, 4]], dtype=np.int32),
                    np.asarray([0, 1], dtype=np.float32),
                    ["u1", "u2"],
                )
            }
            output = root / "submission.csv"
            with patch(
                "scripts.export_checkpoint_submission.load_official_modules",
                return_value=(object(), object()),
            ), patch(
                "scripts.export_checkpoint_submission.encode_history",
                return_value=({"test": rows}, encoded, 6, ["user", "item"]),
            ):
                result = export_submission(
                    "unused", "unused", str(root / "model.npz"),
                    str(root / "config.json"), str(output),
                )
            self.assertEqual(2, result["rows"])
            self.assertFalse(result["test_labels_used_for_scoring"])
            self.assertEqual(
                "row_id,user_id,video_id,score", output.read_text().splitlines()[0]
            )

    def test_public_run_log_uses_controlled_plan_diff_not_workspace_diff(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "experiments" / "configs" / "run" / "E000.json"
            config_path.parent.mkdir(parents=True)
            config_path.write_text(json.dumps({
                "changes": [{
                    "path": "experiments/configs/run/E000-active-variant.json",
                    "old_text": "", "new_text": '{"variant":"pairwise"}\n',
                }]
            }), encoding="utf-8")
            state = {
                "run_id": "run",
                "history": [{
                    "iteration": 0, "run_id": "run-E000", "status": "accepted",
                    "hypothesis": "ranking loss helps", "rationale": "controlled test",
                    "single_primary_change": "use BPR", "requested_tool": "run_pairwise",
                    "params": {"lr": 0.001}, "feature_flags": {"pairwise": True},
                    "config_path": "experiments/configs/run/E000.json",
                    "code_diff_summary": "untrusted noisy workspace diff",
                    "GAUC": 0.6, "nDCG@5": 0.5, "primary": 0.55,
                    "decision_rationale": "new best", "error_class": None,
                    "recovery_action": None, "attempt": 1, "planner_source": "llm",
                    "planner_error": None, "elapsed_seconds": 1.0,
                    "token_usage": 10, "gpu_hours": 0.0,
                    "human_intervention": False,
                    "human_intervention_reason": None,
                }],
            }
            records = public_records(root, state)
            self.assertEqual("create", records[0]["code_diff_applied"][0]["operation"])
            self.assertNotIn("workspace", json.dumps(records))
            report = markdown_report(state, records, 2.0)
            self.assertIn("Manual interventions: **0**", report)
            self.assertIn("10", report)


if __name__ == "__main__":
    unittest.main()
