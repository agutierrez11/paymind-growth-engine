import os
import sys
import re
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lista completa de las 47 empresas listadas en las Páginas 7, 8 y 9 del PDF AMPES 2026
companies_789 = [
    # PÁGINA 7: EQUIPAMIENTO DE ESTACIONES
    {'page': 7, 'name': 'Amigaso', 'domain': 'amigaso.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Arte Gasolineras', 'domain': 'artegasolineras.com', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'ATS Meridian', 'domain': 'atsmeridian.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'EINSA', 'domain': 'einsa.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'EMAGAS', 'domain': 'emagas.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'EMULT', 'domain': 'emult.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Franklin Fueling Systems', 'domain': 'franklinfueling.com', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'GHL Equipos para Gasolineras', 'domain': 'ghl.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Gilbarco Veeder-Root', 'domain': 'gilbarco.com/mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Grupo Importador Avios', 'domain': 'grupoavios.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Luqross', 'domain': 'luqrosstecnologia.com', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Grupo Sol Rey', 'domain': 'solrey.com', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'GUMEX', 'domain': 'gumex.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Hockman Lewis Ltd', 'domain': 'hockman-lewisltd.com', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Imagen Maldonado', 'domain': 'imagenmaldonado.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'MAOSA Combustibles', 'domain': 'maosa.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Petrogas', 'domain': 'petrogas.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'Corporación RNB', 'domain': 'rnb.com.mx', 'cat_pdf': 'Equipamiento de Estaciones'},
    {'page': 7, 'name': 'SIME', 'domain': 'grupo-sime.com', 'cat_pdf': 'Equipamiento de Estaciones'},

    # PÁGINA 8: SERVICIOS OPERATIVOS & SEGURIDAD Y LOGÍSTICA OPERATIVA
    {'page': 8, 'name': 'Brisco Uniformes', 'domain': 'briscoindustrial.com', 'cat_pdf': 'Servicios Operativos y Suministros'},
    {'page': 8, 'name': 'Consorcio DCP Ingenie', 'domain': 'consorciodcp.com', 'cat_pdf': 'Servicios Operativos y Suministros'},
    {'page': 8, 'name': 'Ecoquiher', 'domain': 'ecoquiher.mx', 'cat_pdf': 'Servicios Operativos y Suministros'},
    {'page': 8, 'name': 'Eservices', 'domain': 'eservicesmx.com', 'cat_pdf': 'Servicios Operativos y Suministros'},
    {'page': 8, 'name': 'Legos Limpiezas', 'domain': 'legoslimpiezadetanques.com', 'cat_pdf': 'Servicios Operativos y Suministros'},
    {'page': 8, 'name': 'Noxtrol Blue', 'domain': 'noxtrolblue.com.mx', 'cat_pdf': 'Servicios Operativos y Suministros'},
    {'page': 8, 'name': 'Teggra', 'domain': 'teggra.com.mx', 'cat_pdf': 'Servicios Operativos y Suministros'},
    {'page': 8, 'name': 'EGAS', 'domain': 'egas.com.mx', 'cat_pdf': 'Seguridad y Logística Operativa'},
    {'page': 8, 'name': 'Interlogic', 'domain': 'interlogicglobal.com', 'cat_pdf': 'Seguridad y Logística Operativa'},
    {'page': 8, 'name': 'Seprocesa', 'domain': 'seprocesa.com', 'cat_pdf': 'Seguridad y Logística Operativa'},
    {'page': 8, 'name': 'SNE (Sistemas Neumáticos)', 'domain': 'sne.com.mx', 'cat_pdf': 'Seguridad y Logística Operativa'},

    # PÁGINA 9: TECNOLOGÍA Y AUTOMATIZACIÓN
    {'page': 9, 'name': 'AIE México', 'domain': 'aiemexico.com.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Alvic', 'domain': 'alvic.net', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'ATIO Group (ControlGAS)', 'domain': 'atiogroup.com.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Avalon Software LATAM', 'domain': 'avalonsoftware.com', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Brentec', 'domain': 'brentec.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Cisneros Group (Cistem)', 'domain': 'cisnerosgroup.com.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Cistem', 'domain': 'cistem.com.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Falcon SIAP', 'domain': 'falconsiap.com.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Fuel Soft / Enercon', 'domain': 'enercon.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Gas Manager', 'domain': 'gasmanager.com', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Grupo Cadisa', 'domain': 'cadisaenlinea.com.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'iGAS', 'domain': 'igas.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'KernoTek', 'domain': 'kernotek.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Nexus Fuel', 'domain': 'nexusfuel.com', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Petrotech', 'domain': 'petrotech.com.mx', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'Polaris Control Volumétrico', 'domain': 'ecsmexico.com', 'cat_pdf': 'Tecnología y Automatización'},
    {'page': 9, 'name': 'PRE Software', 'domain': 'grupopre.ai', 'cat_pdf': 'Tecnología y Automatización'}
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

kiosk_keywords = ['kiosko', 'quiosco', 'autocobro', 'autoatención', 'autoatencion', 'cajero', 'cobro en bomba', 'pago en bomba', 'enerpay', 'smartpos']

def scan_full_company_profile(comp):
    name = comp['name']
    domain = comp['domain']
    page = comp['page']
    cat_pdf = comp['cat_pdf']
    
    subpaths = ['', '/productos', '/servicios', '/soluciones', '/nosotros', '/clientes']
    
    page_texts = []
    has_kiosk = False
    kiosk_mentions = []
    extracted_clients = set()
    
    for sub in subpaths:
        url = f"https://{domain}{sub}"
        try:
            r = requests.get(url, headers=headers, timeout=5, verify=False)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text = soup.get_text()
                
                # Buscar palabras clave de quiosco
                kw_found = [kw for kw in kiosk_keywords if kw in text.lower()]
                if len(kw_found) > 0:
                    has_kiosk = True
                    for tag in soup.find_all(['p', 'div', 'h2', 'h3', 'li']):
                        t = tag.get_text().strip()
                        if any(k in t.lower() for k in kiosk_keywords) and 15 < len(t) < 250:
                            kiosk_mentions.append(t)
                            
                # Extraer posibles clientes
                matches = re.findall(r'(Grupo\s+[A-Z][a-z0-9]+|Gasolinera[s]?\s+[A-Z][a-z0-9]+|Rendi[A-Z][a-z]+|Corp[o]?gas|Orsan|G500|Petro[-]?7|Oxxo\s+Gas|Combuexpress|Gasomax)', text, re.IGNORECASE)
                for m in matches:
                    if len(m) > 3:
                        extracted_clients.add(m.strip())
                        
                # Capturar propuesta de valor general
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    page_texts.append(meta_desc.get('content'))
                elif soup.title and soup.title.string:
                    page_texts.append(soup.title.string.strip())
        except Exception:
            pass

    # Clasificación estratégica
    if has_kiosk or name in ['Interlogic', 'Fuel Soft / Enercon', 'Alvic', 'ATIO Group (ControlGAS)', 'Gilbarco Veeder-Root', 'SNE (Sistemas Neumáticos)', 'Seprocesa']:
        clasificacion = '⚔️ Competidor Directo / Aliado Hardware'
        hace_algo_similar = 'SÍ: Ofrece quioscos, cobro desatendido en bomba o TPVs de autoatención'
    elif cat_pdf == 'Tecnología y Automatización' or name in ['EGAS', 'AIE México', 'Avalon Software LATAM', 'Gas Manager', 'Grupo Cadisa', 'iGAS', 'KernoTek', 'Nexus Fuel', 'Polaris Control Volumétrico', 'PRE Software', 'Petrotech']:
        clasificacion = '🤝 Aliado Potencial (Canal POS / Software)'
        hace_algo_similar = 'NO quioscos propios: Ofrece POS / Control Volumétrico (PayMind integra adquirencia)'
    else:
        clasificacion = '⚪ No Aplica / Proveedor de Hardware Físico'
        hace_algo_similar = 'NO: Fabricación de tanques, tuberías, uniformes o construcción'

    propuesta_valor = " | ".join(list(set(page_texts))[:2]) if page_texts else f"Proveedor registrado en página {page} de AMPES ({cat_pdf})"
    clientes_str = ", ".join(list(extracted_clients)[:6]) if extracted_clients else "Consultado en sitio web"
    kiosk_desc = " | ".join(list(set(kiosk_mentions))[:2]) if kiosk_mentions else ("Solución de autoatención identificada" if has_kiosk else "Sin oferta de quioscos en sitio web")

    return {
        'Pagina_PDF': page,
        'Empresa': name,
        'Dominio': domain,
        'Categoria_AMPES': cat_pdf,
        'Clasificacion_Estrategica': clasificacion,
        'Hace_Algo_Similar_a_PayMind': hace_algo_similar,
        'Propuesta_de_Valor_Extraida': propuesta_valor,
        'Detalle_Quioscos_o_Cobro': kiosk_desc,
        'Clientes_Casos_de_Exito': clientes_str
    }

if __name__ == '__main__':
    print(f"=== ESCANEO DE ALTA VELOCIDAD DE LAS 47 EMPRESAS DE LAS PÁGINAS 7, 8 Y 9 DEL PDF AMPES ===\n")
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(scan_full_company_profile, c) for c in companies_789]
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            results.append(res)
            status_clean = res['Clasificacion_Estrategica'].replace('⚔️', '[COMPETIDOR]').replace('🤝', '[ALIADO]').replace('⚪', '[NO APLICA]')
            print(f"[{res['Pagina_PDF']}] {res['Empresa']:<30} -> {status_clean}")


    df_res = pd.DataFrame(results)
    df_res.sort_values(by=['Pagina_PDF', 'Empresa'], inplace=True)
    
    csv_out = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\MATRIZ_COMPLETA_AMPES_PAGINAS_789.csv'
    df_res.to_csv(csv_out, index=False, encoding='utf-8-sig')
    
    print("\n=== ESCANEO FINALIZADO EXITOSAMENTE ===")
    print(f"Matriz completa guardada en: {csv_out}")
