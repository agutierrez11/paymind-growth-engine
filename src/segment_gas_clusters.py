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
    comp = str(row.get('Compania', 'su empresa')).strip()
    
    if 'Cluster 1' in cluster:
        return (
            f"Hola {nombre},\n\n"
            f"Para macro-grupos como {comp}, cambiar de adquirente bancario no es opción por las tasas corporativas acordadas con BBVA, BanBajío o Afirme. "
            f"El reto real es la pesadilla contable de conciliar miles de depósitos diarios frente a los cortes de caja de las estaciones.\n\n"
            f"En PayMind actuamos como el middleware técnico (mismo modelo que operamos con Grupo ORSAN):\n"
            f"1. Ruteo Puro: Mantienes tus contratos bancarios y tasas corporativas preferenciales.\n"
            f"2. Hardware Certificado: Terminales Nexgo SmartPOS PCI 6.x y especificación ATEX (antichispas) para isla de carga.\n"
            f"3. Conciliación Automatizada: Inyectamos el corte de caja en tiempo real directo a tu ERP (SAP, Dyngas o ControlGAS).\n\n"
            f"¿Tendrás 10 minutos este jueves para revisar cómo automatizar la conciliación de {comp} sin cambiar de banco?\n\n"
            f"Saludos,\nAntonio Gutiérrez | PayMind"
        )
    elif 'Cluster 2' in cluster:
        return (
            f"Hola {nombre},\n\n"
            f"Sabemos que en {comp} operan con su software volumétrico (ControlGAS, CG-MEX o Nexus Fuel) y no buscan complicaciones operativas ni cambiar de banco. "
            f"Sin embargo, las fugas por errores de dedo de despachadores y el retraso de vales siguen afectando la liquidez.\n\n"
            f"Con PayMind te conectas a tu sistema actual sin intrusividad:\n"
            f"1. Conexión a la bomba: La terminal solo cobra el monto exacto del dispensario (cero errores ante el SAT).\n"
            f"2. Unificación de Vales: Recibes tarjetas y vales (Edenred, Sodexo, SiVale) en 1 sola terminal con depósito T+1 para comprar pipas.\n"
            f"3. Respaldo de escala: Tecnología validada en estaciones de Grupo ORSAN (Mobil).\n\n"
            f"¿Platicamos 10 minutos este jueves sobre cómo agilizar el cobro en {comp} sin cambiar de proveedor?\n\n"
            f"Saludos,\nAntonio Gutiérrez | PayMind"
        )
    else:
        return (
            f"Hola {nombre},\n\n"
            f"Para estaciones independientes como {comp}, los bancos tradicionales suelen cobrar comisiones elevadas y entregar terminales fijas viejas que no se hablan con las bombas, obligando al despachador a teclear a mano.\n\n"
            f"En PayMind te ofrecemos la solución 'llave en mano':\n"
            f"1. SmartPOS Inalámbrica Nexgo: Terminal portátil con certificación antichispas (ATEX) y mejores tasas adquirentes.\n"
            f"2. Terminal Bloqueada a la Bomba: Solo cobra el monto despachado, eliminando pérdidas por errores de tu personal.\n"
            f"3. Depósito al día siguiente (T+1) en tarjetas bancarias y todos los vales (Edenred, Sodexo, SiVale).\n\n"
            f"¿Te interesaría ver una demo de 10 minutos para equipar tus bombas?\n\n"
            f"Saludos,\nAntonio Gutiérrez | PayMind"
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
    'Asunto_Paso1': df['Cluster'].apply(lambda c: 'Consolidación de conciliación y ruteo multibanco' if 'Cluster 1' in c else ('Agilizar cobro en bombas sin cambiar de sistema' if 'Cluster 2' in c else 'Equipa tus bombas con terminales inalámbricas T+1')),
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
