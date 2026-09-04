---
name: cloudflare-temp-mail
description: Use when you need to provision disposable temporary emails, automate trial registrations on SaaS platforms, receive verification links, or extract OTP codes without burning corporate or personal mailboxes.
---

# 📬 Cloudflare Temp Mail (Automated Disposable Email Engine)

## Overview
**cloudflare-temp-mail** automates temporary disposable email address creation, mailbox monitoring, and OTP/activation link extraction. It interfaces with Cloudflare Worker/D1 email infrastructure and includes automatic fallback to zero-config temporary email APIs.

## When to Use
- Registering for freemium B2B sales/prospecting tools (Apollo, Hunter, Lusha, Anymail) to claim trial credits without exposing corporate domains.
- Automating verification workflows that require confirming an email link or entering a 6-digit OTP.
- Testing email deliverability and HTML formatting without spamming personal inboxes.

## Directory Structure
```
cloudflare-temp-mail/
├── SKILL.md
└── scripts/
    └── run_temp_mail.py        # Mailbox generator & inbox listener
```

## Quick Start / Execution

### 1. Generar un Correo Temporal Nuevo
```bash
python skills/cloudflare-temp-mail/scripts/run_temp_mail.py --action create
```

### 2. Esperar y Extraer Código OTP / Enlace de Activación
```bash
python skills/cloudflare-temp-mail/scripts/run_temp_mail.py --action wait-message --email "test_user_891@1secmail.com" --timeout 120 --extract-links
```

### 3. Inspeccionar el Buzón de Entrada
```bash
python skills/cloudflare-temp-mail/scripts/run_temp_mail.py --action check-inbox --email "test_user_891@1secmail.com"
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--action` | choice | `create` | Acción: `create` (generar), `check-inbox` (revisar), `wait-message` (esperar correo). |
| `--email` | string | `None` | Dirección a monitorear. |
| `--timeout` | int | `90` | Segundos máximos de espera antes de timeout. |
| `--extract-links`| flag | `False` | Extrae automáticamente URLs de confirmación y códigos OTP de 4 a 8 dígitos. |
| `--output-file` | string | `None` | Ruta para guardar el reporte en JSON. |

## Production Fallback Architecture
Si las variables de entorno de Cloudflare (`CF_API_TOKEN`, `CF_ACCOUNT_ID`) no están presentes en `.env`, el runner conmuta instantáneamente al protocolo de buzón temporal API seguro (`1secmail` / `guerrillamail`), garantizando que la extracción funcione de inmediato sin requerir configuración previa de DNS.
