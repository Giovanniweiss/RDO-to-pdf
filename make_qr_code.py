import barcode
from barcode.writer import ImageWriter
import qrcode

def generate_code39(data, filename):
    # Get the Code39 barcode class
    CODE39 = barcode.get_barcode_class('code39')
    
    # Generate barcode
    code39 = CODE39(data, writer=ImageWriter(), add_checksum=False)
    code39.save(filename)

def generate_code128(data, filename):
    # Get the Code128 barcode class
    CODE128 = barcode.get_barcode_class('code128')
    
    # Generate barcode
    code128 = CODE128(data, writer=ImageWriter())
    code128.save(filename)

def generate_qr_code(data, filename):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create an image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

# Example usage
data = "Rohden Queimadores 12345678910"

generate_code39(data, "code39")
generate_code128(data, "code128")
generate_qr_code(data, "qrcode.png")
