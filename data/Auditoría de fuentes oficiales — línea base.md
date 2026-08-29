# Auditoría de fuentes oficiales — línea base

## Objetivo

Determinar qué números pueden presentarse a nivel CEO sin inflar la oportunidad. La unidad principal será **llegadas de visitantes internacionales por país de residencia/nacionalidad a Quintana Roo**, para un periodo definido. La derrama se presentará aparte como una **estimación calculada**, no como un dato oficial, salvo que una fuente primaria publique directamente el gasto en sitio correspondiente.

## Métricas comparables

| Métrica | Definición que se utilizará | Fuente preferida |
|---|---|---|
| Llegadas | Visitantes del país de origen que llegan a Quintana Roo por vía aérea, con periodo y definición explícitos | DATATUR/SECTUR/SEDETUR/Unidad de Política Migratoria |
| Turistas vs visitantes | Se distinguirán turistas con pernocta de excursionistas y pasajeros en tránsito | DATATUR/SECTUR |
| Gasto | Gasto turístico total o gasto en sitio, sin mezclar ambos | SECTUR/DATATUR, banco central o instituto estadístico del país, con metodología |
| Derrama | Llegadas × gasto medio comparable; se marcará como cálculo propio si no es publicada directamente | Hoja de cálculo auditada |
| Riel de pago | Método local de pago y estado del producto | 8B, banco central o autoridad del país |
| Mercado potencial | Escenario de captura sobre una base de gasto, con porcentaje y fórmula visibles | Modelo propio, no dato oficial |

## Línea base actualmente usada en el proyecto

| País | Repo / compilación reciente | Repo / compendio previo | Problema a resolver |
|---|---:|---:|---|
| Brasil | 380k–420k | 150k | Diferencia material; puede ser residentes, llegadas, años o población distinta |
| Colombia | 280k–310k | 380k | Diferencia material; requiere definición de nacionalidad/residencia y periodo |
| Argentina | 140k–170k | 160k | Compatible como rango, pero falta periodo y fuente exacta |
| Perú | 80k–100k | 135k | Diferencia material; requiere fuente y definición |
| Top 4 | 850k–1.05M | 825k | No usar una cifra única hasta reconciliar los países |
| Gasto medio | $1,095 USD | $1,088.58 USD promedio Top 4 | Las bases por país no son idénticas |
| TAM | $1,150M USD | $1,113.2M USD | La cifra alta requiere explicar ajuste/otros mercados |
| SAM | $362.2M USD | $350.6M USD | Cambia la base y el porcentaje aplicado |
| SOM Año 1 | $54.3M USD | $3.506M USD en otro escenario | Son escenarios diferentes, no una misma proyección |

## Regla de presentación provisional

Hasta que las fuentes primarias confirmen las cifras, el one-pager debe utilizar una **horquilla de mercado** y no un número puntual. El mensaje defendible es que existe un mercado latinoamericano relevante y concentrado en categorías presenciales del Caribe Mexicano, pero el sizing exacto debe cerrarse con la misma definición de visitante, periodo y gasto.

## Fuente primaria mínima a localizar

Para México y Quintana Roo se buscarán DATATUR, SECTUR, SEDETUR Quintana Roo, Unidad de Política Migratoria y estadísticas de aeropuertos cuando corresponda. Para los países de origen se buscarán IBGE/BCB/Embratur o Ministério do Turismo de Brasil; DANE/MinCIT/Banco de la República de Colombia; INDEC/Secretaría de Turismo y Deportes/BCRA de Argentina; y MINCETUR/BCRP/SUNAT o autoridad turística peruana. No se considerarán “oficiales” blogs comerciales ni presentaciones de proveedores de pagos.

## Fuentes oficiales consultadas: México y Quintana Roo

**DATATUR / SECTUR México — Llegadas por residencia:** https://datatur.sectur.gob.mx/SitePages/upmresidencia.aspx. La página identifica el reporte dinámico de la Unidad de Política Migratoria, Registro e Identidad de Personas por residencia y ofrece reportes mensuales 2024, 2025 (cifras validadas), 2026 (cifras preliminares) y una base de datos descargable `BD_Residencia.zip`. Esto confirma que existe una fuente primaria adecuada para trabajar por país de residencia y que el periodo debe expresarse con precisión.

