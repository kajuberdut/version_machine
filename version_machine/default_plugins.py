import re
import typing as t
from collections import UserDict
from enum import Enum, EnumMeta
from pathlib import Path

from version_machine.base_classes import Target
from version_machine.plugin_base import (
    RunablePlugin,
    RunSequencePlugin,
    StatePlugin,
    TargetLoadPlugin,
    TargetSavePlugin,
    VersionTravelPlugin,
)


class MissingSettingsFile(IOError):
    ...


class DefaultRunSequence(RunSequencePlugin):
    sequence: t.ClassVar[list] = ["target_load", "version_travel", "target_save"]

    def run(self):
        [
            self.manager.plugins[plugin].run()
            for plugin in self.sequence
            if isinstance(plugin, RunablePlugin)
        ]


class PyProjectConfig(UserDict):
    def __init__(self, config: dict | None = None):
        if config is None:
            self.data = self.get_pyproject()
        else:
            self.data = config

    def get_pyproject(self):
        try:
            import tomli as toml  # type: ignore
        except ImportError:
            import tomllib as toml  # type: ignore

        if not (pyproject_path := Path("pyproject.toml")).is_file():
            raise MissingSettingsFile("pyproject.toml not found.")
        with open(pyproject_path, "rb") as pyproject_toml:
            return toml.load(pyproject_toml).get("tool", {}).get("version_machine", {})

    def validate_target(self, data):
        "For the default FilePathTarget, anything with a path can be considered a target."
        return True if "path" in data else False

    @property
    def targets(self) -> t.Generator:
        if self.validate_target(self.data):
            return {"main": self.data}
        else:
            return {k: v for k, v in self.data.items() if self.validate_target(v)}


class DictState(UserDict, StatePlugin):
    """Default state plugin."""

    @property
    def targets(self):
        return (v for v in self.data.values() if isinstance(v, Target))

    @targets.setter
    def targets(self, value):
        if isinstance(value, dict):
            self.data.update({k: v for k, v in value.items() if isinstance(v, Target)})
        elif isinstance(value, Target):
            self.data[value.id] = value
        else:
            raise ValueError("Targets must be an instance of Target or a subclass.")


class FilePathTarget(Target):
    def __init__(
        self,
        id: str,
        path: t.Union[str, Path],
        content: str = None,
        encoding: str = "utf-8",
    ) -> None:
        super().__init__(id=id, content=content)
        self.path = path
        self.encoding = encoding


class FileLoad(TargetLoadPlugin):
    """Default target load plugin.
    Loads files to FilePathTargets.
    """

    def load(self, target: FilePathTarget) -> FilePathTarget:
        "Take a FilePathTarget and return it with content loaded from path."
        with open(target.path, "r", encoding=target.encoding) as file_handle:
            target.content = file_handle.read()
        return target

    def run(self) -> None:
        "Execute load on the targets in Manager().config.targets and place them in Manager().state.targets."
        self.manager.state.targets = {
            target.key: self.load(target) for target in self.manager.config.targets
        }


class FileSave(TargetSavePlugin):
    """Default target save plugin.
    Saves FilePathTargets to files.
    """

    def dump(self, target: FilePathTarget) -> None:
        "Takes a FilePathTarget and writes it's Content to it's path."
        with open(target.path, "w", encoding=target.encoding) as file_handle:
            file_handle.write(target.content)

    def run(self) -> None:
        "Execute dump on the targets in Manager().config.targets so they are saved to their target files."
        self.manager.state.targets = {
            target.key: self.load(target) for target in self.manager.config.targets
        }


class VersionMachine(VersionTravelPlugin):
    """Default version travel plugin.
    Uses a regex to find version string, increments based on pythonic/semantic versioning.
    https://peps.python.org/pep-0440/
    """

    extraction_pattern: t.ClassVar[t.Pattern] = re.compile(
        r"""__version__ = ['"](?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)(?P<phase>[^'"]+)?['"]"""
    )

    @property
    def match_text(self):
        if self.match:
            return self.match.group(0)
        else:
            return self.match

    @property
    def future_version(self) -> str:
        if self.force_version is not None:
            return self.force_version

        future = {}
        for k, v in (
            self.match.groupdict()
            if self.match
            else {n.name.lower(): 0 for n in self.IncrementType}
        ).items():
            if k.lower() == "phase":
                future[k] = "" if self.phase is None else self.phase
            elif (o := self.type_ordinal(k)) == (
                t := self.type_ordinal(self.increment)
            ):
                future[k] = int(v) + 1
            elif o > t:
                future[k] = 0
            else:
                future[k] = v

        return "{major}.{minor}.{patch}{phase}".format(**future)

    @property
    def repl(self) -> str:
        return f'__version__ = "{self.future_version}"'

    @property
    def future_text(self) -> str:
        return self.text.replace(self.match_text, self.repl)

    def type_ordinal(self, type: str | EnumMeta) -> int:
        if isinstance(type, str):
            type = self.IncrementType[type.upper()]
        return type.value
    
    def run(self):
        for t in self.manager.state.targets:
            t.content = self.future_text

    class IncrementType(Enum):
        MAJOR = 0
        MINOR = 1
        PATCH = 2
        PHASE = 3
