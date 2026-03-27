from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import datetime

pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))

OUTPUT_NAME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
OUTPUT_PATH = 'result/' + OUTPUT_NAME + '.pdf'


class Document:

    def __init__(self, output_path=OUTPUT_PATH):
        self.story = []
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Стили ----------------------------
        styles = getSampleStyleSheet()
        
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='DejaVuSerif',
            fontSize=16,
            spaceAfter=12,
            alignment=1
        )
        
        self.base_style = ParagraphStyle(
            'BaseStyle',
            parent=styles['Normal'],
            fontName='DejaVuSerif',
            fontSize=10,
            leading=12
        )
        
        self.table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ])
        # Стили ----------------------------

    def build_doc(self):
        self.doc.build(self.story)        
        print('Created')

    def add_space(self):
        self.story.append(Spacer(1, 1*cm))

    def add_paragraph(self, content, style):
        self.story.append(Paragraph(content, style))

    def create_invoice_table(self, items):
        table = Table(items, colWidths=[1*cm, 6*cm, 2*cm, 3*cm, 3*cm])
        table.setStyle(self.table_style)
        self.story.append(table)
        self.add_space()
    
    def create_contragent_table(self, info):
        table = Table(info, colWidths=[3*cm, 6*cm])
        table.setStyle(self.table_style)
        self.story.append(table)
        self.add_space()



if __name__ == "__main__":
    ...
