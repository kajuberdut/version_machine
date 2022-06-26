import typing as t
from abc import ABC, abstractmethod
from enum import Enum

from version_machine.base_classes import Target


class Plugin:
    "Basic plugin class from which all other plugin classes inherit."
    name: str
    manager: "Manager"


class ConfigPlugin(Plugin):
    name: t.ClassVar[str] = "config"


class StatePlugin(Plugin):
    """State plugin is responsible for maintaining all state information while version_machine is processing versions."""

    name: t.ClassVar[str] = "state"

    @property
    @abstractmethod
    def targets(self) -> t.Iterable | t.Generator | None:
        pass

    @targets.setter
    @abstractmethod
    def targets(self, value: t.Any) -> None:
        pass


class RunablePlugin(Plugin):
    @abstractmethod
    def run(self):
        "Runs the primary function of plugin."
        pass


class RunSequencePlugin(RunablePlugin):
    "Defines the sequence of plugin execution."
    name: t.ClassVar[str] = "run_sequence"


class VersionTravelPlugin(RunablePlugin):
    "Handles changing the version information in a target str."
    name: t.ClassVar[str] = "version_travel"

    class IncrementType(Enum):
        """Version plugins should define an enum representing the increment types
            of the target version system.
        """
        UNDEFINED = 0

    @abstractmethod
    def run(self) -> None:
        """For each target in self.manager.state.targets
        , update the target.content based on the other config in target."""
        pass



class TargetLoadPlugin(RunablePlugin, ABC):
    "Handles loading targets."
    name: t.ClassVar[str] = "target_load"

    @abstractmethod
    def load(self, target: Target) -> Target:
        """Method for loading content of a Target."""
        pass

    @abstractmethod
    def run(self) -> None:
        """Method to load all self.manager.config.targets
            and placed them in self.manager.state.targets
        """
        pass


class TargetSavePlugin(RunablePlugin, ABC):
    "Handles saving targets."
    name: t.ClassVar[str] = "target_save"

    @abstractmethod
    def dump(self, target: Target) -> None:
        """Method for saving the content of a Target."""
        pass

    @abstractmethod
    def save_targets(self) -> None:
        """Method to dump all self.manager.state.targets."""
        pass

    @abstractmethod
    def run(self) -> None:
        """Method to save all self.manager.state.targets to their intended target destination."""
        pass
