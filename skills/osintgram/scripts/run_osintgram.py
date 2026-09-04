#!/usr/bin/env python3
"""
Production Runner for Osintgram
Public Instagram reconnaissance, bio parsing, and contact extraction.
"""

import os
import re
import json
import argparse
import urllib.request
import urllib.parse
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_PATTERN = re.compile(r'(?:\+?52\s*)?(?:\(?\d{2,3}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}')

def scrape_instagram_public_profile(username):
    url = f"https://www.instagram.com/{username}/"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Accept-Language": "es-MX,es;q=0.9,en;q=0.8"
        }
    )
    
    profile_data = {
        "username": username,
        "url": url,
        "exists": False,
        "is_verified": False,
        "bio": "",
        "external_url": None,
        "extracted_emails": [],
        "extracted_phones": []
    }
    
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status == 200:
                profile_data["exists"] = True
                html = resp.read().decode("utf-8", errors="ignore")
                
                # Extraer meta description
                desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
                if desc_match:
                    desc_content = desc_match.group(1)
                    profile_data["bio"] = desc_content
                    
                    # Buscar emails
                    emails = set(re.findall(EMAIL_PATTERN, desc_content))
                    profile_data["extracted_emails"] = list(emails)
                    
                    # Buscar teléfonos
                    phones = set(re.findall(PHONE_PATTERN, desc_content))
                    profile_data["extracted_phones"] = [p for p in phones if len(re.sub(r'\D', '', p)) >= 10]
                    
                # Extraer título
                title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
                if title_match:
                    profile_data["display_name"] = title_match.group(1).split("(@")[0].strip()
                    
    except urllib.error.HTTPError as e:
        if e.code == 404:
            profile_data["status"] = "USER_NOT_FOUND"
        elif e.code == 429:
            profile_data["status"] = "RATE_LIMITED_BY_META"
    except Exception as e:
        profile_data["error"] = str(e)
        
    return profile_data

def main():
    parser = argparse.ArgumentParser(description="Osintgram - Instagram Intelligence Runner")
    parser.add_argument("--target", required=True, help="Handle de usuario de Instagram (sin @)")
    parser.add_argument("--extract-contacts", action="store_true", default=True, help="Extraer emails y teléfonos de la bio")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Formato de salida")
    parser.add_argument("--output-file", help="Ruta de archivo para guardar resultados")
    
    args = parser.parse_args()
    clean_user = args.target.strip().lstrip("@")
    
    print(f"[*] Reconocimiento OSINT en Instagram para: @{clean_user}")
    data = scrape_instagram_public_profile(clean_user)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "query": clean_user,
        "profile": data
    }
    
    if args.format == "json":
        output = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        output = f"# 📸 REPORTE OSINTGRAM: @{clean_user}\n\n"
        output += f"- **URL:** [{data['url']}]({data['url']})\n"
        output += f"- **Estado:** {'Activo / Encontrado' if data.get('exists') else 'No verificado o bloqueado'}\n"
        if data.get("display_name"):
            output += f"- **Nombre Visible:** {data['display_name']}\n"
        if data.get("bio"):
            output += f"- **Biografía:** {data['bio']}\n\n"
            
        output += "## 📞 Datos de Contacto Detectados\n"
        if data.get("extracted_emails"):
            output += f"- **Correos:** {', '.join(data['extracted_emails'])}\n"
        else:
            output += "- **Correos:** Ninguno en bio pública\n"
            
        if data.get("extracted_phones"):
            output += f"- **Teléfonos:** {', '.join(data['extracted_phones'])}\n"
            
    print("\n" + "="*50)
    print(output)
    print("="*50)
    
    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)) if os.path.dirname(args.output_file) else ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[✓] Salida exportada en: {args.output_file}")

if __name__ == "__main__":
    main()
