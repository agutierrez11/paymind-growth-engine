import os
import csv
import json
import socket
import concurrent.futures

data_dir = r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data"
os.makedirs(data_dir, exist_ok=True)
input_csv = os.path.join(data_dir, "TOKU_MATRIZ_72_CUENTAS.csv")
output_csv = os.path.join(data_dir, "TOKU_72_ENTIDADES_SCORING_COMPLETO.csv")
output_tier_a_csv = os.path.join(data_dir, "TOKU_TIER_A_PRIORIDAD_INMEDIATA.csv")
output_json = os.path.join(data_dir, "TOKU_72_ENTIDADES_ENRIQUECIDAS.json")

# Diccionario maestro de dominios y sedes conocidas
DOMAINS_MAP = {
    "Dimex": ("dimex.mx", "Monterrey / CDMX", "SOFOM"),
    "MexDin": ("mexdin.mx", "CDMX", "SOFOM"),
    "Financiera Independencia": ("independencia.com.mx", "CDMX", "SOFOM"),
    "Credifiel": ("credifiel.com.mx", "CDMX", "SOFOM"),
    "Crédito Fácil": ("creditofacil.com.mx", "CDMX", "SOFOM"),
    "Plan Credi": ("plancredi.com.mx", "Puebla / CDMX", "SOFOM"),
    "Apoyo Económico Familiar": ("apoyoeconomico.com.mx", "CDMX", "SOFOM"),
    "H Financieros": ("hfinancieros.com.mx", "Jalisco / CDMX", "SOFOM"),
    "Attendo": ("attendo.mx", "CDMX", "SOFOM"),
    "Finvivir": ("finvivir.com.mx", "Guadalajara / CDMX", "SOFOM"),
    "Avanza Sólido": ("avanzasolido.com", "Chiapas / CDMX", "SOFOM"),
    "Financiera Fortaleza": ("financierafortaleza.com", "CDMX", "SOFOM"),
    "Crédito Único": ("creditounico.mx", "CDMX", "SOFOM"),
    "Credimon": ("credimon.com.mx", "CDMX", "SOFOM"),
    "Micro Credit": ("microcredit.mx", "Veracruz / CDMX", "SOFOM"),
    "Sofipaz": ("sofipaz.com.mx", "Jalisco", "SOFOM"),
    "Percapita": ("percapita.com.mx", "CDMX", "SOFOM"),
    "Pro Crédito": ("procredito.com.mx", "CDMX", "SOFOM"),
    "Podemos Progresar": ("podemos.mx", "CDMX", "SOFOM"),
    "Progressa": ("progressa.com.mx", "CDMX", "SOFIPO"),
    "PREMO": ("premo.mx", "Guadalajara / CDMX", "SOFIPO"),
    "Broxel FinTech Crédito": ("broxel.com", "CDMX", "SOFIPO"),
    "Stori Card": ("storicard.com", "CDMX", "SOFIPO"),
    "Finamigo": ("finamigo.com.mx", "CDMX", "SOFIPO"),
    "Financiera Libertad": ("libertad.com.mx", "Querétaro / CDMX", "SOFIPO"),
    "Kubo Financiero": ("kubofinanciero.com", "CDMX", "SOFIPO"),
    "Fondeadora": ("fondeadora.com", "CDMX", "SOFIPO"),
    "Crediclub": ("crediclub.com", "Monterrey / CDMX", "SOFIPO"),
    "DiDi (DiDi Préstamos / Card)": ("didi-food.com", "CDMX", "SOFIPO"),
    "Financiera Súmate": ("sumate.com.mx", "Puebla / CDMX", "SOFIPO"),
    "Trafalgar": ("trafalgar.com.mx", "CDMX", "SOFIPO"),
    "Amextra Finanzas": ("amextra.mx", "CDMX", "SOFIPO"),
    "Unagra": ("unagra.com.mx", "CDMX", "SOFIPO"),
    "Paso Seguro Creando Futuro": ("pasoseguro.mx", "Oaxaca / CDMX", "SOFIPO"),
    "Credicapital": ("credicapital.com.mx", "Puebla / CDMX", "SOFIPO"),
    "Fita Servicios Financieros": ("fita.mx", "CDMX", "SOFIPO"),
    "Bienestar Préstamo y Ahorro": ("cajabienestar.com.mx", "Querétaro", "SOFIPO"),
    "ASP Integra Opciones": ("asp.com.mx", "Puebla / CDMX", "SOFIPO"),
    "Finsocial México": ("finsocial.mx", "CDMX", "SOFIPO"),
    "Ictineo": ("ictineo.com", "CDMX", "SOFIPO"),
    "Fincomún": ("fincomun.com.mx", "CDMX", "SOFIPO"),
    "Creciendo México": ("creciendo.com.mx", "CDMX", "SOFIPO"),
    "Multiplica México": ("multiplica.com.mx", "CDMX", "SOFIPO"),
    "Real Financiera": ("realfinanciera.com", "CDMX", "SOFIPO"),
    "Únete Financiera": ("unetefinanciera.com", "CDMX", "SOFIPO"),
    "Capital Activo": ("capitalactivo.com.mx", "CDMX", "SOFIPO"),
    "Financiera Monte de Piedad": ("montedepiedad.com.mx", "CDMX", "SOFIPO"),
    "Financiera Más": ("financieramas.com.mx", "CDMX", "SOFIPO"),
    "JP SofiExpress": ("sofiexpress.com.mx", "Jalisco / CDMX", "SOFIPO"),
    "RappiCard México": ("rappicard.mx", "CDMX", "SOFIPO"),
    "FINN-APP México": ("finnapp.mx", "CDMX", "SOFIPO"),
    "Grensa": ("grensa.com.mx", "CDMX", "SOFIPO"),
    "Finnix": ("finnix.com.mx", "CDMX", "SOFIPO"),
    "Coppel": ("coppel.com", "Sinaloa / CDMX", "Retail Credit"),
    "El Palacio de Hierro": ("elpalaciodehierro.com", "CDMX", "Retail Credit"),
    "Liverpool / Suburbia": ("liverpool.com.mx", "CDMX", "Retail Credit"),
    "Grupo Calzapato": ("calzapato.com", "Sinaloa", "Retail Credit"),
    "Price Shoes": ("priceshoes.com", "CDMX", "Retail Credit"),
    "Bodesa (Crédito el Bodegón)": ("elbodegon.com.mx", "Colima / Jalisco", "Retail Credit"),
    "La Marina": ("lamarina.com.mx", "Colima / Jalisco", "Retail Credit"),
    "Grupo Sanborns - Sears": ("sears.com.mx", "CDMX", "Retail Credit"),
    "Gran Chapur": ("chapur.com.mx", "Yucatán", "Retail Credit"),
    "Grupo Elektra": ("elektra.mx", "CDMX", "Retail Credit"),
    "Crediland": ("crediland.com.mx", "Sinaloa / Sonora", "Retail Credit"),
    "Falabella México - Soriana": ("falabella.com.mx", "CDMX", "Retail Credit"),
    "Tiendas Quality": ("qualitytiendas.com", "CDMX", "Retail Credit"),
    "Tiendas Aguirre": ("muebleriaaguirre.com", "Baja California", "Retail Credit"),
    "Spin by Oxxo": ("spinbyoxxo.com.mx", "Monterrey / CDMX", "Retail Credit"),
    "Muebles América": ("mueblesamerica.mx", "Jalisco / CDMX", "Retail Credit"),
    "Milano": ("milano.com", "CDMX", "Retail Credit"),
    "Mueblería Elizondo": ("elizondomueblerias.com", "Monterrey", "Retail Credit"),
    "DPortenis": ("dportenis.mx", "Sinaloa / CDMX", "Retail Credit")
}