**SITUR Quintana Roo — Indicadores turísticos:** https://siturq.gob.mx/indicadores-turisticos. La navegación textual no cargó contenido usable en esta sesión; se conserva como fuente oficial a revisar por descarga o consulta alternativa. El buscador identifica que publica estimaciones de la Secretaría de Turismo del Estado de Quintana Roo con datos de diversas fuentes, por lo que sus cifras deben distinguirse de las tablas UPM/DATATUR.

La página pública de DATATUR muestra el botón `Base de datos` enlazado a `https://datatur.sectur.gob.mx/Documentoscompartidos/upm/BD_Residencia.zip`. El enlace fue activado en navegador; no se obtuvo confirmación de descarga en la sesión, por lo que los números del repositorio todavía no deben presentarse como reconciliados con esa base hasta leer el archivo o los reportes mensuales oficiales.

## Resultado oficial de SEDETUR Quintana Roo

Fuente: https://sedetur.qroo.gob.mx/presenta-sedetur-resultados-ante-el-congreso-del-estado-quintana-roo-continua-siendo-lider-nacional-en-materia-turistica/

El comunicado de SEDETUR sobre la comparecencia del Tercer Informe reporta que, al cierre de 2024, Quintana Roo recibió **20.9 millones de turistas**, registró **32.7 millones de pasajeros** y atendió **7.1 millones de cruceristas**. Para enero-julio de 2025 reporta **más de 12 millones de turistas**, de los cuales **66.1% fueron internacionales y 33.9% nacionales**, además de **4.5 millones de cruceristas**, y señala un crecimiento de 3.2% contra el mismo periodo de 2024. También reporta más de 135 mil habitaciones y conexión con 125 ciudades.

Estas cifras son estatales y agregadas; no validan por sí solas los 850 mil–1.05 millones de turistas sudamericanos ni el desglose por Brasil, Colombia, Argentina y Perú. Para eso se requiere la base DATATUR/UPM por país de residencia y mismo periodo.

## Fuente oficial estatal clave: SITUR Quintana Roo, Mercados Estratégicos diciembre 2024

Reporte oficial: https://returq.siturq.gob.mx/storage/pdf/situr/strategic-markets/be07fec7-2224-4d24-a845-58b713aceb89.pdf

El informe reporta para enero-diciembre de 2024, por **nacionalidad**, 237,667 pasajeros de Colombia, 226,431 de Argentina y 85,520 de Brasil. Perú aparece en mercados emergentes con 67,933 pasajeros. La suma de estos cuatro países es **617,551 pasajeros**.

Por **país de residencia**, el mismo informe reporta 219,848 Colombia, 217,197 Argentina, 73,888 Brasil y 62,942 Perú; la suma es **573,875 pasajeros**. Esta es la base más defendible para un análisis de demanda por residencia, pero debe llamarse `pasajeros a los aeropuertos de Quintana Roo`, no automáticamente turistas únicos.

El reporte también informa **15,945,568 pasajeros totales** en los aeropuertos de Quintana Roo en 2024, de los cuales **10,314,613 fueron internacionales**. La fuente metodológica indicada es INM para internacionales y Aeronáutica Civil para nacionales. El reporte separa nacionalidad y residencia, una distinción que debe conservarse en el one-pager.

La misma publicación informa participaciones 2024 por nacionalidad de 1.5% Colombia, 1.4% Argentina y 0.5% Brasil; Perú se trata como mercado emergente. Por residencia, los valores son 219,848 Colombia, 217,197 Argentina, 73,888 Brasil y 62,942 Perú.

## Fuente oficial de país de origen: INDEC Argentina

Informe: https://www.indec.gob.ar/uploads/informesdeprensa/eti_10_24FB49392E89.pdf

