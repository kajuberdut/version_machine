import argparse
import random
import string
import sys
import typing as t
import warnings
from pathlib import Path
from plugin_base import Plugin
from version_machine.base_classes import Config

class Manager:
    # Borg pattern, all instances share plugins dicts
    plugins: t.ClassVar[dict] = {}

    def __init__(self, *args):
        for plugin in args:
            self.register(plugin)

    def register(self, plugin: Plugin) -> None:
        instance = plugin()
        instance.manager = self
        self.plugins[instance.name] = instance

    def __getattr__(self, __name: str) -> Plugin:
        try:
            return self.plugins[__name]
        except KeyError:
            raise RuntimeError(f"{__name} is a required plugin and was not found.")
        
    def run_sequence(self):
        self.sequence.run()

def random_name(root: str = "", random_chars: int = 5):
    rand = "".join(random.choice(string.ascii_lowercase) for i in range(random_chars))
    return f"{root}{rand}"

def main(
    config: Config | dict | None = None,
    lock: bool = False,
    lock_path: Path | None = None,
    force: bool = False,
):
    # check_dirty(warn=force)
    # if lock:
    #     l = Lock(lock_path)
    # else:
    #     l = NoLock(lock_path)
    # if l.current_tag in l.data:
    #     warnings.warn(
    #         f"HEAD ({l.current_tag}) is locked to version {l[l.current_tag]}."
    #         "\nNo actions taken.",
    #         LockedTag,
    #     )
    #     return
    config = Config(config=config) if not isinstance(config, Config) else config
    version = None
    # for target in config.targets:
    #     version = version_travel(**target)
    # l.set_version(version)
    # l.lock()


# def parse_args(args):
#     parser = argparse.ArgumentParser(description="Move version numbers.")
#     parser.add_argument(
#         "--path",
#         action="store",
#         required=False,
#         default=None,
#         type=Path,
#         help="path of file to change version in.",
#     )
#     parser.add_argument(
#         "-i",
#         "--increment",
#         action="store",
#         required=False,
#         default="PATCH",
#         type=VersionMachine.increment,
#         choices=[i for i in VersionMachine.IncrementType],
#         help="Version part to be incrememnted.",
#     )
#     parser.add_argument(
#         "-f",
#         "--force",
#         action="store_true",
#         help="Ignore warnings and force version move.",
#     )
#     parser.add_argument(
#         "-L",
#         "--lock",
#         action="store_true",
#         help="Lock the current git head commit tag to a specific version.",
#     )

#     return parser.parse_args(args)


# def cli():
#     args = parse_args(sys.argv[1:])
#     cli_conf = {
#         random_name(root="cli_config_"): {
#             a: getattr(args, a) for a in ["path", "increment"] if getattr(args, a)
#         }
#     }
#     if cli_conf:
#         config = Config()
#         config.update(cli_conf)
#     else:
#         config = None  # pragma: no cover
#     main(force=args.force, lock=args.lock, config=config)
