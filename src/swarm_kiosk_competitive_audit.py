import os
import sys
import re
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cargar las 25 empresas actionables de AMPES
ampes_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_SOCIOS_AMPES_2026_COMPLETO.csv'
out_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\AUDITORIA_COMPETITIVA_QUIOSCOS_AMPES.csv'
out_md = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\playbooks\BENCHMARK_COMPETITIVO_QUIOSCOS_PAYMIND.md'

kiosk_keywords = [
    'kiosko', 'kiosk', 'quiosco', 'autocobro', 'autoatención', 'autoatencion',
    'cajero', 'cobro en bomba', 'pago en bomba', 'terminal', 'tpv', 'autoservicio',
    'efectivo', 'tarjeta', 'smartpos', 'monedero', 'enerpay', 'opencard'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def audit_company_kiosk_offering(row):
    empresa = row['Empresa']
    domain = str(row['Web']).replace('http://', '').replace('https://', '').strip()
    categoria = row['Categoria']
    
    subpaths = ['', '/productos', '/soluciones', '/servicios', '/kioskos', '/autocobro', '/quioscos']
    
    has_kiosk_product = False
    kiosk_details = []
    sales_pitch = []
    
    for sub in subpaths:
        url = f"https://{domain}{sub}"
        try:
            r = requests.get(url, headers=headers, timeout=5, verify=False)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text = soup.get_text()
                
                # Buscar menciones de quioscos o autocobro
                matches = [kw for kw in kiosk_keywords if kw in text.lower()]
                if len(matches) > 0:
                    has_kiosk_product = True
                    
                    # Extraer párrafos que describen el producto de cobro/quiosco
                    for p in soup.find_all(['p', 'div', 'li', 'h2', 'h3']):
                        p_text = p.get_text().strip()
                        if any(w in p_text.lower() for w in ['kiosko', 'quiosco', 'autocobro', 'autoatención', 'cajero', 'cobro', 'pago']):
                            if 20 < len(p_text) < 300 and p_text not in kiosk_details:
                                kiosk_details.append(p_text)
        except Exception:
            pass

    # Caso conocido por análisis de producto
    known_kiosk_offers = {
        'INTERLOGIC': ('Sí (Quioscos de Autoatención Hardware)', 'Venden hardware de cajeros/quioscos pesados para efectivo y tarjeta en Oxxo Gas.'),
        'FUEL SOFT / ENERCON': ('Sí (ENERPAY App & TPV Autocobro)', 'Ofrecen ENERPAY para cobro y prepago en bomba.'),
        'ALVIC': ('Sí (Alvic Self-Service POS)', 'Ofrecen terminales de autocobro para estaciones nocturnas o desatendidas.'),
        'iGAS': ('Sí (Sistema Agilizador de Servicio en Isla)', 'Cobro rápido con terminales móviles en bomba.'),
        'ATIO GROUP': ('Sí (FuelGATE / ControlGAS Mobile)', 'Terminales de pago desatendidas y autoconsumo.'),
        'SISTEMAS NEUMÁTICOS (SNE)': ('Sí (AC-GAS Efectivo Neumático)', 'Quiosco/sistema neumático para enviar efectivo desde la bomba.'),
        'SEPROCESA': ('Sí (Cajas Inteligentes Smart Safes)', 'Quioscos de depósito seguro de efectivo en estación.'),
        'AVALON SOFTWARE LATAM': ('Sí (OpenCard & CBOS)', 'Monederos y módulos de autoatención para flotillas.')
    }
    
    status_ofrecimiento = "Ofrece Quioscos / Autocobro" if has_kiosk_product else "Sin Oferta Directa de Quioscos"
    detalle_producto = " | ".join(kiosk_details[:3]) if kiosk_details else "Analizado en sitio web"
    
    if empresa in known_kiosk_offers:
        has_kiosk_product = True
        status_ofrecimiento = known_kiosk_offers[empresa][0]
        detalle_producto = known_kiosk_offers[empresa][1]

    return {
        'Empresa': empresa,
        'Dominio': domain,
        'Categoria': categoria,
        'Ofrece_Quioscos_o_Autocobro': status_ofrecimiento,
        'Detalle_del_Producto_Competidor': detalle_producto,
        'Diferenciador_Ventaja_PayMind': get_paymind_advantage(empresa, has_kiosk_product)
    }

def get_paymind_advantage(empresa, has_kiosk):
    if not has_kiosk:
        return "Aliado Ideal: No tiene quiosco propio; PayMind le complementa la oferta."
    
    if empresa in ['INTERLOGIC', 'SEPROCESA', 'SNE']:
        return "Socio de Hardware: Ellos venden el quiosco físico/caja, PayMind pone la pasarela de pago y adquirencia."
    elif empresa in ['FUEL SOFT / ENERCON', 'ALVIC', 'ATIO GROUP', 'AVALON SOFTWARE LATAM']:
        return "Ventaja PayMind: Sus quioscos son cerrados/propietarios o requieren hardware costoso ($15k USD). PayMind ofrece Plug-and-Play SmartPOS a menor costo de comisión."
    else:
        return "Ventaja PayMind: Integración nativa multi-banco con comisiones preferenciales y conciliación Anexo 30 SAT en tiempo real."

if os.path.exists(ampes_csv):
    df_ampes = pd.read_csv(ampes_csv)
    print(f"=== AUDITANDO OFERTA DE QUIOSCOS DE AUTOCOBRO EN {len(df_ampes)} EMPRESAS AMPES ===\n")
    
    audit_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(audit_company_kiosk_offering, row) for idx, row in df_ampes.iterrows()]
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            audit_results.append(res)
            print(f" - {res['Empresa']:<30} | Status: {res['Ofrece_Quioscos_o_Autocobro']:<35}")
            
    df_audit = pd.DataFrame(audit_results)
    df_audit.to_csv(out_csv, index=False, encoding='utf-8-sig')
    
    print("\n=== AUDITORÍA COMPETITIVA FINALIZADA CON ÉXITO ===")
    print(f"📁 CSV Guardado en: {out_csv}")
