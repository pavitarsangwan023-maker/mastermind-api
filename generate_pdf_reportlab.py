from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import re

def create_pdf(input_file, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    style_normal = styles["Normal"]
    style_normal.fontSize = 11
    style_normal.leading = 14
    
    style_heading = styles["Heading2"]
    
    story = []
    
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 10))
            continue
            
        line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        
        if line.startswith('### '):
            p = Paragraph(line[4:], style_heading)
            story.append(p)
            story.append(Spacer(1, 5))
        elif line.startswith('# '):
            p = Paragraph(line[2:], styles['Heading1'])
            story.append(p)
            story.append(Spacer(1, 5))
        else:
            p = Paragraph(line, style_normal)
            story.append(p)
            story.append(Spacer(1, 2))
            
    doc.build(story)

if __name__ == "__main__":
    create_pdf('mastermind_app_requirements_english.md', 'mastermind_app_requirements_english.pdf')
