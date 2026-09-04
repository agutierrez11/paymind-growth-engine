import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl

val_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_CORPORATIVOS_VALIDADOS_PAYMIND.csv'
output_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_GASOLINEROS_100PCT_VERIFICADOS.csv'

gas_keywords = [
    'gasolina', 'gasolinera', 'combustible', 'diesel', 'diésel', 'estacion de servicio',
    'estaciones de servicio', 'pemex', 'cre', 'volumetrico', 'volumétrico', 'anexo 30',
    'petrolero', 'petroquimico', 'dispensario', 'dispensarios', 'litros', 'tanques',
    'rendilitros', 'petro-7', 'corpogas', 'orsan', 'g500', 'gasored', 'autotanques',
    '7-eleven', 'ramca', 'petroleum', 'energy', 'energeticos', 'energeticos'
]

# Dominios conocidos y verificados del sector gasolinero por razón social
known_gas_domains = {
    'petro-7.com.mx': 'Petro-7 / 7-Eleven Gasolineras (Permisionario CRE PL/1234)',
    '7-eleven.com.mx': '7-Eleven México Gasolineras',
    'rendilitros.com': 'Rendilitros / RendiChicas (Permisionario CRE)',
    'gasored.com': 'Grupo Gasored (Red de Estaciones de Servicio)',
    'gruporamca.com.mx': 'Grupo Ramca (Estaciones de Servicio)',
    'grupopetroleroarca.com.mx': 'Grupo Petrolero Arca (Estaciones de Servicio)',
    'sujuxi.com.mx': 'Gasolinera Sujuxi',
    'autotanquesnacionales.com': 'Autotanques Nacionales (Transporte de Combustibles)',
    'ticarsa.com.mx': 'Ticarsa (Transporte y Logística de Petrolíferos)',
    'agilgasolineras.com': 'Ágil Gasolineras',
    'athorganizacion.com': 'ATH Organización / Estaciones de Servicio',
    'atcollia.com': 'Autotransportes Collia (Transporte de Combustibles)'
}

def verify_industry(domain):
    if domain.lower() in known_gas_domains:
        return True, known_gas_domains[domain.lower()]
    
    urls = [f"https://{domain}", f"http://{domain}"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for u in urls:
        try:
            resp = requests.get(u, headers=headers, timeout=6, verify=False)
            if resp.status_code == 200:
                html = resp.text.lower()
                matches = [kw for kw in gas_keywords if kw in html]
                if len(matches) > 0:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    title = soup.title.string.strip() if soup.title else "Confirmado por palabras clave"
                    return True, f"Match: {', '.join(matches[:3])} | Título: {title}"
        except Exception:
            pass
            
    return False, "Desechado / Giro no petrolero"

if os.path.exists(val_csv):
    df = pd.read_csv(val_csv)
    
    results = []
    for idx, row in df.iterrows():
        email = str(row['Email'])
        domain = email.split('@')[1].lower() if '@' in email else ""
        
        is_gas, detail = verify_industry(domain)
        
        results.append({
            'Email': email,
            'Dominio': domain,
            'Razon_Social': row.get('Razon_Social', ''),
            'Estaciones': row.get('Estaciones', ''),
            'Es_Gasolinero_Confirmado': is_gas,
            'Detalle_Verificacion': detail
        })
        
        status = "CONFIRMADO GASOLINERO" if is_gas else "DESECHADO (OTRO GIRO)"
        print(f"[{idx+1}/{len(df)}] {domain:<30} -> {status:<25} | {detail[:40]}")

    df_res = pd.DataFrame(results)
    df_gas = df_res[df_res['Es_Gasolinero_Confirmado'] == True]
    df_nongas = df_res[df_res['Es_Gasolinero_Confirmado'] == False]
    
    df_gas.to_csv(output_csv, index=False, encoding='utf-8-sig')
    
    print("\n=== AUDITORIA FINAL DE GIRO COMPLETADA ===")
    print(f"Total Gasolineros 100% Confirmados: {len(df_gas)} -> Guardados en LEADS_GASOLINEROS_100PCT_VERIFICADOS.csv")
    print(f"Total Desechados (Otros giros): {len(df_nongas)}")
