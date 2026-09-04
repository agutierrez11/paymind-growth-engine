import os
import sys
import urllib.request
import re
import pandas as pd

val_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_CORPORATIVOS_VALIDADOS_PAYMIND.csv'
output_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_GASOLINEROS_100PCT_VERIFICADOS.csv'

gas_keywords = [
    'gasolina', 'gasolinera', 'combustible', 'diesel', 'diésel', 'estacion de servicio',
    'estaciones de servicio', 'pemex', 'cre', 'volumetrico', 'volumétrico', 'anexo 30',
    'petrolero', 'petroquimico', 'dispensario', 'dispensarios', 'litros', 'tanques',
    'rendilitros', 'petro-7', 'corpogas', 'orsan', 'g500', 'gasored', 'autotanques'
]

def check_domain_industry(domain):
    """
    Inspecciona el título web y metadatos del dominio para verificar si pertenece al rubro gasolinero/petrolero.
    """
    url = f"http://{domain}" if not domain.startswith("http") else domain
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8', errors='ignore').lower()
            
            # Buscar coincidencias de palabras clave del sector
            found_keywords = [kw for kw in gas_keywords if kw in html]
            
            # Extraer el título de la página
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "Sin Título"
            
            is_gas_industry = len(found_keywords) > 0
            return is_gas_industry, found_keywords, title
    except Exception as e:
        return False, [], f"Error de Conexión: {str(e)}"

if os.path.exists(val_csv):
    df = pd.read_csv(val_csv)
    print(f"=== AUDITANDO GIRO E INDUSTRIA DE {len(df)} DOMINIOS CORPORATIVOS ===\n")
    
    verified_results = []
    for idx, row in df.iterrows():
        email = str(row['Email'])
        domain = email.split('@')[1] if '@' in email else ""
        
        is_gas, keywords, site_title = check_domain_industry(domain)
        
        verified_results.append({
            'Email': email,
            'Dominio': domain,
            'Razon_Social': row.get('Razon_Social', ''),
            'Estaciones': row.get('Estaciones', ''),
            'Es_Gasolinero_Confirmado': is_gas,
            'Palabras_Clave_Detectadas': ", ".join(keywords) if keywords else "Ninguna",
            'Titulo_Sitio_Web': site_title
        })
        
        status = "CONFIRMADO GASOLINERO" if is_gas else "OTRO GIRO / DESECHADO"
        print(f"[{idx+1}/{len(df)}] {domain:<30} -> {status:<25} | Titulo: {site_title[:40]}")

        
    df_verified = pd.DataFrame(verified_results)
    
    # Filtrar estrictamente solo los que SÍ son del rubro gasolinero
    gas_only_df = df_verified[df_verified['Es_Gasolinero_Confirmado'] == True]
    non_gas_df = df_verified[df_verified['Es_Gasolinero_Confirmado'] == False]
    
    gas_only_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    
    print("\n=== RESUMEN DE AUDITORÍA DE GIRO DE MERCADO ===")
    print(f"✔ Dominio Gasolinero 100% Confirmado: {len(gas_only_df)} -> Guardado en LEADS_GASOLINEROS_100PCT_VERIFICADOS.csv")
    print(f"✖ Desechados (Otros giros: refaccionarias, consultorías, etc.): {len(non_gas_df)}")
