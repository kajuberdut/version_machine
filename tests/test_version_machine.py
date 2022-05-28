from ensurepip import version
from unittest import TestCase, main
from unittest.mock import patch, mock_open
from version_machine.core import version_travel


class TestVersionMachine(TestCase):
    def setUp(self):
        self.mock_open = mock_open(read_data='__version__ = "0.0.1"')
        self.patch_file = patch("builtins.open", self.mock_open)
        self.patch_file.start()
        return super().setUp()

    def tearDown(self) -> None:
        self.patch_file.stop()
        return super().tearDown()

    def test_basic_major(self):
        version_travel(path="", increment_type="MAJOR")
        self.mock_open.return_value.write.assert_called_once_with('__version__ = "1.0.0"')

    def test_basic_minor(self):
        version_travel(path="", increment_type="MINOR")
        self.mock_open.return_value.write.assert_called_once_with('__version__ = "0.1.0"')
        
    def test_basic_patch(self):
        version_travel(path="", increment_type="PATCH")
        self.mock_open.return_value.write.assert_called_once_with('__version__ = "0.0.2"')

    def test_basic_override(self):
        version_travel(path="", increment_type="PATCH", override_version="9.9.9")
        self.mock_open.return_value.write.assert_called_once_with('__version__ = "9.9.9"')


if __name__ == "__main__":
    main()  # pragma: no cover
