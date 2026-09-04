---
name: reverse-skill
description: Use when you need to route and perform reverse engineering tasks, static code analysis, APK inspection, JavaScript bundle decompilation, or detect hardcoded secrets and payment gateway endpoints in target applications.
---

# 🛡️ Reverse Skill (Production Security & Reverse Engineering Router)

## Overview
**reverse-skill** acts as a structured decision and execution layer for reverse engineering and static analysis. It inspects software artifacts (APKs, JavaScript bundles, executables), extracts hidden endpoints, hardcoded credentials, and routes the analysis to specialized playbooks.

## When to Use
- Auditing competitor mobile apps or kiosk software (e.g. inspecting kiosk apps to identify which payment terminal protocols or dispensor APIs they use).
- Scanning frontend web bundles for leaked API keys, staging URLs, or authorization tokens.
- Performing pre-deployment code auditing on internal payment microservices.

## Directory Structure
```
reverse-skill/
├── SKILL.md
└── scripts/
    └── run_reverse_router.py   # Static analysis, string extractor & secret scanner
```

## Quick Start / Execution

### 1. Escanear un Archivo o Bundle de Código (Detección de Secretos y APIs)
```bash
python skills/reverse-skill/scripts/run_reverse_router.py --target "assets/app_bundle.js" --extract-secrets --extract-urls
```

### 2. Inspeccionar una Aplicación o Carpeta de Proyecto
```bash
python skills/reverse-skill/scripts/run_reverse_router.py --target "tools/" --format markdown --output-file "data/security_audit_tools.md"
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--target` | string | **Requerido** | Ruta a un archivo (.js, .py, .apk, .bin) o directorio a auditar. |
| `--extract-secrets`| flag | `True` | Busca patrones de tokens (Bearer, AWS, Stripe, Conekta, STP, API keys). |
| `--extract-urls` | flag | `True` | Extrae todos los endpoints y URLs encontrados. |
| `--format` | choice | `markdown` | Formato de salida: `markdown`, `json`. |
| `--output-file` | string | `None` | Ruta para guardar el reporte de auditoría. |

## Safe Execution Guardrails
El runner opera en modo estático (*passive static analysis*). No ejecuta binarios desconocidos ni inyecta código, asegurando compatibilidad completa y seguridad dentro de entornos corporativos.
