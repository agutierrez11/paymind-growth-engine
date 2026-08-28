# 🚀 ESTRATEGIA REFORZADA DE CRECIMIENTO PARA PAYMIND EN GASOLINERAS DE MÉXICO

> **Versión Ejecutiva — 27 de agosto de 2026**  
> **Autor:** Antonio Gutiérrez | Consultor de Crecimiento & Pagos  
> **Protocolo:** Zero-Assumption, Rigor Sectorial ONEXPO y SAT Anexo 30

---

## 📌 1. Tesis Estratégica

PayMind no debe posicionarse como otro proveedor de terminales. La categoría correcta es **infraestructura de cobro y operación para estaciones de servicio**, con un producto ancla muy concreto: **pago autónomo por posición/bomba, integrado al control volumétrico, la facturación y la conciliación**.

El kiosco es la “cuña” comercial porque resuelve un problema visible para el conductor: no tener que esperar a que el operador termine con el vehículo que llegó antes, ni depender de una sola terminal compartida. Para el gasolinero, la venta no debe basarse en “innovación”, sino en cuatro resultados medibles: reducir espera, aumentar transacciones por posición en horas pico, bajar errores de conciliación y extender capacidad operativa sin añadir la misma cantidad de personal.

> **Posicionamiento recomendado:** “PayMind convierte cada posición de carga en un punto de cobro autónomo, conectado y medible, sin perder control fiscal ni operativo.”

---

## ⚖️ 2. Tratamiento de Cifras y Evidencia (Protocolo Zero-Assumption)

| Elemento de la versión original | Evaluación | Tratamiento recomendado |
|---|---|---|
| Control volumétrico como integración central | Sólido | Mantener. El SAT define el control volumétrico como registros de entradas, salidas y existencias asociados con facturas [1]. |
| ATIO/ControlGAS como partner potencial | Plausible y verificable como proveedor | Mantener como cuenta estratégica, sin afirmar market share sin datos públicos. ControlGAS comunica conexión a dispensarios, inventarios y CFDI [4]. |
| 500 estaciones con autoservicio y 4,000 en 2030 | Señal sectorial | Usar como hipótesis de mercado atribuida a ONEXPO [3]. |
| 50% menor tiempo y 30% mayor satisfacción | Benchmark de proveedor | Presentar como caso publicado por LKS para Sinopec [2]. |
| 50–60% de abandono de filas en México | No verificado | Eliminar. Medir abandono real por cámara u observación. |
| $630k–$945k de ventas perdidas mensuales | Modelo especulativo | Eliminar del pitch. Sustituir por un calculador por estación. |
| $250k de inversión por estación | Referencia sectorial útil | Incluir en TCO preliminar como rango citado por ONEXPO [3]. |
| PayMind Ads y gamificación desde el inicio | Prematuro | Mover a Fase 2 (tras estabilidad del core). |
| 500 estaciones activas en 12 meses | Agresivo | Convertir en meta condicionada a integraciones y soporte (25, 75 y 200 estaciones). |

---

## 🎯 3. Segmentación Real del Mercado Gasolinero en México

La información sectorial de ONEXPO reporta aproximadamente **11,259 gasolineras**, con ventas mensuales desde 20 hasta 120 millones de pesos según ubicación, y un **35% de operaciones en efectivo** principalmente en zonas rurales [5].

| Segmento Prioritario | Señales de Dolor | Producto Inicial | Por qué Compraría |
|---|---|---|---|
| **Urbana de Alto Tráfico** | Filas, terminal compartida, picos predecibles | Kiosco asistido + pago por posición | Más capacidad en horas pico y menor frustración |
| **Carretera / Autopista** | Alto volumen, urgencia del conductor, nocturnos | Kiosco de autoservicio + redundancia offline | Continuidad y velocidad de atención |
| **Cadena Mediana (3-30 est.)** | Conciliación centralizada, estandarización | Plataforma multiestación + kioscos | Control corporativo y despliegue repetible |
| **Rural / Bajo Volumen** | Efectivo, conectividad, menor inversión | Terminal móvil / QR primero | Menor CAPEX y adopción gradual |
| **Autoconsumo / Flotillas** | Control por vehículo, centros de costo | Kiosco con identificación de flota | Trazabilidad y control de gasto |

---

## 💡 4. Propuesta de Valor: Del "Momento WOW" al Resultado Económico

| Momento | Experiencia del Conductor | Métrica de Producto | Monetización Posterior |
|---|---|---|---|
| **Llegada** | Ve una instrucción clara y número de posición | Tiempo hasta iniciar pago | Sin monetizar al inicio |
| **Pago** | Tarjeta, NFC, QR o método autorizado | Tasa de autorización y respuesta | Comisión de procesamiento |
| **Carga** | Confirmación del monto/volumen y estatus | Tiempo de ciclo y errores | Oferta contextual opcional |
| **Cierre** | Ticket digital / factura cuando aplique | Tasa de tickets emitidos | Lealtad y CRM |
| **Recompensa** | Cupón de tienda, lavado o bebida | Conversión e incrementalidad | Revenue share con comercio |

