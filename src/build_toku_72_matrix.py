import csv
import os

data_dir = r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data"
os.makedirs(data_dir, exist_ok=True)
output_csv = os.path.join(data_dir, "TOKU_MATRIZ_72_CUENTAS.csv")

# 72 Cuentas exactas extraídas del PDF confidencial de Toku 2026
entities = [
    # 01 SOFOM (19 entidades)
    {"id": 1, "entidad": "Dimex", "categoria": "SOFOM", "subtipo": "Crédito de Nómina y Pensionados", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 2, "entidad": "MexDin", "categoria": "SOFOM", "subtipo": "Préstamos Personales", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 3, "entidad": "Financiera Independencia", "categoria": "SOFOM", "subtipo": "Crédito al Consumo Masivo", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 4, "entidad": "Credifiel", "categoria": "SOFOM", "subtipo": "Crédito Gubernamental y Nómina", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 5, "entidad": "Crédito Fácil", "categoria": "SOFOM", "subtipo": "Préstamos Personales", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 6, "entidad": "Plan Credi", "categoria": "SOFOM", "subtipo": "Financiamiento", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 7, "entidad": "Apoyo Económico Familiar", "categoria": "SOFOM", "subtipo": "Préstamos Grupales e Individuales", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 8, "entidad": "H Financieros", "categoria": "SOFOM", "subtipo": "Financiamiento Corporativo/Pyme", "prioridad": "Media", "dificultad": "Media"},
    {"id": 9, "entidad": "Attendo", "categoria": "SOFOM", "subtipo": "Crédito de Nómina", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 10, "entidad": "Finvivir", "categoria": "SOFOM", "subtipo": "Microcréditos Populares", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 11, "entidad": "Avanza Sólido", "categoria": "SOFOM", "subtipo": "Microfinanzas Rural/Urbano", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 12, "entidad": "Financiera Fortaleza", "categoria": "SOFOM", "subtipo": "Crédito de Nómina", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 13, "entidad": "Crédito Único", "categoria": "SOFOM", "subtipo": "Préstamos Personales", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 14, "entidad": "Credimon", "categoria": "SOFOM", "subtipo": "Crédito y Liquidez", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 15, "entidad": "Micro Credit", "categoria": "SOFOM", "subtipo": "Microcréditos", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 16, "entidad": "Sofipaz", "categoria": "SOFOM", "subtipo": "Crédito Popular", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 17, "entidad": "Percapita", "categoria": "SOFOM", "subtipo": "Financiamiento", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 18, "entidad": "Pro Crédito", "categoria": "SOFOM", "subtipo": "Crédito Pyme y Consumo", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 19, "entidad": "Podemos Progresar", "categoria": "SOFOM", "subtipo": "Crédito Grupal Mujeres", "prioridad": "Alta", "dificultad": "Media"},

    # 02 SOFIPOS (34 entidades)
    {"id": 20, "entidad": "Progressa", "categoria": "SOFIPO", "subtipo": "Ahorro y Crédito Popular", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 21, "entidad": "PREMO", "categoria": "SOFIPO", "subtipo": "Crédito Pyme FinTech", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 22, "entidad": "Broxel FinTech Crédito", "categoria": "SOFIPO", "subtipo": "Medios de Pago y Crédito", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 23, "entidad": "Stori Card", "categoria": "SOFIPO", "subtipo": "Tarjetas de Crédito / Ahorro", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 24, "entidad": "Finamigo", "categoria": "SOFIPO", "subtipo": "Microfinanzas", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 25, "entidad": "Financiera Libertad", "categoria": "SOFIPO", "subtipo": "Servicios Financieros Masivos", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 26, "entidad": "Kubo Financiero", "categoria": "SOFIPO", "subtipo": "Crédito e Inversión Digital", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 27, "entidad": "Fondeadora", "categoria": "SOFIPO", "subtipo": "Neobanco / Cuenta Débito y Crédito", "prioridad": "Estratégica", "dificultad": "Media"},
    {"id": 28, "entidad": "Crediclub", "categoria": "SOFIPO", "subtipo": "Ahorro y Microcréditos", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 29, "entidad": "DiDi (DiDi Préstamos / Card)", "categoria": "SOFIPO", "subtipo": "FinTech Crédito al Consumo", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 30, "entidad": "Financiera Súmate", "categoria": "SOFIPO", "subtipo": "Microcrédito Productivo", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 31, "entidad": "Trafalgar", "categoria": "SOFIPO", "subtipo": "FinTech / Wallets", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 32, "entidad": "Amextra Finanzas", "categoria": "SOFIPO", "subtipo": "Microcréditos Solidarios", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 33, "entidad": "Unagra", "categoria": "SOFIPO", "subtipo": "Financiamiento Agropecuario", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 34, "entidad": "Paso Seguro Creando Futuro", "categoria": "SOFIPO", "subtipo": "Ahorro y Préstamo", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 35, "entidad": "Credicapital", "categoria": "SOFIPO", "subtipo": "Crédito Pyme e Inversión", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 36, "entidad": "Fita Servicios Financieros", "categoria": "SOFIPO", "subtipo": "Crédito Regional", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 37, "entidad": "Bienestar Préstamo y Ahorro", "categoria": "SOFIPO", "subtipo": "Caja Popular Regional", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 38, "entidad": "ASP Integra Opciones", "categoria": "SOFIPO", "subtipo": "Crédito y Arrendamiento", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 39, "entidad": "Finsocial México", "categoria": "SOFIPO", "subtipo": "Crédito Social", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 40, "entidad": "Ictineo", "categoria": "SOFIPO", "subtipo": "FinTech / Cuentas de Ahorro", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 41, "entidad": "Fincomún", "categoria": "SOFIPO", "subtipo": "Servicios Financieros Populares", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 42, "entidad": "Creciendo México", "categoria": "SOFIPO", "subtipo": "Microfinanzas", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 43, "entidad": "Multiplica México", "categoria": "SOFIPO", "subtipo": "Crédito Productivo", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 44, "entidad": "Real Financiera", "categoria": "SOFIPO", "subtipo": "Crédito de Nómina y Pyme", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 45, "entidad": "Únete Financiera", "categoria": "SOFIPO", "subtipo": "Préstamos Personales", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 46, "entidad": "Capital Activo", "categoria": "SOFIPO", "subtipo": "Financiamiento Empresarial", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 47, "entidad": "Financiera Monte de Piedad", "categoria": "SOFIPO", "subtipo": "Crédito Prendario y Personal", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 48, "entidad": "Financiera Más", "categoria": "SOFIPO", "subtipo": "Microcréditos", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 49, "entidad": "JP SofiExpress", "categoria": "SOFIPO", "subtipo": "Crédito al Consumo", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 50, "entidad": "RappiCard México", "categoria": "SOFIPO", "subtipo": "Tarjeta de Crédito FinTech", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 51, "entidad": "FINN-APP México", "categoria": "SOFIPO", "subtipo": "Crédito Digital App", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 52, "entidad": "Grensa", "categoria": "SOFIPO", "subtipo": "Financiera Regional", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 53, "entidad": "Finnix", "categoria": "SOFIPO", "subtipo": "FinTech / Crédito Ágil", "prioridad": "Alta", "dificultad": "Baja"},

    # 03 Tiendas departamentales y Retail Credit (19 entidades)
    {"id": 54, "entidad": "Coppel", "categoria": "Retail Credit", "subtipo": "Crédito Departamental / BanCoppel", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 55, "entidad": "El Palacio de Hierro", "categoria": "Retail Credit", "subtipo": "Tarjeta Departamental Luxury", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 56, "entidad": "Liverpool / Suburbia", "categoria": "Retail Credit", "subtipo": "Tarjeta Liverpool / Suburbia", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 57, "entidad": "Grupo Calzapato", "categoria": "Retail Credit", "subtipo": "Vales y Crédito Calzado", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 58, "entidad": "Price Shoes", "categoria": "Retail Credit", "subtipo": "Venta por Catálogo / Crédito", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 59, "entidad": "Bodesa (Crédito el Bodegón)", "categoria": "Retail Credit", "subtipo": "Muebles y Línea Blanca a Crédito", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 60, "entidad": "La Marina", "categoria": "Retail Credit", "subtipo": "Tiendas Departamentales Regionales", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 61, "entidad": "Grupo Sanborns - Sears", "categoria": "Retail Credit", "subtipo": "Tarjeta Sears / Crédito Slim", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 62, "entidad": "Gran Chapur", "categoria": "Retail Credit", "subtipo": "Tiendas Departamentales Yucatán", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 63, "entidad": "Grupo Elektra", "categoria": "Retail Credit", "subtipo": "Banco Azteca / Abonos Semanales", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 64, "entidad": "Crediland", "categoria": "Retail Credit", "subtipo": "Crédito en Muebles y Electrodomésticos", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 65, "entidad": "Falabella México - Soriana", "categoria": "Retail Credit", "subtipo": "Tarjeta Falabella Soriana", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 66, "entidad": "Tiendas Quality", "categoria": "Retail Credit", "subtipo": "Comercio y Crédito", "prioridad": "Media", "dificultad": "Baja"},
    {"id": 67, "entidad": "Tiendas Aguirre", "categoria": "Retail Credit", "subtipo": "Mueblerías y Crédito Directo", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 68, "entidad": "Spin by Oxxo", "categoria": "Retail Credit", "subtipo": "Wallet y Cuenta Digital Femsa", "prioridad": "Estratégica", "dificultad": "Alta"},
    {"id": 69, "entidad": "Muebles América", "categoria": "Retail Credit", "subtipo": "Crédito Muebles / Préstamos", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 70, "entidad": "Milano", "categoria": "Retail Credit", "subtipo": "Ropa y Crédito Masivo", "prioridad": "Alta", "dificultad": "Media"},
    {"id": 71, "entidad": "Mueblería Elizondo", "categoria": "Retail Credit", "subtipo": "Crédito Muebles y Línea Blanca", "prioridad": "Alta", "dificultad": "Baja"},
    {"id": 72, "entidad": "DPortenis", "categoria": "Retail Credit", "subtipo": "Vales DP / Crédito Calzado", "prioridad": "Alta", "dificultad": "Baja"}
]

