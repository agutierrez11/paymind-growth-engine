import os
import pandas as pd

# Las 24 empresas 100% útiles del directorio AMPES 2026 para PayMind
all_24_ampes_partners = [
    # CATEGORÍA 1: SOFTWARE POS & CONTROL VOLUMÉTRICO (14 ISVs)
    {'Empresa': 'ATIO GROUP', 'Categoria': 'Software POS & Control Volumétrico', 'Sistema': 'ControlGAS / FuelGATE', 'Email': 'marketing@atio.com.mx', 'Telefono': '55.5001.5100', 'Web': 'www.atiogroup.com.mx', 'Clientes_Conocidos': 'Petro-7, Orsan, G500, Hidrosina, Rendilitros (+5,000 estaciones)'},
    {'Empresa': 'PRE SOFTWARE', 'Categoria': 'Software POS & Analytics IA', 'Sistema': 'GASPRE / FacturaPRE', 'Email': 'dalvarez@gaspre.mx', 'Telefono': '55.2728.4708', 'Web': 'www.grupopre.ai', 'Clientes_Conocidos': 'RendiChicas, Grupo Burgos, Combuexpress, Gasomax, Ruta, Petrum, Gilga, Corporativo AP, Top Energy, Gomasa, Gonergy'},
    {'Empresa': 'ALVIC', 'Categoria': 'Software POS & Automatización', 'Sistema': 'Alvic Octane POS', 'Email': 'contactomx@alvic.com.mx', 'Telefono': '55.4624.1000', 'Web': 'www.alvic.net', 'Clientes_Conocidos': 'Estaciones de Servicio y Terminales de Almacenamiento'},
    {'Empresa': 'EGAS', 'Categoria': 'Software POS & Control Volumétrico', 'Sistema': 'e-Gas POS', 'Email': 'ventas@egas.com.mx', 'Telefono': '55.5566.5951', 'Web': 'www.egas.com.mx', 'Clientes_Conocidos': 'Grupo Petrolero Arca, Cadenas Centro y Bajío'},
    {'Empresa': 'iGAS', 'Categoria': 'Software POS & Agilizador de Isla', 'Sistema': 'iGAS Anexo 21', 'Email': 'ventas@igas.com.mx', 'Telefono': '668.816.2160', 'Web': 'www.igas.mx', 'Clientes_Conocidos': 'Estaciones de servicio e independientes'},
    {'Empresa': 'AIE MÉXICO', 'Categoria': 'Software POS & Control Volumétrico', 'Sistema': 'Software SIGMA-AIE', 'Email': 'ventas@aiemexico.com.mx', 'Telefono': '777.608.6633', 'Web': 'www.aiemexico.com.mx', 'Clientes_Conocidos': 'Estaciones de Servicio a nivel nacional'},
    {'Empresa': 'AVALON SOFTWARE LATAM', 'Categoria': 'Software POS & Monederos', 'Sistema': 'Arcadia CBOS / OpenCard', 'Email': 'xmunguia@avaloninformatica.com', 'Telefono': '56.1164.7838', 'Web': 'www.avalonsoftware.com', 'Clientes_Conocidos': 'Grupos gasolineros y retail'},
    {'Empresa': 'GAS MANAGER', 'Categoria': 'Software POS & Despacho', 'Sistema': 'Gas Manager Volumétrico', 'Email': 'info@gasmanager.com', 'Telefono': '811.224.0330', 'Web': 'www.gasmanager.com', 'Clientes_Conocidos': 'Gasolineras, autoconsumos y transportistas'},
    {'Empresa': 'GRUPO CADISA', 'Categoria': 'Software POS & Control Despacho', 'Sistema': 'Cadisa Control', 'Email': 'marcos.robles@cadisaenlinea.com.mx', 'Telefono': '662.112.0745', 'Web': 'www.cadisaenlinea.com.mx', 'Clientes_Conocidos': 'Estaciones de servicio y flotillas'},
    {'Empresa': 'FUEL SOFT / ENERCON', 'Categoria': 'Software TPV & Control Volumétrico', 'Sistema': 'Enercon TPV / ENERPAY', 'Email': 'gtapia@enercon.mx', 'Telefono': '444.651.2376', 'Web': 'www.enercon.mx', 'Clientes_Conocidos': 'Estaciones de Servicio PEMEX y privadas'},
    {'Empresa': 'BRENTEC', 'Categoria': 'Software a Medida & Volumétrico', 'Sistema': 'Brentec Control', 'Email': 'gcantov@brentec.mx', 'Telefono': '999.163.3598', 'Web': 'www.brentec.mx', 'Clientes_Conocidos': 'Empresas del sector petrolífero'},
    {'Empresa': 'KERNOTEK', 'Categoria': 'Software & Hardware Volumétrico', 'Sistema': 'Kernotek Anexo 21', 'Email': 'ventas@kernotek.mx', 'Telefono': '464.649.3407', 'Web': 'www.kernotek.mx', 'Clientes_Conocidos': 'Estaciones de servicio e industria'},
    {'Empresa': 'NEXUS FUEL', 'Categoria': 'Software & Automatización Operativa', 'Sistema': 'Nexus POS', 'Email': 'info@nexusfuel.com', 'Telefono': '664.375.2177', 'Web': 'www.nexusfuel.com', 'Clientes_Conocidos': 'Cadenas del noroeste y centro'},
    {'Empresa': 'POLARIS CONTROL VOLUMÉTRICO', 'Categoria': 'Software POS & Flotillas', 'Sistema': 'Polaris Downstream', 'Email': 'info@ecsmexico.com', 'Telefono': '81.8100.9605', 'Web': 'www.ecsmexico.com', 'Clientes_Conocidos': 'Estaciones de servicio y liquidaciones'},
    {'Empresa': 'LUQROSS', 'Categoria': 'Software Control Volumétrico', 'Sistema': 'Suite Olimpo Anexo 30', 'Email': 'david_rosas@luqross.com', 'Telefono': '55.1992.5117', 'Web': 'www.luqrosstecnologia.com', 'Clientes_Conocidos': 'Estaciones de servicio'},

    # CATEGORÍA 2: FABRICANTES DE QUIOSCOS & MANEJO DE EFECTIVO (4 EMPRESAS)
    {'Empresa': 'INTERLOGIC', 'Categoria': 'Fabricante de Quioscos & Cajeros', 'Sistema': 'Quioscos Autoatención', 'Email': 'comercial@interlogic.com.mx', 'Telefono': '66.2215.7715', 'Web': 'www.interlogicglobal.com', 'Clientes_Conocidos': 'Oxxo Gas, cadenas de conveniencia y bancos'},
    {'Empresa': 'SEPROCESA', 'Categoria': 'Gestión y Control de Efectivo', 'Sistema': 'Smart Safes / Efectivo', 'Email': 'gina.munoz@seprocesa.com.mx', 'Telefono': '449.329.5956', 'Web': 'www.seprocesa.com', 'Clientes_Conocidos': 'Estaciones de servicio y retail'},
    {'Empresa': 'SISTEMAS NEUMÁTICOS DE ENVÍOS (SNE)', 'Categoria': 'Transporte Neumático Efectivo Isla', 'Sistema': 'aerocom AC-GAS', 'Email': 'ventas@sne.com.mx', 'Telefono': '55.5377.2170', 'Web': 'www.sne.com.mx', 'Clientes_Conocidos': 'Estaciones de servicio a nivel nacional'},
    {'Empresa': 'CISTEM / CISNEROS GROUP', 'Categoria': 'Hardware & Sistemas de Estaciones', 'Sistema': 'Equipagas / Gasmen', 'Email': 'lcisneros@cistem.com.mx', 'Telefono': '664.621.0631', 'Web': 'www.cistem.com.mx', 'Clientes_Conocidos': 'Estaciones de servicio e industria'},

    # CATEGORÍA 3: HARDWARE, DISPENSARIOS & INTEGRACIÓN ISV (6 EMPRESAS)
    {'Empresa': 'GILBARCO VEEDER-ROOT', 'Categoria': 'Dispensarios & POS Doms/Orpak', 'Sistema': 'Gilbarco / Invenco', 'Email': 'marketing.la@gilbarco.com', 'Telefono': 'Oficial LA', 'Web': 'www.gilbarco.com/mx', 'Clientes_Conocidos': 'Líder global en gasolineras'},
    {'Empresa': 'PETROTECH', 'Categoria': 'Distribuidor Platinum ControlGAS & Hardware', 'Sistema': 'ControlGAS / Gilbarco / Wayne', 'Email': 'rarreola@petrotech.com.mx', 'Telefono': '333.634.9293', 'Web': 'www.petrotech.com.mx', 'Clientes_Conocidos': 'Grupos gasolineros en Occidente y Centro'},
    {'Empresa': 'PETROGAS', 'Categoria': 'Equipamiento & Dispensarios (17 Sucursales)', 'Sistema': 'Gilbarco Veeder-Root', 'Email': 'contacto@petrogas.com.mx', 'Telefono': '818.305.0800', 'Web': 'www.petrogas.com.mx', 'Clientes_Conocidos': 'Estaciones de servicio México y EE.UU.'},
    {'Empresa': 'EMAGAS', 'Categoria': 'Dispensarios & Sistemas de Control', 'Sistema': 'Bennett / Petrotec', 'Email': 'otrevino@emagas.com.mx', 'Telefono': '55.6120.2366', 'Web': 'www.emagas.com.mx', 'Clientes_Conocidos': 'Estaciones de servicio'},
    {'Empresa': 'SIME (Mecatrónica Arciga)', 'Categoria': 'Mantenimiento & Integrador Sigma/Alvic', 'Sistema': 'Wayne / Gilbarco / Alvic', 'Email': 'jorgeheg@hotmail.com', 'Telefono': '55.5551.2437', 'Web': 'www.grupo-sime.com', 'Clientes_Conocidos': 'Gasolineras PEMEX e independientes'},
    {'Empresa': 'GRUPO SOL REY', 'Categoria': 'Equipamiento Dover Fueling / Wayne', 'Sistema': 'Wayne / OPW', 'Email': 'adal.solis@solrey.com', 'Telefono': '333.837.3760', 'Web': 'www.solrey.com', 'Clientes_Conocidos': 'Estaciones de servicio en México'}
]

out_csv = r'c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\LEADS_SOCIOS_AMPES_2026_COMPLETO.csv'
df = pd.DataFrame(all_24_ampes_partners)
df.to_csv(out_csv, index=False, encoding='utf-8-sig')

print(f"=== AUDITORÍA COMPLETA: {len(df)} EMPRESAS 100% ÚTILES DE AMPES 2026 ===")
print(f"Guardados en: {out_csv}")
