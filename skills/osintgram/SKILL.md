---
name: osintgram
description: Use when you need to perform OSINT reconnaissance on Instagram accounts, extract public profile metadata, scrape bio emails and phone numbers, and map executive social presence.
---

# 📸 Osintgram (Instagram Intelligence & Profile Reconnaissance Engine)

## Overview
**osintgram** extracts public intelligence from target Instagram profiles, focusing on business information, linked domains, contact email addresses in bio, tagged collaborators, and account verification status.

## When to Use
- Investigating brand presence or executive accounts for retail businesses (e.g. gym owners, retail fuel marketing campaigns).
- Extracting public customer support emails or phone numbers listed directly in business Instagram bios.
- Mapping executive social footprints when LinkedIn data is sparse.

## Directory Structure
```
osintgram/
├── SKILL.md
└── scripts/
    └── run_osintgram.py        # Public profile recon & bio contact scraper
```

## Quick Start / Execution

### 1. Auditar Perfil y Extraer Datos de Contacto
```bash
python skills/osintgram/scripts/run_osintgram.py --target "cps_gym_oficial" --extract-contacts --format markdown
```

### 2. Exportar en Formato JSON
```bash
python skills/osintgram/scripts/run_osintgram.py --target "empresa_objetivo" --output-file "data/instagram_recon.json"
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--target` | string | **Requerido** | Handle de Instagram (sin @). |
| `--extract-contacts`| flag | `True` | Busca correos y teléfonos en la biografía pública. |
| `--format` | choice | `json` | Formato: `json`, `markdown`. |
| `--output-file` | string | `None` | Archivo para exportar resultados. |

## Operational Guardrails
El script consulta endpoints web públicos sin requerir credenciales maestras y maneja cabeceras de navegador para evitar bloqueos por parte de Meta.
