"""Runs demonstrations and creates dependency-free evidence images and charts."""
from pathlib import Path
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
TITLE = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)

def text_image(text, path, title):
    lines = text.splitlines() or [""]
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    width = max(760, max(probe.textlength(x, font=FONT) for x in lines) + 50)
    image = Image.new("RGB", (int(width), 65 + 28 * len(lines)), "#f8fafc")
    draw = ImageDraw.Draw(image); draw.text((20, 18), title, fill="#172554", font=TITLE)
    for i, line in enumerate(lines):
        draw.text((22, 55 + 28*i), line, fill="#111827", font=FONT)
    image.save(path)

modules = [("Module_1_Merge_Sort", "merge_sort.py"), ("Module_2_Quick_Sort", "quick_sort.py"),
           ("Module_3_Binary_Search", "binary_search.py"), ("Module_4_Strassen_Matrix_Multiplication", "strassen.py")]
for folder, script in modules:
    module = ROOT / folder; code = module / "Source_Code" / script
    shots = module / "Report" / "Screenshots"; shots.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([sys.executable, str(code)], text=True, capture_output=True, check=True)
    (shots / "output.txt").write_text(result.stdout)
    text_image(code.read_text(), shots / "source_code.png", f"Source code: {script}")
    text_image(result.stdout, shots / "output.png", "Program output")

def chart(path, title, labels, values_a, values_b, a_label, b_label):
    w, h, left, bottom = 1000, 580, 95, 100
    im = Image.new("RGB", (w, h), "white"); d = ImageDraw.Draw(im)
    d.text((left, 22), title, fill="#172554", font=TITLE); maxv = max(values_a + values_b)
    for k in range(5):
        y = h-bottom-k*(h-bottom-100)/4; d.line((left,y,w-35,y), fill="#e5e7eb")
        d.text((8,y-8), f"{maxv*k/4:.1e}", fill="#374151", font=FONT)
    xstep = (w-left-50)/(len(labels)-1)
    def points(vals): return [(left+i*xstep, h-bottom-(v/maxv)*(h-bottom-100)) for i,v in enumerate(vals)]
    for pts, color in [(points(values_a), "#2563eb"), (points(values_b), "#dc2626")]:
        d.line(pts, fill=color, width=4)
        for x,y in pts: d.ellipse((x-5,y-5,x+5,y+5), fill=color)
    for i,label in enumerate(labels): d.text((left+i*xstep-15,h-bottom+15), label, fill="#374151", font=FONT)
    d.rectangle((650,40,670,55), fill="#2563eb"); d.text((680,38), a_label, fill="#111827", font=FONT)
    d.rectangle((650,68,670,83), fill="#dc2626"); d.text((680,66), b_label, fill="#111827", font=FONT)
    im.save(path)

charts = ROOT / "Final_Design_and_Analysis" / "Graphs"; charts.mkdir(parents=True, exist_ok=True)
ns = [10,100,1000,10000,100000,10000000]
chart(charts / "growth_comparison.png", "Divide and conquer growth comparison", ["10","100","1k","10k","100k","10m"],
      [n*math.log2(n) for n in ns], [math.ceil(math.log2(n+1)) for n in ns], "Merge Sort n log2 n", "Binary Search log2 n")
sizes = [2**k for k in range(1,11)]
chart(charts / "strassen_vs_conventional.png", "Scalar multiplication count", [str(n) for n in sizes],
      [n**3 for n in sizes], [7**k for k in range(1,11)], "Conventional n cubed", "Strassen 7 to log2 n")
