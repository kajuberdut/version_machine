from argparse import ArgumentError
from multiprocessing.sharedctypes import Value
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from version_machine.core import VersionMachine, cli, parse_args


def fake_config(*args, **kwargs):
    return {}


MockConfig = MagicMock(side_effect=fake_config)


class TestCLI(TestCase):
    def test_argparser(self):
        test_path = "C:/something"
        args = parse_args(["-fL", "--path", test_path, "--increment", "MAJOR"])
        self.assertEqual(args.force, True)
        self.assertEqual(args.lock, True)
        self.assertIsInstance(args.path, Path)
        self.assertEqual(args.path, Path(test_path))
        self.assertIsInstance(args.increment, VersionMachine.IncrementType)
        self.assertEqual(args.increment, VersionMachine.IncrementType.MAJOR)
        self.assertRaises(SystemExit, parse_args, ["-i", "WRONG"])

    @patch("version_machine.core.main")
    @patch("version_machine.core.Config", mock=MockConfig)
    def test_cli(self, mock_config, mock_main):
        cli()
        mock_main.assert_called_with(
            force=False,
            lock=False,
            config=mock_config(),
        )


if __name__ == "__main__":
    main()  # pragma: no cover
