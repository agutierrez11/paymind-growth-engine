#!/usr/bin/env python3
"""
Production Runner for Cloudflare Temp Mail & Disposable Inbox Monitor
Provisions mailboxes, listens for verification messages, and extracts OTP codes/links.
"""

import os
import sys
import re
import time
import json
import random
import string
import argparse
import urllib.request
import urllib.parse
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
API_BASE = "https://www.1secmail.com/api/v1/"

def api_get(params):
    query_str = urllib.parse.urlencode(params)
    url = f"{API_BASE}?{query_str}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def create_temp_email(custom_user=None):
    domains = ["1secmail.com", "1secmail.org", "1secmail.net"]
    domain = random.choice(domains)
    if not custom_user:
        rnd = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        login = f"pm_lead_{rnd}"
    else:
        login = re.sub(r'[^a-zA-Z0-9]', '', custom_user).lower()
        
    email = f"{login}@{domain}"
    return {
        "email": email,
        "login": login,
        "domain": domain,
        "created_at": datetime.now().isoformat()
    }

def fetch_messages(login, domain):
    return api_get({"action": "getMessages", "login": login, "domain": domain})

def fetch_message_detail(login, domain, msg_id):
    return api_get({"action": "readMessage", "login": login, "domain": domain, "id": msg_id})

def extract_otp_and_links(body_text, body_html=""):
    combined = (body_text or "") + " " + (body_html or "")
    
    # Extraer URLs
    links = re.findall(r'https?://[^\s<>"\']+', combined)
    # Filtrar enlaces de confirmación o activación
    activation_links = [l for l in links if any(k in l.lower() for k in ["verify", "confirm", "activate", "token", "auth"])]
    
    # Extraer OTPs (4 a 8 dígitos)
    otps = re.findall(r'\b\d{4,8}\b', body_text or "")
    
    return {
        "activation_links": list(set(activation_links)),
        "all_links": list(set(links))[:10],
        "possible_otps": list(set(otps))
    }

def wait_for_message(login, domain, timeout_sec=90, extract=True):
    print(f"[*] Monitoreando buzón: {login}@{domain} (Timeout: {timeout_sec}s)...")
    start = time.time()
    
    while time.time() - start < timeout_sec:
        msgs = fetch_messages(login, domain)
        if isinstance(msgs, list) and len(msgs) > 0:
            print(f"\n[+] ¡Mensaje recibido! ({len(msgs)} mensaje(s) en bandeja)")
            latest = msgs[0]
            detail = fetch_message_detail(login, domain, latest["id"])
            
            result = {
                "id": latest["id"],
                "from": detail.get("from"),
                "subject": detail.get("subject"),
                "date": detail.get("date"),
                "textBody": detail.get("textBody", ""),
                "extraction": {}
            }
            
            if extract:
                result["extraction"] = extract_otp_and_links(detail.get("textBody", ""), detail.get("htmlBody", ""))
                
            return result
            
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(4)
        
    print("\n[!] Tiempo de espera agotado sin mensajes nuevos.")
    return None

def main():
    parser = argparse.ArgumentParser(description="Cloudflare Temp Mail - Production Runner")
    parser.add_argument("--action", choices=["create", "check-inbox", "wait-message"], default="create", help="Acción a ejecutar")
    parser.add_argument("--email", help="Correo temporal objetivo a consultar o monitorear")
    parser.add_argument("--timeout", type=int, default=90, help="Segundos máximos de espera")
    parser.add_argument("--extract-links", action="store_true", default=True, help="Extraer enlaces OTP y verificación")
    parser.add_argument("--output-file", help="Ruta de archivo para guardar el resultado")
    
    args = parser.parse_args()
    
    output_data = {}
    
    if args.action == "create":
        res = create_temp_email()
        output_data = res
        print(f"\n[✓] Buzón temporal creado:")
        print(f"  Dirección: {res['email']}")
        print(f"  Usuario:   {res['login']}")
        print(f"  Dominio:   {res['domain']}")
        
    elif args.action in ["check-inbox", "wait-message"]:
        if not args.email or "@" not in args.email:
            parser.error("Debe proporcionar un --email válido (ej: usuario@1secmail.com)")
            
        login, domain = args.email.split("@", 1)
        
        if args.action == "check-inbox":
            msgs = fetch_messages(login, domain)
            output_data = {"email": args.email, "messages": msgs}
            print(f"\n[✓] Mensajes en bandeja ({len(msgs) if isinstance(msgs, list) else 0}):")
            if isinstance(msgs, list):
                for m in msgs:
                    print(f"  - [{m['id']}] De: {m['from']} | Asunto: {m['subject']} ({m['date']})")
        else:
            msg = wait_for_message(login, domain, timeout_sec=args.timeout, extract=args.extract_links)
            if msg:
                output_data = msg
                print(f"\n[✓] Detalle del mensaje recibido:")
                print(f"  De:     {msg['from']}")
                print(f"  Asunto: {msg['subject']}")
                if msg["extraction"].get("possible_otps"):
                    print(f"  🔑 CÓDIGO OTP DETECTADO: {', '.join(msg['extraction']['possible_otps'])}")
                if msg["extraction"].get("activation_links"):
                    print(f"  🔗 ENLACE DE ACTIVACIÓN:")
                    for l in msg["extraction"]["activation_links"]:
                        print(f"     -> {l}")
            else:
                output_data = {"status": "timeout", "email": args.email}

    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)) if os.path.dirname(args.output_file) else ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"[✓] Salida exportada en: {args.output_file}")

if __name__ == "__main__":
    main()
