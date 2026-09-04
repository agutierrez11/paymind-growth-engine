import os
import sys
import pandas as pd

# Path to script
sys.path.append(r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\src')
from verify_emails_free import check_email_exists

master_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\Snovio_Gasolineras_Segmentada_Clusters.csv'
output_dir = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data'

if os.path.exists(master_csv):
    df = pd.read_csv(master_csv)
    print(f"Total de registros cargados: {len(df)}")
    
    # 1. Separar correos corporativos vs dominios públicos
    public_domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com', 'live.com', 'icloud.com', 'prodigy.net.mx']
    
    def is_corporate(email):
        if pd.isna(email) or '@' not in str(email):
            return False
        dom = str(email).split('@')[1].lower()
        return dom not in public_domains

    df['es_corporativo'] = df['Email'].apply(is_corporate)
    
    corp_df = df[df['es_corporativo']].copy()
    public_df = df[~df['es_corporativo']].copy()
    
    print(f"• Correos Corporativos (Prioridad #1): {len(corp_df)}")
    print(f"• Correos Públicos (Gmail/Hotmail/Yahoo): {len(public_df)}")
    
    # 2. Validar correos corporativos uno por uno con verify_emails_free
    print("\n=== VERIFICANDO VALIDEZ DE CORREOS CORPORATIVOS CON DNS/SMTP ===")
    results = []
    for idx, row in corp_df.iterrows():
        email = row['Email']
        valid, reason = check_email_exists(email)
        results.append({
            'Email': email,
            'Valido': valid,
            'Motivo': reason,
            'Razon_Social': row.get('Razon_Social', ''),
            'Estaciones': row.get('Estaciones', ''),
            'Contacto': row.get('Contacto', ''),
            'Puesto': row.get('Puesto', ''),
            'Telefono': row.get('Telefono', '')
        })
        print(f"[{idx+1}/{len(corp_df)}] {email:<35} -> Valido: {valid} ({reason})")
        
    df_results = pd.DataFrame(results)
    
    # Filtrar solo corporativos 100% válidos
    valid_corp_df = df_results[df_results['Valido'] == True]
    invalid_corp_df = df_results[df_results['Valido'] == False]
    
    # Guardar resultados
    valid_csv_path = os.path.join(output_dir, 'LEADS_CORPORATIVOS_VALIDADOS_PAYMIND.csv')
    public_csv_path = os.path.join(output_dir, 'LEADS_PUBLICOS_GMAIL_HOTMAIL.csv')
    
    valid_corp_df.to_csv(valid_csv_path, index=False, encoding='utf-8-sig')
    public_df.to_csv(public_csv_path, index=False, encoding='utf-8-sig')
    
    print("\n=== RESUMEN DE PROCESAMIENTO ===")
    print(f"✔ Corporativos Válidos Listos para Campaña: {len(valid_corp_df)} -> Guardados en LEADS_CORPORATIVOS_VALIDADOS_PAYMIND.csv")
    print(f"✖ Corporativos Inexistentes/Descartados: {len(invalid_corp_df)}")
    print(f"📁 Correos Públicos en Reserva: {len(public_df)} -> Guardados en LEADS_PUBLICOS_GMAIL_HOTMAIL.csv")

else:
    print(f"Archivo no encontrado en: {master_csv}")