El informe oficial de INDEC de septiembre y tercer trimestre de 2024 distingue visitantes, turistas y excursionistas y define la Encuesta de Turismo Internacional. Para septiembre de 2024 reporta 580.0 mil turistas residentes que salieron de Argentina por todas las vías internacionales; los principales destinos fueron Chile, Brasil y Europa. El documento confirma que la fuente argentina tiene una metodología estadística formal, pero no ofrece en el fragmento revisado una cifra anual comparable de argentinos que viajaron específicamente a Quintana Roo. Por tanto, para el sizing México debe preferirse el dato de llegada en Quintana Roo de SITUR/INM y usar INDEC como contexto de turismo emisivo, no como sustituto del dato destino.

## Fuentes oficiales de rieles en países de origen

**Argentina — BCRA Transferencias 3.0:** https://www.bcra.gob.ar/transferencias-3-0/. El BCRA define transferencias inmediatas con acreditación en línea en un máximo de 15 segundos, disponibles 24/7. Incluye pagos con transferencia mediante códigos QR y los describe como interoperables: cualquier billetera puede pagar cualquier marca de QR. También informa que los pagos recibidos son inmediatos e irrevocables una vez acreditados. Esto sí sustenta la tesis de experiencia doméstica interoperable, pero no prueba disponibilidad del corredor Argentina–México en 8B.

**Perú — BCRP, Reporte del Sistema Nacional de Pagos marzo 2026:** https://www.bcrp.gob.pe/publicaciones/reporte-del-sistema-nacional-de-pagos/rspf-marzo-2026.html. El BCRP reporta que en 2025 los pagos digitales alcanzaron 665 por adulto al año; las fases 1 y 2 —interoperabilidad Yape/Plin y aplicativos bancarios/códigos QR— generaron más de 263 millones de transacciones mensuales en diciembre de 2025. Los pagos QR mostrados por comercios crecieron de 27 a 47 millones mensuales entre diciembre de 2024 y diciembre de 2025. Esto respalda la relevancia del comportamiento QR interoperable peruano, pero no una cifra de turistas a México.

**Colombia — Banco de la República, Bre-B:** https://www.banrep.gov.co/es/bre-b. El banco central define Bre-B como el sistema de pagos inmediatos interoperable de Colombia y mantiene una página oficial con novedades, regulación y evolución del sistema. Esto respalda el riel conceptual, pero el one-pager debe mantener `Bre-B` como fase sujeta a disponibilidad de 8B/EthosPay.

**Brasil — Banco Central do Brasil, Pix:** https://www.bcb.gov.br/en/pressdetail/2640/nota y https://www.bcb.gov.br/estabilidadefinanceira/pix-em-numeros-estatisticas. El BCB mantiene estadísticas oficiales de Pix y un comunicado institucional que reporta casi 170 millones de usuarios y BRL 11 billones en transacciones durante 2024. El contenido de la página inglesa no se cargó por depender de JavaScript, por lo que la cifra debe citarse como comunicado del BCB y no mezclarse con los claims de los PDFs de 8B hasta revisar el documento institucional completo.

## Reconciliación cuantitativa preliminar

Con la tabla oficial de SITUR/INM por **residencia** para 2024, los cuatro países suman: Colombia 219,848 + Argentina 217,197 + Brasil 73,888 + Perú 62,942 = **573,875 pasajeros**. Esto es 251,125 menos que los 825,000 del Top 4 del repositorio, una diferencia de 30.4%.

Si se multiplican esos pasajeros por los gastos promedio por país que usa el repositorio —Colombia $1,039.55, Argentina $1,125.75, Brasil $1,209 y Perú $980— se obtiene una **derrama indicativa de $624.1M USD**. Ese cálculo no es una cifra oficial: combina conteos oficiales de pasajeros con supuestos de gasto del modelo. Debe presentarse como `escenario de gasto en sitio` y no como derrama observada.

La cifra oficial más sólida para el one-pager es, por tanto, **573,875 pasajeros por residencia en Quintana Roo durante 2024**. La cifra de gasto debe mantenerse como rango o escenario hasta encontrar una publicación primaria que reporte gasto por país y destino bajo la misma definición.

Los 573,875 pasajeros por residencia de Colombia, Argentina, Brasil y Perú representan aproximadamente **5.56%** de los 10,314,613 pasajeros internacionales reportados para Quintana Roo en 2024. La cifra es un cálculo aritmético sobre datos del informe y debe mostrarse como participación aproximada, no como penetración comercial.
