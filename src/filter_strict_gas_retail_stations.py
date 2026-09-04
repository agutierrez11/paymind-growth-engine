import os
import pandas as pd

in_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_GASOLINEROS_100PCT_VERIFICADOS.csv'
out_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_CADENAS_GASOLINERAS_QUIOSCOS_PAYMIND.csv'

# Lista de exclusión estricta de transporte / logística / pipas
transport_keywords = [
    'autotanques', 'fletera', 'transporte', 'autotransportes', 'tanques', 
    'flete', 'pipas', 'logistica', 'logística', 'rodeli', 'collía', 'collia', 
    'ticarsa', 'flgaal', 'transbaga', 'salave', 'reco'
]

if os.path.exists(in_csv):
    df = pd.read_csv(in_csv)
    
    clean_retail_leads = []
    excluded_leads = []
    
    for idx, row in df.iterrows():
        email = str(row['Email']).lower()
        domain = str(row['Dominio']).lower()
        detail = str(row['Detalle_Verificacion']).lower()
        razon = str(row['Razon_Social']).lower()
        
        full_text = f"{email} {domain} {detail} {razon}"
        
        is_transport = any(kw in full_text for kw in transport_keywords)
        
        if is_transport:
            excluded_leads.append(row)
        else:
            clean_retail_leads.append(row)
            
    df_retail = pd.DataFrame(clean_retail_leads)
    df_excluded = pd.DataFrame(excluded_leads)
    
    df_retail.to_csv(out_csv, index=False, encoding='utf-8-sig')
    
    print("=== FILTRADO STRICT RETAIL GAS STATIONS (QUIOSCOS & AUTOCOBRO) ===")
    print(f"CONFIRMADO - Cadenas de Gasolineras Retail 100% Calificadas: {len(df_retail)} -> Guardados en LEADS_CADENAS_GASOLINERAS_QUIOSCOS_PAYMIND.csv")
    print(f"DESECHADOS (Autotransportes/Logistica/Pipas): {len(df_excluded)}")
    print("\nDETALLE DE OBJETIVOS RETAIL CONFIRMADOS:")
    for idx, r in df_retail.iterrows():
        print(f" - [{r['Email']}] -> Dominio: {r['Dominio']} | {r['Detalle_Verificacion']}")

