---
name: qwen-uncensored-router
description: Use when you need to route prompts to abliterated or uncensored models (such as Qwen 3.8 27B Uncensored) via Ollama, vLLM, or OpenAI-compatible endpoints for red-teaming, unconstrained reasoning, or security auditing.
---

# 🔓 Qwen Uncensored Router (Abliterated Model Runner & Inference Router)

## Overview
**qwen-uncensored-router** manages prompt dispatching and inference routing to safety-abliterated models (specifically `orcarouter/Qwen3.8-27B-Uncensored`). It supports local runtime backends (Ollama GGUF, vLLM FP8/BF16) and remote OpenAI-compatible API gateways.

## When to Use
- Executing red-teaming and threat modeling simulations where standard models trigger false-positive refusals.
- Conducting unrestrained competitive and forensic analysis on corporate structures or defensive architectures.
- Running offline inference when internet connectivity is restricted.

## Directory Structure
```
qwen-uncensored-router/
├── SKILL.md
└── scripts/
    └── run_qwen_inference.py   # Ollama / vLLM / OpenAI API router
```

## Quick Start / Execution

### 1. Inferencia Local vía Ollama
```bash
python skills/qwen-uncensored-router/scripts/run_qwen_inference.py --prompt "Analiza los vectores de falla en la arquitectura de cobro de una SOFOM" --backend ollama
```

### 2. Inferencia vía vLLM o Endpoint Compatible con OpenAI
```bash
python skills/qwen-uncensored-router/scripts/run_qwen_inference.py --prompt "¿Qué debilidades de liquidez surgen con la Circular 14/2017?" --endpoint "http://localhost:8000/v1" --backend vllm
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--prompt` | string | **Requerido** | Prompt o consulta a procesar. |
| `--backend` | choice | `ollama` | Motor: `ollama`, `vllm`, `openai_compat`. |
| `--model` | string | `orcarouter/qwen3.8-27b-uncensored` | Identificador del modelo cargado en el runtime. |
| `--endpoint` | string | `http://localhost:11434` | URL base del servidor de inferencia. |
| `--temperature`| float | `0.7` | Creatividad y variabilidad de respuesta. |
| `--output-file`| string | `None` | Archivo para guardar la respuesta generada. |

## Fallback Mode
Si no hay un servidor Ollama o vLLM corriendo localmente en los puertos 11434 u 8000, el runner reporta los comandos exactos de inicio (`ollama run ...` o `vllm serve ...`) para que el usuario levante el servicio en su GPU en 1 comando.
