"""Run the six CO4B programs and save full stdout plus paginated screenshots."""

from pathlib import Path
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_PATHS = ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Supplemental/Courier New.ttf")
LINES_PER_CAPTURE = 28


def mono_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_capture(task, lines, page, pages, destination):
    font, title_font = mono_font(15), mono_font(16)
    wrapped = []
    for line in lines:
        wrapped.extend(textwrap.wrap(line, width=118, subsequent_indent="      ",
                                    replace_whitespace=False, drop_whitespace=True,
                                    break_long_words=True, break_on_hyphens=False) or [""])
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    widest = max((probe.textbbox((0, 0), line, font=font)[2] for line in wrapped), default=900)
    width = max(1080, min(1400, widest + 36))
    height = 48 + 25 * len(wrapped) + 18
    image = Image.new("RGB", (width, height), "#171923")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 34), fill="#292d3e")
    draw.text((16, 8), f"Task {task} - Program execution - capture {page}/{pages}", font=title_font, fill="#e6e9ef")
    y = 45
    for line in wrapped:
        draw.text((18, y), line, font=font, fill="#b8e994")
        y += 25
    image.save(destination)


def main():
    for task in range(1, 7):
        source = ROOT / f"Source_Code/Task_{task}/task_{task}.py"
        output_dir = ROOT / f"Source_Code/Task_{task}/Output"
        output_dir.mkdir(parents=True, exist_ok=True)
        result = subprocess.run([sys.executable, str(source)], check=True, capture_output=True,
                                text=True, timeout=60)
        (output_dir / "output.txt").write_text(result.stdout, encoding="utf-8")
        lines = result.stdout.rstrip().splitlines()
        chunks = [lines[i:i + LINES_PER_CAPTURE] for i in range(0, len(lines), LINES_PER_CAPTURE)]
        for old in output_dir.glob("output_*.png"):
            old.unlink()
        for i, chunk in enumerate(chunks, 1):
            name = "output.png" if i == 1 else f"output_{i:02}.png"
            make_capture(task, chunk, i, len(chunks), output_dir / name)
        print(f"Task {task}: passed; captured {len(lines)} stdout lines in {len(chunks)} screenshot(s)")


if __name__ == "__main__":
    main()
