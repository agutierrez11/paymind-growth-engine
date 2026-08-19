import pandas as pd
import os
import shutil

excel_path = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\Campana_PayMind_MultiSegmento_CPS.xlsx"
df_gas = pd.read_excel(excel_path, sheet_name="Gasolineras_433")

# Clean column names
df_gas.columns = [c.strip() for c in df_gas.columns]

# Filter rows that have an email and a direct contact name
valid_leads = []
for idx, row in df_gas.iterrows():
    email = str(row.get('Email', '')).strip()
    nombre = str(row.get('Nombre_Contacto', '')).strip()
    empresa = str(row.get('Empresa', '')).strip()
    estado = str(row.get('Estado', '')).strip()
    
    if email and '@' in email and email.lower() != 'nan' and 'sin_correo' not in email.lower():
        # Clean company name
        clean_empresa = empresa.replace("S.A. DE C.V.", "").replace("SA DE CV", "").replace("S.A.", "").strip()
        clean_nombre = nombre if nombre and nombre.lower() != 'nan' else 'Director'
        clean_estado = estado if estado and estado.lower() != 'nan' else 'su región'
        
        valid_leads.append({
            "Email": email,
            "Nombre": clean_nombre,
            "Empresa": clean_empresa,
            "Estado": clean_estado,
            "Cargo": "Director / Propietario"
        })

df_clean = pd.DataFrame(valid_leads)
out_csv = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\Snovio_Gasolineras_Lanzamiento.csv"
df_clean.to_csv(out_csv, index=False, encoding='utf-8-sig')

# Also save in Downloads and Desktop
downloads_csv = r"C:\Users\Antonio\Downloads\Snovio_Gasolineras_Lanzamiento.csv"
desktop_csv = r"C:\Users\Antonio\Desktop\Snovio_Gasolineras_Lanzamiento.csv"

shutil.copyfile(out_csv, downloads_csv)
shutil.copyfile(out_csv, desktop_csv)

print(f"Total leads limpios listos para Snov.io: {len(df_clean)}")
print(f"Guardado en: {downloads_csv}")
