#!/usr/bin/env python3
"""
Production Runner for Reverse-Skill Router
Static analysis, secrets scanner, and reverse engineering router.
"""

import os
import re
import json
import argparse
from datetime import datetime

SECRET_PATTERNS = [
    ("AWS_ACCESS_KEY", r"AKIA[0-9A-Z]{16}", "HIGH"),
    ("STRIPE_API_KEY", r"(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24,34}", "CRITICAL"),
    ("CONEKTA_KEY", r"key_[0-9a-zA-Z]{20,30}", "CRITICAL"),
    ("GENERIC_BEARER", r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}", "HIGH"),
    ("JWT_TOKEN", r"eyJ[a-zA-Z0-9_\-]+\.eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+", "HIGH"),
    ("PASSWORD_IN_CODE", r"(?:password|passwd|secret|token)\s*[:=]\s*['\"][^'\"]{6,}['\"]", "MEDIUM"),
    ("PRIVATE_KEY_HEADER", r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----", "CRITICAL")
]

URL_PATTERN = re.compile(r'https?://[a-zA-Z0-9\.\-_/:\?=%&#]+')

def analyze_file(filepath, extract_secrets=True, extract_urls=True):
    findings = {
        "file": filepath,
        "secrets": [],
        "urls": []
    }
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        if extract_secrets:
            for name, pattern, severity in SECRET_PATTERNS:
                matches = re.finditer(pattern, content)
                for m in matches:
                    snippet = m.group(0)
                    masked = snippet[:6] + "..." + snippet[-4:] if len(snippet) > 10 else "***"
                    findings["secrets"].append({
                        "type": name,
                        "severity": severity,
                        "match": masked,
                        "span": [m.start(), m.end()]
                    })
                    
        if extract_urls:
            found_urls = set(re.findall(URL_PATTERN, content))
            findings["urls"] = list(found_urls)[:25] # Limitar a primeras 25 URLs por archivo
            
    except Exception as e:
        findings["error"] = str(e)
        
    return findings

def scan_target(target_path, extract_secrets=True, extract_urls=True):
    results = []
    
    if os.path.isfile(target_path):
        results.append(analyze_file(target_path, extract_secrets, extract_urls))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            if any(ign in root for ign in [".git", "node_modules", "__pycache__", ".venv"]):
                continue
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in [".js", ".py", ".html", ".json", ".ts", ".jsx", ".tsx", ".env", ".yaml", ".yml", ".txt"]:
                    full_p = os.path.join(root, f)
                    res = analyze_file(full_p, extract_secrets, extract_urls)
                    if res["secrets"] or res["urls"]:
                        results.append(res)
    return results

def main():
    parser = argparse.ArgumentParser(description="Reverse-Skill Router - Static Code & Secrets Auditor")
    parser.add_argument("--target", required=True, help="Ruta de archivo o directorio a analizar")
    parser.add_argument("--extract-secrets", action="store_true", default=True, help="Buscar secretos y credenciales")
    parser.add_argument("--extract-urls", action="store_true", default=True, help="Buscar endpoints y URLs")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Formato del informe")
    parser.add_argument("--output-file", help="Ruta de archivo para guardar el informe")
    
    args = parser.parse_args()
    
    print(f"[*] Analizando estáticamente: {args.target}")
    scans = scan_target(args.target, args.extract_secrets, args.extract_urls)
    
    total_secrets = sum(len(s.get("secrets", [])) for s in scans)
    total_urls = sum(len(s.get("urls", [])) for s in scans)
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "target": args.target,
        "files_scanned": len(scans),
        "total_secrets_detected": total_secrets,
        "total_urls_detected": total_urls,
        "results": scans
    }
    
    if args.format == "json":
        output = json.dumps(report_data, indent=2, ensure_ascii=False)
    else:
        output = f"# 🛡️ REPORTE DE AUDITORÍA ESTÁTICA: {args.target}\n\n"
        output += f"- **Fecha:** {report_data['timestamp']}\n"
        output += f"- **Archivos con hallazgos:** {report_data['files_scanned']}\n"
        output += f"- **Secretos potenciales detectados:** {total_secrets}\n"
        output += f"- **Endpoints / URLs encontrados:** {total_urls}\n\n"
        
        if total_secrets > 0:
            output += "## 🚨 Secretos y Credenciales Detectados\n\n"
            output += "| Archivo | Tipo de Secreto | Severidad | Muestra |\n| :--- | :--- | :--- | :--- |\n"
            for r in scans:
                for s in r.get("secrets", []):
                    rel_p = os.path.basename(r['file'])
                    output += f"| `{rel_p}` | `{s['type']}` | **{s['severity']}** | `{s['match']}` |\n"
            output += "\n"
            
        output += "## 🌐 Endpoints y APIs Identificadas\n\n"
        for r in scans[:5]:
            if r.get("urls"):
                rel_p = os.path.basename(r['file'])
                output += f"### Archivo: `{rel_p}`\n"
                for u in r["urls"][:6]:
                    output += f"- `{u}`\n"
                    
    print("\n" + "="*60)
    print(output)
    print("="*60)
    
    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)) if os.path.dirname(args.output_file) else ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[✓] Informe de auditoría guardado en: {args.output_file}")

if __name__ == "__main__":
    main()
