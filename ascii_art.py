#!/usr/bin/env python3
"""Convert an image to simple ASCII art and optionally drop it into README.md."""

import argparse

from PIL import Image, ImageOps

CHARS = " .:+#@"  # light -> dark, keep short for a simple (not fancy) look


def image_to_ascii(path, width=60, aspect_correction=0.55, autocontrast=True):
    img = Image.open(path).convert("L")
    if autocontrast:
        img = ImageOps.autocontrast(img, cutoff=2)

    w, h = img.size
    new_h = int(width * h / w * aspect_correction)
    img = img.resize((width, new_h))

    pixels = list(img.getdata())
    rows = []
    for y in range(new_h):
        row = ""
        for x in range(width):
            p = pixels[y * width + x]
            idx = int((p / 255) * (len(CHARS) - 1))
            row += CHARS[idx]
        rows.append(row)

    return "\n".join(rows)


def update_readme(ascii_art, readme_path="README.md"):
    with open(readme_path) as f:
        content = f.read()

    start_marker = "<pre>\n"
    end_marker = "\n</pre>"

    start = content.index(start_marker) + len(start_marker)
    end = content.index(end_marker, start)

    new_content = content[:start] + ascii_art + content[end:]

    with open(readme_path, "w") as f:
        f.write(new_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", help="path to the source image, e.g. me.png")
    parser.add_argument("--width", type=int, default=60, help="output width in characters")
    parser.add_argument(
        "--aspect-correction",
        type=float,
        default=0.55,
        help="compensates for characters being taller than wide",
    )
    parser.add_argument(
        "--no-autocontrast",
        action="store_true",
        help="skip contrast boosting (useful for plain/studio backgrounds)",
    )
    parser.add_argument(
        "--update-readme",
        action="store_true",
        help="write the result directly into README.md's <pre> block",
    )
    parser.add_argument("--readme", default="README.md", help="path to README.md")
    args = parser.parse_args()

    art = image_to_ascii(
        args.image,
        width=args.width,
        aspect_correction=args.aspect_correction,
        autocontrast=not args.no_autocontrast,
    )

    if args.update_readme:
        update_readme(art, args.readme)
        print(f"Updated {args.readme}")
    else:
        print(art)


"""
To RUN:
python3 ascii_art.py me.png

# save it to a file instead
python3 ascii_art.py me.png > art.txt

# make it wider/narrower (default is 60 characters wide)
python3 ascii_art.py me.png --width 80

# regenerate AND drop it straight into README.md's <pre> block
python3 ascii_art.py me.png --update-readme
"""