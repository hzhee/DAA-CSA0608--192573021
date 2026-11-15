from pathlib import Path
from docx import Document
from docx.shared import Inches,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
root=Path(__file__).resolve().parents[1];out=root/'Final_Report';out.mkdir(exist_ok=True)
def make(src,dest,title):
 d=Document();sec=d.sections[0];sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65)
 st=d.styles['Normal'];st.font.name='Aptos';st.font.size=Pt(10)
 p=d.add_paragraph();p.style='Title';p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run(title)
 for line in src.read_text().splitlines():
  if not line.strip():continue
  if line.startswith('# '):continue
  if line.startswith('## '):d.add_heading(line[3:],1)
  elif line.startswith('### '):d.add_heading(line[4:],2)
  elif line.startswith('|'):
   d.add_paragraph(line.replace('|','  |  '))
  else:d.add_paragraph(line.replace('`','').replace('**',''))
 d.save(dest)
make(root/'Combined_Report.md',out/'CO3_Assignment_Report.docx','CO3 Assignment Report')
contrib=root/'Combined_Report.md'
d=Document();d.add_heading('Student Contribution Record',0);d.add_paragraph('Replace Student A and Student B with actual names and confirm this record reflects the pair’s real work before submission.')
d.add_heading('Planned contribution distribution',1)
for line in contrib.read_text().splitlines():
 if line.startswith('| Q'):d.add_paragraph(line.replace('|','  |  '))
d.add_heading('Shared accountability',1);d.add_paragraph('Both students are expected to explain each question, decomposition, base case, recurrence, experiment and design choice during viva.')
d.save(out/'Student_Contribution_Record.docx')
