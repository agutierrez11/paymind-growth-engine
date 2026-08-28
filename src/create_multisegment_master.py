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

multi_excel_path = os.path.join(data_dir, "Campana_PayMind_MultiSegmento_CPS.xlsx")
snovio_gas_path = os.path.join(data_dir, "Snovio_Gasolineras_Segmentada_Clusters.csv")
onexpo_csv_path = os.path.join(data_dir, "directorio_asociaciones_onexpo_mexico.csv")

xl = pd.ExcelFile(multi_excel_path)

df_gas = pd.read_csv(snovio_gas_path, encoding='utf-8-sig') if os.path.exists(snovio_gas_path) else xl.parse('Gasolineras_433')
df_hoteles = xl.parse('Hoteles_Boutique_256') if 'Hoteles_Boutique_256' in xl.sheet_names else pd.DataFrame()
df_escuelas = xl.parse('Escuelas_Colegios') if 'Escuelas_Colegios' in xl.sheet_names else pd.DataFrame()
df_clinicas = xl.parse('Clinicas_Medicas') if 'Clinicas_Medicas' in xl.sheet_names else pd.DataFrame()
df_playbook = xl.parse('Playbook_CPS_Metodologia') if 'Playbook_CPS_Metodologia' in xl.sheet_names else pd.DataFrame()
df_onexpo = pd.read_csv(onexpo_csv_path, encoding='utf-8-sig') if os.path.exists(onexpo_csv_path) else pd.DataFrame()

# Crear el Excel Maestro Multisectorial Completo
master_multi_path = os.path.join(data_dir, "00_BASE_MAESTRA_PAYMIND_MULTISEGMENTO.xlsx")
with pd.ExcelWriter(master_multi_path, engine='openpyxl') as writer:
    df_gas.to_excel(writer, sheet_name='Gasolineras_433_Clusters', index=False)
    if not df_hoteles.empty:
        df_hoteles.to_excel(writer, sheet_name='Hoteles_Boutique_256', index=False)
    if not df_escuelas.empty:
        df_escuelas.to_excel(writer, sheet_name='Escuelas_Y_Colegios', index=False)
    if not df_clinicas.empty:
        df_clinicas.to_excel(writer, sheet_name='Clinicas_Medicas', index=False)
    if not df_onexpo.empty:
        df_onexpo.to_excel(writer, sheet_name='Asociaciones_ONEXPO_32_Estados', index=False)
    if not df_playbook.empty:
        df_playbook.to_excel(writer, sheet_name='Playbook_CPS_Metodologia', index=False)

# Copiar a carpetas del escritorio
for d in desktop_dirs:
    if os.path.exists(d):
        dst = os.path.join(d, "00_BASE_MAESTRA_PAYMIND_MULTISEGMENTO.xlsx")
        shutil.copy2(master_multi_path, dst)
        print(f"[OK] Base Maestra Multisectorial guardada en: {dst}")

print("Generación de Base Maestra Multisectorial completada con éxito.")
