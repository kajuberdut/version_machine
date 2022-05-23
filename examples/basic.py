from version_machine import version_travel
from pathlib import Path

THIS_FILE = Path(__file__)
example_path = THIS_FILE.parent / "example_version.py" 

version_travel(path=example_path, increment_type="major")