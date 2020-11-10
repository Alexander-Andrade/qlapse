from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.graphics.barcode import qr
import io
from django.contrib.staticfiles.storage import staticfiles_storage


class PdfBannerGenerator:
    WIDTH = 250
    HEIGHT = 250
    QR_CODE_H = 330
    QR_CODE_W = 285
    PHONE_NUMBER_H = 100
    PHONE_NUMBER_W = 100
    FONT_HEIGHT = 50

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def generate(self):
        buffer = io.BytesIO()
        canvas = Canvas(buffer)
        self.__draw_background(canvas)
        self.__draw_qr(canvas)
        self.__draw_phone_number(canvas)
        canvas.showPage()
        canvas.save()
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def __draw_background(self, canvas):
        background_drawing = svg2rlg(staticfiles_storage.open('banners/banner_background.svg'))
        renderPDF.draw(background_drawing, canvas, 0, 0)

    def __draw_qr(self, canvas):
        qr_widget = qr.QrCodeWidget('phone_number')
        bounds = qr_widget.getBounds()
        qr_widget_width = bounds[2] - bounds[0]
        qr_widget_height = bounds[3] - bounds[1]
        transform = [self.WIDTH / qr_widget_width, 0, 0, self.HEIGHT / qr_widget_height, 0, 0]
        qr_drawing = Drawing(self.WIDTH, self.HEIGHT, transform=transform)
        qr_drawing.add(qr_widget)
        renderPDF.draw(qr_drawing, canvas, self.QR_CODE_W, self.QR_CODE_H)

    def __draw_phone_number(self, canvas):
        canvas.setFont("Courier", self.FONT_HEIGHT)
        canvas.drawString(self.PHONE_NUMBER_W, self.PHONE_NUMBER_H, self.phone_number)
