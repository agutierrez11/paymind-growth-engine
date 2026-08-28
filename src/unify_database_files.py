import os
import shutil
import pandas as pd

base_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine"
data_dir = os.path.join(base_dir, "data")
desktop_dirs = [
    r"C:\Users\Antonio\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Escritorio\Paymind Strategy"
]

# Leer el CSV maestro segmentado de Snov.io
csv_snovio_path = os.path.join(data_dir, "Snovio_Gasolineras_Segmentada_Clusters.csv")
df_snovio = pd.read_csv(csv_snovio_path, encoding='utf-8-sig')

# Leer directorio ONEXPO
onexpo_path = os.path.join(data_dir, "directorio_asociaciones_onexpo_mexico.csv")
df_onexpo = pd.read_csv(onexpo_path, encoding='utf-8-sig') if os.path.exists(onexpo_path) else pd.DataFrame()

# Crear el Excel Unificado Maestro con Pestañas claras
master_excel_path = os.path.join(data_dir, "BASE_MAESTRA_GASOLINERAS_PAYMIND.xlsx")
with pd.ExcelWriter(master_excel_path, engine='openpyxl') as writer:
    df_snovio.to_excel(writer, sheet_name='Base_433_Gasolineras', index=False)
    if not df_onexpo.empty:
        df_onexpo.to_excel(writer, sheet_name='Asociaciones_ONEXPO_32_Estados', index=False)

# Crear el CSV ÚNICO para Snov.io llamado Snovio_Gasolineras_Lanzamiento.csv
single_csv_path = os.path.join(data_dir, "Snovio_Gasolineras_Lanzamiento.csv")
df_snovio.to_csv(single_csv_path, index=False, encoding='utf-8-sig')

# Limpiar carpetas del escritorio eliminando archivos duplicados viejos
old_files_to_remove = [
    "Campana_PayMind_MultiSegmento_CPS.xlsx",
    "Campana_PayMind_Gasolineras_400.xlsx",
    "Snovio_Gasolineras_Segmentada_Clusters.csv",
    "directorio_asociaciones_onexpo_mexico.csv"
]

for d in desktop_dirs:
    if os.path.exists(d):
        # Borrar viejos duplicados
        for old in old_files_to_remove:
            old_p = os.path.join(d, old)
            if os.path.exists(old_p):
                try:
                    os.remove(old_p)
                    print(f"Eliminado duplicado viejo: {old_p}")
                except Exception as e:
                    print(f"Error borrando {old_p}: {e}")

        # Copiar los 2 únicos nuevos archivos unificados
        shutil.copy2(master_excel_path, os.path.join(d, "00_BASE_MAESTRA_GASOLINERAS_PAYMIND.xlsx"))
        shutil.copy2(single_csv_path, os.path.join(d, "Snovio_Gasolineras_Lanzamiento.csv"))
        print(f"[OK] Copiada Base Unificada a: {d}")

print("Unificación de archivos completada exitosamente.")
