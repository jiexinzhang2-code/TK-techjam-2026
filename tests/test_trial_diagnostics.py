import unittest

import numpy as np

from evaluate import evaluate
from models.trial_lab_core import (
    FM,
    build_data_profile,
    build_feature_profile,
    build_model_diagnostics,
    build_prediction_diagnostics,
    build_training_diagnostics,
)


class TrialDiagnosticsTests(unittest.TestCase):
    def test_profiles_are_aggregate_and_exclude_test(self):
        train = [
            (20220408, "u1", "v1", "a1", "1", 100.0, 1),
            (20220409, "u2", "v2", "a2", "1", 200.0, 0),
        ]
        valid = [
            (20220422, "u1", "v3", "UNK", "2", 150.0, 1),
            (20220423, "u3", "v2", "a2", "2", 250.0, 0),
        ]
        profile = build_data_profile({"train": train, "valid": valid})
        self.assertEqual(2, profile["splits"]["train"]["rows"])
        self.assertEqual(0.5, profile["splits"]["valid"]["positive_rate"])
        self.assertEqual(0.5, profile["valid_cold_start_rate"]["users"])
        self.assertNotIn("test", profile["splits"])
        self.assertNotIn("u1", str(profile))

    def test_feature_training_prediction_and_model_summaries(self):
        X_train = np.asarray([[0, 3], [1, 4], [0, 3]], dtype=np.int32)
        X_valid = np.asarray([[0, 5], [2, 4]], dtype=np.int32)
        feature = build_feature_profile(X_train, X_valid, ["user", "item"], 6)
        self.assertEqual(3, feature["fields"][0]["dimension_including_unk"])
        self.assertEqual(0.5, feature["fields"][0]["valid_unseen_rate"])
        self.assertEqual(0.5, feature["fields"][1]["valid_unseen_rate"])

        epochs = [
            {"epoch": 1, "loss": 0.7, "valid": {"primary": 0.50}},
            {"epoch": 2, "loss": 0.6, "valid": {"primary": 0.55}},
            {"epoch": 3, "loss": 0.58, "valid": {"primary": 0.53}},
        ]
        training = build_training_diagnostics(epochs, 10, 1, 2)
        self.assertTrue(training["stopped_early"])
        self.assertEqual(3, training["actual_epochs"])
        self.assertEqual(-0.02, training["primary_trend"]["after_best_delta"])

        users = ["a", "a", "b", "b", "c", "c"]
        labels = np.asarray([1, 0, 1, 0, 0, 0], dtype=np.float32)
        scores = np.asarray([2.0, 1.0, 0.0, 1.0, -1.0, -2.0], dtype=np.float32)
        prediction = build_prediction_diagnostics(users, labels, scores, evaluate)
        self.assertIn("score_distribution", prediction)
        self.assertEqual(0.5, prediction["ranking_errors"]["mixed_user_top1_miss_rate"])

        model = FM(6, k=2, seed=0)
        diagnostics = build_model_diagnostics(model, X_train, ["user", "item"], 6)
        self.assertEqual(2, diagnostics["embedding_dimension"])
        self.assertEqual(2, len(diagnostics["feature_group_importance_proxy"]))


if __name__ == "__main__":
    unittest.main()
