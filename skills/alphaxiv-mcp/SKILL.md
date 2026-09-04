---
name: alphaxiv-mcp
description: Use when you need to search, retrieve, and analyze arXiv research papers, extract technical methodologies, or access linked GitHub repositories via the alphaXiv Model Context Protocol (MCP) server.
---

# 📚 alphaXiv MCP (Scientific Research & ArXiv Paper Intelligence Engine)

## Overview
**alphaxiv-mcp** integrates with alphaXiv's Model Context Protocol (MCP) and the arXiv API. It allows AI agents and developers to search academic literature, download paper abstracts, extract technical methodology sections, and locate linked open-source code repositories.

## When to Use
- Researching state-of-the-art architectures (e.g. LLM routing, TTS voice cloning algorithms, agentic workflows).
- Locating official GitHub implementations and benchmark code directly tied to published research papers.
- Summarizing complex academic papers into executive briefs.

## Directory Structure
```
alphaxiv-mcp/
├── SKILL.md
└── scripts/
    └── run_alphaxiv_mcp.py     # MCP client & arXiv search runner
```

## Quick Start / Execution

### 1. Búsqueda de Papers por Tema
```bash
python skills/alphaxiv-mcp/scripts/run_alphaxiv_mcp.py --query "zero shot voice cloning tts" --max-results 3
```

### 2. Obtener Detalles de un Paper por ID
```bash
python skills/alphaxiv-mcp/scripts/run_alphaxiv_mcp.py --paper-id "2402.01234" --format markdown
```

## CLI Parameters
| Parámetro | Tipo | Default | Descripción |
| :--- | :--- | :--- | :--- |
| `--query` | string | `None` | Términos de búsqueda científica. |
| `--paper-id` | string | `None` | ID de arXiv (ej: `2310.06825`). |
| `--max-results`| int | `3` | Número de papers a recuperar. |
| `--format` | choice | `markdown` | Formato de salida: `markdown`, `json`. |
| `--output-file`| string | `None` | Ruta de exportación. |

## MCP Endpoint Integration
- Soporta conexión directa a `https://api.alphaxiv.org/mcp/v1` para clientes MCP (Claude Code, Cursor, Antigravity) con fallback automático a la API oficial de arXiv.
