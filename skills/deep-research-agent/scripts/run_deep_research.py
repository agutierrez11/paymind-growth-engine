#!/usr/bin/env python3
"""
Production Runner for Deep Research Agent
Autonomous recursive intelligence search & briefing engine.
"""

import os
import sys
import re
import json
import argparse
import urllib.request
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def fetch_page_text(url, timeout=5):
    """Descarga y extrae texto limpio de una página web."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                return ""
            html = resp.read().decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                tag.decompose()
                
            text = " ".join(soup.stripped_strings)
            return text[:4000] # Limitar a primeros 4000 caracteres de alta densidad
    except Exception:
        return ""

def search_web_queries(query, max_results=5):
    """Busca en la web mediante el endpoint público de DuckDuckGo HTML."""
    encoded = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml"
        }
    )
    
    results = []
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            
            for item in soup.select(".result"):
                link_el = item.select_one(".result__snippet")
                title_el = item.select_one(".result__title a")
                
                if title_el and link_el:
                    raw_href = title_el.get("href", "")
                    # Desempacar redirect de DDG
                    parsed = urllib.parse.urlparse(raw_href)
                    qs = urllib.parse.parse_qs(parsed.query)
                    actual_url = qs.get("uddg", [raw_href])[0]
                    
                    if actual_url.startswith("http"):
                        results.append({
                            "title": title_el.get_text(strip=True),
                            "snippet": link_el.get_text(strip=True),
                            "url": actual_url
                        })
                        if len(results) >= max_results:
                            break
    except Exception as e:
        print(f"  [!] Nota en búsqueda web: {e}")
        
    return results

def run_deep_research_pipeline(objective, depth=2, max_sources=6):
    print(f"[*] Iniciando Deep Research sobre: '{objective}'")
    print(f"[*] Profundidad: {depth} | Límite de fuentes: {max_sources}")
    
    # 1. Desglose de sub-preguntas (Hypothesis Generation)
    subqueries = [
        objective,
        f"{objective} modelo operacion problemas regulacion",
        f"{objective} directores finanzas cobranza cfo linkedin"
    ][:depth + 1]
    
    gathered_sources = []
    seen_urls = set()
    
    for sq in subqueries:
        print(f"\n  [🔎] Buscando hipótesis: '{sq}'")
        found = search_web_queries(sq, max_results=max_sources // len(subqueries) + 1)
        for f in found:
            if f["url"] not in seen_urls and len(gathered_sources) < max_sources:
                seen_urls.add(f["url"])
                print(f"    -> Extrayendo contenido de: {f['url']}")
                page_text = fetch_page_text(f["url"])
                gathered_sources.append({
                    "title": f["title"],
                    "url": f["url"],
                    "snippet": f["snippet"],
                    "body_excerpt": page_text[:1200]
                })
                
    # 2. Análisis y Síntesis de Evidencia
    print(f"\n[*] Procesando {len(gathered_sources)} fuentes analizadas...")
    
    key_facts = []
    regulatory_cites = []
    entities_detected = set()
    
    for src in gathered_sources:
        text = src["snippet"] + " " + src["body_excerpt"]
        
        # Extracción de menciones regulatorias
        regs = re.findall(r"(?:Circular|Anexo|Ley|CNBV|Banxico|CONDUSEF|SAT|3DS|SPEI|STP)\s+[A-Za-z0-9/.-]+", text, re.IGNORECASE)
        for r in regs:
            regulatory_cites.append(r.strip())
            
        # Extracción de nombres/títulos
        titles = re.findall(r"(?:Director|Gerente|CFO|Head|Presidente)\s+(?:de\s+)?[A-Za-zÁÉÍÓÚáéíóúñ]+(?:\s+[A-Za-zÁÉÍÓÚáéíóúñ]+)?", text)
        for t in titles:
            entities_detected.add(t.strip())
            
        if len(src["snippet"]) > 40:
            key_facts.append(src["snippet"])

    # 3. Construcción del Dossier Estructurado
    report = {
        "timestamp": datetime.now().isoformat(),
        "objective": objective,
        "depth": depth,
        "total_sources_scanned": len(gathered_sources),
        "key_entities": list(entities_detected)[:8],
        "regulatory_findings": list(set(regulatory_cites))[:8],
        "sources": gathered_sources
    }
    
    return report

def main():
    parser = argparse.ArgumentParser(description="Deep Research Agent - Production Intelligence Runner")
    parser.add_argument("--query", required=True, help="Objetivo o pregunta de investigación")
    parser.add_argument("--depth", type=int, default=2, choices=[1, 2, 3], help="Profundidad recursiva")
    parser.add_argument("--max-sources", type=int, default=6, help="Máximo número de fuentes a consultar")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Formato de salida")
    parser.add_argument("--output-file", help="Ruta de archivo para guardar el informe")
    
    args = parser.parse_args()
    
    data = run_deep_research_pipeline(args.query, args.depth, args.max_sources)
    
    if args.format == "json":
        output = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        output = f"# 🕵️ EXPEDIENTE DEEP RESEARCH: {data['objective']}\n\n"
        output += f"> **Fecha:** {data['timestamp']} | **Profundidad:** {data['depth']} | **Fuentes:** {data['total_sources_scanned']}\n\n"
        output += "## 1. 🎯 Resumen Ejecutivo y Hallazgos Clave\n"
        for s in data["sources"][:3]:
            output += f"- **{s['title']}:** {s['snippet']}\n"
            
        if data["key_entities"]:
            output += "\n## 2. 👤 Roles y Decisores Detectados\n"
            for e in data["key_entities"]:
                output += f"* `{e}`\n"
                
        if data["regulatory_findings"]:
            output += "\n## 3. ⚖️ Puntos Regulatorios y de Cumplimiento\n"
            for r in data["regulatory_findings"]:
                output += f"* `{r}`\n"
                
        output += "\n## 4. 🌐 Fuentes y Evidencia Consultada\n"
        for i, s in enumerate(data["sources"], 1):
            output += f"{i}. [{s['title']}]({s['url']})\n"
            if s.get("body_excerpt"):
                clean_excerpt = s['body_excerpt'][:300].replace('\n', ' ')
                output += f"   > *\"{clean_excerpt}...\"*\n"

    print("\n" + "="*60)
    print(output)
    print("="*60)
    
    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)), exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n[✓] Expediente Deep Research guardado en: {args.output_file}")

if __name__ == "__main__":
    main()
