---
name: voice-studio
description: Use when you need to clone voices, generate high-fidelity speech (TTS), create audio workouts, or produce personalized voice notes for sales outreach or gym coaching without cloud API costs.
---

# 🎙️ Voice Studio (Universal Voice Cloning & High-Fidelity Audio Engine)

## Overview
**voice-studio** provides local, zero-subscription voice synthesis, zero-shot voice cloning, and audio production. Inspired by ElevenLabs and built for high-volume operational environments (like **CPS Gym** workout routines, member notifications, and cold outreach voice drops).

## When to Use
- Producing workout routines, rep counts, and coaching audio for **CPS Gym**.
- Generating personalized WhatsApp voice notes for C-level executives or member renewals.
- Automating reception and membership reminder messages with human cadence in Spanish.

## Directory Structure
```
voice-studio/
├── SKILL.md
└── scripts/
    └── run_voice_studio.py     # Local audio generation & cloning runner
```

## Quick Start / Execution

### 1. Generar Audio de Entrenamiento para CPS Gym
```bash
python skills/voice-studio/scripts/run_voice_studio.py --text "¡Venga equipo CPS! Iniciamos circuito de fuerza. 45 segundos de sentadilla profunda, listos... ¡ahora!" --output-audio "data/gym_circuito_1.wav" --voice-preset "coach_energetico"
```

### 2. Mensaje de Cobranza / Bienvenida Personalizado
```bash
python skills/voice-studio/scripts/run_voice_studio.py --text "Hola Carlos, te recordamos que tu membresía en CPS Gym vence este viernes. Renueva hoy para mantener tu tarifa congelada." --output-audio "data/recordatorio_carlos.wav" --voice-preset "recepcion_amable"
```

### 3. Clonación de Voz con Muestra (Zero-Shot Cloning)
```bash
python skills/voice-studio/scripts/run_voice_studio.py --text "Texto a sintetizar..." --speaker-ref "assets/sample_coach.wav" --output-audio "data/audio_clonado.wav"
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--text` | string | **Requerido** | Texto a convertir en voz (soporta pausas con comas y signos). |
| `--output-audio`| string | `output.wav` | Ruta de salida del archivo de audio (.wav). |
| `--voice-preset`| choice | `coach_energetico` | Preset de entonación: `coach_energetico`, `recepcion_amable`, `formal_b2b`. |
| `--speaker-ref` | string | `None` | Ruta a archivo .wav de muestra (5-15 seg) para clonación zero-shot. |
| `--speed` | float | `1.0` | Velocidad de reproducción (0.8 a 1.4). |

## Production Audio Formats
- Genera archivos PCM WAV estándar (16-bit, 24kHz/44.1kHz) compatibles con WhatsApp, reproductores de audio y sistemas de megafonía de gimnasios.

## Hardware Acceleration
- Si se detecta GPU NVIDIA CUDA en el sistema, la síntesis se realiza por hardware acelerado. En caso contrario, conmuta de forma transparente al motor optimizado por CPU.
