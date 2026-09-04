---
name: gtm-outreach-swarm
description: Use when you need to research B2B target companies, extract operational pain points, and generate multi-variant personalized cold outreach emails with anti-spam deliverability auditing based on Shubham Saboo's GTM Outreach Agent.
---

# 🎯 GTM Outreach Swarm (Multi-Agent B2B Personalization & Deliverability Engine)

## Overview
**gtm-outreach-swarm** is a specialized multi-agent pipeline based on **Shubham Saboo's GTM Outreach Architecture**. It replaces generic templates with an autonomous swarm that profiles the target account, maps their technical friction, drafts consultative emails (120-150 words), and audits deliverability to prevent spam filters.

## When to Use
- Generating personalized outreach sequences for the **72 Wish List accounts of Toku** ($2,000 USD / meeting).
- Crafting executive cold outreach for gas station directors, AMPES partners, and Odoo ERP integrators in **PayMind**.
- Auditing existing sales copies to remove spam trigger words and calculate open-rate probability.

## Swarm Architecture
1. **Target Profiler Agent:** Ingests the company name, sector, and known operational friction (e.g. Circular Banxico 14/2017, Anexo 30 SAT, payroll deduction failures).
2. **Value Prop Matcher Agent:** Formulates the exact technical resolution (multi-rail STP, predictive retry, self-service adquirencia).
3. **Copywriting Agent:** Drafts the email using 4 battle-tested styles: `Consultative`, `Cold`, `Professional`, or `Casual`.
4. **Deliverability Auditor Agent:** Scans for spam keywords, verifies subject line length (< 45 chars), and ensures a low-friction CTA.

## Directory Structure
```
gtm-outreach-swarm/
├── SKILL.md
└── scripts/
    └── run_gtm_outreach.py     # Multi-agent outreach runner & deliverability auditor
```

## Quick Start / Execution

### 1. Generar Outreach para una Cuenta de Toku (Ej: Credifiel)
```bash
python skills/gtm-outreach-swarm/scripts/run_gtm_outreach.py --company "Credifiel" --target-role "Director de Cobranza" --pain-point "Desfase en retención quincenal de dependencias públicas y rebote de domiciliación bancaria" --value-prop "Segundo riel de domiciliación CLABE vía STP con reintentos predictivos" --style Consultative
```

### 2. Generar Outreach para Gasolineras PayMind (Ej: Grupo G500 / OxxoGas)
```bash
python skills/gtm-outreach-swarm/scripts/run_gtm_outreach.py --company "Grupo Hidrocarburos del Norte" --target-role "Director de Operaciones" --pain-point "Comisión bancaria del 2% sobre el PVP con 40% de IEPS e IVA" --value-prop "Terminal adquirente integrada que reduce la tasa efectiva y cumple Anexo 30" --style Cold
```

### 3. Auditar un Copy Existente para Entrega Anti-Spam
```bash
python skills/gtm-outreach-swarm/scripts/run_gtm_outreach.py --audit-only --subject "Oportunidad de ahorro 100% garantizada urgente" --body "Texto del correo..."
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--company` | string | `None` | Nombre de la empresa objetivo. |
| `--target-role`| string | `CFO` | Cargo del tomador de decisión objetivo. |
| `--pain-point` | string | `None` | Problema operativo o regulatorio específico. |
| `--value-prop` | string | `None` | Propuesta de solución concreta. |
| `--style` | choice | `Consultative` | Estilo: `Consultative`, `Cold`, `Professional`, `Casual`. |
| `--output-file`| string | `None` | Ruta de guardado (JSON / Markdown). |
