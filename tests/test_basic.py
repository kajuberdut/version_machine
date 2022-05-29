import typing as t
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import ANY, mock_open, patch

from version_machine.core import Lock, version_travel


class MockOpen:
    return_data: t.ClassVar[str] = "No return_data"
    
    def setUp(self):
        self.mock_open = mock_open(read_data=self.return_data)
        self.patch_file = patch("builtins.open", self.mock_open)
        self.patch_file.start()
        return super().setUp()

    def tearDown(self) -> None:
        self.patch_file.stop()
        return super().tearDown()


class TestVersionMachine(MockOpen, TestCase):
    return_data: t.ClassVar[str] = '__version__ = "0.0.1"'

    def test_basic_major(self):
        version_travel(path="", increment="MAJOR")
        self.mock_open.return_value.write.assert_called_once_with(
            '__version__ = "1.0.0"'
        )

    def test_basic_minor(self):
        version_travel(path="", increment="MINOR")
        self.mock_open.return_value.write.assert_called_once_with(
            '__version__ = "0.1.0"'
        )

    def test_basic_patch(self):
        version_travel(path="", increment="PATCH")
        self.mock_open.return_value.write.assert_called_once_with(
            '__version__ = "0.0.2"'
        )

    def test_basic_override(self):
        version_travel(path="", increment="PATCH", override_version="9.9.9")
        self.mock_open.return_value.write.assert_called_once_with(
            '__version__ = "9.9.9"'
        )


class TestLocked(MockOpen, TestCase):
    
    return_data: t.ClassVar[str] = '{"versions": {"fake_tag": "1.0.0"}}'
    

    @patch("version_machine.core.json.dump")
    @patch(
        "version_machine.core.current_tag",
        return_value="another_tag",
    )
    def test_lock(self, mock_current_tag, mock_json_dump):
        path = Path("/thingy")
        with patch.object(Path, "is_file") as mock_exists:
            path.is_file.return_value = True

            l = Lock(path=path)
            self.assertEqual(l["fake_tag"], "1.0.0")
            self.assertEqual(l["1.0.0"], "fake_tag")

            l.set_version("2.0.0")

            l.lock()
            mock_json_dump.assert_called_with(
                {"versions": {"fake_tag": "1.0.0", "another_tag": "2.0.0"}}, ANY
            )



if __name__ == "__main__":
    main()  # pragma: no cover
