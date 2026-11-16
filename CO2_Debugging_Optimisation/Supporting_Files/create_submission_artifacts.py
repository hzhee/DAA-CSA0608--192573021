"""Build screenshot PNGs and combined PDF hand-in files from repository sources."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Preformatted,Spacer
from reportlab.lib import colors
from html import escape

ROOT=Path(__file__).resolve().parents[1]; SHOTS=ROOT/'Supporting_Files'/'Screenshots'; SHOTS.mkdir(exist_ok=True)
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14)
def png(title,text,path):
 lines=text.splitlines() or ['']; im=Image.new('RGB',(1200,max(150,55+25*len(lines))),'#f8fafc');d=ImageDraw.Draw(im)
 d.text((18,15),title,fill='#172554',font=font)
 for i,line in enumerate(lines):d.text((18,42+25*i),line,fill='#111827',font=font)
 im.save(path)
for f in sorted((ROOT/'Source_Code').rglob('*.py')):png(f'Source code: {f.name}',f.read_text(),SHOTS/(f'{f.stem}_source.png'))
for f in sorted(SHOTS.glob('*_output.txt')):png(f'Execution output: {f.name}',f.read_text(),SHOTS/(f'{f.stem}.png'))

pseudos=sorted((ROOT/'Pseudocode').glob('*.txt')); combined='\n\n'.join(f'# {p.stem}\n\n{p.read_text()}' for p in pseudos)
(ROOT/'Pseudocode'/'Combined_Pseudocode.md').write_text(combined)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='CodeBlock',fontName='Courier',fontSize=7.5,leading=9.5,backColor=colors.HexColor('#f1f5f9'),borderPadding=5,spaceAfter=7));styles.add(ParagraphStyle(name='Body2',parent=styles['BodyText'],fontSize=9,leading=12,spaceAfter=5))
def footer(c,d):c.saveState();c.setFont('Helvetica',8);c.setFillColor(colors.grey);c.drawString(40,24,'CSA06 CO2 SentinelOps');c.drawRightString(555,24,f'Page {d.page}');c.restoreState()
def to_pdf(src,out,title):
 story=[Paragraph(title,styles['Title']),Spacer(1,12)];code=False;buf=[]
 for raw in src.read_text().splitlines():
  s=raw.strip()
  if s.startswith('```'):
   if code:story.append(Preformatted('\n'.join(buf),styles['CodeBlock']));buf=[]
   code=not code;continue
  if code:buf.append(raw);continue
  if not s:continue
  if s.startswith('# '):continue
  if s.startswith('## '):story.append(Paragraph(s[3:],styles['Heading1']));continue
  if s.startswith('### '):story.append(Paragraph(s[4:],styles['Heading2']));continue
  clean=escape(s.replace('`','').replace('**','')).replace('&lt;br&gt;','; ')
  if s.startswith('|'):story.append(Paragraph(clean.replace('|',' &nbsp; | &nbsp; '),styles['Body2']));continue
  story.append(Paragraph(clean,styles['Body2']))
 SimpleDocTemplate(str(out),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=42,bottomMargin=40).build(story,onFirstPage=footer,onLaterPages=footer)
to_pdf(ROOT/'Report'/'CO2_Assessment_Report.md',ROOT/'Report'/'CO2_Assessment_Report.pdf','CO2 SentinelOps Debugging and Optimisation Report')
to_pdf(ROOT/'Pseudocode'/'Combined_Pseudocode.md',ROOT/'Pseudocode'/'Combined_Pseudocode.pdf','CO2 Combined Pseudocode')
