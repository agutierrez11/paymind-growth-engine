# 🛠️ Guía Paso a Paso: Configuración Exacta de la Campaña PayMind en Snov.io

> **Basado en la Documentación Oficial de Snov.io & Marco Anti-Spam Zero-Assumption**

---

## 🎯 Configuración General
* **Remitente:** `antonio.gutierrez@paymind.mx`
* **Archivo de Destinatarios:** `Snovio_Gasolineras_AB_Master.csv` (o `Snovio_Gasolineras_AB_A.csv` / `Snovio_Gasolineras_AB_B.csv`)
* **Límite Diario:** Conservador de 10 a 20 correos/día (Espaciado simulando comportamiento humano).
* **Horario de Envío:** Lunes a Viernes, de 9:00 AM a 2:00 PM (Hora Centro de México / CST).

---

## 📌 Paso 1: Secuencia de Correos (Constructor Visual)

Construye el flujo visual conectando los elementos de la barra derecha:

```
[Inicio] 
   │
   ▼
[Email 1: Apertura]
   │
   ▼
[Retraso: 3 Días]
   │
   ▼
[Email 2: Follow-up 1]
   │
   ▼
[Retraso: 3 Días]
   │
   ▼
[Email 3: Follow-up 2]
   │
   ▼
[Retraso: 3 Días]
   │
   ▼
[Email 4: Follow-up 3 / Enrutamiento]
   │
   ▼
[Retraso: 4 Días]
   │
   ▼
[Email 5: Breakup / Cierre de Hilo]
   │
   ▼
[Objetivo / Fin]
```

### 💡 Pruebas A/B dentro de Snov.io:
* Si cargas la base completa con la columna `Variante_AB`, puedes crear una **Prueba A/B en el Email 1** haciendo clic en `+ Agregar` debajo del elemento de correo.
* **Variante A (Usted):** Copy con registro formal.
* **Variante B (Tú):** Copy con registro cercano.
* Snov.io enviará automáticamente el 50% a cada variante.

---

## 📌 Paso 2: Selección de la Lista de Prospectos

1. Selecciona la lista importada desde el CSV (`Snovio_Gasolineras_Lanzamiento.csv` o `Snovio_Gasolineras_AB_Master.csv`).
2. **Correos múltiples:** Selecciona *"Solo al correo principal"*.
3. **Filtro de Entregabilidad:** Marca la opción *"Excluir correos no verificados o no verificables"* (Hard Bounces < 2%).
4. **Datos Faltantes:** Dado que usamos la apertura impersonal socrática (`"Buen día, le escribo a {Empresa}..."`), **el mensaje no depende de que exista el campo `{Nombre}`**, evitando fallas por variables vacías.

---

## 📌 Paso 3: Opciones de Envío & Ajustes Anti-Spam (CRÍTICO)

1. **Cuenta Remitente:** Selecciona `antonio.gutierrez@paymind.mx` (conectada vía SMTP/Gmail).
2. **Seguimiento de Aperturas (Open Tracking):** **ACTIVADO** (para medir tasa de apertura).
3. **Seguimiento de Enlaces (Link Tracking):** ⚠️ **DESACTIVADO**  
   *(El video oficial advierte que rastrear enlaces sin Custom Tracking Domain daña la entregabilidad a spam. Además, en el Paso 1 usaremos Texto Plano Puro sin links).*
4. **Detener para los que responden (Stop on Reply):** **ACTIVADO (Por defecto)**  
   *(En cuanto un gasolinero responda "no nos interesa" o "habla con el CP Juan", la campaña se frena en automático).*
5. **Programación por Horario:** Crear horario `México B2B`:
   * Días: Lunes a Viernes.
   * Ventana: `09:00 - 14:00` (Hora CDMX / CST).

---

## 📌 Paso 4: Revisión & Lanzamiento

1. **Email de Prueba:** Usa el botón *Enviar un email de prueba* hacia tu correo personal para verificar la apariencia en bandeja de entrada (revisar que no haya saltos de línea extraños o caracteres raros en acentos).
2. **Nombre de la Campaña:** `Campaña Gasolineras 2026 - A/B Test Impersonal Socrático`.
3. Haz clic en **Iniciar**.
