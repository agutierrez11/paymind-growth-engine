import os
import pandas as pd

odoo_gas_partners = [
    {
        'Partner_Odoo': 'Exdoo',
        'Dominio': 'exdoo.mx',
        'Contacto_Email': 'contacto@exdoo.mx',
        'Ubicacion': 'México',
        'Especialidad': 'Implementaciones Odoo Enterprise en Gasolineras',
        'Clientes_Gasolineros_Confirmados': 'Petroplus Gasolineras, Latenergy, Purefill',
        'Oportunidad_PayMind': 'Integrar la pasarela PayMind al módulo Odoo POS de sus clientes gasolineros'
    },
    {
        'Partner_Odoo': 'Soltein',
        'Dominio': 'soltein.mx',
        'Contacto_Email': 'contacto@soltein.mx',
        'Ubicacion': 'Guadalajara y Monterrey',
        'Especialidad': 'Odoo Petrolero y Manejo de Combustibles',
        'Clientes_Gasolineros_Confirmados': 'Empresas petroleras y distribución de combustibles',
        'Oportunidad_PayMind': 'Alianza de adquirencia y quioscos para proyectos Odoo petroleros'
    },
    {
        'Partner_Odoo': 'Vex Soluciones',
        'Dominio': 'vexsoluciones.com',
        'Contacto_Email': 'ventas@vexsoluciones.com',
        'Ubicacion': 'México / LATAM',
        'Especialidad': 'Módulo Vertical Odoo para Gasolineras y Estaciones de Servicio',
        'Clientes_Gasolineros_Confirmados': 'Cadenas de Estaciones de Servicio en México',
        'Oportunidad_PayMind': 'Módulo nativo de cobro en quiosco e isla integrado a su vertical Odoo'
    },
    {
        'Partner_Odoo': 'SYCA',
        'Dominio': 'syca.com.mx',
        'Contacto_Email': 'contacto@syca.com.mx',
        'Ubicacion': 'México',
        'Especialidad': 'Odoo Flotas y Registro de Combustibles',
        'Clientes_Gasolineros_Confirmados': 'Flotillas comerciales y autoconsumo',
        'Oportunidad_PayMind': 'Integración de cobro de flotillas'
    }
]

out_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_PARTNERS_ODOO_GASOLINEROS.csv'
df = pd.DataFrame(odoo_gas_partners)
df.to_csv(out_csv, index=False, encoding='utf-8-sig')

print(f"=== EXTRAÍDOS {len(df)} PARTNERS DE ODOO ESPECIALIZADOS EN GASOLINERAS ===")
print(f"Guardados en: {out_csv}")
