import os
import qrcode
from PIL import Image

desktop_dirs = [
    r"C:\Users\Antonio\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Escritorio\Paymind Strategy"
]

for d in desktop_dirs:
    os.makedirs(d, exist_ok=True)

# URL por defecto (Puede ser el enlace a su OneDrive, Google Drive o Web)
default_cv_url = "https://paymind-growth-engine.pages.dev"

def generate_qr(url_or_data, output_filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # Alta corrección de errores (30%)
        box_size=10,
        border=4,
    )
    qr.add_data(url_or_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF") # Slate Dark & Blanco
    
    for d in desktop_dirs:
        if os.path.exists(d):
            dst = os.path.join(d, output_filename)
            img.save(dst)
            print(f"[OK] Código QR generado en: {dst}")

# Generar QR para el sitio web / CV en nube
generate_qr(default_cv_url, "CODIGO_QR_CV_ANTONIO.png")

# Generar también VCard QR (Guardar contacto en el teléfono sin internet)
vcard_data = """BEGIN:VCARD
VERSION:3.0
N:Gutiérrez;Antonio;;;
FN:Antonio Gutiérrez
TITLE:Consultor de Crecimiento & Pagos B2B
ORG:PayMind
EMAIL;TYPE=INTERNET,PREF:antonio.gutierrez@paymind.mx
URL:https://paymind-growth-engine.pages.dev
NOTE:Especialista en Infraestructura de Pagos y Adquirencia en Bomba para Estaciones de Servicio.
END:VCARD"""

generate_qr(vcard_data, "CODIGO_QR_TARJETA_CONTACTO_VCARD.png")

print("Generación de Códigos QR completada.")