* **Modo Autónomo:** El usuario completa el flujo en el kiosco.
* **Modo Asistido:** El despachador puede intervenir desde una terminal móvil para evitar que una falla paralice la isla.

---

## 🏗️ 5. Arquitectura Técnica Recomendada (8 Capas)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ARQUITECTURA DE ORQUESTACIÓN PAYMIND                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. DISPENSARIO / VOLUMÉTRICO ➔ ControlGAS, eGas, Nexus, Intelisis           │
│ 2. KIOSCO / TERMINAL SmartPOS ➔ Interfaz Touch, ATEX antichispas, NFC/QR    │
│ 3. PAYMIND ORCHESTRATION     ➔ Estado de orden, idempotencia, audit ledger  │
│ 4. ADQUIRENCIA / PAYFAC      ➔ BBVA, BanBajío, Afirme (T+1)                 │
│ 5. FACTURACIÓN / CFDI        ➔ Enlace con PAC / Proveedor fiscal            │
│ 6. CONCILIACIÓN AUTOMÁTICA   ➔ Cruce Despacho - Pago - Factura - Liquidación │
│ 7. ANALYTICS OPERACIONAL     ➔ Throughput, uptime y tiempo de espera        │
│ 8. RETAIL MEDIA / LEALTAD    ➔ Módulo de anuncios patrocinados (Fase 2)     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤝 6. Alianzas Estratégicas: Orden Correcto de Prioridad

1. **Prioridad 1 — Control Volumétrico / POS:** ATIO/ControlGAS, eGas, NexusFuel, Gasomarshal Odoo *(API, certificación, sponsor y 3 pilotos)*.
2. **Prioridad 2 — Integradores de Estaciones:** Distribuidores e implementadores locales *(Producto adicional y comisión por activación)*.
3. **Prioridad 3 — Hardware de Surtidores / Kioscos:** Gilbarco, Dover Fueling, LKS *(Capa de pagos y conciliación)*.
4. **Prioridad 4 — Adquirente / PayFac:** BBVA, BanBajío, Afirme *(Volumen incremental y liquidez T+1)*.
5. **Prioridad 5 — POS de Tienda / Lavado:** Conveniencia y servicios complementarios *(Cupones y revenue share)*.
6. **Prioridad 6 — Marcas / Retail Media:** CPG, automotrices, seguros *(Audiencia contextual tras escala)*.

---

## 📊 7. Modelo Comercial, Financiero y Hoja de Ruta de 18 Meses

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HOJA DE RUTA A 18 MESES                             │
├─────────────┬───────────────────────────────┬───────────────────────────────┤
│ Periodo     │ Prioridad Estratégica         │ Meta / Entregable             │
├─────────────┼───────────────────────────────┼───────────────────────────────┤
│ 0-2 Meses   │ Descubrimiento & Compliance   │ 15 entrevistas, 5 estaciones  │
│ 2-4 Meses   │ Producto Mínimo (MVP)         │ Kiosco asistido, pagos, T+1   │
│ 4-6 Meses   │ Piloto Validado               │ 3-5 estaciones (Urbana/Carre) │
│ 6-9 Meses   │ Repetibilidad Commercial      │ 10 oportunidades calificados  │
│ 9-12 Meses  │ Land & Expand                 │ 25 a 75 estaciones pagadoras  │
│ 12-18 Meses │ Escala Selectiva              │ 100 a 200 estaciones activas  │
└─────────────┴───────────────────────────────┴───────────────────────────────┘
```

---

## 💬 8. Mensaje Comercial Recomendado (Pitch Ejecutivo)

> **“PayMind permite cobrar en la propia posición de carga, integrado con el control volumétrico y la conciliación de tu estación. En seis semanas medimos cuánto tiempo de espera eliminas, cuántas transacciones adicionales puedes procesar y cuánto reduces las diferencias de caja. Si el resultado no aparece en tus datos, no escalamos.”**

---

## 📚 Referencias

[1] SAT — Preguntas frecuentes sobre controles volumétricos (Anexo 30).  
[2] LKS Kiosk — Application analysis of self-service terminal in petrochemical industry (Sinopec).  
[3] ONEXPO — Las gasolineras en México quieren reducir costos y automatizar estaciones.  
[4] ATIO Group — ControlGAS Software de Control Volumétrico.  
[5] ONEXPO — Pagos digitales obligatorios elevarán competencia entre estaciones gasolineras.  
[6] Yuno — Success stories (Vibra / Premmia Brasil).
