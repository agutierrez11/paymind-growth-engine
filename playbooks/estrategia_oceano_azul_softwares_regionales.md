# 🌊 Estrategia de Océano Azul: Conquista del Mid-Market Gasolinero en México

> **Preparado por:** Antonio Gutiérrez | Consultor de Crecimiento & Pagos  
> **Asunto:** Mapeo de softwares volumétricos regionales y de nicho (eGas, Gasomarshal, Pegasus, GT Soluciones) para capturar más de 3,500 estaciones de servicio desatendidas por los gigantes.  
> **Ámbito:** Exclusivo Mercado Mexicano 2026 (Anexo 30 SAT, Odoo Enterprise, Conectividad Híbrida).

---

## 🗺️ 1. El Océano Azul: Mapeo de Líderes Regionales "Ocultos"

Mientras las agencias tradicionales pierden tiempo intentando competir por grandes cuentas como Oxxo Gas o Petro-7 frente a ATIO Group (ControlGAS), existe un **Océano Azul de más de 3,500 estaciones medianas e independientes** operadas por 4 jugadores regionales clave:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│              MAPA DEL OCÉANO AZUL DE SOFTWARES REGIONALES EN MÉXICO              │
├────────────────────┬────────────────────┬─────────────────┬──────────────────────┤
│ Software / Partner │ Estaciones / Base  │ Región Dominante│ Diferenciador Clave  │
├────────────────────┼────────────────────┼─────────────────┼──────────────────────┤
│ 🟢 eGas            │ +1,500 Estaciones  │ Centro, Sureste,│ Certificación PCI-DSS│
│    (Petrosmart)    │                    │ Bajío, Noreste  │ y presencia en 7 edos│
├────────────────────┼────────────────────┼─────────────────┼──────────────────────┤
│ 🔵 Gasomarshal     │ +350 Estaciones    │ Centro de México│ Backoffice integrado │
│    (FuelDBox)      │ (+1,500 usuarios)  │                 │ a **Odoo Enterprise**│
├────────────────────┼────────────────────┼─────────────────┼──────────────────────┤
│ 🟡 Pegasus Control │ +1,000 Estaciones  │ Bajío & Occident│ 40+ años. Gasolineras│
│    (Zapopan, Jal)  │                    │ (Jal, Gto, Mich)│ y Plantas de Gas LP. │
├────────────────────┼────────────────────┼─────────────────┼──────────────────────┤
│ 🔴 GT Soluciones   │ +800 Estaciones    │ Noroeste &      │ Distribuidor Gilbarco│
│    (Gasolwin)      │                    │ Península       │ con FacturaGas app.  │
└────────────────────┴────────────────────┴─────────────────┴──────────────────────┘
```

---

## 🧠 2. Los 2 Factores Estructurales del Mercado Mexicano

### A. El Factor Distribuidor ("Los Fierreros")
En México, el software de control volumétrico no se compra de forma aislada; **se empaqueta junto con la venta de dispensarios físicos (Gilbarco Veeder-Root, Wayne, Bennett)** que realizan los ingenieros locales.
* *Ejemplo:* Si una empresa de ingeniería en Sinaloa es la distribuidora oficial de Gilbarco en el Pacífico y empaqueta **Gasolwin / GT Soluciones**, todas las gasolineras que se abran en Sinaloa, Sonora y Baja California nacen por defecto con ese software.

### B. El Factor Seguridad & Conectividad Híbrida en Pista
En regiones con fricción operativa o conectividad inestable (Michoacán, Guerrero, Tamaulipas, Edomex), los gasolineros huyen de sistemas 100% en la nube. **Si se cae el internet, la bomba no puede parar porque el SAT multa**.
* *La Solución:* Softwares locales/híbridos como **Pegasus Control** o **FuelDBox** guardan los JSON del Anexo 30 de forma local en la estación y los sincronizan después. **PayMind SmartPOS opera en este mismo modelo híbrido (4G + local cache)**.

---

## 🛠️ 3. Plan de Integración por Partner (Ganar-Ganar)

### 🟢 Canal A: eGas (de Petrosmart) – (+1,500 Estaciones)
* **Presencia:** Fábrica en CDMX + oficinas en Veracruz, Chiapas, Puebla, Querétaro, SLP, Guadalajara y Monterrey.
* **Propuesta PayMind:** eGas tiene el control volumétrico y certificación PCI-DSS, pero carece de una suite SmartPOS inalámbrica en pista. PayMind se integra como la pasarela de pagos oficial recomendable para sus usuarios.

### 🔵 Canal B: Gasomarshal (FuelDBox) – (+350 Estaciones en Odoo)
* **Dato de Oro:** Construyeron su ERP vertical sobre **Odoo Enterprise**.
* **Propuesta PayMind:** Conciliar pasarelas de pago mexicanas en Odoo es complejo. PayMind se conecta por API a la vertical de Odoo de Gasomarshal: el despachador cobra en bomba con la SmartPOS Nexgo ATEX y el asiento contable se genera en automático dentro de Odoo.

### 🟡 Canal C: Pegasus Control – (Bajío, Occidente & Gas LP)
* **Presencia:** Zapopan, Jalisco. 40+ años operando gasolineras y carburación de Gas LP.
* **Propuesta PayMind:** Proveer las SmartPOS inalámbricas antichispas (ATEX) que corren el software SGC Ventas de Pegasus, ruteando transacciones bajo el número de afiliación propia del comercio.

---

## ✉️ 4. Copys de Alianza y Co-Prospección para el Océano Azul

### 🔹 Para Alianza con eGas / Petrosmart
```text
Asunto: [Nombre], habilitamos cobro inalámbrico SmartPOS integrado nativo para eGas

