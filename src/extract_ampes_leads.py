import os
import pandas as pd

ampes_leads = [
    # ISVs Y CONTROLES VOLUMÉTRICOS (SOCIOS CLAVE PARA INTEGRACIÓN DE PAYMIND)
    {
        'Empresa': 'ATIO GROUP (ControlGAS)',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'marketing@atio.com.mx',
        'Telefono': '55.5001.5100 / 800.087.2646',
        'Sitio_Web': 'www.atiogroup.com.mx',
        'Relevancia_PayMind': 'Integración directa con ControlGAS (líder en +5,000 estaciones)'
    },
    {
        'Empresa': 'EGAS',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'ventas@egas.com.mx',
        'Telefono': '55.5566.5951',
        'Sitio_Web': 'www.egas.com.mx',
        'Relevancia_PayMind': 'Integración con software POS e-Gas para gasolineras'
    },
    {
        'Empresa': 'ALVIC',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'contactomx@alvic.com.mx',
        'Telefono': '55.4624.1000',
        'Sitio_Web': 'www.alvic.net',
        'Relevancia_PayMind': 'Integración de quioscos con terminales y software Alvic'
    },
    {
        'Empresa': 'iGAS',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'ventas@igas.com.mx',
        'Telefono': '668.816.2160',
        'Sitio_Web': 'www.igas.mx',
        'Relevancia_PayMind': 'Sistema agilizador de ventas en isla y Anexo 21'
    },
    {
        'Empresa': 'AIE MÉXICO (SIGMA)',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'ventas@aiemexico.com.mx',
        'Telefono': '777.608.6633',
        'Sitio_Web': 'www.aiemexico.com.mx',
        'Relevancia_PayMind': 'Software SIGMA-AIE de automatización de estaciones'
    },
    {
        'Empresa': 'AVALON SOFTWARE LATAM',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'xmunguia@avaloninformatica.com',
        'Telefono': '56.1164.7838',
        'Sitio_Web': 'www.avalonsoftware.com',
        'Relevancia_PayMind': 'Automatización de POS y medios de pago para grupos'
    },
    {
        'Empresa': 'GAS MANAGER',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'info@gasmanager.com',
        'Telefono': '811.224.0330',
        'Sitio_Web': 'www.gasmanager.com',
        'Relevancia_PayMind': 'Control volumétrico y cortes automáticos en despacho'
    },
    {
        'Empresa': 'GRUPO CADISA',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'marcos.robles@cadisaenlinea.com.mx',
        'Telefono': '662.112.0745',
        'Sitio_Web': 'www.cadisaenlinea.com.mx',
        'Relevancia_PayMind': 'Terminales de punto de venta y control de despacho'
    },
    {
        'Empresa': 'KERNOTEK',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'ventas@kernotek.mx',
        'Telefono': '464.649.3407',
        'Sitio_Web': 'www.kernotek.mx',
        'Relevancia_PayMind': 'Hardware y software de control volumétrico Anexo 21'
    },
    {
        'Empresa': 'NEXUS FUEL',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'info@nexusfuel.com',
        'Telefono': '664.375.2177',
        'Sitio_Web': 'www.nexusfuel.com',
        'Relevancia_PayMind': 'Automatización de procesos operativos en gasolineras'
    },
    {
        'Empresa': 'POLARIS CONTROL VOLUMÉTRICO',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'info@ecsmexico.com',
        'Telefono': '81.8100.9605',
        'Sitio_Web': 'www.ecsmexico.com',
        'Relevancia_PayMind': 'Liquidación y facturación en isla'
    },
    {
        'Empresa': 'LUQROSS (Suite Olimpo)',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'david_rosas@luqross.com',
        'Telefono': '55.1992.5117',
        'Sitio_Web': 'www.luqrosstecnologia.com',
        'Relevancia_PayMind': 'Control volumétrico Suite Olimpo Anexo 30 SAT'
    },
    {
        'Empresa': 'FUEL SOFT / ENERCON',
        'Categoria': 'ISV / Control Volumétrico & POS',
        'Contacto_Email': 'gtapia@enercon.mx',
        'Telefono': '444.651.2376',
        'Sitio_Web': 'www.enercon.mx',
        'Relevancia_PayMind': 'TPV integradas a control volumétrico SAT/PEMEX'
    },
    {
        'Empresa': 'PRE (SOFTWARE CON IA)',
        'Categoria': 'ISV / Analytics & Facturación',
        'Contacto_Email': 'dalvarez@gaspre.mx',
        'Telefono': '55.2728.4708',
        'Sitio_Web': 'www.grupopre.ai',
        'Relevancia_PayMind': 'FacturaPRE WhatsApp & clientes Rendichicas, Burgos, Combu-express'
    },
    
    # FABRICANTES Y PROVEEDORES DE QUIOSCOS & MANEJO DE EFECTIVO
    {
        'Empresa': 'INTERLOGIC',
        'Categoria': 'Quioscos & Cajeros de Autoatención',
        'Contacto_Email': 'comercial@interlogic.com.mx',
        'Telefono': '66.2215.7715',
        'Sitio_Web': 'www.interlogicglobal.com',
        'Relevancia_PayMind': 'Socio estratégico directo: Fabricante de quioscos de autoatención'
    },
    {
        'Empresa': 'SEPROCESA',
        'Categoria': 'Manejo Seguro de Efectivo',
        'Contacto_Email': 'gina.munoz@seprocesa.com.mx',
        'Telefono': '449.329.5956',
        'Sitio_Web': 'www.seprocesa.com',
        'Relevancia_PayMind': 'Gestión de efectivo y trazabilidad en cajas'
    },
    {
        'Empresa': 'SNE (Sistemas Neumáticos de Envíos)',
        'Categoria': 'Manejo de Efectivo en Isla',
        'Contacto_Email': 'ventas@sne.com.mx',
        'Telefono': '55.5377.2170 / 55.1051.8091',
        'Sitio_Web': 'www.sne.com.mx',
        'Relevancia_PayMind': 'Sistema aerocom AC-GAS de efectivo en islas de despacho'
    },
    
    # DISTRIBUIDORES DE DISPENSARIOS Y HARDWARE
    {
        'Empresa': 'GILBARCO VEEDER-ROOT',
        'Categoria': 'Hardware & Dispensarios',
        'Contacto_Email': 'marketing.la@gilbarco.com',
        'Telefono': 'Sitio Oficial',
        'Sitio_Web': 'www.gilbarco.com/mx',
        'Relevancia_PayMind': 'Líder global en dispensarios e integración con TPV'
    },
    {
        'Empresa': 'PETROTECH',
        'Categoria': 'Hardware & Dispensarios',
        'Contacto_Email': 'rarreola@petrotech.com.mx',
        'Telefono': '333.634.9293',
        'Sitio_Web': 'www.petrotech.com.mx',
        'Relevancia_PayMind': 'Distribuidor Platinum de ControlGAS y dispensarios Wayne/Gilbarco'
    },
    {
        'Empresa': 'PETROGAS',
        'Categoria': 'Equipamiento & Dispensarios',
        'Contacto_Email': 'contacto@petrogas.com.mx',
        'Telefono': '818.305.0800',
        'Sitio_Web': 'www.petrogas.com.mx',
        'Relevancia_PayMind': 'Distribuidor Gilbarco con 17 sucursales'
    },
    {
        'Empresa': 'ATS MERIDIAN DE MÉXICO',
        'Categoria': 'Equipamiento & Dispensarios',
        'Contacto_Email': 'aescobedo@atsmeridian.com.mx',
        'Telefono': '55.5604.6434',
        'Sitio_Web': 'www.atsmeridian.com.mx',
        'Relevancia_PayMind': 'Distribuidor de dispensarios Wayne y Franklin Fueling'
    }
]

out_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_SOCIOS_AMPES_2026.csv'
df = pd.DataFrame(ampes_leads)
df.to_csv(out_csv, index=False, encoding='utf-8-sig')

print(f"=== EXTRAÍDOS {len(df)} SOCIOS CLAVE DE AMPES 2026 PARA PAYMIND ===")
print(f"Guardados en: {out_csv}")
