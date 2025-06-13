import os
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from utils.match_excel import match_excel_existing

os.makedirs("barcodes", exist_ok=True)

categorias = ["MUE001", "ECT002", "BCT003"]

def generate_code_bar():
    codes = []
   
    for cat in categorias:
        for i in range(100):
            code = f"{cat}-000{i + 1}"
            codes.append(code)

    for code in codes:
        filename = os.path.join("barcodes", code)
        barcode = Code128(code, writer=ImageWriter())
        barcode.save(filename)
    print("Códigos de barra generados como PNG en carpeta 'barcodes'.")
    return codes

def create_pdf(image_dir="barcodes", output_pdf="barcodes.pdf"):
    codes = generate_code_bar()
    match_excel_existing(codes)
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    margin = 40
    x, y = margin, height - margin

    col_count = 3
    spacing_x = (width - 2 * margin) / col_count
    spacing_y = 90
    img_width = 120
    img_height = 70
    border_padding = 5

    count = 0
    for code in codes:
        img_path = os.path.join(image_dir, f"{code}.png")
        if os.path.exists(img_path):
            c.drawImage(img_path, x, y - img_height, width=img_width, height=img_height)

            c.setDash(3, 3)
            c.setStrokeColorRGB(0, 0, 0)
            c.rect(x - border_padding, y - img_height - border_padding, img_width + 2 * border_padding, img_height + 2 * border_padding, stroke=1, fill=0)
            c.setDash()

            count += 1
            x += spacing_x
            if count % col_count == 0:
                x = margin
                y -= spacing_y
                if y < margin + img_height:
                    c.showPage()
                    y = height - margin
    c.save()
    print(f"PDF generado: {output_pdf}")


def generateCodes():
    create_pdf()
    
if __name__ == "__main__":
     generateCodes()