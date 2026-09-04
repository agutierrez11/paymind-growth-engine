#!/usr/bin/env python3
"""
Production Runner for alphaXiv MCP Client
Queries scientific literature, arXiv papers, and linked repositories.
"""

import os
import re
import json
import argparse
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) alphaXiv-MCP-Client/1.0"
ARXIV_API = "http://export.arxiv.org/api/query"

def search_arxiv(query=None, id_list=None, max_results=3):
    params = {"max_results": str(max_results)}
    if query:
        params["search_query"] = f"all:{query}"
    if id_list:
        params["id_list"] = id_list
        
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    
    results = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read().decode("utf-8")
            root = ET.fromstring(xml_data)
            
            # Namespace de Atom
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            
            for entry in root.findall("atom:entry", ns):
                title = entry.find("atom:title", ns)
                summary = entry.find("atom:summary", ns)
                published = entry.find("atom:published", ns)
                paper_id = entry.find("atom:id", ns)
                
                authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns) if a.find("atom:name", ns) is not None]
                
                pdf_url = None
                for link in entry.findall("atom:link", ns):
                    if link.attrib.get("title") == "pdf":
                        pdf_url = link.attrib.get("href")
                        
                results.append({
                    "id": paper_id.text if paper_id is not None else "",
                    "title": title.text.strip().replace("\n", " ") if title is not None else "",
                    "authors": authors[:5],
                    "published": published.text[:10] if published is not None else "",
                    "pdf_url": pdf_url or (paper_id.text.replace("abs", "pdf") if paper_id is not None else ""),
                    "summary": summary.text.strip().replace("\n", " ") if summary is not None else ""
                })
    except Exception as e:
        print(f"[!] Error consultando arXiv: {e}")
        
    return results

def main():
    parser = argparse.ArgumentParser(description="alphaXiv MCP - Scientific Literature Search Runner")
    parser.add_argument("--query", help="Consulta de búsqueda científica")
    parser.add_argument("--paper-id", help="ID específico de arXiv (ej: 2310.06825)")
    parser.add_argument("--max-results", type=int, default=3, help="Número de papers a recuperar")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Formato de salida")
    parser.add_argument("--output-file", help="Ruta de archivo para guardar resultados")
    
    args = parser.parse_args()
    
    if not args.query and not args.paper-id if hasattr(args, "paper-id") else (not args.query and not args.paper_id):
        parser.error("Debe proporcionar --query o --paper-id")
        
    p_id = getattr(args, "paper_id", None)
    print(f"[*] Consultando papers arXiv: Query='{args.query}' | ID='{p_id}'...")
    papers = search_arxiv(query=args.query, id_list=p_id, max_results=args.max_results)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "query": args.query or p_id,
        "total_results": len(papers),
        "papers": papers
    }
    
    if args.format == "json":
        output = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        output = f"# 📚 ALPHAXIV / ARXIV RESEARCH BRIEF: {args.query or p_id}\n\n"
        output += f"- **Fecha:** {report['timestamp']}\n"
        output += f"- **Total de Papers Recuperados:** {report['total_results']}\n\n"
        
        for i, p in enumerate(papers, 1):
            output += f"## {i}. {p['title']}\n"
            output += f"- **Autores:** {', '.join(p['authors'])}\n"
            output += f"- **Publicado:** {p['published']}\n"
            output += f"- **PDF:** [{p['pdf_url']}]({p['pdf_url']})\n"
            output += f"- **Resumen Ejecutivo:**\n  > *{p['summary'][:350]}...*\n\n"

    print("\n" + "="*60)
    print(output)
    print("="*60)
    
    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)) if os.path.dirname(args.output_file) else ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[✓] Resultados guardados en: {args.output_file}")

if __name__ == "__main__":
    main()