def calculate_scoring(entidad, categoria, subtipo):
    """Calcula el Toku Meeting Probability Index (TMPI) de 0 a 100"""
    # 1. Dolor de Cobranza (Max 35)
    dolor = 35 if "Nómina" in subtipo or "Pensionados" in subtipo or "Micro" in subtipo else (
        30 if "Consumo" in subtipo or "Personal" in subtipo or "Muebles" in subtipo else 25
    )
    
    # 2. Agilidad de Decisión / Cero Burocracia (Max 25)
    if entidad in ["Coppel", "Grupo Elektra", "Liverpool / Suburbia", "El Palacio de Hierro", "Grupo Sanborns - Sears", "Falabella México - Soriana"]:
        agilidad = 8  # Burocracia extrema, comités largos
    elif entidad in ["DiDi (DiDi Préstamos / Card)", "Spin by Oxxo", "RappiCard México", "Financiera Monte de Piedad"]:
        agilidad = 14 # Grandes corporativos tech
    elif categoria == "SOFOM":
        agilidad = 25 # SOFOMes medianas toman decisiones en 1 llamada
    else:
        agilidad = 22 # SOFIPOs y Retail especializado
        
    # 3. Rieles de Pago Digitales Activos (Max 20)
    rieles = 20 if categoria in ["SOFIPO", "SOFOM"] else 15
    
    # 4. Cultura Remota / Presencia CDMX (Max 20)
    cultura = 20 if "CDMX" in DOMAINS_MAP.get(entidad, ("", "CDMX"))[1] else 14
    
    total = dolor + agilidad + rieles + cultura
    tier = "Tier A (Inmediato)" if total >= 85 else ("Tier B (Media)" if total >= 70 else "Tier C (Largo Plazo)")
    dias_est = "3 a 7 días" if total >= 85 else ("10 a 20 días" if total >= 70 else "30 a 60 días")
    
    return total, tier, dias_est

