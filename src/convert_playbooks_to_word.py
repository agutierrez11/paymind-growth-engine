import os
import re
import shutil
import glob
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Configurar carpetas destino en Escritorio
desktop_dirs = [
    r"C:\Users\Antonio\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Desktop\Paymind Strategy",
    r"C:\Users\Antonio\OneDrive\Escritorio\Paymind Strategy"
]

for d in desktop_dirs:
    os.makedirs(d, exist_ok=True)

base_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine"
playbooks_dir = os.path.join(base_dir, "playbooks")

def style_heading(p, text, level):
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.bold = True
    if level == 1:
        run.font.size = Pt(20)
        run.font.color.rgb = RGBColor(15, 23, 42) # Slate Dark
    elif level == 2:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(37, 99, 235) # Accent Blue
    elif level == 3:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(30, 41, 59)

def parse_markdown_to_docx(md_path, docx_path):
    doc = Document()
    
    # Margenes de pagina (0.8 pulgadas)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_lines = []

    for line in lines:
        raw_line = line.rstrip('\n\r')
        stripped = raw_line.strip()

        # Manejo de Tablas
        if '|' in stripped and ('---' in stripped or stripped.startswith('|')):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table and '|' not in stripped:
            process_table(doc, table_lines)
            in_table = False
            table_lines = []

        if in_table:
            continue

        if not stripped:
            continue

        # Encabezados
        if stripped.startswith('# '):
            p = doc.add_paragraph()
            style_heading(p, stripped[2:].strip(), 1)
        elif stripped.startswith('## '):
            p = doc.add_paragraph()
            style_heading(p, stripped[3:].strip(), 2)
        elif stripped.startswith('### '):
            p = doc.add_paragraph()
            style_heading(p, stripped[4:].strip(), 3)
        elif stripped.startswith('> '):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(stripped[2:].strip())
            run.font.name = 'Calibri'
            run.font.italic = True
            run.font.color.rgb = RGBColor(71, 85, 105)
        elif stripped.startswith('* ') or stripped.startswith('- ') or stripped.startswith('1. ') or stripped.startswith('2. '):
            p = doc.add_paragraph(style='List Bullet' if stripped.startswith(('* ', '- ')) else 'List Number')
            p.paragraph_format.space_after = Pt(3)
            content = re.sub(r'^(\*|-|\d+\.)\s+', '', stripped)
            add_formatted_text(p, content)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            add_formatted_text(p, stripped)

    if in_table and table_lines:
        process_table(doc, table_lines)

    doc.save(docx_path)

def add_formatted_text(paragraph, text):
    parts = re.split(r'(\*\*.*?\*\*|`.*?`|\[.*?\]\(.*?\))', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = paragraph.add_run(part[2:-2])
            r.font.name = 'Calibri'
            r.bold = True
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif part.startswith('`') and part.endswith('`'):
            r = paragraph.add_run(part[1:-1])
            r.font.name = 'Consolas'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(225, 29, 72)
        elif part.startswith('[') and ']' in part and '(' in part and part.endswith(')'):
            link_text = part[1:part.index(']')]
            r = paragraph.add_run(link_text)
            r.font.name = 'Calibri'
            r.font.color.rgb = RGBColor(37, 99, 235)
            r.underline = True
        else:
            r = paragraph.add_run(part)
            r.font.name = 'Calibri'
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(51, 65, 85)

def process_table(doc, lines):
    rows_data = []
    for line in lines:
        if '---' in line:
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells:
            rows_data.append(cells)

    if not rows_data:
        return

    num_rows = len(rows_data)
    num_cols = max(len(r) for r in rows_data)

    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for r_idx, row in enumerate(rows_data):
        for c_idx, val in enumerate(row):
            if c_idx < num_cols:
                cell = table.cell(r_idx, c_idx)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(2)
                add_formatted_text(p, val)
                
                if r_idx == 0:
                    shd = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
                    cell._tc.get_or_add_tcPr().append(shd)
                    for run in p.runs:
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.bold = True
                else:
                    if r_idx % 2 == 1:
                        shd = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
                        cell._tc.get_or_add_tcPr().append(shd)

    doc.add_paragraph()

# Convertir todos los Playbooks a Word (.docx)
file_order = [
    "ONE_PAGER_PLAN_GTM_VS_AGENCIA.md",
    "propuesta_ejecutiva_ceo_paymind.md",
    "roadmap_comercial_y_caso_negocio.md",
    "segmentacion_clusters_gtm_gasolineras.md",
    "lead_magnet_1_checkup_anexo30_sat.md",
    "lead_magnet_2_matriz_optimizacion_bancaria.md",
    "matriz_alianzas_cps_y_copys_partnerships.md",
    "estrategia_oceano_azul_softwares_regionales.md",
    "framework_comunicacion_c_level_y_tercera_transferencia.md",
    "directorio_expositores_encuentro_empresarial_2026.md",
    "estrategia_guerrilla_evento_mariano_paymind.md",
    "modelo_comisiones_y_soberania_comercial_antonio.md",
    "investigacion_softwares_volumetricos_mexico.md",
    "brief_marketing_paymind_gasolineras.md",
    "directorio_onexpo_estatal_mexico.md"
]

converted_count = 0
for idx, fname in enumerate(file_order, 1):
    src_md = os.path.join(playbooks_dir, fname)
    if os.path.exists(src_md):
        clean_name = fname.replace('.md', '').replace('_', ' ').title()
        docx_name = f"{idx:02d}_{clean_name}.docx"
        
        for d in desktop_dirs:
            target_docx = os.path.join(d, docx_name)
            parse_markdown_to_docx(src_md, target_docx)
            print(f"[OK] Creado Documento Word: {target_docx}")
        converted_count += 1

# Copiar Excels y CSVs a la carpeta del Escritorio
data_dir = os.path.join(base_dir, "data")
data_files = [
    "Campana_PayMind_MultiSegmento_CPS.xlsx",
    "Campana_PayMind_Gasolineras_400.xlsx",
    "Snovio_Gasolineras_Segmentada_Clusters.csv",
    "directorio_asociaciones_onexpo_mexico.csv"
]

for dfname in data_files:
    src_data = os.path.join(data_dir, dfname)
    if os.path.exists(src_data):
        for d in desktop_dirs:
            dst_data = os.path.join(d, dfname)
            shutil.copy2(src_data, dst_data)
            print(f"[OK] Copiado Excel/CSV: {dst_data}")

# Copiar versión HTML del One-Pager
src_html = os.path.join(playbooks_dir, "ONE_PAGER_PLAN_GTM_VS_AGENCIA.html")
if os.path.exists(src_html):
    for d in desktop_dirs:
        dst_html = os.path.join(d, "00_ONE_PAGER_EJECUTIVO_IMPRIMIBLE.html")
        shutil.copy2(src_html, dst_html)
        print(f"[OK] Copiado HTML Imprimible: {dst_html}")

print(f"\nPROCESO COMPLETADO EXITOSAMENTE: {converted_count} documentos de Word (.docx) creados en 'Paymind Strategy'.")
