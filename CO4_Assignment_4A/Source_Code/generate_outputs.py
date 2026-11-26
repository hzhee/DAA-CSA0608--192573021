"""Execute all CO4 solutions and save their console output and PNG captures."""

from pathlib import Path
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONT_PATHS = (
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Supplemental/Courier New.ttf",
)


def mono_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def write_capture(task_number, output, destination):
    font = mono_font(15)
    title_font = mono_font(16)
    lines = []
    for source_line in output.rstrip().splitlines():
        wrapped = textwrap.wrap(
            source_line,
            width=96,
            subsequent_indent="      ",
            replace_whitespace=False,
            drop_whitespace=True,
            break_long_words=True,
            break_on_hyphens=False,
        )
        lines.extend(wrapped or [""])
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    widest = max((probe.textbbox((0, 0), line, font=font)[2] for line in lines), default=700)
    width = max(900, min(1150, widest + 36))
    line_height = 25
    height = max(140, 48 + line_height * len(lines) + 18)
    image = Image.new("RGB", (width, height), "#171923")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 34), fill="#292d3e")
    draw.text((16, 8), f"Task {task_number} - Program execution", font=title_font, fill="#e6e9ef")
    y = 45
    for line in lines:
        draw.text((18, y), line, font=font, fill="#b8e994")
        y += line_height
    image.save(destination)


def main():
    for task_number in range(1, 7):
        source = ROOT / f"Source_Code/Task_{task_number}/task_{task_number}.py"
        output_dir = ROOT / f"Source_Code/Task_{task_number}/Output"
        output_dir.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [sys.executable, str(source)],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        (output_dir / "output.txt").write_text(output, encoding="utf-8")
        write_capture(task_number, output, output_dir / "output.png")
        print(f"Task {task_number}: executed successfully; saved output.txt and output.png")


if __name__ == "__main__":
    main()
