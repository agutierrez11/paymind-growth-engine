# 🧠 Investigación Técnica: Cómo funcionan "Condition" y "Goal" en Snov.io

> **Guía de Arquitectura de Secuencias y Ramificación en el Constructor de Snov.io**

---

## 📌 1. Elemento: CONDITION (Condición / Disparador)

### ¿Qué es y cómo funciona?
**Condition** es un nodo de decisión lógica (`SI / NO`) que ramifica el flujo de la campaña basándose en la interacción previa del destinatario.

### Eventos que evalúa Snov.io:
1. `Opened email` (El contacto abrió un correo específico).
2. `Clicked on link` (El contacto hizo clic en un enlace).
3. `Booked meeting via Calendly` (El contacto agendó una cita).

### El parámetro `Wait Time` (Tiempo de Espera):
* Estableces un marco de tiempo (ej. *Wait up to 2 days*).
* **Si el prospecto cumple la condición dentro del tiempo:** Snov.io lo envía por la rama **YES** (Verde/Morada) inmediatamente.
* **Si transcurre el tiempo SIN cumplir la condición:** Al vencer el plazo, Snov.io lo envía por la rama **NO** (Gris).

### ⚠️ El Riesgo de Usar `Condition: Opened Email` en Frío:
* **Falsos Positivos de Antivirus:** Servidores como Microsoft Outlook/Defender tienen bots de seguridad que abren el correo en milisegundos para escanearlo. Si usas `Opened email`, un bot de seguridad puede activar la rama `YES` sin que el humano lo haya visto jamás.
* **Recomendación:** En prospección B2B saliente en frío, es mejor usar secuencias lineales directas (`Email 1 ➔ Delay ➔ Email 2`) y reservar `Condition` únicamente para clics en enlaces o reuniones agendadas.

---

## 🎯 2. Elemento: GOAL (Objetivo / Meta Final)

### ¿Qué es y cómo funciona?
**Goal** es el nodo terminal de la campaña. Representa el punto de llegada donde la secuencia concluye oficialmente para un destinatario.

### Funciones Principales de Goal:
1. **Detención Automática:** En cuanto un prospecto toca el nodo **Goal**, la campaña se **detiene automáticamente** para él. No volverá a recibir más correos de esta secuencia.
2. **Métricas de Conversión:** En el panel de control de Snov.io, los datos de la campaña te muestran cuántos prospectos de tu lista alcanzaron exitosamente la meta.
3. **Múltiples Objetivos:** Puedes colocar diferentes nodos **Goal** al final de distintas ramas (ejemplo: *Goal A: Prospectos Interesados* vs. *Goal B: Secuencia Completada Sin Respuesta*).

---

## 💡 Resumen Visual de Arquitectura de Campaña

### ❌ Arquitectura Compleja (No recomendada para frío por bots):
```text
[Email 1] ➔ [Delay 3 días] ➔ [Condition: Opened?] ──(YES)──> [Email Especial] ➔ [Goal]
                                                 └──(NO)───> [Email Estándar] ➔ [Goal]
```

### 🟢 Arquitectura Recomendada (Lineal, Limpia y Efectiva):
```text
[Email 1 (Viernes 28)] ➔ [Delay (Wait 3 days)] ➔ [Email 2 (Lunes 31)] ➔ [Goal]
```
*(Se detiene en automático cuando el usuario responde gracias al ajuste de plataforma `Stop on reply`).*
