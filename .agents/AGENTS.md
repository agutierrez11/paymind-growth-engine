# 🛡️ Reglas y Protocolos: PayMind Growth Engine

1. **Protocolo Zero-Assumption:**
   - Todos los cálculos de margen, tasas bancarias y porcentajes impositivos deben respaldarse con datos comprobables (IEPS vigente, IVA 16%, Anexo 30 SAT).
2. **Higiene de Datos y Créditos de API:**
   - Toda consulta a APIs externas DEBE pasar obligatoriamente por `smart_lead_router.py` para consultar la caché local `smart_routing_cache.db` antes de invocar endpoints de pago.
   - Prohibido quemar verificaciones de Hunter.io en dominios públicos (@gmail.com, @hotmail.com).
3. **Control de Versiones y Despliegue:**
   - Este repositorio es independiente. Cualquier despliegue o push debe ejecutarse exclusivamente desde esta carpeta (`scratch/paymind-growth-engine`).
