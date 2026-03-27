from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import datetime
import models

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
        
        self.counetrparty_table_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
            ('FONTNAME', (0, 0), (0, -1), 'DejaVuSerif'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ])


        self.invoice_table_style = TableStyle([
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

    def add_space(self, size):
        self.story.append(Spacer(1, size*cm))

    def add_paragraph(self, content, style):
        self.story.append(Paragraph(content, style))

    def create_invoice_table(self, items):
        table = Table(items, colWidths=[1*cm, 6*cm, 2*cm, 3*cm, 3*cm])
        table.setStyle(self.invoice_table_style)
        self.story.append(table)
        self.add_space(1)
    
    def create_counterparty_table(self, info):
        table = Table(info, colWidths=[3*cm, 6*cm])
        table.setStyle(self.counetrparty_table_style)
        self.story.append(table)
        self.add_space(1)



if __name__ == "__main__":
    seller = models.Counterparty(       
        name='ООО "Ромашка"',
        inn="1234567890",
        account="40702810000000000000",
        bank="ПАО Сбербанк",
        bik="044525225"
    )
   
    buyer = models.Counterparty(       
        name="ИП Иванов И.И.",
        inn="987654321012",
        address="г. Москва, ул. Примерная, д. 1"
    )
    
            
    items = [
        models.ServiceItem("1", "Разработка сайта", "1", "50 000", "50 000"),
        models.ServiceItem("2", "Техническая поддержка", "3", "5 000", "15 000"),
    ]

    invoice = models.Invoice(
            invoice_number="164",
            date="27.03.2026",
            seller=seller,
            buyer=buyer,
            items=items,
            subtotal="65 000",
            vat="Без НДС",
            grand_total="65 000 руб.",
            )

    doc = Document()
    doc.add_paragraph(f'СЧЁТ НА ОПЛАТУ № {invoice.invoice_number}', doc.title_style)
    doc.add_space(0.5)

    doc.create_counterparty_table(seller.to_table_rows())
    doc.create_counterparty_table(buyer.to_table_rows())

    doc.create_invoice_table(invoice.get_items_table())

    doc.build_doc() 

    
