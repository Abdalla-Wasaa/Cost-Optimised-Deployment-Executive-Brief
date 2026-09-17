"""Render the executive source into standalone HTML and one-page PDF.
Optional dependency: reportlab (see exec/requirements-export.txt).
"""
import html
import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

ROOT=Path(__file__).resolve().parents[1]

def inline(text):
    text=html.escape(text)
    text=re.sub(r"\*\*(.*?)\*\*",r"<b>\1</b>",text)
    text=re.sub(r"`(.*?)`",r"<i>\1</i>",text)
    return text

def main():
    source=(ROOT/'exec/executive_brief.md').read_text()
    body=[]
    flow=[]
    normal=ParagraphStyle('body',fontName='Helvetica',fontSize=9.5,leading=12.5,
                          textColor=colors.HexColor('#1e293b'),spaceAfter=6)
    title=ParagraphStyle('title',parent=normal,fontName='Helvetica-Bold',fontSize=17,
                         leading=20,spaceAfter=9,textColor=colors.HexColor('#0b4f57'))
    cell=ParagraphStyle('cell',parent=normal,fontSize=8,leading=10,spaceAfter=0)
    for block in source.strip().split('\n\n'):
        if block.startswith('# '):
            text=inline(block[2:]);body.append('<h1>'+text+'</h1>')
            flow.append(Paragraph(text,title))
        elif block.startswith('|'):
            rows=[[inline(c.strip()) for c in line.strip('|').split('|')]
                  for line in block.splitlines() if not re.match(r'^\|[- :|]+$',line)]
            body.append('<table>'+''.join('<tr>'+''.join('<td>'+c+'</td>' for c in row)+'</tr>' for row in rows)+'</table>')
            table=Table([[Paragraph(c,cell) for c in row] for row in rows],colWidths=[175,175,175])
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e0f2f1')),
                                      ('VALIGN',(0,0),(-1,-1),'TOP'),
                                      ('GRID',(0,0),(-1,-1),.3,colors.HexColor('#cbd5e1')),
                                      ('BOTTOMPADDING',(0,0),(-1,-1),5),
                                      ('TOPPADDING',(0,0),(-1,-1),5)]))
            flow.extend([table,Spacer(1,8)])
        else:
            text=inline(' '.join(block.splitlines()));body.append('<p>'+text+'</p>')
            flow.append(Paragraph(text,normal))
    css='@page{size:A4;margin:14mm}*{box-sizing:border-box}body{max-width:185mm;margin:auto;font:10pt/1.32 Arial,sans-serif;color:#1e293b}h1{font-size:19pt;color:#0b4f57;margin:0 0 10pt}p{margin:0 0 8pt}table{width:100%;border-collapse:collapse;margin:9pt 0;font-size:9pt}td{border:1px solid #cbd5e1;padding:6pt;vertical-align:top}tr:first-child{background:#e0f2f1;font-weight:bold}@media print{body{font-size:9pt}p{margin-bottom:6pt}h1{font-size:17pt}}'
    (ROOT/'exec/executive_brief.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Week 7 executive brief</title><style>'+css+'</style></head><body>'+''.join(body)+'</body></html>')
    doc=SimpleDocTemplate(str(ROOT/'exec/executive_brief.pdf'),pagesize=A4,
                         leftMargin=35,rightMargin=35,topMargin=30,bottomMargin=30,
                         title='Week 7 Cost Optimisation Executive Brief',author='Capstone Engineering')
    doc.build(flow)

if __name__=='__main__': main()
