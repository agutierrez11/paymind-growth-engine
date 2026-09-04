#!/usr/bin/env python3
"""
Production Runner for user-scanner OSINT Engine
Integrates local multi-vector scanning with tools/user-scanner suite.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Core high-signal platforms for B2B intelligence
PLATFORM_PROBES = [
    {
        "name": "GitHub",
        "url_template": "https://api.github.com/users/{target}",
        "type": "api",
        "check_status": 200,
        "profile_url": "https://github.com/{target}",
        "extractor": lambda data: {
            "name": data.get("name"),
            "bio": data.get("bio"),
            "company": data.get("company"),
            "location": data.get("location"),
            "public_repos": data.get("public_repos"),
            "blog": data.get("blog")
        }
    },
    {
        "name": "GitLab",
        "url_template": "https://gitlab.com/api/v4/users?username={target}",
        "type": "api_list",
        "check_status": 200,
        "profile_url": "https://gitlab.com/{target}",
        "extractor": lambda data: {
            "name": data[0].get("name") if len(data) > 0 else None,
            "bio": data[0].get("bio") if len(data) > 0 else None
        } if len(data) > 0 else None
    },
    {
        "name": "Gravatar",
        "url_template": "https://en.gravatar.com/{target}.json",
        "type": "api",
        "check_status": 200,
        "profile_url": "https://en.gravatar.com/{target}",
        "extractor": lambda data: {
            "name": data.get("entry", [{}])[0].get("displayName"),
            "about": data.get("entry", [{}])[0].get("aboutMe"),
            "urls": [u.get("value") for u in data.get("entry", [{}])[0].get("urls", [])]
        } if "entry" in data and len(data["entry"]) > 0 else None
    },
    {
        "name": "Keybase",
        "url_template": "https://keybase.io/_/api/1.0/user/lookup.json?usernames={target}",
        "type": "api",
        "check_status": 200,
        "profile_url": "https://keybase.io/{target}",
        "extractor": lambda data: {
            "full_name": data.get("them", [{}])[0].get("profile", {}).get("full_name"),
            "bio": data.get("them", [{}])[0].get("profile", {}).get("bio"),
            "location": data.get("them", [{}])[0].get("profile", {}).get("location")
        } if data.get("them") and len(data["them"]) > 0 and data["them"][0] else None
    },
    {
        "name": "Dev.to",
        "url_template": "https://dev.to/api/users/by_username?url={target}",
        "type": "api",
        "check_status": 200,
        "profile_url": "https://dev.to/{target}",
        "extractor": lambda data: {
            "name": data.get("name"),
            "summary": data.get("summary"),
            "github_username": data.get("github_username")
        }
    },
    {
        "name": "Medium",
        "url_template": "https://medium.com/@{target}",
        "type": "html",
        "check_status": 200,
        "profile_url": "https://medium.com/@{target}"
    },
    {
        "name": "About.me",
        "url_template": "https://about.me/{target}",
        "type": "html",
        "check_status": 200,
        "profile_url": "https://about.me/{target}"
    }
]

def scan_target(target, fast=False):
    results = []
    print(f"[*] Escaneando vectores para: {target} (Modo: {'Rápido' if fast else 'Completo'})...")
    
    probes = PLATFORM_PROBES[:4] if fast else PLATFORM_PROBES
    
    for probe in probes:
        url = probe["url_template"].format(target=urllib.parse.quote(target))
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json" if "api" in probe["type"] else "text/html"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == probe["check_status"]:
                    profile_info = {
                        "platform": probe["name"],
                        "profile_url": probe["profile_url"].format(target=target),
                        "status": "CONFIRMED_ACTIVE",
                        "metadata": {}
                    }
                    
                    if "api" in probe["type"]:
                        try:
                            raw_body = response.read().decode("utf-8")
                            json_data = json.loads(raw_body)
                            if "extractor" in probe:
                                extracted = probe["extractor"](json_data)
                                if extracted:
                                    profile_info["metadata"] = extracted
                                else:
                                    continue
                        except Exception:
                            pass
                    
                    results.append(profile_info)
                    print(f"  [+] Encontrado en {probe['name']}: {profile_info['profile_url']}")
        except urllib.error.HTTPError as e:
            if e.code in [404, 410]:
                pass # Normal not found
            elif e.code == 429:
                print(f"  [!] Rate limit en {probe['name']} (HTTP 429)")
        except Exception:
            pass

    return results

def main():
    parser = argparse.ArgumentParser(description="User-Scanner Production OSINT Intelligence Runner")
    parser.add_argument("--username", help="Nombre de usuario o handle a escanear")
    parser.add_argument("--email", help="Correo electrónico objetivo")
    parser.add_argument("--fast", action="store_true", help="Escanear solo los vectores prioritarios")
    parser.add_argument("--deep-scan", action="store_true", help="Pivotaje y búsqueda exhaustiva")
    parser.add_argument("--format", choices=["json", "markdown", "table"], default="json", help="Formato de salida")
    parser.add_argument("--output-file", help="Ruta de archivo para guardar el reporte")
    
    args = parser.parse_args()
    
    if not args.username and not args.email:
        parser.error("Debe proporcionar --username o --email")
        
    target = args.username if args.username else args.email.split("@")[0]
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "query": {
            "target": target,
            "type": "username" if args.username else "email",
            "fast_mode": args.fast,
            "deep_scan": args.deep_scan
        },
        "profiles_found": scan_target(target, fast=args.fast)
    }
    
    report["total_found"] = len(report["profiles_found"])
    
    if args.format == "json":
        output_str = json.dumps(report, indent=2, ensure_ascii=False)
    elif args.format == "markdown":
        output_str = f"# Reporte OSINT: {target}\n\n"
        output_str += f"- **Fecha:** {report['timestamp']}\n"
        output_str += f"- **Perfiles confirmados:** {report['total_found']}\n\n"
        output_str += "| Plataforma | URL | Metadatos |\n| :--- | :--- | :--- |\n"
        for p in report["profiles_found"]:
            meta_summary = ", ".join([f"{k}: {v}" for k, v in p.get("metadata", {}).items() if v])
            output_str += f"| {p['platform']} | [{p['platform']}]({p['profile_url']}) | {meta_summary} |\n"
    else:
        output_str = f"Target: {target} | Total perfiles encontrados: {report['total_found']}\n"
        for p in report["profiles_found"]:
            output_str += f"- {p['platform']}: {p['profile_url']}\n"

    print("\n" + "="*50)
    print(output_str)
    print("="*50)
    
    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)), exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"[✓] Reporte guardado con éxito en: {args.output_file}")

if __name__ == "__main__":
    main()
