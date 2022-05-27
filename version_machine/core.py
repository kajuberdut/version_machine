import argparse
import enum
import json
import re
import subprocess
import sys
import typing as t
import warnings
from collections import UserDict
from pathlib import Path
from functools import partial


def git_info(*args, git_command="git"):
    p = [git_command] + list(args)
    return subprocess.check_output(p).decode("ascii").strip()


def check_dirty(warn: bool) -> None:
    status = git_info("diff", "HEAD")
    if status:
        if warn:
            warnings.warn("Git status is not clean.", DirtyFiles)
        else:
            raise DirtyFiles(
                "Dirty files in project. Use --force if you wish to ignore."
            )


current_tag = partial(git_info, "rev-parse", "--short", "HEAD")


class MissingSettingsFile(IOError):
    ...


class DirtyFiles(UserWarning):
    ...


class LockedTag(UserWarning):
    ...


class Config(UserDict):
    def __init__(self, config: dict | None = None):
        if config is None:
            self.data = self.get_pyproject()
        else:
            self.data = config

    def get_pyproject(self):
        try:
            import tomllib as toml  # type: ignore
        except ImportError:
            import tomli as toml  # type: ignore

        if not (pyproject_path := Path("pyproject.toml")).is_file():
            raise MissingSettingsFile("pyproject.toml not found.")
        with open(pyproject_path, "rb") as pyproject_toml:
            return toml.load(pyproject_toml).get("tool", {}).get("version_machine", {})

    @property
    def config(self):
        return self.data

    @property
    def targets(self):
        if "path" in self.data:
            return [self.data]
        else:
            return [v for v in self.data.values() if "path" in v]


class VersionMachine:
    extraction_pattern: t.ClassVar[t.Pattern] = re.compile(
        r"""__version__ = ['"](?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)['"]"""
    )

    def __init__(
        self,
        text: str,
        increment_type: str | enum.EnumMeta = None,
        config: dict = None,
        force_version: str = None,
    ):
        self.text = text
        self.increment_type = increment_type
        self.match = self.extraction_pattern.search(text) or ""
        self.force_version = force_version

    @property
    def match_text(self):
        if self.match:
            return self.match.group(0)
        else:
            return ""

    @property
    def current_version_info(self) -> dict:
        return (
            self.match.groupdict()
            if self.match
            else {n.name.lower(): 0 for n in self.IncrementType}
        )

    @property
    def future_version(self) -> str:
        if self.force_version is not None:
            return self.force_version

        future = {}
        for k, v in self.current_version_info.items():
            v = int(v)
            if (o := self.type_ordinal(k)) == (
                t := self.type_ordinal(self.increment_type)
            ):
                future[k] = v + 1
            elif o > t:
                future[k] = 0
            else:
                future[k] = v

        return "{major}.{minor}.{patch}".format(**future)

    @property
    def repl(self) -> str:
        return f'__version__ = "{self.future_version}"'

    @property
    def future_text(self) -> str:
        return self.text.replace(self.match_text, self.repl)

    def type_ordinal(self, type: str | enum.EnumMeta) -> int:
        if isinstance(type, str):
            type = self.IncrementType[type.upper()]
        return type.value

    class IncrementType(enum.Enum):
        MAJOR = 0
        MINOR = 1
        PATCH = 2


class Lock(UserDict):
    def __init__(self, path: Path | None = None, dict=None, /, **kwargs):
        super().__init__(dict=dict, **kwargs)
        self.path = path if path is not None else Path(".version_machine.lock")
        self.current_tag = current_tag()
        if self.path.is_file():
            with open(self.path, "r") as lf:
                self.data = json.load(lf)["versions"]

    def set_version(self, version: str) -> None:
        self.data[self.current_tag] = version

    def __getitem__(self, key: str) -> str:
        if key in self.data:
            return self.data[key]
        else:
            return {v: k for k, v in self.data.items()}[key]

    def lock(self):
        lock_dict = {"versions": self.data}
        lock_dict["versions"].pop("dict", None)
        with open(self.path, "w+") as lf:
            json.dump(lock_dict, lf)


class NoLock(Lock):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.current_tag = None

    def lock(self):
        pass


def version_travel(
    path: Path,
    increment_type: str | enum.EnumMeta,
    version_machine: t.Type[VersionMachine] = VersionMachine,
    override_version: str = None,
):
    with open(path, "r+") as file_handle:
        text = file_handle.read()
        vm = version_machine(
            text=text, increment_type=increment_type, force_version=override_version
        )
        file_handle.seek(0)
        file_handle.write(vm.future_text)
        file_handle.truncate()
    return vm.future_version


def main(
    config: Config | dict | None = None,
    lock: bool = False,
    force: bool = False,
):
    check_dirty(warn=force)
    if lock:
        l = Lock()
    else:
        l = NoLock()
    if l.current_tag in l.data:
        warnings.warn(
            f"HEAD ({l.current_tag}) is locked to version {l[l.current_tag]}."
            "\nNo actions taken.",
            LockedTag,
        )
        return
    if not isinstance(config, Config):
        config = Config(config=config)
    version = None
    for target in config.targets:
        version = version_travel(**target)
    if lock:
        l.set_version(version)
        l.lock()


def parse_args(args):
    parser = argparse.ArgumentParser(description="Move version numbers.")
    parser.add_argument(
        "--path",
        action="store",
        required=False,
        default=None,
        type=Path,
        help="path of file to change version in.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Ignore warnings and force version move.",
    )
    parser.add_argument(
        "-L",
        "--lock",
        action="store_true",
        help="Lock the current git head commit tag to a specific version.",
    )

    return parser.parse_args(args)


def cli():
    args = parse_args(sys.argv[1:])
    if args.path:
        config = Config({"path": args.path})
    main(force=args.force, lock=args.lock)


if __name__ == "__main__":
    cli()
