import json
import os
import csv

data_dir = r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data"
csv_path = os.path.join(data_dir, "TOKU_MATRIZ_72_CUENTAS.csv")

# Perfiles de dolor y propuesta de valor de Toku según figura regulatoria
PLAYBOOKS_TOKU = {
    "SOFOM": {
        "Dolor_Principal": "Tasa de rechazo en cobro domiciliado de nómina/pensiones (hasta 25% de rebote por saldo insuficiente o cuenta bloqueada).",
        "Propuesta_Toku": "Motor de reintentos inteligentes de domiciliación bancaria y cobro por WhatsApp automatizado con enlace de pago para recuperar cartera en mora temprana sin costo de gestor telefónico.",
        "Apertura_Email": "Hola [Nombre], te contacto porque en Toku ayudamos a financieras de nómina y crédito personal a reducir la tasa de rechazo de domiciliación bancaria hasta en un 30% usando reintentos predictivos. ¿Tienes 10 minutos este jueves para ver cómo se integraría a su core?",
        "Decisor_Ideal": "Director de Cobranza y Recuperación / Director de Riesgo"
    },
    "SOFIPO": {
        "Dolor_Principal": "Costo elevado de procesamiento de abonos y fricción en domiciliación SPEI recurrente para préstamos y ahorro programado.",
        "Propuesta_Toku": "API nativa de recaudación recurrente multi-riel (SPEI, Domiciliación y Tarjeta) con conciliación contable automática en tiempo real.",
        "Apertura_Email": "Hola [Nombre], veo que en [Entidad] manejan alto volumen de colocación digital. En Toku conectamos directamente con el core financiero para automatizar la recaudación recurrente multi-riel y bajar el churn involuntario. ¿Te parecería revisar un caso de uso similar esta semana?",
        "Decisor_Ideal": "CFO / Head de Pagos y Operaciones"
    },
    "Retail Credit": {
        "Dolor_Principal": "Abonos semanales o quincenales en efectivo que dependen de que el cliente vaya a la tienda física; alta mora cuando el cliente no asiste.",
        "Propuesta_Toku": "Cobro digital omnicanal recurrente domiciliado a tarjeta de débito o nómina con recordatorios automatizados antes de la fecha de corte del abono.",
        "Apertura_Email": "Hola [Nombre], te escribo porque trabajamos con grandes cadenas de crédito al consumo ayudándoles a mover hasta el 40% de sus cobros en tienda a domiciliación digital automática sin perder clientes. ¿Podríamos coordinar una llamada de 15 minutos con tu equipo de crédito?",
        "Decisor_Ideal": "Director de Crédito y Cobranza / Director de Finanzas"
    }
}

# 10 Entidades de Ataque Rápido para Agendar Inmediatamente
TOP_10_RAPIDOS = [
    {"Entidad": "Dimex", "Dominio": "dimex.mx", "Categoria": "SOFOM", "Ubicacion": "Monterrey / CDMX"},
    {"Entidad": "Fincomún", "Dominio": "fincomun.com.mx", "Categoria": "SOFIPO", "Ubicacion": "CDMX"},
    {"Entidad": "Credifiel", "Dominio": "credifiel.com.mx", "Categoria": "SOFOM", "Ubicacion": "CDMX"},
    {"Entidad": "Finvivir", "Dominio": "finvivir.com.mx", "Categoria": "SOFOM", "Ubicacion": "Guadalajara / CDMX"},
    {"Entidad": "Kubo Financiero", "Dominio": "kubofinanciero.com", "Categoria": "SOFIPO", "Ubicacion": "CDMX"},
    {"Entidad": "Broxel FinTech Crédito", "Dominio": "broxel.com", "Categoria": "SOFIPO", "Ubicacion": "CDMX"},
    {"Entidad": "Fondeadora", "Dominio": "fondeadora.com", "Categoria": "SOFIPO", "Ubicacion": "CDMX"},
    {"Entidad": "Avanza Sólido", "Dominio": "avanzasolido.com", "Categoria": "SOFOM", "Ubicacion": "Chiapas / CDMX"},
    {"Entidad": "Bodesa (Crédito el Bodegón)", "Dominio": "elbodegon.com.mx", "Categoria": "Retail Credit", "Ubicacion": "Colima / Jalisco"},
    {"Entidad": "Crediland", "Dominio": "crediland.com.mx", "Categoria": "Retail Credit", "Ubicacion": "Sinaloa / Sonora"}
]

print("=== GENERADOR DE PROSPECCIÓN QUIRÚRGICA PARA TOKU ($2,000 USD / CITA) ===")
dossiers = []
for item in TOP_10_RAPIDOS:
    cat = item["Categoria"]
    playbook = PLAYBOOKS_TOKU[cat]
    dossier = {
        "Entidad": item["Entidad"],
        "Dominio": item["Dominio"],
        "Categoria": cat,
        "Sede": item["Ubicacion"],
        "Bounty": "$2,000 USD",
        "Decisor_A_Cazar": playbook["Decisor_Ideal"],
        "Google_LinkedIn_Dork": f'site:linkedin.com/in ("{item["Entidad"]}") ("Director de Cobranza" OR "Director de Crédito" OR "Director de Finanzas" OR "CFO" OR "Head of Payments")',
        "Dolor_Operativo": playbook["Dolor_Principal"],
        "Gancho_Toku": playbook["Propuesta_Toku"],
        "Plantilla_Outreach": playbook["Apertura_Email"].replace("[Entidad]", item["Entidad"])
    }
    dossiers.append(dossier)

out_json = os.path.join(data_dir, "TOKU_TOP_10_ATAQUE_RAPIDO.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(dossiers, f, indent=2, ensure_ascii=False)

print(f"Top 10 generado exitosamente en: {out_json}")
print("Potencial de este lote de 10 citas: $20,000 USD (~$380,000 - $400,000 MXN)")
