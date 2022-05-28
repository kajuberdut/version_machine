from unittest import TestCase, main
from unittest.mock import patch

from version_machine.core import check_dirty, current_tag, git_info, DirtyFiles


class TestGitFeatures(TestCase):
    @patch(
        "version_machine.core.subprocess.check_output",
        return_value="hi".encode("ascii"),
    )
    def test_git_info(self, mock_subprocess):
        self.assertEqual(git_info("something"), "hi")
        mock_subprocess.assert_called_once()

    @patch(
        "version_machine.core.subprocess.check_output",
        return_value="".encode("ascii"),
    )
    def test_check_not_dirty(self, mock_subprocess):
        check_dirty(warn=False)
        mock_subprocess.assert_called_once()

    @patch(
        "version_machine.core.subprocess.check_output",
        return_value="uh oh".encode("ascii"),
    )
    def test_check_is_dirty_error(self, mock_subprocess):
        self.assertRaises(DirtyFiles, check_dirty, warn=False)
        mock_subprocess.assert_called_once()

    @patch(
        "version_machine.core.subprocess.check_output",
        return_value="uh oh".encode("ascii"),
    )
    def test_check_is_dirty_warn(self, mock_subprocess):
        self.assertWarns(DirtyFiles, check_dirty, warn=True)
        mock_subprocess.assert_called_once()

    @patch(
        "version_machine.core.subprocess.check_output",
        return_value="some_tag".encode("ascii"),
    )
    def test_current_tag(self, mock_subprocess):
        self.assertEqual(current_tag(git_command="bob"), "some_tag")
        mock_subprocess.assert_called_once_with(["bob", "rev-parse", "--short", "HEAD"])


if __name__ == "__main__":
    main()  # pragma: no cover
