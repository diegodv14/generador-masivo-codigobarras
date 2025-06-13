import os
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

os.makedirs("barcodes", exist_ok=True)

codes = [f"CODE{i:03}" for i in range(1, 301)]

for code in codes:
    filename = os.path.join("barcodes", code)
    barcode = Code128(code, writer=ImageWriter())
    barcode.save(filename)

print("✅ Códigos de barra generados como PNG en carpeta 'barcodes'.")

def create_pdf(image_dir="barcodes", output_pdf="barcodes.pdf"):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    margin = 40
    x, y = margin, height - margin

    col_count = 3
    spacing_x = (width - 2 * margin) / col_count
    spacing_y = 70
    count = 0
    for code in codes:
        img_path = os.path.join(image_dir, f"{code}.png")
        if os.path.exists(img_path):
            c.drawImage(img_path, x, y - 50, width=120, height=70)

            count += 1
            x += spacing_x
            if count % col_count == 0:
                x = margin
                y -= spacing_y
                if y < margin:
                    c.showPage()
                    y = height - margin
    c.save()
    print(f"📄 PDF generado: {output_pdf}")



def generateCodes():
    create_pdf()

if __name__ == "__main__":
     generateCodes()