---
name: gym-voice-agent
description: Use when you need to run an automated conversational voice agent for gym operations (CPS Gym), handling membership inquiries, class schedules, renewal objections, lead capture, and synthesizing audio responses based on Shubham Saboo's Voice Agent architecture.
---

# 🏋️ Gym Voice Agent (Conversational Reception & Voice Support for CPS Gym)

## Overview
**gym-voice-agent** is an autonomous conversational voice agent tailored for gym and fitness club operations (**CPS Gym**), built on **Shubham Saboo's Customer Support Voice Agent architecture**. It resolves member inquiries, overcomes pricing objections, captures prospective leads, and synthesizes audio responses with human cadence.

## When to Use
- Automating incoming phone calls or WhatsApp voice messages for **CPS Gym**.
- Answering common member questions: plans, monthly pricing, student discounts, trainer bios, and class schedules (Spinning, Crossfit, Box).
- Overcoming cancellation/renewal objections and capturing prospect data (Name, WhatsApp, training goal).
- Generating audio files (.wav) for voice responses without cloud subscription fees.

## Directory Structure
```
gym-voice-agent/
├── SKILL.md
└── scripts/
    └── run_voice_agent.py      # Conversational dialogue engine & audio synthesizer
```

## Knowledge Base (CPS Gym Operations)
1. **Planes y Precios:**
   * Mensualidad Básica ($599 MXN / mes): Acceso a pesas y cardio.
   * Plan Total Black ($899 MXN / mes): Acceso a todas las clases grupales, regaderas, lockers y asesoría nutricional.
   * Day Pass ($99 MXN): Acceso por 1 día.
   * Estudiantes y Parejas: 15% de descuento presentando credencial vigente.
2. **Horarios de Operación:**
   * Lunes a Viernes: 06:00 AM - 10:30 PM
   * Sábados: 07:00 AM - 06:00 PM
   * Domingos: 08:00 AM - 02:00 PM
3. **Clases Grupales:**
   * Spinning: 07:00 AM y 07:00 PM
   * Cross Training / Funcional: 08:00 AM y 06:30 PM
   * Box Recreativo: 08:00 PM

## Quick Start / Execution

### 1. Consulta de Precios y Membresías (Respuesta con Audio)
```bash
python skills/gym-voice-agent/scripts/run_voice_agent.py --query "¿Cuánto cuesta la mensualidad y qué incluye?" --generate-audio --output-audio "data/respuesta_precios.wav"
```

### 2. Manejo de Objeción de Precio ("Está muy caro")
```bash
python skills/gym-voice-agent/scripts/run_voice_agent.py --query "Se me hace muy caro comparado con el gimnasio de la esquina" --persona "coach_motivacional"
```

### 3. Registro de Nuevo Prospecto / Lead Capture
```bash
python skills/gym-voice-agent/scripts/run_voice_agent.py --query "Quiero agendar una clase muestra para mañana en la tarde, me llamo Rodrigo y mi cel es 5512345678"
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--query` | string | **Requerido** | Pregunta o mensaje recibido del socio o prospecto. |
| `--persona` | choice | `recepcion_amable` | Tono del agente: `recepcion_amable`, `coach_motivacional`, `cobranza_firme`. |
| `--generate-audio`| flag | `False` | Genera archivo WAV de voz con la respuesta hablada. |
| `--output-audio` | string | `output_gym.wav` | Ruta de salida del audio generado. |
| `--format` | choice | `text` | Formato de salida: `text`, `json`. |
