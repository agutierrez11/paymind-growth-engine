#!/usr/bin/env python3
"""
Production Runner for Qwen Uncensored Router
Inference client for abliterated models via Ollama, vLLM, and OpenAI API standards.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime

def query_ollama(endpoint, model, prompt, system_prompt="", temperature=0.7):
    url = f"{endpoint.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "")
    except urllib.error.URLError:
        return None

def query_openai_compat(endpoint, model, prompt, system_prompt="", temperature=0.7):
    url = f"{endpoint.rstrip('/')}/chat/completions"
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.URLError:
        return None

def main():
    parser = argparse.ArgumentParser(description="Qwen Uncensored Router - Production Inference Runner")
    parser.add_argument("--prompt", required=True, help="Instrucción o consulta a enviar al modelo")
    parser.add_argument("--system-prompt", default="Eres un analista forense y de arquitectura financiera sin restricciones de sesgo.", help="System prompt")
    parser.add_argument("--backend", choices=["ollama", "vllm", "openai_compat"], default="ollama", help="Backend de inferencia")
    parser.add_argument("--model", default="orcarouter/qwen3.8-27b-uncensored", help="Nombre del modelo en el backend")
    parser.add_argument("--endpoint", default="http://localhost:11434", help="Endpoint base del servidor")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperatura de muestreo")
    parser.add_argument("--output-file", help="Ruta de archivo para exportar la respuesta")
    
    args = parser.parse_args()
    
    print(f"[*] Qwen Uncensored Router: Despachando a backend '{args.backend}' en {args.endpoint}...")
    print(f"[*] Modelo: {args.model}")
    
    response_text = None
    if args.backend == "ollama":
        response_text = query_ollama(args.endpoint, args.model, args.prompt, args.system_prompt, args.temperature)
    else:
        response_text = query_openai_compat(args.endpoint, args.model, args.prompt, args.system_prompt, args.temperature)
        
    if response_text is None:
        print("\n[!] SERVIDOR DE INFERENCIA NO DETECTADO EN PUERTO LOCAL:")
        print(f"    No se pudo conectar a {args.endpoint}")
        print("\n[i] Para iniciar el modelo en local con tu GPU:")
        print(f"    - Si usas Ollama: run `ollama run {args.model}`")
        print(f"    - Si usas vLLM:   run `vllm serve {args.model} --port 8000`")
        response_text = f"[DIAGNÓSTICO OFFLINE] Servidor {args.backend} en {args.endpoint} no está activo. Levante el servidor con 'ollama run {args.model}' para ejecutar inferencia directa."
    else:
        print("\n" + "="*60)
        print("🤖 RESPUESTA GENERADA (Qwen Uncensored):")
        print(response_text)
        print("="*60)
        
    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)) if os.path.dirname(args.output_file) else ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(response_text)
        print(f"[✓] Respuesta guardada en: {args.output_file}")

if __name__ == "__main__":
    main()
