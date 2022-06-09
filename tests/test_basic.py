import typing as t
from collections import UserDict
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import ANY, MagicMock, mock_open, patch

from version_machine.core import Config, Lock, LockedTag, MissingSettingsFile
from version_machine.core import main as version_machine_main
from version_machine.core import version_travel


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


class TestVersionMachineNoData(MockOpen, TestCase):
    return_data: t.ClassVar[str] = ""

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


class TestConfig(MockOpen, TestCase):
    return_data: t.ClassVar[
        str
    ] = """[tool.version_machine]

    [tool.version_machine.one]
    path = "things/stuff.py"
    increment = "patch"
    
    [tool.version_machine.two]
    path = "things/other.py"
    increment = "Major"
""".encode(
        "utf-8"
    )

    @patch("version_machine.core.Path")
    def test_config(self, mock_path_constructor):
        mock_path = MagicMock()
        mock_path_constructor.return_value = mock_path

        mock_path.is_file.return_value = True

        config = Config()
        self.assertEqual(len(config.targets), 2)
        self.assertEqual(config.targets[1]["increment"], "Major")

        mock_path.is_file.return_value = False
        self.assertRaises(MissingSettingsFile, Config)

        new_conf = Config(config={"thing": "stuff"})
        self.assertEqual(new_conf["thing"], "stuff")
        self.assertEqual(len(new_conf.targets), 0)
        new_conf["path"] = "none"
        self.assertEqual(len(new_conf.targets), 1)


class FakeLock(UserDict):
    def __init__(self, lock_path):
        self.data = {"tag": 1}
        self.current_tag = "tag"


class TestMain(MockOpen, TestCase):

    return_data: t.ClassVar[str] = '__version__ = "0.0.1"'

    @patch(
        "version_machine.core.check_dirty",
    )
    def test_main_no_lock(self, mock_check_dirty):
        version_machine_main(lock=False, config={"path": "thing", "increment": "patch"})

    @patch(
        "version_machine.core.check_dirty",
    )
    @patch("version_machine.core.Lock")
    def test_main_with_lock(self, mock_lock, mock_check_dirty):
        mock_lock.return_value = FakeLock("no_path")
        self.assertWarns(
            LockedTag,
            version_machine_main,
            lock=True,
            config={"path": "thing", "increment": "patch"},
        )


if __name__ == "__main__":
    main()  # pragma: no cover
