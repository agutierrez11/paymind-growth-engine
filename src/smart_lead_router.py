"""
Smart Lead Routing Engine & Multi-API Credit Optimizer
Orchestrates: Local Cache -> Apify -> Hunter.io -> Snov.io -> Apollo.io
Maximizes enrichment yield while preserving expensive API credits.
"""

import os
import json
import sqlite3
import requests
from typing import Dict, Any, Optional

# --- CONFIGURACIÓN DE CREDENCIALES ---
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY", "OaI8S24Xrmh-2LFLuSE3XQ")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "a8db20c2773b153216979d9e0a334412c84487fd")
SNOV_CLIENT_ID = os.getenv("SNOV_CLIENT_ID", "b88e919d3049b70ff54f21b37bc4472a")
SNOV_CLIENT_SECRET = os.getenv("SNOV_CLIENT_SECRET", "c3dd201a21c5f47e5d80c67da72aad02")

CACHE_DB = os.path.join(os.path.dirname(__file__), "smart_routing_cache.db")


class SmartLeadRouter:
    def __init__(self):
        self._init_cache()
        self.snov_token = None

    def _init_cache(self):
        """Inicializa caché SQLite local para no quemar créditos en duplicados."""
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrichment_cache (
                key TEXT PRIMARY KEY,
                provider TEXT,
                data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM enrichment_cache WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
        return None

    def _save_to_cache(self, key: str, provider: str, data: Dict[str, Any]):
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO enrichment_cache (key, provider, data) VALUES (?, ?, ?)",
            (key, provider, json.dumps(data, ensure_ascii=False))
        )
        conn.commit()
        conn.close()

    # --- TIER 0: SNOV.IO OAUTH ---
    def _get_snov_token(self) -> Optional[str]:
        if self.snov_token:
            return self.snov_token
        try:
            url = "https://api.snov.io/v1/oauth/access_token"
            resp = requests.post(url, data={
                "grant_type": "client_credentials",
                "client_id": SNOV_CLIENT_ID,
                "client_secret": SNOV_CLIENT_SECRET
            }, timeout=8)
            if resp.status_code == 200:
                self.snov_token = resp.json().get("access_token")
                return self.snov_token
        except Exception as e:
            print(f"[SmartRouter] Error autenticando Snov: {e}")
        return None

    # --- TIER 1: VERIFICACIÓN Y ENRIQUECIMIENTO RÁPIDO (HUNTER.IO) ---
    def verify_email_hunter(self, email: str) -> Dict[str, Any]:
        cache_key = f"hunter_verify_{email.lower()}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return {"source": "cache_hunter", **cached}

        url = "https://api.hunter.io/v2/email-verifier"
        params = {"email": email, "api_key": HUNTER_API_KEY}
        try:
            r = requests.get(url, params=params, timeout=6)
            if r.status_code == 200:
                res = r.json().get("data", {})
                result = {
                    "status": res.get("status"),
                    "score": res.get("score"),
                    "domain": res.get("domain")
                }
                self._save_to_cache(cache_key, "hunter", result)
                return {"source": "live_hunter", **result}
        except Exception as e:
            print(f"[Hunter Error] {e}")
        return {"source": "hunter_fail", "status": "unknown"}

    # --- TIER 2: SNOV.IO VERIFIER & FINDER (FALLBACK / BATCH) ---
    def verify_email_snov(self, email: str) -> Dict[str, Any]:
        cache_key = f"snov_verify_{email.lower()}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return {"source": "cache_snov", **cached}

        token = self._get_snov_token()
        if not token:
            return {"source": "snov_auth_error"}

        url = "https://api.snov.io/v1/get-emails-verification-status"
        try:
            r = requests.post(url, data={"access_token": token, "emails[]": [email]}, timeout=8)
            if r.status_code == 200:
                data = r.json().get(email, {})
                status_desc = data.get("status", {}).get("identifier", "unknown")
                result = {"status": status_desc, "data": data}
                self._save_to_cache(cache_key, "snov", result)
                return {"source": "live_snov", **result}
        except Exception as e:
            print(f"[Snov Error] {e}")
        return {"source": "snov_fail"}

    # --- TIER 3: APOLLO.IO (HIGH-INTENT DECISION MAKERS & PHONES) ---
    def search_apollo_decision_makers(self, domain_or_org: str, titles=["Director", "Gerente", "Dueño", "Finanzas", "Operaciones"]) -> Dict[str, Any]:
        cache_key = f"apollo_decision_{domain_or_org.lower()}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return {"source": "cache_apollo", **cached}

        url = "https://api.apollo.io/v1/mixed_people/search"
        headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}
        payload = {
            "api_key": APOLLO_API_KEY,
            "q_organization_domains": domain_or_org if "." in domain_or_org else None,
            "q_organization_name": domain_or_org if "." not in domain_or_org else None,
            "person_titles": titles,
            "page": 1,
            "per_page": 5
        }
        # Limpiar llaves nulas
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            r = requests.post(url, headers=headers, json=payload, timeout=10)
            if r.status_code == 200:
                res_data = r.json()
                people = res_data.get("people", [])
                contacts = []
                for p in people:
                    contacts.append({
                        "name": p.get("name"),
                        "title": p.get("title"),
                        "email": p.get("email"),
                        "linkedin_url": p.get("linkedin_url"),
                        "organization": p.get("organization", {}).get("name")
                    })
                result = {"total_found": len(contacts), "contacts": contacts}
                self._save_to_cache(cache_key, "apollo", result)
                return {"source": "live_apollo", **result}
        except Exception as e:
            print(f"[Apollo Error] {e}")
        return {"source": "apollo_fail", "contacts": []}

    # --- SMART ROUTING CASCADE ---
    def enrich_lead_smart(self, raw_lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica cascada inteligente:
        1. Limpieza y descarte de correos basura/desechables sin costo.
        2. Extracción de dominio corporativo.
        3. Si el correo es genérico (Hotmail/Gmail), busca dominio corporativo y tomadores de decisión en Apollo.
        4. Si el correo tiene dominio institucional, verifica con Hunter -> Snov.
        """
        company = raw_lead.get("Compañia") or raw_lead.get("Hotel_Nombre") or raw_lead.get("Nombre") or ""
        email = raw_lead.get("Email") or raw_lead.get("Correo") or ""
        
        result = {
            "original_company": company,
            "original_email": email,
            "is_generic_email": False,
            "verified_status": "unverified",
            "decision_makers": [],
            "recommended_action": "review"
        }

        domain = email.split("@")[-1].lower() if "@" in email else ""
        generic_domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "live.com", "prodigy.net.mx"]

        if domain in generic_domains or not domain:
            result["is_generic_email"] = True
            # No quemamos créditos de Hunter en @hotmail; usamos Apollo para buscar al tomador de decisión por nombre de empresa
            if company and len(company) > 3:
                apollo_res = self.search_apollo_decision_makers(company)
                result["decision_makers"] = apollo_res.get("contacts", [])
                result["recommended_action"] = "reach_decision_maker" if result["decision_makers"] else "manual_search"
        else:
            # Correo institucional: Verificamos primero con Hunter
            hunter_res = self.verify_email_hunter(email)
            result["verified_status"] = hunter_res.get("status", "unknown")
            
            if result["verified_status"] == "deliverable":
                result["recommended_action"] = "ready_for_drip"
            else:
                # Fallback a Snov si Hunter es incierto
                snov_res = self.verify_email_snov(email)
                result["snov_status"] = snov_res.get("status")
                
                # Si sigue dudoso, buscamos contacto alternativo en Apollo
                apollo_res = self.search_apollo_decision_makers(domain)
                result["decision_makers"] = apollo_res.get("contacts", [])

        return result


if __name__ == "__main__":
    router = SmartLeadRouter()
    print("SmartLeadRouter inicializado con éxito.")
