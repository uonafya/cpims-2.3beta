
"""Creating AKI certificate."""
import os.path
from functools import partial
from PIL import Image as PImage
from django.conf import settings
from decimal import Decimal
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import (
    TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT)
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, Image,
    TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
STATIC_ROOT = settings.STATICFILES_DIRS[0]


class FooterCanvas(canvas.Canvas):
    """Class to do footers."""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        # page = "Page %s of %s" % (self._pageNumber, page_count)
        page = ""
        # x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.25)
        # self.line(48, 78, LETTER[0] - 66, 78)
        self.setFont('Times-Roman', 9)
        self.drawString(48, 65, page)


class MyReport:
    def __init__(self, response, params, *args, **kwargs):
        author = params['insurance']
        self.doc = SimpleDocTemplate(
            response, pagesize=A4, title="Marine Insurance",
            author=author, subject="Marine Cargo Insurance",
            creator="Marine Cargo Insurance",
            keywords="MCI, Marine Cargo Insurance",
            rightMargin=48, leftMargin=48,
            topMargin=18, bottomMargin=18)
        if 'left_footer' in kwargs:
            self.left_footer = kwargs['left_footer']
        else:
            self.left_footer = None
        self.Story = []
        self.params = params
        self.response = response

    def onMyFirstPage(self, canvas, doc):
        # If the left_footer attribute is not None, then add it to the page
        canvas.saveState()
        if self.left_footer is not None:
            # canvas.setFont('Helvetica', 8)
            # canvas.drawString(1 * cm, 1 * cm, self.left_footer)
            canvas.setFont("Times-Roman", 150)
            canvas.setStrokeColorRGB(0.74, 0.74, 0.74)
            canvas.setFillColorRGB(0.74, 0.74, 0.74)
            canvas.translate(A4[0]/2, A4[1]/2)
            canvas.rotate(45)
            canvas.drawCentredString(20, 0, self.left_footer)
        canvas.restoreState()

    def onMyLaterPages(self, canvas, doc):
        # If the left_footer attribute is not None, then add it to the page
        canvas.saveState()
        if self.left_footer is not None:
            canvas.setFont('Helvetica', 8)
            canvas.drawString(1 * cm, 1 * cm, self.left_footer)
        canvas.restoreState()

    def generateReport(self):
        self.reportContent()
        self.doc.build(self.Story, canvasmaker=FooterCanvas, 
                       onFirstPage=self.onMyFirstPage,
                       onLaterPages=self.onMyLaterPages)

    def reportContent(self):
        params = self.params
        author = params['insurance']
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='Justify', alignment=TA_JUSTIFY,
            fontName='Times', fontSize=9, leading=9))
        styles.add(ParagraphStyle(
            name='Normals', alignment=TA_LEFT,
            fontName='Times', fontSize=9, leading=10))
        styles.add(ParagraphStyle(
            name='Heading', alignment=TA_LEFT,
            fontName='Times', fontSize=9, leading=14))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        story = []
        logo = "%s/img/gok_logo.png" % (STATIC_ROOT)

        if not os.path.isfile(logo):
            logo = "%s/img/logo_0.png" % (STATIC_ROOT)
        ins_address = params['insurances']
        coname = params['insurance']
        para = '<para align=center><font size=14>'
        company_name = '%s%s</font></para>' % (para, coname)
        address_parts = ["phy_addr",
                         "postal_addr", "tel", "email"]
        im = PImage.open(logo)
        imw, imh = im.size
        limw = imw / 180.0
        limh = imh / 180.0
        im = Image(logo, limw * inch, limh * inch, hAlign='LEFT')
        fsd = Table([[im]])
        # story.append(im)
        story.append(fsd)
        doc_head = 'MINISTRY OF LABOUR AND SOCIAL PROTECTION'
        head = '<strong>%s</strong>' % (doc_head)
        story.append(Spacer(1, 1))
        ptext = '<para align=center><font size=14>%s</font></para>' % (head)
        story.append(Paragraph(ptext, styles["Heading"]))
        story.append(Spacer(1, 6))
        doc_head = 'DEPARTMENT OF CHILDREN SERVICES'
        head = '<strong>%s</strong>' % (doc_head)
        story.append(Spacer(1, 1))
        ptext = '<para align=center><font size=14>%s</font></para>' % (head)
        story.append(Paragraph(ptext, styles["Heading"]))
        story.append(Spacer(1, 6))
        dhead = 'PRESIDENTIAL BURSARY APPLICATION FORM'
        story.append(Spacer(1, 1))
        ptext = '<para align=center><font size=12>%s</font></para>' % (dhead)
        story.append(Paragraph(ptext, styles["Heading"]))
        story.append(Spacer(1, 6))
        self.Story = story



def create_mcert(response, params):
    """Actual method."""
    # generate_certificate(response, params)
    wmark = '' if params['status_id'] == 1 else 'Cancelled'

    report = MyReport(response, params, left_footer=wmark)
    # I can now specify my custom footer in runtime!
    report.generateReport()