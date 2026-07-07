from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 14)
        self.cell(0, 10, 'Mastermind App - Project Details', new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', new_x="LMARGIN", new_y="NEXT", align='C')

def create_pdf(input_file, output_file):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("helvetica", size=11)
    
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
        
    for line in text.split('\n'):
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
        line = re.sub(r'^#+\s+', '', line)
        if line.startswith('- '):
            line = '  ' + line
            
        line = line.encode('latin-1', 'replace').decode('latin-1')
        if not line.strip():
            pdf.ln(5)
        else:
            pdf.multi_cell(0, 7, text=line)

    pdf.output(output_file)

if __name__ == "__main__":
    create_pdf('mastermind_app_requirements_english.md', 'mastermind_app_requirements_english.pdf')