Hola [Nombre],

Sé que en eGas protegen a más de 1,500 estaciones en México asegurando su control volumétrico y cumplimiento fiscal. Sin embargo, muchos de sus clientes independientes siguen sufriendo pérdidas en pista por usar terminales bancarias manuales que no se hablan con sus dispensarios.

En PayMind desarrollamos una pasarela transaccional multi-adquirente que corre en SmartPOS Android inalámbricas de uso rudo (Nexgo ATEX). Queremos proponerles una alianza técnica: certificar nuestra pasarela con su sistema para que la bomba le envíe el monto exacto a la terminal de PayMind de forma nativa.

Ustedes robustecen la oferta de eGas en pista sin gastar en desarrollo de pagos, y nosotros aportamos el ruteo transaccional inteligente respetando el banco actual del cliente. ¿Hará sentido una breve llamada de 10 minutos para revisar documentación API?

Saludos cordiales,
Antonio Gutiérrez | PayMind
```

---

### 🔹 Para Alianza con Gasomarshal (Especialistas en Odoo)
```text
Asunto: [Nombre], conciliación bancaria automatizada para las estaciones Odoo de Gasomarshal

Hola [Nombre],

Su liderazgo integrando Odoo Enterprise con FuelDBox ha transformado la administración de más de 350 estaciones en el país. El único eslabón que sigue requiriendo horas hombre en el backoffice de sus clientes es la conciliación manual de los vouchers de tarjeta contra el módulo contable de Odoo.

PayMind es una pasarela de ruteo agnóstica conectada a isla. Queremos co-desarrollar o conectar un puente API para que cada cobro procesado en nuestras SmartPOS inyecte el asiento contable conciliado en tiempo real directo a su módulo de Odoo Gasomarshal.

Cerramos la pinza de automatización total para sus usuarios en un esquema ganar-ganar. ¿Tendrán disponibilidad para una sesión de 10 minutos esta semana?

Saludos cordiales,
Antonio Gutiérrez | PayMind
```

---

## 🚀 5. Presentación por Partes al CEO (Blindaje Comercial)

En tu próxima junta ejecutiva con el CEO de PayMind, pon estos argumentos sobre la mesa:

1. **"En lugar de pelearnos con ATIO por Oxxo Gas, capturemos las 1,500 estaciones de eGas y las 350 de Gasomarshal en bloque."**
2. **"La alianza con Gasomarshal Odoo nos da el argumento de venta más poderoso para un CFO mediano: conciliación bancaria automática directa a Odoo."**
3. **"Mantenemos la lista privada de 433 contactos como nuestra aceleradora in-house de prospección."**
