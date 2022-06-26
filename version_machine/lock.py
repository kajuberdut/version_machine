import json
from collections import UserDict
from pathlib import Path

from version_machine.git import current_tag


class LockedTag(UserWarning):
    ...


class Lock(UserDict):
    def __init__(self, path: Path | None = None):
        self.path = path if path is not None else Path(".version_machine.lock")
        self.current_tag = current_tag()
        if self.path.is_file():
            with open(self.path, "r") as lf:
                self.data = json.load(lf)["versions"]
        else:
            self.data = {}  # pragma: no cover

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
        self.current_tag = None
        self.data = {}

    def lock(self):
        pass
