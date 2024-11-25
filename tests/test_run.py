import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import run

class TestRun(unittest.TestCase):
    def setUp(self):
        # Create mock features
        self.mock_feature_1 = MagicMock()
        self.mock_feature_1.name.return_value = "Feature 1"
        self.mock_feature_1.description.return_value = "Description of Feature 1"
        self.mock_feature_1.get_arguments_info.return_value = [
            MagicMock(flags="--arg1", help="Argument 1 help text")
        ]
        self.mock_feature_1.add_arguments = lambda parser: parser.add_argument('--arg1', help="Argument 1 help text")

        self.mock_feature_2 = MagicMock()
        self.mock_feature_2.name.return_value = "Feature 2"
        self.mock_feature_2.description.return_value = "Description of Feature 2"
        self.mock_feature_2.get_arguments_info.return_value = [
            MagicMock(flags="--arg2", help="Argument 2 help text")
        ]
        self.mock_feature_2.add_arguments = lambda parser: parser.add_argument('--arg2', help="Argument 2 help text")

        # Patch the analyses.FEATURES dictionary
        self.patcher = patch("run.analyses", autospec=True)
        self.mock_analyses = self.patcher.start()
        self.mock_analyses.FEATURES = {1: self.mock_feature_1, 2: self.mock_feature_2}

        # Patch the config module
        self.config_patcher = patch("run.config", autospec=True)
        self.mock_config = self.config_patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.config_patcher.stop()

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_features(self, mock_stdout):
        with patch("sys.argv", ["run.py", "--list-features"]):
            with self.assertRaises(SystemExit):
                run.main()
        output = mock_stdout.getvalue()
        self.assertIn("Available Features:", output)
        self.assertIn("1: Feature 1: Description of Feature 1", output)
        self.assertIn("2: Feature 2: Description of Feature 2", output)

    @patch("sys.stderr", new_callable=StringIO)
    def test_missing_feature_or_list_flag(self, mock_stderr):
        with patch("sys.argv", ["run.py"]):
            with self.assertRaises(SystemExit):
                run.main()
        output = mock_stderr.getvalue()
        self.assertIn("error: one of the arguments --feature/-f --list-features/-l is required", output)

    @patch("sys.stderr", new_callable=StringIO)
    def test_unknown_argument(self, mock_stderr):
        with patch("sys.argv", ["run.py", "--feature", "1", "--unknown-arg", "value"]):
            with self.assertRaises(SystemExit):
                run.main()
        output = mock_stderr.getvalue()
        self.assertIn("error: unrecognized arguments: --unknown-arg value", output)

    def test_feature_specific_argument(self):
        with patch("sys.argv", ["run.py", "--feature", "1", "--arg1", "value"]):
            run.main()
        self.mock_feature_1.run.assert_called_once()
        self.mock_config.overwrite_from_args.assert_called_once()

    # @patch("sys.stderr", new_callable=StringIO)
    # def test_invalid_feature_id(self, mock_stderr):
    #     with patch("sys.argv", ["run.py", "--feature", "999"]):
    #         with self.assertRaises(SystemExit):
    #             run.main()
    #     output = mock_stderr.getvalue()
    #     self.assertIn("Error: Feature with ID 999 is not recognized.", output)

    def test_run_feature_1(self):
        with patch("sys.argv", ["run.py", "--feature", "1", "--arg1", "value"]):
            run.main()
        self.mock_feature_1.run.assert_called_once()
        self.mock_config.overwrite_from_args.assert_called_once()

    def test_run_feature_2(self):
        with patch("sys.argv", ["run.py", "--feature", "2", "--arg2", "value"]):
            run.main()
        self.mock_feature_2.run.assert_called_once()
        self.mock_config.overwrite_from_args.assert_called_once()

if __name__ == "__main__":
    unittest.main()