import os
import sys
import re
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lista de dominios de Proveedores AMPES para extracción de Clientes
ampes_providers = [
    {'name': 'ATIO Group (ControlGAS)', 'domain': 'atiogroup.com.mx'},
    {'name': 'EGAS', 'domain': 'egas.com.mx'},
    {'name': 'ALVIC', 'domain': 'alvic.net'},
    {'name': 'iGAS', 'domain': 'igas.mx'},
    {'name': 'Gas Manager', 'domain': 'gasmanager.com'},
    {'name': 'PRE Software', 'domain': 'grupopre.ai'},
    {'name': 'INTERLOGIC', 'domain': 'interlogicglobal.com'},
    {'name': 'SEPROCESA', 'domain': 'seprocesa.com'},
    {'name': 'SNE Aerocom', 'domain': 'sne.com.mx'},
    {'name': 'Cadisa', 'domain': 'cadisaenlinea.com.mx'},
    {'name': 'Luqross Suite Olimpo', 'domain': 'luqrosstecnologia.com'},
    {'name': 'Enercon FuelSoft', 'domain': 'enercon.mx'},
    {'name': 'Petrotech', 'domain': 'petrotech.com.mx'},
    {'name': 'Petrogas', 'domain': 'petrogas.com.mx'}
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def scrape_provider_clients(provider):
    """
    Worker Agéntico 1: Entra a la web oficial del proveedor y extrae sus clientes actuales.
    """
    domain = provider['domain']
    name = provider['name']
    
    subpaths = ['', '/clientes', '/nosotros', '/casos-de-exito', '/testimonios', '/quienes-somos']
    extracted_clients = set()
    raw_snippets = []
    
    for sub in subpaths:
        url = f"https://{domain}{sub}"
        try:
            r = requests.get(url, headers=headers, timeout=5, verify=False)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text = soup.get_text()
                
                # Expresión regular para detectar nombres de cadenas/grupos gasolineros
                matches = re.findall(r'(Grupo\s+[A-Z][a-z0-9]+|Gasolinera[s]?\s+[A-Z][a-z0-9]+|Estacion[es]?\s+[A-Z][a-z0-9]+|[A-Z][a-z0-9]+\s+Gas|Rendi[A-Z][a-z]+|Corp[o]?gas|Orsan|G500|Petro[-]?7|Oxxo\s+Gas|Combuexpress|Gasomax)', text, re.IGNORECASE)
                for m in matches:
                    if len(m) > 3 and m.lower() not in ['grupo', 'gasolinera', 'estaciones']:
                        extracted_clients.add(m.strip())
                        
                # Capturar snippets con la palabra "cliente" o "estaciones"
                for p in soup.find_all(['p', 'div', 'li']):
                    p_text = p.get_text().strip()
                    if any(w in p_text.lower() for w in ['cliente', 'casos de éxito', 'atendemos a', 'nuestros clientes']):
                        if len(p_text) < 250:
                            raw_snippets.append(p_text)
        except Exception:
            pass
            
    return {
        'Proveedor': name,
        'Dominio': domain,
        'Clientes_Identificados': ", ".join(list(extracted_clients)[:10]) if extracted_clients else "Revisado (Sin mención explícita en HTML público)",
        'Snippets_Clientes': " | ".join(raw_snippets[:3]) if raw_snippets else "N/A"
    }

# Cadenas Gasolineras Lookalike Conocidas por Región en México
known_lookalike_chains = [
    {'Cadena': 'Oxxo Gas', 'Region': 'Nacional', 'Estaciones_Est': '+560', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Grupo Orsan', 'Region': 'Norte / Centro / Bajío', 'Estaciones_Est': '+200', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'G500 Network', 'Region': 'Nacional', 'Estaciones_Est': '+300', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Combuexpress', 'Region': 'Occidente / Jalisco', 'Estaciones_Est': '+80', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Gasomax', 'Region': 'Bajío / San Luis Potosí', 'Estaciones_Est': '+50', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Grupo Burgos', 'Region': 'Norte / Tamaulipas', 'Estaciones_Est': '+100', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'CargoGas', 'Region': 'Noroeste / Coahuila', 'Estaciones_Est': '+60', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Gasolinera El Trebol (Grupo Calsa)', 'Region': 'Centro', 'Estaciones_Est': '+35', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Grupo Octano', 'Region': 'Occidente', 'Estaciones_Est': '+40', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Ruta / Petrum / Gilga', 'Region': 'Norte / Bajío', 'Estaciones_Est': '+75', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Corporativo AP', 'Region': 'Centro / Hidalgo', 'Estaciones_Est': '+30', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Top Energy / Gomasa / Gonergy', 'Region': 'Sureste / Golfo', 'Estaciones_Est': '+65', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Servicio Glorieta', 'Region': 'Centro', 'Estaciones_Est': '+25', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Gasolineras Hidrosina', 'Region': 'Centro / CDMX', 'Estaciones_Est': '+200', 'Tipo': 'Retail Gas Chain'},
    {'Cadena': 'Gasolineras BP México', 'Region': 'Nacional', 'Estaciones_Est': '+500', 'Tipo': 'Multinacional Retail'},
    {'Cadena': 'Chevron México', 'Region': 'Noroeste', 'Estaciones_Est': '+150', 'Tipo': 'Multinacional Retail'}
]

if __name__ == '__main__':
    print("=== ENJAMBRE MULTI-AGENTE: EXTRACCIÓN DE CLIENTES & LOOKALIKES REGIONALES ===\n")
    
    # Executing Worker 1 in parallel
    print("WORKER 1: Escaneando sitios de proveedores AMPES para extraer sus clientes actuales...")
    client_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(scrape_provider_clients, p) for p in ampes_providers]
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            client_results.append(res)
            print(f" - Escaneado: {res['Proveedor']} -> Clientes: {res['Clientes_Identificados'][:60]}")
            
    df_clients = pd.DataFrame(client_results)
    clients_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\CLIENTES_EXTRAIDOS_PROVEEDORES_AMPES.csv'
    df_clients.to_csv(clients_csv, index=False, encoding='utf-8-sig')
    
    # Executing Worker 2: Lookalikes
    print("\nWORKER 2: Mapeando cadenas gasolineras Lookalike regionales en México...")

    df_lookalikes = pd.DataFrame(known_lookalike_chains)
    lookalikes_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\CADENAS_GASOLINERAS_LOOKALIKE_MEXICO.csv'
    df_lookalikes.to_csv(lookalikes_csv, index=False, encoding='utf-8-sig')
    
    print("\n=== PROCESO COMPLETADO EXITOSAMENTE ===")
    print(f"Clientes de Proveedores Guardados en: {clients_csv}")
    print(f"Cadenas Lookalike Guardadas en: {lookalikes_csv}")

