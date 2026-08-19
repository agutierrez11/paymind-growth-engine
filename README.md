# ⚡ PayMind Growth Engine & Multi-API Prospector

Plataforma unificada de prospección B2B, enriquecimiento de leads y automatización de cadencias de venta para **PayMind México** (Verticales clave: Redes Gasolineras y Sector Hotelero).

---

## 🏗️ Estructura del Workspace

```
paymind-growth-engine/
├── .agents/
│   └── AGENTS.md                  # Reglas del proyecto, contexto y protocolos zero-assumption
├── data/
│   ├── Campana_PayMind_Gasolineras_400.xlsx  # 433 gasolineras segmentadas con 4 pasos de copy
│   ├── Campana_PayMind_Gasolineras_400.csv   # Base CSV lista para ingesta
│   ├── hoteles_deduplicados.csv              # 256 hoteles limpios y deduplicados
│   └── Calculadora_PayMind_Gasolineras.html  # Calculadora interactiva de comisiones vs bancos
├── playbooks/
│   ├── analisis_propuesta_paymind.md         # Análisis contractual, red flags y guion de negociación
│   └── PAYMIND_GASOLINERAS_PITCH_PLAYBOOK.md # Playbook comercial: Macroeconomía, SAT Anexo 30 y Vales
├── src/
│   ├── smart_lead_router.py                  # Motor de cascada inteligente (Apollo, Hunter, Snov, Apify)
│   └── smart_routing_cache.db                # Caché persistente SQLite (0 créditos en duplicados)
├── .env.example                              # Template de llaves y credenciales
└── README.md
```

---

## 🔌 Stack de APIs Integradas (Smart Routing)

1. **Apollo.io API:** Búsqueda de C-Level, Dueños de Franquicias, Directores de Finanzas y teléfonos directos.
2. **Hunter.io API:** Búsqueda de dominios institucionales y verificación de entregabilidad SMTP.
3. **Snov.io API:** Orquestación de secuencias frías (Drip Campaigns), email warmup y parada automática.
4. **Apify API:** Scraping geográfico masivo en Google Maps (+70 USD de saldo).

---

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install requests pandas openpyxl

# 2. Ejecutar router inteligente de enriquecimiento
python src/smart_lead_router.py
```
