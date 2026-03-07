#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".avif"}


def read_existing(csv_path: Path):
    existing = {}
    if not csv_path.exists():
        return existing

    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = (row.get("filename") or "").strip()
            if not filename:
                continue
            existing[filename] = {
                "filename": filename,
                "tier": (row.get("tier") or "").strip(),
                "Type": (row.get("Type") or "").strip(),
            }
    return existing


def collect_images(images_dir: Path):
    files = []
    for path in images_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        files.append(path.name)
    return sorted(set(files))


def render_csv(rows):
    lines = ["filename,tier,Type"]
    for row in rows:
        filename = row["filename"].replace(",", "")
        tier = row["tier"].replace(",", "")
        image_type = row["Type"].replace(",", "")
        lines.append(f"{filename},{tier},{image_type}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", required=True)
    parser.add_argument("--csv-path", required=True)
    args = parser.parse_args()

    images_dir = Path(args.images_dir)
    csv_path = Path(args.csv_path)

    existing = read_existing(csv_path)
    image_names = collect_images(images_dir)

    rows = []
    for image_name in image_names:
        row = existing.get(image_name, {"filename": image_name, "tier": "", "Type": ""})
        rows.append(row)

    output = render_csv(rows)
    previous = csv_path.read_text(encoding="utf-8") if csv_path.exists() else ""

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.write_text(output, encoding="utf-8")

    changed = output != previous
    print("changed=true" if changed else "changed=false")


if __name__ == "__main__":
    main()
