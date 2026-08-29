# ⏱️ Bitácora Ejecutiva: Ramping de New Hire, "Afilar el Hacha" y Tiempos del Embudo (PayMind)

> **Documento de Telemetría Comercial, Time-to-Value (TTV) y Playbook de Onboarding para la Célula de Growth**
> **Autor:** Antonio Gutiérrez — Estrategia Comercial & RevOps
> **Fecha de Inicio de Registro:** Agosto 2026

---

## 📌 1. Propósito Estratégico de la Bitácora

Este documento registra empíricamente el tiempo, esfuerzo y pasos metodológicos desde el **Día 1 de Onboarding (New Hire)** hasta la generación de **Revenue Facturado en PayMind**.

### Objetivos Principales:
1. **Medir el Time-to-Value (TTV):** Cuántos días toma pasar de investigación de mercado a la primera campaña saliente en producción.
2. **Establecer el Benchmark de Ramping:** Crear la guía estándar de incorporación para futuros SDRs y Account Executives en PayMind.
3. **Auditar la Eficiencia del Embudo (Sales Cycle Telemetry):** Registrar la latencia exacta entre cada etapa del funnel (Lead ➔ Envíos ➔ Respuestas ➔ Reuniones ➔ Demos ➔ Cierre).

---

## 🪓 2. Fase 1: "Afilar el Hacha" (Investigación, Depuración y Construcción GTM)

### 🗓️ Hitos de Trabajo & Arquitectura de Datos:

#### Hito 1: Investigación de Mercado y Lenguaje Sectorial (Gasolineras México)
* **Acciones:** Análisis exhaustivo del ecosistema de software volumétrico en México (ControlGAS, eGas, Nexus, Intelisis, Gilbarco, Wayne).
* **Hallazgo Clave:** El sector no compra "tecnología abstracta", compra soluciones a dolores operativos de fin de mes (conciliación de tarjeta vs. dispensario y cumplimiento de Anexo 30 SAT / CRE).
* **Resultado:** Eliminación del lenguaje robótico (`{{Empresa}}`) y adopción del léxico de pista (*isla, dispensario, posición de carga, volumen*).

#### Hito 2: Protocolo Zero-Assumption y Matriz Anti-Humo
* **Acciones:** Auditoría rigurosa de propuestas comerciales para eliminar cifras inventadas o afirmaciones académicas no respaldadas.
* **Resultado:** Establecimiento de la credibilidad basada en evidencia pública verificada:  
  * Mención pública de Grupo Orsan en `paymind.mx`.
  * Delimitación clara: *PayMind se integra a los sistemas volumétricos para la conectividad y conciliación del cobro en pista, aclarando que no emite facturación.*

#### Hito 3: Limpieza y Estructuración de la Base Heredada de Antonio
* **Acciones:** Deduplicación, normalización de dominios y segmentación de la **base de datos heredada por Antonio** (conocimiento y red preexistente en el sector gasolinero).
* **Entregables:**  
  * `BASE_MAESTRA_GASOLINERAS_PAYMIND.xlsx`
  * `Snovio_Gasolineras_AB_Master.csv` (433 prospectos)
  * CSVs limpios para Mailsuite y Snov.io (`Grupo A: 217`, `Grupo B: 216`).

#### Hito 4: Construcción del Hito Saliente (Viernes 28 de Agosto de 2026)
* **Hora de Ejecución:** 4:50 PM (Hora Centro de México).
* **Acción:** Lanzamiento oficial de la prueba A/B para la ventana de **Cierre Fiscal de Mes (28 al 31 de Agosto)**.
* **Resultado Inmediato (Primeras 5 Horas):**
  * **76 correos procesados / 67 enviados.**
  * **10 correos extintos aislados en automático (14% Bounce Rate / Base 100% purificada).**
  * **11 lecturas confirmadas (17% Open Rate inicial a la 1:30 AM del Sábado 29).**
  * **0% de quejas / 0% desuscritos.**

---

## 📈 3. Modelo Matemático de Probabilidad de Negocio Cerrado (RevOps Pipeline Forecast)

Tomando en cuenta que la base utilizada es una **base heredada por Antonio** (contactos calificados del sector con mayor afinidad que un raspado en frío genérico), este es el modelo de conversión proyectado:

### 📊 Tabla de Conversión y Rendimiento Esperado:

| Etapa del Embudo | Escenario Conservador (300 Snov.io Free) | Escenario Objetivo (433 Base Completa) | Tasa de Conversión Asumida |
| :--- | :---: | :---: | :---: |
| **Base Alcanzada** | 300 estaciones | 433 estaciones | 100% |
| **Entregados en Inbox (87%)** | 261 entregados | 376 entregados | 87% (Empírico) |
| **Lecturas Únicas (Open Rate)** | 91 lecturas | 169 lecturas | 35% - 45% |
| **Respuestas Humanas (Replies)** | 10 a 15 respuestas | 20 a 30 respuestas | 4% - 8% (Base Heredada) |
| **Reuniones / Pitch Agendados** | **4 a 6 Reuniones** | **8 a 12 Reuniones** | 40% - 50% de las respuestas |
| 🏆 **CONTRATOS CERRADOS GANADOS** | **1 a 2 Contratos** | **3 a 4 Contratos** | 20% - 30% Win Rate B2B |

---

### 💰 Impacto Comercial Esperado:

En el sector gasolinero B2B, un **contrato ganado** suele involucrar **grupos de 2 a 5 estaciones de servicio**:
* **Cerrar 1 a 3 contratos** equivale a conectar entre **3 y 15 estaciones de servicio adicionales a PayMind**.
* Esto genera un impacto directo en volumen transaccionado en pista y MRR de comisiones por integración.

---

## 📊 4. Matriz de Telemetría del Embudo de Conversión (Funnel Tracking)

| Etapa del Embudo | Métrica / Hito | Tiempo Acumulado (Días/Horas) | Benchmark / Meta | Estado Actual |
| :--- | :--- | :---: | :---: | :---: |
| **Etapa 0** | Onboarding New Hire & Base Heredada | Días de preparación | < 10 días | **Completado** |
| **Etapa 1** | Lanzamiento Primera Campaña Saliente | Viernes 28 Aug 4:50 PM | Día 0 de campaña | **Completado (76 envíos)** |
| **Etapa 2** | Primeras Lecturas Confirmadas (17% Open) | Sábado 29 Aug 1:35 AM | < 12 horas | **Completado (11 opens)** |
| **Etapa 3** | Primeras Respuestas Humanas (Replies) | Lunes 31 Aug (Pendiente) | < 72 horas | ⏳ En espera del lunes |
| **Etapa 4** | Primera Reunión Agendada (Discovery Call) | Por definir | < 5 días desde respuesta | ⏳ Próximo hito |
| **Etapa 5** | Demostración Técnica / Pitch Volumétrico | Por definir | < 10 días desde Discovery | ⏳ Próximo hito |
| **Etapa 6** | Cierre Comercial / Alta de Estación en PayMind | Por definir | < 30 días de ciclo total | ⏳ Meta final |

---

*Última actualización: Sábado 29 de Agosto de 2026, 01:50 AM (CST).*
