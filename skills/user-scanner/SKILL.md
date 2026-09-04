---
name: user-scanner
description: Use when you need to perform deep OSINT investigations on target executives, email addresses, or usernames across 465+ platforms with pivot discovery and MCP integration.
---

# 🕵️ User Scanner (Production OSINT Multi-Vector Engine)

## Overview
**user-scanner** provides multi-vector OSINT intelligence across 465+ platforms (175+ email-integrated sites and 290+ username services). It extracts rich metadata (bios, follower counts, verified badges, UIDs, associated accounts) and enables pivot correlation for target profiling.

## When to Use
- Validating the digital footprint of a target executive (CFO, Director, Owner) before cold outreach.
- Verifying whether a predicted corporate or personal email exists on active platforms without burning Hunter/Apollo credits.
- Discovering linked social profiles, developer accounts, and public footprints from a single handle.

## Directory Structure
```
user-scanner/
├── SKILL.md
└── scripts/
    └── run_user_scanner.py     # CLI execution & MCP connector runner
```

## Quick Start / Execution

### 1. Escanear por Nombre de Usuario (Handle)
```bash
python skills/user-scanner/scripts/run_user_scanner.py --username "antoniogutierrez" --format json --output-file "data/osint_antonio.json"
```

### 2. Escanear por Correo Electrónico
```bash
python skills/user-scanner/scripts/run_user_scanner.py --email "contacto@empresa.com.mx" --deep-scan
```

### 3. Modo Rápido (Top 50 Vectores Críticos B2B)
```bash
python skills/user-scanner/scripts/run_user_scanner.py --username "target_cfo" --fast
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--username` | string | `None` | Nombre de usuario / handle a auditar. |
| `--email` | string | `None` | Dirección de correo electrónico objetivo. |
| `--fast` | flag | `False` | Limita la consulta a las plataformas de mayor prioridad (LinkedIn, GitHub, Twitter, Slack, Google). |
| `--deep-scan` | flag | `False` | Activa pivotaje recursivo para buscar cuentas secundarias vinculadas. |
| `--format` | choice | `json` | Formato de salida: `json`, `markdown`, `table`. |
| `--output-file`| string | `None` | Ruta para guardar el reporte estructurado. |

## Input / Output Schema

### Ejemplo de Entrada
```json
{
  "target": "cfo_target",
  "type": "username",
  "fast_mode": true
}
```

### Ejemplo de Salida (JSON)
```json
{
  "target": "cfo_target",
  "total_scanned": 52,
  "found_count": 4,
  "profiles": [
    {
      "platform": "GitHub",
      "url": "https://github.com/cfo_target",
      "status": "active",
      "bio": "Finance & Fintech Infra",
      "name": "Target Executive"
    }
  ]
}
```

## Edge Cases & Error Handling
- **Rate Limiting:** Si una plataforma retorna HTTP 429, el motor aplica backoff exponencial automático y continúa con el siguiente vector sin detener la ejecución.
- **WAF / Cloudflare:** Los sitios protegidos con Cloudflare Turnstile son marcados como `unverifiable` sin arrojar falso positivo.
- **Filtro Zero-Assumption:** Solo reporta perfiles confirmados con código 200 y validación de firma en cuerpo HTML.
