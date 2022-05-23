from pathlib import Path
import re

ROOT_PATH = Path(__file__).parent
EXAMPLES_PATH = ROOT_PATH / "examples"
README_PATH = ROOT_PATH / "readme.md"
TEMPLATE_PATH = ROOT_PATH / "readme.template.md"


def get_value(match: re.Match) -> str:
    tag = match.groupdict()["tag"]
    example_path = (EXAMPLES_PATH / tag).with_suffix(".py")
    with open(example_path, "r", encoding="utf-8") as example_file:
        return example_file.read()


def build():
    with open(TEMPLATE_PATH, encoding="utf-8") as template_file:
        template = template_file.read()

    output = re.sub(r"{{(?P<tag>[^}]+)}}", get_value, template)
    with open(README_PATH, "w", encoding="utf-8") as readme_file:
        readme_file.write(output)


if __name__ == "__main__":
    build()
