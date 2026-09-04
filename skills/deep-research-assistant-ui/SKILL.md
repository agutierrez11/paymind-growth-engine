---
name: deep-research-assistant-ui
description: Use when you need to deploy or run an interactive Deep Research Assistant with a Next.js web UI, LangChain Deep Agents, real-time task planning (write_todos), and fully cited research reports based on Sumanth077/Hands-On-AI-Engineering.
---

# 🖥️ Deep Research Assistant UI (LangChain Deep Agents & Next.js Interface)

## Overview
**deep-research-assistant-ui** is the full-stack implementation of an interactive AI research agent based on **Sumanth077/Hands-On-AI-Engineering**. It combines a Next.js Deep Agents visual frontend with a FastAPI / LangChain Deep Agents backend, utilizing structured web search grounding (Liner/DuckDuckGo) to synthesize comprehensive, cited markdown reports.

## When to Use
- Running an interactive visual UI to watch an AI agent plan (`write_todos`), execute search queries, and cite sources in real time.
- Conducting structured, cited market research with visual progress tracking.
- Deploying a local web interface for non-technical team members to run deep investigations.

## Directory Structure
```
deep-research-assistant-ui/
├── SKILL.md
└── scripts/
    └── run_research_ui.py      # Launcher for backend agent and Next.js frontend
```

## Underlying Tool Location
- Source code lives in [`tools/hands-on-deep-research/`](file:///c:/Users/Antonio/.gemini/antigravity-ide/scratch/paymind-growth-engine/tools/hands-on-deep-research/):
  - `backend/`: FastAPI + LangChain Deep Agents + Liner Search Tool.
  - `frontend/`: Next.js 14 + Tailwind CSS + Deep Agents UI components.

## Quick Start / Execution

### 1. Ejecutar en Modo Headless / CLI Rápido
```bash
python skills/deep-research-assistant-ui/scripts/run_research_ui.py --mode cli --query "Análisis del mercado de SOFOMes en México y cobranza nómina"
```

### 2. Iniciar el Servidor Backend de Agentes
```bash
python skills/deep-research-assistant-ui/scripts/run_research_ui.py --mode backend --port 8000
```

### 3. Iniciar el Frontend Visual Next.js
```bash
python skills/deep-research-assistant-ui/scripts/run_research_ui.py --mode frontend --port 3000
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--mode` | choice | `cli` | Modo de ejecución: `cli` (consulta directa), `backend` (servidor FastAPI/LangGraph), `frontend` (Next.js UI). |
| `--query` | string | `None` | Pregunta de investigación (requerida en modo CLI). |
| `--port` | int | `8000` / `3000`| Puerto para el servidor backend o frontend. |
| `--output-file` | string | `None` | Ruta para guardar el reporte final en Markdown. |

## Production Architecture
- **Planificación:** Utiliza `TodoListMiddleware` para desglosar la investigación en tareas visibles antes de disparar búsquedas.
- **Citación:** Cada afirmación en el reporte final está respaldada por un número de fuente (`[1]`, `[2]`) verificado contra la respuesta cruda del buscador.
