# Qwen 3.8 27B Uncensored (OrcaRouter Abliterated Model)

## Model Overview
- **Base Architecture:** Qwen 3.8 27B Parameter Transformer
- **Abliteration Method:** Orthogonal refusal vector removal across residual streams.
- **Provider:** OrcaRouter (`orcarouter/Qwen3.8-27B-Uncensored`)
- **Supported Deployments:**
  - Ollama (GGUF Quantization Q4_K_M / Q8_0)
  - vLLM (FP8 / AWQ / BF16)
  - Hugging Face Inference API / OpenAI Compatible Endpoint

## Hardware Requirements
- **VRAM Requerido:** 16 GB (FP8 / Q4_K_M) - 28 GB (BF16)
- **Context Window:** 32,768 tokens (hasta 128k con RoPE scaling)
- **Local Runner:** `skills/qwen-uncensored-router/scripts/run_qwen_inference.py`
