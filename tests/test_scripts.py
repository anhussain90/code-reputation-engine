import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestFindLatestAnalysisRun(unittest.TestCase):
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token", "REPO": "owner/repo", "GITHUB_OUTPUT": "/tmp/output"})
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_find_latest_run(self, mock_file, mock_get):
        mock_get.side_effect = [
            MagicMock(json=lambda: {"workflows": [{"name": "Static Analysis", "id": 123}]}),
            MagicMock(json=lambda: {"workflow_runs": [{"id": 456}]})
        ]
        
        import find_latest_analysis_run
        
        self.assertEqual(mock_get.call_count, 2)
        mock_file().write.assert_called_once_with("run_id=456\n")


class TestCollectAnnotations(unittest.TestCase):
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token", "REPO": "owner/repo", "RUN_ID": "789"})
    @patch("requests.get")
    @patch("os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_collect_annotations(self, mock_file, mock_makedirs, mock_get):
        mock_get.side_effect = [
            MagicMock(json=lambda: {"head_sha": "abc123"}),
            MagicMock(json=lambda: {"check_suites": [{"id": 1}]}),
            MagicMock(json=lambda: {"check_runs": [{"id": 2, "name": "test"}]}),
            MagicMock(json=lambda: [{"annotation_level": "warning", "path": "test.py", "start_line": 1, "end_line": 1, "message": "issue"}]),
            MagicMock(json=lambda: [])
        ]
        
        import collect_annotations
        
        self.assertEqual(mock_get.call_count, 5)
        mock_makedirs.assert_called_once_with("reports", exist_ok=True)


if __name__ == "__main__":
    unittest.main()
