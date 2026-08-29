# Auditoría de base y diseño A/B para gasolineras

## Resumen ejecutivo

La base contiene **433 contactos**, no aproximadamente 400. No hay correos duplicados ni formatos de correo inválidos, pero la calidad de identificación del contacto es el principal riesgo: **315 registros, equivalentes a 72.75%, usan dominios personales o gratuitos** como Hotmail, Gmail, Yahoo, Prodigy, Outlook o Live. Esto no demuestra que estén equivocados, pero sí reduce la confianza en que sean correos corporativos vigentes o que la persona continúe en el puesto.

Por esa razón, la nueva secuencia evita el nombre del contacto y tampoco menciona una supuesta responsabilidad del destinatario. Comienza preguntando cómo se resuelve el cobro con tarjeta en la estación y, cuando corresponde, pide orientación hacia la persona que lleva pagos, operaciones o sistemas.

| Hallazgo | Resultado | Implicación |
|---|---:|---|
| Registros totales | 433 | El experimento debe asignar 217 a A y 216 a B. |
| Correos únicos | 433 | No hay duplicados exactos por email. |
| Empresas únicas | 433 | No hay duplicados exactos por nombre de empresa; conviene validar grupos relacionados por dominio o razón social. |
| Correos personales/gratuitos | 315, 72.75% | No personalizar por nombre ni inferir cargo. Priorizar confirmación de contacto. |
| Direcciones con apariencia funcional o de área | 27 | Son señales débiles; deben validarse, no asumirse como decisores. |
| Correos con formato inválido | 0 | La sintaxis es válida, pero esto no garantiza entregabilidad ni vigencia. |
| Desajuste simple entre dominio y empresa | 106 | Es una alerta heurística; puede deberse a marcas, razones sociales, consultores, dominios de grupo o correos personales. |
| Cluster 1 corporativo | 10 | Muestra pequeña; interpretar resultados sólo como señal direccional. |
| Cluster 2 regional | 331 | Es el segmento con mayor poder estadístico operativo. |
| Cluster 3 independiente/PYME | 92 | Conviene analizarlo por separado, no mezclarlo sin control. |

## Problemas detectados en la secuencia original

La secuencia original trataba como hechos varias condiciones que no estaban confirmadas por contacto: que el prospecto está evaluando cobro en bomba, que usa un banco adquirente específico, que le importa T+1, que necesita antifraude, que quiere terminales ATEX y que tiene autoridad sobre la operación. También repetía prácticamente el mismo argumento con distintos asuntos, por lo que las variantes no constituían un experimento limpio de hipótesis comerciales.

El nuevo diseño evita esos supuestos. No presenta PayMind como respuesta antes de entender la operación y no pide una demo en el primer contacto. La primera acción deseada es más modesta y medible: que el mensaje llegue a la persona correcta o que el contacto describa brevemente cómo se resuelve hoy el pago.

## Diseño del A/B test

Se utilizó una asignación aleatoria reproducible con semilla fija y balanceada dentro de cada cluster. Así se evita que el resultado dependa de que un grupo tenga más empresas grandes, independientes o corporativas.

| Grupo | Hipótesis que prueba | Asunto inicial | CTA principal |
|---|---|---|---|
| A | Una pregunta concreta sobre el proceso actual genera conversación. | “Una pregunta sobre el cobro en pista” | Describir cómo se paga hoy y orientar al responsable. |
| B | Identificar al responsable antes de profundizar mejora el enrutamiento. | “¿Quién lleva el tema de pagos en la estación?” | Compartir el contacto de pagos, operaciones o sistemas. |

La variable principal no debe ser la apertura. En una base con 72.75% de correos personales, la apertura puede estar más determinada por entregabilidad, antigüedad de la dirección o filtros del proveedor que por la calidad del mensaje. El orden recomendado de métricas es: **respuesta humana**, **respuesta que redirige al responsable**, **conversación calificada** y finalmente **reunión aceptada**.

| Métrica | Definición sugerida | Cómo clasificarla |
|---|---|---|
| Entregado | El proveedor no registra rebote duro. | Control de calidad de base, no éxito comercial. |
| Respuesta humana | Respuesta escrita por una persona, positiva o negativa. | Éxito de conversación. |
| Respuesta útil | Indica cómo operan, quién decide o quién es el contacto correcto. | Métrica primaria. |
| Reunión | Aceptación explícita de conversar. | Métrica de avance. |
| Rebote duro | Dirección inexistente, dominio inválido o rechazo permanente. | Depurar y no reintentar. |
| Desuscripción o molestia | Solicitud de no contacto o respuesta negativa clara. | Suprimir de inmediato. |

## Reglas de ejecución

Carga los archivos A y B como campañas separadas o utiliza el campo `Test_Group` para dividirlos. No mezcles ambas secuencias en la misma campaña si la plataforma puede reenviar varias variantes al mismo contacto. Mantén iguales los días y horarios de envío, la firma, el remitente y el número máximo de seguimientos. No cambies el copy después de comenzar la prueba, salvo para corregir un error factual o de entregabilidad.

La cadencia sugerida es de cinco toques en un periodo aproximado de 10 a 14 días, pero la secuencia debe detenerse en cuanto haya respuesta, rebote, desuscripción o una indicación de que la persona ya no pertenece a la empresa. El último mensaje es un cierre, no un intento adicional de presión.

## Revisión de identidad

Antes de interpretar una respuesta como oportunidad, confirma quién responde, qué relación tiene con la estación y si puede orientar hacia operaciones, sistemas, administración o pagos. En los 106 desajustes heurísticos entre empresa y dominio, no corrijas automáticamente el registro: marca la fila para revisión manual. Un dominio distinto puede ser válido si pertenece a una marca comercial, grupo empresarial, despacho externo o proveedor.

## Limitaciones

El archivo no contiene cargo, estación específica, ciudad, fuente del dato, fecha de verificación ni evidencia de que el contacto siga en la empresa. Por lo tanto, no es posible calcular una tasa real de contactos válidos sólo a partir del CSV. El A/B test medirá qué mensaje funciona mejor **sobre esta base actual**, no qué mensaje es universalmente mejor para el sector gasolinero.

La asignación queda balanceada a nivel de cluster, pero el Cluster 1 sólo tiene 10 registros. Cualquier diferencia observada en ese segmento debe considerarse exploratoria y no concluyente.
