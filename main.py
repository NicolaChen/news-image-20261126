"""Emit the immutable news illustration for the offline contest runner."""
from os import environ
from pathlib import Path
from shutil import copyfile


def main() -> None:
    source = Path(__file__).with_name("entry.png")
    output = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output.mkdir(parents=True, exist_ok=True)
    copyfile(source, output / "entry.png")


if __name__ == "__main__":
    main()