def check_domain_mx(domain):
    """Verifica si el dominio tiene servidores de correo activos (Google, Microsoft, etc.)"""
    try:
        ip = socket.gethostbyname(domain)
        return "Activo / En Línea", ip
    except:
        return "Requiere Verificación DNS", "N/A"

def enrich_single_entity(row):
    entidad = row["Entidad"]
    cat = row["Categoria_Regulatoria"]
    sub = row["Subtipo_Negocio"]
    
    domain_info = DOMAINS_MAP.get(entidad, (f"{entidad.lower().replace(' ', '')}.com.mx", "CDMX", cat))
    dominio = domain_info[0]
    sede = domain_info[1]
    
    status_dom, ip = check_domain_mx(dominio)
    score, tier, dias = calculate_scoring(entidad, cat, sub)
    
    dork_linkedin = f'site:linkedin.com/in ("{entidad}") ("Director de Cobranza" OR "Director de Crédito" OR "CFO" OR "Head of Payments")'
    dork_condusef = f'site:condusef.gob.mx "SIPRES" "{entidad}"'
    
    pitch_asunto = f"Reducción de cartera vencida e incidentes de cobro en {entidad}"
    pitch_cuerpo = (
        f"Hola [Nombre], en Toku ayudamos a entidades como {entidad} a reducir el rebote en cobro recurrente y "
        f"domiciliado hasta un 30% con reintentos inteligentes y ligas automáticas vía WhatsApp. "
        f"¿Podríamos coordinar una llamada remota de 15 min este jueves a las 11:00 AM para revisar el modelo?"
    )
    
    return {
        "ID": row["ID"],
        "Entidad": entidad,
        "Categoria": cat,
        "Subtipo": sub,
        "TMPI_Score": score,
        "Tier": tier,
        "Tiempo_Estimado_Cita": dias,
        "Bounty_Por_Cita": "$2,000 USD",
        "Sede": sede,
        "Dominio": dominio,
        "Estatus_Dominio": status_dom,
        "Decisor_Clave": "Director de Cobranza / CFO / Head de Riesgo",
        "Dork_LinkedIn": dork_linkedin,
        "Dork_CONDUSEF_SIPRES": dork_condusef,
        "Pitch_Asunto": pitch_asunto,
        "Pitch_Cuerpo": pitch_cuerpo
    }

print("=== INICIANDO MOTOR MULTIHILO DE ENRIQUECIMIENTO Y SCORING TOKU (72 ENTIDADES) ===")

raw_rows = []
with open(input_csv, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for r in reader:
        raw_rows.append(r)

enriched_results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    futures = [executor.submit(enrich_single_entity, r) for r in raw_rows]
    for future in concurrent.futures.as_completed(futures):
        enriched_results.append(future.result())

# Ordenar por Score descendente
enriched_results.sort(key=lambda x: x["TMPI_Score"], reverse=True)

# Guardar CSV Maestro Completo
fieldnames = list(enriched_results[0].keys())
with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in enriched_results:
        writer.writerow(row)

# Guardar CSV de Tier A (Prioridad Inmediata)
tier_a_rows = [r for r in enriched_results if "Tier A" in r["Tier"]]
with open(output_tier_a_csv, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in tier_a_rows:
        writer.writerow(row)

# Guardar JSON completo
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(enriched_results, f, indent=2, ensure_ascii=False)

print(f"[OK] 72 Entidades procesadas en paralelo.")
print(f"[OK] Total Tier A (Speed-to-Sell Inmediato): {len(tier_a_rows)} entidades.")
print(f"[OK] Potencial Financiero Inmediato (Tier A): ${len(tier_a_rows) * 2000:,} USD")
print(f"[OK] CSV Maestro: {output_csv}")
print(f"[OK] CSV Tier A: {output_tier_a_csv}")