fieldnames = [
    "ID", "Entidad", "Categoria_Regulatoria", "Subtipo_Negocio", 
    "Prioridad_Prospeccion", "Dificultad_Acceso", "Decisor_1_Cargo", 
    "Decisor_2_Cargo", "Decisor_3_Cargo", "Canal_Sugerido", "Bounty_USD", "Estatus"
]

with open(output_csv, mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for e in entities:
        writer.writerow({
            "ID": e["id"],
            "Entidad": e["entidad"],
            "Categoria_Regulatoria": e["categoria"],
            "Subtipo_Negocio": e["subtipo"],
            "Prioridad_Prospeccion": e["prioridad"],
            "Dificultad_Acceso": e["dificultad"],
            "Decisor_1_Cargo": "Director / Gerente de Cobranza y Recuperación",
            "Decisor_2_Cargo": "Director de Finanzas (CFO) / Tesorería",
            "Decisor_3_Cargo": "Director de Operaciones / Medios de Pago",
            "Canal_Sugerido": "LinkedIn InMail + Email Corporativo + WhatsApp",
            "Bounty_USD": "$2,000 USD",
            "Estatus": "Pendiente de Enriquecimiento"
        })

print(f"Matriz generada con éxito en: {output_csv}")
print(f"Total de entidades registradas: {len(entities)}")
