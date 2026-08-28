import os
import pandas as pd

base_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine"
csv_in = os.path.join(base_dir, "data", "Snovio_Gasolineras_Segmentada_Clusters.csv")

df = pd.read_csv(csv_in, encoding='utf-8-sig')

# Asuntos y Cuerpos limpios, genuinos, sin asumir dolores y sin clichés
def clean_subject(cluster):
    return "Consulta breve sobre cobro en bomba"

def clean_body(row):
    nombre = str(row.get('Nombre', 'Director')).strip()
    if nombre.lower() in ['director', 'propietario', 'gerente', 'nan', '']:
        saludo = "Hola,"
    else:
        saludo = f"Hola {nombre},"
        
    return (
        f"{saludo}\n\n"
        f"Soy especialista en medios de pago y adquirencia bancaria. No pretendo asumir cómo operan la cobranza hoy en día ni qué retos particulares tienen.\n\n"
        f"Desde la parte técnica, ayudamos a estaciones de servicio a conectar terminales inalámbricas de cobro al pie del auto, manteniendo las mismas cuentas bancarias que ya utilizan (BBVA, BanBajío, Afirme) y con depósitos al día siguiente (T+1).\n\n"
        f"Si están abiertos a evaluar alternativas para agilizar la cobranza con tarjeta, ¿valdrá la pena platicar 5 minutos esta semana?\n\n"
        f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
    )

df['Asunto_Paso1'] = df['Cluster'].apply(clean_subject)
df['Cuerpo_Paso1'] = df.apply(clean_body, axis=1)

# Guardar CSV actualizado
df.to_csv(csv_in, index=False, encoding='utf-8-sig')

# Copiar a Escritorio
desktop_dirs = [
    r"C:\Users\Antonio\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Escritorio\Paymind Strategy"
]

for d in desktop_dirs:
    if os.path.exists(d):
        dst = os.path.join(d, "Snovio_Gasolineras_Segmentada_Clusters.csv")
        df.to_csv(dst, index=False, encoding='utf-8-sig')
        print(f"Actualizado CSV genuino en: {dst}")

print("CSV actualizado con éxito con los copys genuinos sin asunciones.")
