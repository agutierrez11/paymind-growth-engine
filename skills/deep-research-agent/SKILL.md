---
name: deep-research-agent
description: Use when you need to perform autonomous, recursive deep research on companies, executives, regulatory frameworks, or complex technical domains with multi-step search queries, link traversing, and cited report synthesis.
---

# 🧠 Deep Research Agent (Autonomous Recursive Intelligence Engine)

## Overview
**deep-research-agent** reproduces the recursive reasoning and search loop of OpenAI Deep Research. Given a high-level research goal, it breaks down the query into specialized search hypotheses, traverses web citations, extracts high-signal paragraphs, cross-correlates facts, and generates an exhaustive intelligence briefing with full source tracking.

## When to Use
- Building forensic dossiers on target accounts (SOFOMes, Fintechs, retail fuel groups).
- Investigating regulatory updates (CNBV Circular 14/2017, Anexo 30 SAT, interchange fee caps).
- Profiling executive backgrounds, board members, and vendor partnerships across public and corporate registries.

## Directory Structure
```
deep-research-agent/
├── SKILL.md
└── scripts/
    └── run_deep_research.py    # Recursive agent research engine
```

## Quick Start / Execution

### 1. Investigar una Empresa Objetivo (Dossier B2B)
```bash
python skills/deep-research-agent/scripts/run_deep_research.py --query "Credifiel SOFOM infraestructura cobranza nomina STP" --depth 2 --max-sources 8 --output-file "data/dossier_credifiel_deep.md"
```

### 2. Auditoría Regulatoria o Técnica
```bash
python skills/deep-research-agent/scripts/run_deep_research.py --query "Anteproyecto CNBV topes cuota intercambio adquirencia gasolineras" --depth 1
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--query` | string | **Requerido** | Objetivo o pregunta de investigación principal. |
| `--depth` | int | `2` | Nivel de recursión (1: directo, 2: profundizar en fuentes clave, 3: exhaustivo). |
| `--max-sources`| int | `6` | Número máximo de fuentes / dominios a consultar y procesar. |
| `--format` | choice | `markdown` | Formato del reporte: `markdown`, `json`. |
| `--output-file`| string | `None` | Ruta de archivo donde se guardará el informe final. |

## Input / Output Schema

### Ejemplo de Salida (Markdown)
```markdown
# 📑 Deep Research Briefing: Credifiel Cobranza Nómina STP
- **Fecha de Ejecución:** 2026-09-03
- **Fuentes Analizadas:** 6
- **Confianza de Datos:** Alta (Validada con Anexo 30 / SIPRES)

## 1. Resumen Ejecutivo
...
## 2. Hallazgos Forenses y Stack Técnico
...
## 3. Fuentes y Referencias Citadas
1. [Condusef SIPRES] https://...
2. [Fitch Ratings México] https://...
```

## Error Recovery
- **Fallo de Conexión:** Si un endpoint o sitio web objetivo bloquea el scraping (HTTP 403 / Cloudflare), el agente descarta la fuente de inmediato y pivota a fuentes secundarias de caché (web archives, registros públicos, boletines oficiales).
