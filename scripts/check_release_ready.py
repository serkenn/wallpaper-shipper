#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".avif"}


def collect_images(images_dir: Path):
    names = set()
    for path in images_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
            names.add(path.name)
    return names


def check(csv_path: Path, image_names: set[str]):
    if not csv_path.exists():
        return False, "metadata CSV does not exist"

    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_fields = {"filename", "tier"}
        if not required_fields.issubset(set(reader.fieldnames or [])):
            return False, "CSV header must include filename,tier"

        rows = list(reader)

    if not rows:
        return False, "CSV has no rows"

    csv_names = set()
    for idx, row in enumerate(rows, start=2):
        filename = (row.get("filename") or "").strip()
        tier = (row.get("tier") or "").strip()

        if not filename:
            return False, f"row {idx}: filename is empty"
        if not tier:
            return False, f"row {idx}: tier is empty"

        csv_names.add(filename)

    missing = sorted(image_names - csv_names)
    extra = sorted(csv_names - image_names)
    if missing:
        return False, f"missing CSV rows for images: {', '.join(missing[:5])}"
    if extra:
        return False, f"CSV has rows for non-existent images: {', '.join(extra[:5])}"

    return True, "CSV is complete and consistent"


def set_output(key: str, value: str):
    output_raw = __import__("os").environ.get("GITHUB_OUTPUT", "").strip()
    if output_raw:
        output_path = Path(output_raw)
        with output_path.open("a", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", required=True)
    parser.add_argument("--csv-path", required=True)
    args = parser.parse_args()

    images_dir = Path(args.images_dir)
    csv_path = Path(args.csv_path)

    image_names = collect_images(images_dir)
    ready, reason = check(csv_path, image_names)

    set_output("ready", "true" if ready else "false")
    set_output("reason", reason)
    print(reason)


if __name__ == "__main__":
    main()
