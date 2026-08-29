import os
import pandas as pd

base_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine"
csv_in = os.path.join(base_dir, "data", "Campana_PayMind_Gasolineras_400.csv")

# Leer CSV con soporte utf-8-sig / latin1
try:
    df = pd.read_csv(csv_in, encoding='utf-8-sig')
except:
    df = pd.read_csv(csv_in, encoding='latin1')

comp_col = [c for c in df.columns if 'Compañía' in c or 'Compania' in c or 'Empresa' in c][0]
df.rename(columns={comp_col: 'Compania'}, inplace=True)

macro_keywords = ['ORSAN', 'OXXO', 'PETRO-7', 'PETRO 7', 'HIDROSINA', 'G500', 'CORPOGAS', 'ENERSER', 'SERVIFACIL', 'VALERO', 'BP', 'MOBIL', 'SHELL', 'REPSOL', 'PEMEX', 'REDCO']
mid_keywords = ['OCTANO', 'NEXUM', 'RENDICHIKAS', 'RENDICHICAS', 'LA GAS', 'LAGAS', 'GASOL', 'ENERGETICO', 'GRUPO', 'CADENA', 'DISTRIBUIDORA', 'GASOLINERA', 'ESTACION', 'COMBUSTIBLE', 'SERVICE', 'PETROLEO', 'FUELS', 'OIL', 'RODELI', 'INPESMAR']

def classify_cluster(row):
    comp = str(row.get('Compania', '')).upper()
    email = str(row.get('Email', '')).upper()
    
    # Check Macro Keywords
    for k in macro_keywords:
        if k in comp or k in email:
            return 'Cluster 1: Macro-Grupo Corporativo (Top Tier)'
            
    # Check Mid Keywords
    for k in mid_keywords:
        if k in comp or k in email:
            return 'Cluster 2: Grupo Regional Consolidado (Mid Market)'
            
    return 'Cluster 3: Estacion Independiente / PYME (Long Tail)'

def assign_gtm_strategy(cluster):
    if 'Cluster 1' in cluster:
        return 'Estrategia ABM: Pasarela / Middleware Ruteo Puro + Conciliación ERP (Conserva tu banco)'
    elif 'Cluster 2' in cluster:
        return 'Integración a tu ERP/Volumétrico actual + Antifraude + Vales T+1'
    else:
        return 'Modelo Agregador: Adquirencia Directa PayMind + Terminal Nexgo ATEX Llave en Mano'

