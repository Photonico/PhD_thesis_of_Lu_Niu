#!/usr/bin/env python3
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

# python kernel selection
# Cmd + P
# input: >Python: Select Interpreter

def find_inkscape() -> str:
    """Find the Inkscape executable on macOS/Linux/Windows."""
    candidates = [
        shutil.which("inkscape"),
        "/Applications/Inkscape.app/Contents/MacOS/inkscape",  # macOS app path
        "C:/Program Files/Inkscape/bin/inkscape.exe",          # common Windows path
    ]

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)

    raise FileNotFoundError(
        "Cannot find Inkscape. Install Inkscape first, or add it to PATH."
    )


def convert_svg_to_pdf(svg_path: Path, overwrite: bool = False) -> None:
    svg_path = svg_path.resolve()
    pdf_path = svg_path.with_suffix(".pdf")

    if pdf_path.exists() and not overwrite:
        print(f"Skip existing: {pdf_path}")
        return

    inkscape = find_inkscape()

    command = [
        inkscape,
        str(svg_path),
        "--export-type=pdf",
        f"--export-filename={pdf_path}",
    ]

    print(f"Converting: {svg_path} -> {pdf_path}")
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Failed to convert {svg_path}")

    print(f"Done: {pdf_path}")


def collect_svg_files(path: Path, recursive: bool = False) -> list[Path]:
    path = path.resolve()

    if path.is_file():
        if path.suffix.lower() != ".svg":
            raise ValueError(f"Input file is not an SVG file: {path}")
        return [path]

    if path.is_dir():
        pattern = "**/*.svg" if recursive else "*.svg"
        return sorted(path.glob(pattern))

    raise FileNotFoundError(f"Path does not exist: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert SVG files to PDF using Inkscape without rasterizing."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="SVG file or directory containing SVG files. Default: current directory.",
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Search SVG files recursively in subdirectories.",
    )
    parser.add_argument(
        "-f", "--overwrite",
        action="store_true",
        help="Overwrite existing PDF files.",
    )

    args = parser.parse_args()

    svg_files = collect_svg_files(Path(args.path), recursive=args.recursive)

    if not svg_files:
        print("No SVG files found.")
        return

    for svg_file in svg_files:
        convert_svg_to_pdf(svg_file, overwrite=args.overwrite)

#%%
if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

# %%
