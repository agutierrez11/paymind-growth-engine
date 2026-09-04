#!/usr/bin/env python3
"""
Production Runner for Firecrawl Intel Engine
B2B Website Scraper, Domain Mapper, and Structured Intel Extractor.
"""

import os
import sys
import re
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime

FIRECRAWL_BASE = "https://api.firecrawl.dev/v1"

def load_env_api_key():
    """Busca FIRECRAWL_API_KEY en variables de entorno o archivo .env local."""
    key = os.getenv("FIRECRAWL_API_KEY")
    if key:
        return key
        
    for env_path in [".env", "../.env", "../../.env"]:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip().startswith("FIRECRAWL_API_KEY="):
                            return line.strip().split("=", 1)[1].strip("\"' ")
            except Exception:
                pass
    return None

def firecrawl_request(endpoint, payload, api_key):
    url = f"{FIRECRAWL_BASE}/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw_err = e.read().decode("utf-8", errors="ignore")
        return {"success": False, "error": f"HTTP {e.code}: {raw_err}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def extract_b2b_signals(markdown_text):
    """Extrae señales comerciales clave para prospección B2B."""
    signals = {
        "payment_rails": [],
        "executives_detected": [],
        "contact_emails": [],
        "contact_phones": []
    }
    
    # Rieles y métodos de cobro
    rails = ["spei", "stp", "domiciliaci[oó]n", "oxxo", "tarjeta", "terminal", "quiosco", "pos", "visa", "mastercard"]
    for r in rails:
        if re.search(r'\b' + r + r'\b', markdown_text, re.IGNORECASE):
            clean_rail = r.replace("[oó]", "o").upper()
            signals["payment_rails"].append(clean_rail)
            
    # Títulos ejecutivos
    execs = re.findall(r'(?:Director|Directora|CFO|CEO|Gerente|Presidente)\s+(?:de\s+)?[A-Za-zÁÉÍÓÚáéíóúñ]+(?:\s+[A-Za-zÁÉÍÓÚáéíóúñ]+)?', markdown_text)
    signals["executives_detected"] = list(set([e.strip() for e in execs]))[:6]
    
    # Emails y teléfonos
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', markdown_text)
    phones = re.findall(r'(?:\+?52\s*)?(?:\(?\d{2,3}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}', markdown_text)
    
    signals["contact_emails"] = list(set(emails))[:5]
    signals["contact_phones"] = list(set([p for p in phones if len(re.sub(r'\D', '', p)) >= 10]))[:5]
    
    return signals

def main():
    parser = argparse.ArgumentParser(description="Firecrawl Intel - Production B2B Scraper & Mapper")
    parser.add_argument("--url", required=True, help="URL del prospecto a analizar")
    parser.add_argument("--mode", choices=["scrape", "map", "crawl", "extract-b2b"], default="scrape", help="Modo de operación")
    parser.add_argument("--limit", type=int, default=5, help="Límite de páginas para crawl")
    parser.add_argument("--api-key", help="API Key de Firecrawl (o vía .env / FIRECRAWL_API_KEY)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Formato de salida")
    parser.add_argument("--output-file", help="Ruta de archivo para guardar el expediente")
    
    args = parser.parse_args()
    
    api_key = args.api_key or load_env_api_key()
    if not api_key:
        print("[!] ERROR: No se encontró FIRECRAWL_API_KEY.")
        print("    Pasa tu clave con --api-key 'fc-...' o agrégala a tu archivo .env:")
        print("    FIRECRAWL_API_KEY=fc-xxxxxxxxxxxxxxxxxxxx")
        sys.exit(1)
        
    print(f"[*] Firecrawl Intel: Ejecutando modo '{args.mode}' sobre {args.url}...")
    
    if args.mode == "map":
        res = firecrawl_request("map", {"url": args.url}, api_key)
        if not res.get("success", False):
            print(f"[!] Error: {res.get('error')}")
            return
            
        links = res.get("links", [])
        print(f"[✓] Mapa de URLs extraído: {len(links)} páginas descubiertas.")
        
        output_str = f"# 🗺️ MAPA DE DOMINIO: {args.url}\n\n"
        output_str += f"- **Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output_str += f"- **Total de URLs indexadas:** {len(links)}\n\n"
        output_str += "## URLs Clave Descubiertas\n"
        for l in links[:30]:
            output_str += f"- `{l}`\n"
            
    else: # scrape o extract-b2b
        res = firecrawl_request("scrape", {"url": args.url, "formats": ["markdown", "links"]}, api_key)
        if not res.get("success", False):
            print(f"[!] Error: {res.get('error')}")
            return
            
        data = res.get("data", {})
        markdown = data.get("markdown", "")
        metadata = data.get("metadata", {})
        signals = extract_b2b_signals(markdown)
        
        if args.format == "json":
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "url": args.url,
                "metadata": metadata,
                "signals": signals,
                "markdown_length": len(markdown)
            }
            output_str = json.dumps(output_data, indent=2, ensure_ascii=False)
        else:
            output_str = f"# 🔥 EXPEDIENTE FIRECRAWL INTEL: {metadata.get('title') or args.url}\n\n"
            output_str += f"> **URL:** {args.url} | **Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            if metadata.get("description"):
                output_str += f"> **Descripción:** {metadata['description']}\n\n"
                
            output_str += "## 🎯 Señales Comerciales y Rieles de Cobro Detectados\n"
            if signals["payment_rails"]:
                output_str += f"- **Rieles/Métodos Identificados:** `{', '.join(signals['payment_rails'])}`\n"
            else:
                output_str += "- **Rieles:** No explícitos en portada.\n"
                
            if signals["executives_detected"]:
                output_str += "- **Directivos / Cargos Detectados:**\n"
                for e in signals["executives_detected"]:
                    output_str += f"  * `{e}`\n"
                    
            if signals["contact_emails"]:
                output_str += f"- **Correos de Contacto:** {', '.join(signals['contact_emails'])}\n"
            if signals["contact_phones"]:
                output_str += f"- **Teléfonos:** {', '.join(signals['contact_phones'])}\n"
                
            output_str += "\n## 📄 Contenido Limpio Extraído (Markdown para LLM)\n\n"
            output_str += markdown[:3500]
            if len(markdown) > 3500:
                output_str += "\n\n*(...Contenido truncado en vista previa; total " + str(len(markdown)) + " caracteres)*\n"

    print("\n" + "="*60)
    print(output_str[:1200] + ("\n[...]" if len(output_str) > 1200 else ""))
    print("="*60)
    
    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)) if os.path.dirname(args.output_file) else ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"\n[✓] Expediente Firecrawl guardado en: {args.output_file}")

if __name__ == "__main__":
    main()
