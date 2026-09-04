---
name: firecrawl-intel
description: Use when you need to perform deep B2B website intelligence, convert prospect domains into clean Markdown, map corporate site architectures, or extract structured decision-maker and customer data using the Firecrawl API (MendableAI).
---

# 🔥 Firecrawl Intel (B2B Website Scraping & Enterprise Intelligence Engine)

## Overview
**firecrawl-intel** connects directly to the **Firecrawl API** (`api.firecrawl.dev`) to turn entire prospect websites into clean, LLM-ready Markdown and structured JSON. It strips away navigation bars, scripts, and cookie banners, extracting raw business intelligence: decision makers, technological stacks, partner logos, payment gateways, and client rosters.

## When to Use
- Ingesting full corporate websites of the **72 Wish List accounts of Toku** (SOFOMes, financieras, escuelas) to identify their repayment workflows.
- Auditing websites of **grupos gasolineros de AMPES** to inspect if they offer billing portals, mobile apps, or self-service kiosks.
- Mapping complete domain URLs (`/v1/map`) to uncover hidden employee directories, customer support portals, or payment checkout endpoints.
- Feeding clean Markdown text directly into Deep Research or GTM Outreach pipelines.

## Directory Structure
```
firecrawl-intel/
├── SKILL.md
└── scripts/
    └── run_firecrawl_intel.py   # Multi-mode Firecrawl engine (scrape, crawl, map, extract)
```

## Quick Start / Execution

### 1. Escanear un Sitio Web y Extraer Inteligencia B2B
```bash
python skills/firecrawl-intel/scripts/run_firecrawl_intel.py --url "https://credifiel.com.mx" --mode scrape --output-file "data/credifiel_intel.md"
```

### 2. Mapear Todas las Subpáginas y Endpoints de un Prospecto
```bash
python skills/firecrawl-intel/scripts/run_firecrawl_intel.py --url "https://dimex.mx" --mode map
```

### 3. Rastrear Páginas Clave (Nosotros, Contacto, Servicios)
```bash
python skills/firecrawl-intel/scripts/run_firecrawl_intel.py --url "https://avanzasolido.com" --mode crawl --limit 5
```

### 4. Extracción Estructurada B2B (Decisores, Productos, Contacto)
```bash
python skills/firecrawl-intel/scripts/run_firecrawl_intel.py --url "https://finvivir.com.mx" --mode extract-b2b
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--url` | string | **Requerido** | URL del prospecto a investigar. |
| `--mode` | choice | `scrape` | Operación: `scrape` (1 página a Markdown), `crawl` (múltiples páginas), `map` (árbol de URLs), `extract-b2b` (extracción estructurada). |
| `--limit` | int | `5` | Límite máximo de páginas en modo `crawl`. |
| `--api-key` | string | `None` | API Key de Firecrawl (por defecto lee de la variable de entorno `FIRECRAWL_API_KEY`). |
| `--format` | choice | `markdown` | Formato de salida: `markdown`, `json`. |
| `--output-file`| string | `None` | Archivo de destino para guardar el expediente. |

## Environment Configuration
Agrega tu llave al archivo `.env` en la raíz del proyecto:
```env
FIRECRAWL_API_KEY=fc-tu-llave-aqui
```
Si la variable no está configurada, el script te solicitará introducirla o puedes pasarla directamente con la bandera `--api-key "fc-..."`.
