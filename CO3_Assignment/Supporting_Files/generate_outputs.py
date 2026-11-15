from pathlib import Path
from subprocess import run
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',15)
for q in root.glob('Q*/Implementation_Code'):
 for code in q.glob('*.py'):
  out=run(['python3',str(code)],capture_output=True,text=True,check=True).stdout; d=q.parent/'Output_Screenshots';d.mkdir(exist_ok=True);(d/'output.txt').write_text(out)
  im=Image.new('RGB',(850,max(150,45+28*len(out.splitlines()))),'white');draw=ImageDraw.Draw(im);draw.text((20,18),out,fill='black',font=font,spacing=8);im.save(d/'output.png')
