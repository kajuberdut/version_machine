import subprocess
from functools import partial
import typing as t
import warnings


class DirtyFiles(UserWarning):
    ...


def git_info(*args, git_command="git") -> t.Optional[str]:
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