def assign_email_pitch_step1(row, cluster):
    nombre = str(row.get('Nombre', 'Director')).strip()
    comp = str(row.get('Compania', 'su estación')).strip()
    if nombre.lower() in ['director', 'propietario', 'gerente', 'nan', '']:
        saludo = "Hola,"
    else:
        saludo = f"Hola {nombre},"
    
    if 'Cluster 1' in cluster:
        return (
            f"{saludo}\n\n"
            f"Voy conociendo cómo operan la cobranza corporativa distintos grupos gasolineros, y cada uno tiene retos distintos.\n\n"
            f"En el caso de {comp}, ¿hoy la conciliación de los cobros con tarjeta contra los cierres del volumétrico se procesa automáticamente hacia su ERP o todavía requiere revisión manual por estación?\n\n"
            f"Si tiene 5 minutos esta semana, me gustaría entender cómo lo resuelven ustedes — no vengo con un pitch armado, vengo a escuchar su proceso primero.\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
    elif 'Cluster 2' in cluster:
        return (
            f"{saludo}\n\n"
            f"Una pregunta directa sobre la operación en sus estaciones: ¿hoy el despachador cobra con una terminal que jala el monto directo del volumétrico (ControlGAS, eGas, NexusFuel), o todavía se teclea manualmente lo que marca la bomba?\n\n"
            f"Pregunto porque varía mucho estación por estación y me interesa entender su caso real antes de plantear si hay algo que valga la pena platicar.\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
    else:
        return (
            f"{saludo}\n\n"
            f"Le escribo con una duda puntual sobre su estación: ¿cómo se reparte hoy el cobro entre efectivo y tarjeta? Y de la parte con tarjeta, ¿se cobra al pie del auto o el cliente tiene que pasar a caja?\n\n"
            f"No asumo que buscan cambiar nada — solo quiero entender cómo opera su isla antes de saber si hace sentido platicar.\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )

df['Cluster'] = df.apply(classify_cluster, axis=1)
df['Estrategia_GTM'] = df['Cluster'].apply(assign_gtm_strategy)
df['Pitch_Paso1_Personalizado'] = df.apply(lambda r: assign_email_pitch_step1(r, r['Cluster']), axis=1)

# Guardar CSV de Snovio listo con Clusters
snovio_df = pd.DataFrame({
    'Email': df['Email'],
    'Nombre': df['Nombre'],
    'Empresa': df['Compania'],
    'Cluster': df['Cluster'],
    'Estrategia_GTM': df['Estrategia_GTM'],
    'Asunto_Paso1': df['Cluster'].apply(lambda c: 'Conciliación de cobro en pista' if 'Cluster 1' in c else ('Cómo cobran hoy en la isla' if 'Cluster 2' in c else 'Mezcla de pago en su estación')),
    'Cuerpo_Paso1': df['Pitch_Paso1_Personalizado']
})

out_csv = os.path.join(base_dir, "data", "Snovio_Gasolineras_Segmentada_Clusters.csv")
snovio_df.to_csv(out_csv, index=False, encoding="utf-8-sig")

# Generar Playbook de Clusters
md_content = """# 🗺️ Playbook de Segmentación GTM por Clusters: PayMind Gasolineras

> **Estrategia:** Clasificación de la base de 433 contactos en 3 baldes de prospección hiper-personalizados para maximizar la tasa de conversión en outbound y ABM.

---

## 🏢 Cluster 1: Los Macro-Grupos Corporativos (Top Tier)
* **Quiénes son:** Grupos de +50 estaciones (Oxxo Gas, Petro-7, Hidrosina, Grupo ORSAN, G500, CorpoGAS, Enerser, Servifácil, Valero).
* **Perfil Técnico:** Servidores propios, directores de TI dedicados, ControlGAS / Alvic Enterprise, macro-ERPs (SAP Business One, Dyngas / Dynamics 365).
* **Estrategia PayMind:** **ABM Middleware / Ruteo Puro** *(Conserva sus afiliaciones de BBVA, BanBajío, Afirme) + Conciliación ERP en tiempo real + Validador Grupo ORSAN*.

---

## 🗺️ Cluster 2: Los Grupos Regionales Consolidados (Mid Market)
* **Quiénes son:** Cadenas de 10 a 50 estaciones (Grupo Octano, Nexum, Redco, Rendichicas, La Gas).
* **Perfil Técnico:** ControlGAS, CG-MEX, Volutrak, Nexus Fuel, Intelisis Gasolineras, EFT ERP.
* **Estrategia PayMind:** **Integración a su Proveedor Actual + Solución Antifraude en Bomba + Unificación de Vales T+1**.

---

## ⛽ Cluster 3: Los Independientes / "Hombre-Estación" (Long Tail / PYME)
* **Quiénes son:** Dueños o familias con 1 a 5 estaciones (Franquicias Pemex o independientes).
* **Perfil Técnico:** Volumétricos económicos (Verifuel, Smartgas), SaaS ligero (getcastores.mx + TicketFact), software contable (Aspel COI).
* **Estrategia PayMind:** **Modelo Agregador (Adquirencia Directa PayMind) Llave en Mano** *con SmartPOS Nexgo ATEX antichispas, mejor tasa y terminal bloqueada a la bomba*.

---

## 👥 Conteo de Contactos en Base de Datos (433 Total)

"""

cluster_counts = df['Cluster'].value_counts()
for c_name, count in cluster_counts.items():
    md_content += f"* **{c_name}:** `{count} Contactos` ({round(count/len(df)*100, 1)}%)\n"

md_path = os.path.join(base_dir, "playbooks", "segmentacion_clusters_gtm_gasolineras.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Segmentación completada exitosamente.")
print(cluster_counts)
