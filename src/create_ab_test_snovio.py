import os
import pandas as pd

base_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine"
data_dir = os.path.join(base_dir, "data")
csv_in = os.path.join(data_dir, "Campana_PayMind_Gasolineras_400.csv")

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
    
    for k in macro_keywords:
        if k in comp or k in email:
            return 'Cluster 1: Macro-Grupo Corporativo (Top Tier)'
            
    for k in mid_keywords:
        if k in comp or k in email:
            return 'Cluster 2: Grupo Regional Consolidado (Mid Market)'
            
    return 'Cluster 3: Estacion Independiente / PYME (Long Tail)'

df['Cluster'] = df.apply(classify_cluster, axis=1)

# Asignar A/B split estratificado 50/50 por Cluster (Grupo A: Usted, Grupo B: Tú)
df = df.sort_values(by=['Cluster', 'Email']).reset_index(drop=True)
df['Variante_AB'] = df.groupby('Cluster').cumcount().apply(lambda x: 'Grupo A (Usted)' if x % 2 == 0 else 'Grupo B (Tu)')

def build_sequence(row):
    comp = str(row.get('Compania', 'su estación')).strip()
    variante = row['Variante_AB']
    is_usted = ('Usted' in variante)
    
    if is_usted:
        paso1_asunto = "Cómo cobran hoy en la estación"
        paso1_cuerpo = (
            f"Buen día,\n\n"
            f"Le escribo a {comp} sin saber si usted lleva el tema de cobro en pista — si no es así, le agradezco me oriente con quien sí.\n\n"
            f"Estoy tratando de entender cómo se resuelve el cobro con tarjeta en la posición: ¿el operador lleva la terminal al vehículo, el cliente pasa a caja, o manejan otro esquema?\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        paso2_asunto = "Una pregunta sobre el cobro con tarjeta"
        paso2_cuerpo = (
            f"Buen día,\n\n"
            f"Una duda breve sobre {comp}: cuando llegan varios vehículos al mismo tiempo, ¿cómo organizan el pago con tarjeta?\n\n"
            f"Me interesa entender la operación real, no asumir que una terminal adicional sería útil.\n\n"
            f"¿Es un reto para ustedes o normalmente lo resuelven sin problema?\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        paso3_asunto = "¿Qué parte del cobro les cuesta más?"
        paso3_cuerpo = (
            f"Buen día,\n\n"
            f"Estoy aprendiendo sobre la operación de estaciones y agradecería una respuesta honesta: si pudiera cambiar una sola cosa del cobro en pista, ¿qué sería?\n\n"
            f"Puede ser la espera, la señal, las cancelaciones, la conciliación, el efectivo o ninguna de las anteriores.\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        paso4_asunto = "¿Tiene sentido seguir con esta conversación?"
        paso4_cuerpo = (
            f"Buen día,\n\n"
            f"Si el cobro actual funciona bien en {comp}, no quiero hacerle perder tiempo. Sólo quería confirmar si vale la pena investigar una alternativa de cobro en la posición.\n\n"
            f"Si usted no es la persona indicada, ¿me podría orientar con quien sí?\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        paso5_asunto = "Cierro el hilo"
        paso5_cuerpo = (
            f"Buen día,\n\n"
            f"Cierro el hilo para no insistir. Gracias de todos modos por leerme. Si en algún momento gusta compartir cómo resolvieron el cobro en {comp}, me dará gusto aprender.\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
    else:
        paso1_asunto = "Cómo cobran hoy en la estación"
        paso1_cuerpo = (
            f"Buen día,\n\n"
            f"Te escribo a {comp} sin saber si tú llevas el tema de cobro en pista — si no es así, te agradezco me orientes con quien sí.\n\n"
            f"Estoy tratando de entender cómo se resuelve el cobro con tarjeta en la posición: ¿el operador lleva la terminal al vehículo, el cliente pasa a caja, o manejan otro esquema?\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        paso2_asunto = "Una pregunta sobre el cobro con tarjeta"
        paso2_cuerpo = (
            f"Buen día,\n\n"
            f"Una duda breve sobre {comp}: cuando llegan varios vehículos al mismo tiempo, ¿cómo organizan el pago con tarjeta?\n\n"
            f"Me interesa entender la operación real, no asumir que una terminal adicional sería útil.\n\n"
            f"¿Es un reto para ustedes o normalmente lo resuelven sin problema?\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        paso3_asunto = "¿Qué parte del cobro les cuesta más?"
        paso3_cuerpo = (
            f"Buen día,\n\n"
            f"Estoy aprendiendo sobre la operación de estaciones y agradecería una respuesta honesta: si pudieras cambiar una sola cosa del cobro en pista, ¿qué sería?\n\n"
            f"Puede ser la espera, la señal, las cancelaciones, la conciliación, el efectivo o ninguna de las anteriores.\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        paso4_asunto = "¿Tiene sentido seguir con esta conversación?"
        paso4_cuerpo = (
            f"Buen día,\n\n"
            f"Si el cobro actual funciona bien en {comp}, no quiero hacerte perder tiempo. Sólo quería confirmar si vale la pena investigar una alternativa de cobro en la posición.\n\n"
            f"Si tú no eres la persona indicada, ¿me podrías orientar con quien sí?\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        paso5_asunto = "Cierro el hilo"
        paso5_cuerpo = (
            f"Buen día,\n\n"
            f"Cierro el hilo para no insistir. Gracias de todos modos por leerme. Si en algún momento quieres compartir cómo resolvieron el cobro en {comp}, me dará gusto aprender.\n\n"
            f"Saludos,\nAntonio Gutiérrez\nantonio.gutierrez@paymind.mx"
        )
        
    return pd.Series([
        paso1_asunto, paso1_cuerpo,
        paso2_asunto, paso2_cuerpo,
        paso3_asunto, paso3_cuerpo,
        paso4_asunto, paso4_cuerpo,
        paso5_asunto, paso5_cuerpo
    ])

seq_cols = [
    'Paso1_Asunto', 'Paso1_Cuerpo',
    'Paso2_Asunto', 'Paso2_Cuerpo',
    'Paso3_Asunto', 'Paso3_Cuerpo',
    'Paso4_Asunto', 'Paso4_Cuerpo',
    'Paso5_Asunto', 'Paso5_Cuerpo'
]

df[seq_cols] = df.apply(build_sequence, axis=1)

# Guardar CSV final optimizado para Snovio A/B Test
snovio_df = pd.DataFrame({
    'Email': df['Email'],
    'Empresa': df['Compania'],
    'Cluster': df['Cluster'],
    'Variante_AB': df['Variante_AB'],
    'Paso1_Asunto': df['Paso1_Asunto'],
    'Paso1_Cuerpo': df['Paso1_Cuerpo'],
    'Paso2_Asunto': df['Paso2_Asunto'],
    'Paso2_Cuerpo': df['Paso2_Cuerpo'],
    'Paso3_Asunto': df['Paso3_Asunto'],
    'Paso3_Cuerpo': df['Paso3_Cuerpo'],
    'Paso4_Asunto': df['Paso4_Asunto'],
    'Paso4_Cuerpo': df['Paso4_Cuerpo'],
    'Paso5_Asunto': df['Paso5_Asunto'],
    'Paso5_Cuerpo': df['Paso5_Cuerpo']
})

out_csv = os.path.join(data_dir, "Snovio_Gasolineras_Lanzamiento.csv")
snovio_df.to_csv(out_csv, index=False, encoding="utf-8-sig")

# Copiar a carpetas del escritorio
desktop_dirs = [
    r"C:\Users\Antonio\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Escritorio\Paymind Strategy"
]

for d in desktop_dirs:
    if os.path.exists(d):
        dst = os.path.join(d, "Snovio_Gasolineras_Lanzamiento.csv")
        snovio_df.to_csv(dst, index=False, encoding="utf-8-sig")
        print(f"[OK] Sincronizado A/B Test Impersonal a: {dst}")

print("\n--- RESUMEN DEL SPLIT ESTRATIFICADO A/B TEST ---")
print(pd.crosstab(snovio_df['Cluster'], snovio_df['Variante_AB']))
