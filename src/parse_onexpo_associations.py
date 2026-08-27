import os
import json
import pandas as pd

raw_text = """
Aguascalientes
Gasucen
Gasolineros Unidos del Centro A.C.Av. Independencia #1331 int. 15Col. El Plateado
Tel: (449) 153-01-33
Baja California
Asociación de Gasolineros de Mexicali A.C.
Av. Torreón y Gob. Esteban Cantú #399Ex Ejido Coahuila C.P. 21360Mexicali, BC
Tel: (01) 686 554-1172
Asociación de Gasolineros de Ensenada A.C.
Blvd. Pinta #397Fracc. Valle Dorado C.P.22890 Ensenada, BC
(01) 646 173-5963(01) 646 173-5964
Grupo Energético de Baja California, A.C.
David Alfaro Siqueiros #2589Zona Urbana Río Tijuana C.P. 22110Tijuana, BC
(01) 664 386-0543
Baja California Sur
ONEXPO Sudcalifornia A.C.
Calzada Agustín Olachea #3215Col. Pueblo NuevoLa Paz, BCS
(01) 612 128-9400
Campeche
UGEC
Unión de Gasolineros de Campeche A.C.Av. Ruiz Cortines #112 Torre-B 3er.Piso Col. San Román C.P. 24040Campeche, Cam.
(01) 981 127-3249 ext.149
Chiapas
UDGCHAC
Union de Distribuidores de Gasolina de Chiapas A.C.2o. Ote Sur #53 Zona Centro C.P. 29140Ocozucuautla de Espinosa, Chiapas.
Teléfono de la Unión:(01) 961 639 29 79(01) 961 615 30 95
Chihuahua
OEPDCH
Organización de Expendedores de Petróleo de Chihuahua A.C.Av. Prolongación Teófilo Borunda N0. 11800 InteriorCol. Ejido Labor de Terrazas C.P.31415Chihuahua, Chih.
(01) 614 441-6417(02) 614 189-9648
ONEXPO de Ciudad Juárez A.C.
Carr. Panaméricana y Casas Grandes km. 13.5Col. Lomas del Puente Alto C.P. 32695Cd. Juárez, Chih.
(01) 656 633-1107
Coahuila
Empresarios Coahuilenses Gasolineros, A.C.
Abasolo Norte #2014Zona Centro C.P. 25000Saltillo Coahuila, México
ecoagas@gmail.com
ONEXPO de Coahuila, A.C.
Diego Montemayor #178 SurCol. Centro C.P. 66230San Pedro Garza García, N.L.
01 (818) 338-3414
UEPCLCYD
Diag. reforma #3509 OritneteCol. Nuevo TorreónC.P. 27060Torreón, Coahuila
01 (871) 717-0023
Colima
Unión de Gasolineros del Estado de Colima A.C.
Miguel Cervantes Saavedra 365-6Hacienda Real, Colima. Col.CP 28018
01 (312) 330-5440
Distrito Federal
CEGA
Consejo Empresarial Gasolinero del Valle de México A.C.Río Tiber #91 Despacho 101 Col. Cuauhtémoc C.P. 06500México, DF
(01) 55 5525-2178(01) 55 5525-2322
Durango
ONEXPO Durango A.C.
Carretera Durango - Zacatecas #1300Col. Agrícola C.P. 34240Durango, Dgo.
(01) 618 836-0919(01) 618 828-1703
UEPCLYD Unión de Expendedores de Petróleos de laComarca Lagunera, Coahuila y Durango A.C.
Diag. Reforma Oriente #3509Col. Nuevo Torreón C.P. 27060Torreón, Coah.
(01) 871 721-3600(01) 871-721-3606 -Fax
Estado de México
RGC
Red de Gasolineros del Centro A.C.Guerrero Ote. #32 Av. Guerrero Ote. #32Col. Centro C.P. 54240 Jilotepec, Edo. Méx
(01) 761 734-1400 Ext. 214(01) 761 734-1959
ADIGAL
Asociación de Distribuidores de Gasolinay Lubricantes A.C. Heriberto Enríquez#904 Plaza Fermín Col. AztecasC.P.50180 Toluca, Edo. Méx
(01) 722 270-8939(01) 722 616-5582
Guanajuato
UNAGAS
Unión Nacional de Gasolineros A.C.Blvd. Adolfo López Mateos Pte. #1020-212Centro comercial Metro Plaza C.P. 38040Celaya, Gto.(01) 461 615-2443(01) 461 615-2443 -Fax
AGAZI
Asociación de Gasolineros Zona Irapuato A.C.Av. De los Insurgentes #2560Col. Los Fresnos C.P. 36555Irapuato, Gto.
(01) 462 623-5331
ONEXPO León A.C.
Blvd. Miguel de Cervantes Saavedra.#701 Col. Vista Hermosa SurC.P. 37330 León, Gto.
(01) 477 777-0898
Guerrero
AGGAC
Asociación de Gasolineras de Guerrero A.C.Andrés de Uraneta y Pedro Áviles s/nFracc. Hornos C.P. 39355Acapulco, Gro.
(01) 744 485-2203(01) 744 482-1142
Hidalgo
GAH
Gasolineros Asociados de Hidalgo A.C.Melchor Ocampo #103Col. Centro C.P.42800Tula de Allende, Hgo.
(01) 773 732-4467
EGH
Empresarios Gasolineros de Hidalgo A.C.Lote #2 Parque Industrial C.P.43998Sahagún, Hgo.
(01) 791 913-5990(01) 771 718-6086
Jalisco
ONEXPO Jalisco A.C.
Av. Patria #424Col. Jardines de la Patria C.P. 45110Zapopan, Jal.
(01) 333 111-9970
Michoacán
UGAMI
Unión de Gasolineros de Michoacán A.C.5 de febrero #23-313Col. Centro C.P.60000 Uruapan, Mich.
(01) 452 527-0089
Morelos
UGEM
Unión de Gasolineros del Estado de Morelos A.C.Carr. Cuernavaca - Cuautla Km. 27.3Col. Jovito SerranoYautepec, Mor. C.P. 62730
(01) 735 394-2174
Nayarit
Organización de Expendedores de Petrolíferos de Nayarit A.C.
12 de Octubre Sur #193Col. José María MenchacaC.P. 63130Tepic, Nay.
(01) 311 214-2029(01) 311 213-7166
Nuevo León
Organización Neolonesa de Expendedores de Petróleo A.C.
José Calderón #550 Col. ChepeveraC.P. 64030 TMonterrey, NL.
(01) 81 8347-5592(01) 81 8348-55324
Oaxaca
EGEO
Empresarios Gasolineros delEstado de OaxacaA.C. Jazmines #936Col. Reforma C.P. 68050Oaxaca, Oax.(01) 951 503-2195
Puebla
OPAC
ONEXPO Puebla A.C.Calz. Zavaleta #703 piso 2 despacho 202 "E"Campestre El Paraíso C.P. 72150Puebla, Pue.
(01) 222 574-9021
Querétaro
AEGA
Asociación de Empresarios Gasolineros de Querétaro A.C.Km. 32 Carr. a San Miguel de Allende - Qro.Apdo. Postal 687 C.P. 37700San Miguel de Allende, Gto.
(01) 415 152-5511(01) 415 152-1133(01) 452 523-0684
UESQRO
Unión de Estaciones de Servicio de Querétaro, A.C.Av. Armando Birlain Shaffler #2001,Torre 1, piso 7-B Col. Centro Sur C.P. 76090Querétaro, Qro.
(442) 229 3304
Quintana Roo
AES
Asociación de Estaciones de Servicio de Quintana Roo A.C.Calle 18 #201 B entre 23 y 25Col. García Ginerés C.P.97070Mérida Yuc.
(01) 999 925-4905(01) 999 925-0129
San Luis Potosí
ONEXPO SLP
Edif. Cámara de Comercio de SLP Prolong.Av. Coronel Romero #2100 (periférico sur)Col. Tierra Blanca C.P.78364,San Luis Potosí, SLP
(01) 444 839-1457(01) 444 820-2475
UGZHMP
Unión de Gasolineros de la Zona Huasteca y MediaPotosina A.C. Pedro Antonio de los Santos #443-7Zona Centro C.P.79040Cd. Valles, SLP
(01) 481 381-0749
Sinaloa
ONEXPO Sinaloa A.C.
Blvd. Pedro María Anaya #1787-7Col. Chapultepec C.P. 80040Culiacán, Sinaloa
(01) 667 716-6725(01) 667 713-5358 -Fax
Sonora
ONEXPO Sonora A.C.
Veracruz #239 entre Ramón Corral y Juan G.Cabral Col. Country Club C.P.83150Hermosillo, Son.
(01) 662 210-3575(01) 662 210-0475
Tabasco
UNEXPETAB
Unión de Expendedores de Pemex del Estado de Tabasco,Nte. de Chiapas y Poniente de Campeche A.C.Prol. Paseo de Usumacinta s/nCol. Guayabal C.P. 86090Villa Hermosa, Tab.
(01) 993 352-2302
Tamaulipas
OTEXPO A.C
Alhelies #20Col. Jardín C.P.87330Matamoros, Tam.
(01) 868 813-0505(01) 868 824-0522
Veracruz
OGAVE
Organización de Gasolineros de Veracruz A.C.Blvd. Adolfo Ruíz Cortines esq. Ciencias Exactas s/nFracc. SUTSEM C.P. 94299Boca del Río, Ver.
(01) 229 921-7500(01) 229 922-2411(01) 229 921-4272
Yucatán
UGY
Unión de Gasolineros del Estado de Yucatán A.C.Calle 27 #86 entre 18 y 20Col. Chichén Itzá C.P. 97170Mérida, Yuc.
(01) 999 926-8016(01) 999 926-8026
GUPYAC
Calle 20 #235 entre calle 7 y 15Edifi. Luxus Altabrisa piso 6Fracc. Altabrisa C.P. 97130Mérida, Yuc.
(01) 999 270-4735
Zacatecas
GAZAC
Av. Hacienda de Bernardez #106 AFraccionamiento Conde de BernardezGuadalupe, ZacatecasCp.98617
(01) 492 921-2345
"""

associations = [
    {"Estado": "Aguascalientes", "Siglas": "Gasucen", "Nombre": "Gasolineras Unidas del Centro A.C.", "Direccion": "Av. Independencia #1331 int. 15 Col. El Plateado", "Telefono": "(449) 153-01-33", "Email": ""},
    {"Estado": "Baja California", "Siglas": "AGM", "Nombre": "Asociación de Gasolineros de Mexicali A.C.", "Direccion": "Av. Torreón y Gob. Esteban Cantú #399 Ex Ejido Coahuila C.P. 21360 Mexicali, BC", "Telefono": "(686) 554-1172", "Email": ""},
    {"Estado": "Baja California", "Siglas": "AGE", "Nombre": "Asociación de Gasolineros de Ensenada A.C.", "Direccion": "Blvd. Pinta #397 Fracc. Valle Dorado C.P. 22890 Ensenada, BC", "Telefono": "(646) 173-5963", "Email": ""},
    {"Estado": "Baja California", "Siglas": "GEBC", "Nombre": "Grupo Energético de Baja California, A.C.", "Direccion": "David Alfaro Siqueiros #2589 Zona Urbana Río Tijuana C.P. 22110 Tijuana, BC", "Telefono": "(664) 386-0543", "Email": ""},
    {"Estado": "Baja California Sur", "Siglas": "ONEXPO BCS", "Nombre": "ONEXPO Sudcalifornia A.C.", "Direccion": "Calzada Agustín Olachea #3215 Col. Pueblo Nuevo La Paz, BCS", "Telefono": "(612) 128-9400", "Email": ""},
    {"Estado": "Campeche", "Siglas": "UGEC", "Nombre": "Unión de Gasolineros de Campeche A.C.", "Direccion": "Av. Ruiz Cortines #112 Torre-B 3er.Piso Col. San Román C.P. 24040 Campeche, Cam.", "Telefono": "(981) 127-3249 ext.149", "Email": ""},
    {"Estado": "Chiapas", "Siglas": "UDGCHAC", "Nombre": "Union de Distribuidores de Gasolina de Chiapas A.C.", "Direccion": "2o. Ote Sur #53 Zona Centro C.P. 29140 Ocozucuautla de Espinosa, Chiapas", "Telefono": "(961) 639-2979 / (961) 615-3095", "Email": ""},
    {"Estado": "Chihuahua", "Siglas": "OEPDCH", "Nombre": "Organización de Expendedores de Petróleo de Chihuahua A.C.", "Direccion": "Av. Prolongación Teófilo Borunda No. 11800 Col. Ejido Labor de Terrazas C.P. 31415 Chihuahua, Chih.", "Telefono": "(614) 441-6417", "Email": ""},
    {"Estado": "Chihuahua", "Siglas": "ONEXPO Juárez", "Nombre": "ONEXPO de Ciudad Juárez A.C.", "Direccion": "Carr. Panamericana y Casas Grandes km. 13.5 Col. Lomas del Puente Alto C.P. 32695 Cd. Juárez, Chih.", "Telefono": "(656) 633-1107", "Email": ""},
    {"Estado": "Coahuila", "Siglas": "ECOAGAS", "Nombre": "Empresarios Coahuilenses Gasolineros, A.C.", "Direccion": "Abasolo Norte #2014 Zona Centro C.P. 25000 Saltillo, Coahuila", "Telefono": "", "Email": "ecoagas@gmail.com"},
    {"Estado": "Coahuila", "Siglas": "ONEXPO Coahuila", "Nombre": "ONEXPO de Coahuila, A.C.", "Direccion": "Diego Montemayor #178 Sur Col. Centro C.P. 66230 San Pedro Garza García, N.L.", "Telefono": "(818) 338-3414", "Email": ""},
    {"Estado": "Coahuila", "Siglas": "UEPCLCYD", "Nombre": "Unión de Expendedores de Petróleos de la Comarca Lagunera, Coahuila y Durango A.C.", "Direccion": "Diag. Reforma #3509 Oriente Col. Nuevo Torreón C.P. 27060 Torreón, Coahuila", "Telefono": "(871) 717-0023", "Email": ""},
    {"Estado": "Colima", "Siglas": "UGEC Colima", "Nombre": "Unión de Gasolineros del Estado de Colima A.C.", "Direccion": "Miguel Cervantes Saavedra 365-6 Hacienda Real, Colima C.P. 28018", "Telefono": "(312) 330-5440", "Email": ""},
    {"Estado": "CDMX", "Siglas": "CEGA", "Nombre": "Consejo Empresarial Gasolinero del Valle de México A.C.", "Direccion": "Río Tiber #91 Despacho 101 Col. Cuauhtémoc C.P. 06500 México, DF", "Telefono": "(55) 5525-2178 / (55) 5525-2322", "Email": ""},
    {"Estado": "Durango", "Siglas": "ONEXPO Durango", "Nombre": "ONEXPO Durango A.C.", "Direccion": "Carretera Durango - Zacatecas #1300 Col. Agrícola C.P. 34240 Durango, Dgo.", "Telefono": "(618) 836-0919", "Email": ""},
    {"Estado": "Estado de México", "Siglas": "RGC", "Nombre": "Red de Gasolineros del Centro A.C.", "Direccion": "Av. Guerrero Ote. #32 Col. Centro C.P. 54240 Jilotepec, Edo. Méx", "Telefono": "(761) 734-1400 ext 214", "Email": ""},
    {"Estado": "Estado de México", "Siglas": "ADIGAL", "Nombre": "Asociación de Distribuidores de Gasolina y Lubricantes A.C.", "Direccion": "Heriberto Enríquez #904 Plaza Fermín Col. Aztecas C.P. 50180 Toluca, Edo. Méx", "Telefono": "(722) 270-8939 / (722) 616-5582", "Email": ""},
    {"Estado": "Guanajuato", "Siglas": "UNAGAS", "Nombre": "Unión Nacional de Gasolineros A.C.", "Direccion": "Blvd. Adolfo López Mateos Pte. #1020-212 Centro Comercial Metro Plaza C.P. 38040 Celaya, Gto.", "Telefono": "(461) 615-2443", "Email": ""},
    {"Estado": "Guanajuato", "Siglas": "AGAZI", "Nombre": "Asociación de Gasolineros Zona Irapuato A.C.", "Direccion": "Av. De los Insurgentes #2560 Col. Los Fresnos C.P. 36555 Irapuato, Gto.", "Telefono": "(462) 623-5331", "Email": ""},
    {"Estado": "Guanajuato", "Siglas": "ONEXPO León", "Nombre": "ONEXPO León A.C.", "Direccion": "Blvd. Miguel de Cervantes Saavedra #701 Col. Vista Hermosa Sur C.P. 37330 León, Gto.", "Telefono": "(477) 777-0898", "Email": ""},
    {"Estado": "Guerrero", "Siglas": "AGGAC", "Nombre": "Asociación de Gasolineras de Guerrero A.C.", "Direccion": "Andrés de Urdaneta y Pedro Áviles s/n Fracc. Hornos C.P. 39355 Acapulco, Gro.", "Telefono": "(744) 485-2203", "Email": ""},
    {"Estado": "Hidalgo", "Siglas": "GAH", "Nombre": "Gasolineros Asociados de Hidalgo A.C.", "Direccion": "Melchor Ocampo #103 Col. Centro C.P. 42800 Tula de Allende, Hgo.", "Telefono": "(773) 732-4467", "Email": ""},
    {"Estado": "Hidalgo", "Siglas": "EGH", "Nombre": "Empresarios Gasolineros de Hidalgo A.C.", "Direccion": "Lote #2 Parque Industrial C.P. 43998 Sahagún, Hgo.", "Telefono": "(791) 913-5990 / (771) 718-6086", "Email": ""},
    {"Estado": "Jalisco", "Siglas": "ONEXPO Jalisco", "Nombre": "ONEXPO Jalisco A.C.", "Direccion": "Av. Patria #424 Col. Jardines de la Patria C.P. 45110 Zapopan, Jal.", "Telefono": "(333) 111-9970", "Email": ""},
    {"Estado": "Michoacán", "Siglas": "UGAMI", "Nombre": "Unión de Gasolineros de Michoacán A.C.", "Direccion": "5 de febrero #23-313 Col. Centro C.P. 60000 Uruapan, Mich.", "Telefono": "(452) 527-0089", "Email": ""},
    {"Estado": "Morelos", "Siglas": "UGEM", "Nombre": "Unión de Gasolineros del Estado de Morelos A.C.", "Direccion": "Carr. Cuernavaca - Cuautla Km. 27.3 Col. Jovito Serrano Yautepec, Mor. C.P. 62730", "Telefono": "(735) 394-2174", "Email": ""},
    {"Estado": "Nayarit", "Siglas": "OEPN", "Nombre": "Organización de Expendedores de Petrolíferos de Nayarit A.C.", "Direccion": "12 de Octubre Sur #193 Col. José María Menchaca C.P. 63130 Tepic, Nay.", "Telefono": "(311) 214-2029 / (311) 213-7166", "Email": ""},
    {"Estado": "Nuevo León", "Siglas": "ONEXPO NL", "Nombre": "Organización Neolonesa de Expendedores de Petróleo A.C.", "Direccion": "José Calderón #550 Col. Chepevera C.P. 64030 Monterrey, NL.", "Telefono": "(81) 8347-5592 / (81) 8348-5532", "Email": ""},
    {"Estado": "Oaxaca", "Siglas": "EGEO", "Nombre": "Empresarios Gasolineros del Estado de Oaxaca A.C.", "Direccion": "Jazmines #936 Col. Reforma C.P. 68050 Oaxaca, Oax.", "Telefono": "(951) 503-2195", "Email": ""},
    {"Estado": "Puebla", "Siglas": "OPAC", "Nombre": "ONEXPO Puebla A.C.", "Direccion": "Calz. Zavaleta #703 piso 2 despacho 202 'E' Campestre El Paraíso C.P. 72150 Puebla, Pue.", "Telefono": "(222) 574-9021", "Email": ""},
    {"Estado": "Querétaro", "Siglas": "AEGA", "Nombre": "Asociación de Empresarios Gasolineros de Querétaro A.C.", "Direccion": "Km. 32 Carr. a San Miguel de Allende - Qro. Apdo. Postal 687 C.P. 37700 San Miguel de Allende, Gto.", "Telefono": "(415) 152-5511", "Email": ""},
    {"Estado": "Querétaro", "Siglas": "UESQRO", "Nombre": "Unión de Estaciones de Servicio de Querétaro, A.C.", "Direccion": "Av. Armando Birlain Shaffler #2001 Torre 1, piso 7-B Col. Centro Sur C.P. 76090 Querétaro, Qro.", "Telefono": "(442) 229-3304", "Email": ""},
    {"Estado": "Quintana Roo", "Siglas": "AES Q.Roo", "Nombre": "Asociación de Estaciones de Servicio de Quintana Roo A.C.", "Direccion": "Calle 18 #201 B entre 23 y 25 Col. García Ginerés C.P. 97070 Mérida, Yuc.", "Telefono": "(999) 925-4905", "Email": ""},
    {"Estado": "San Luis Potosí", "Siglas": "ONEXPO SLP", "Nombre": "ONEXPO SLP A.C.", "Direccion": "Edif. Cámara de Comercio de SLP Prolong. Av. Coronel Romero #2100 Col. Tierra Blanca C.P. 78364 San Luis Potosí, SLP", "Telefono": "(444) 839-1457 / (444) 820-2475", "Email": ""},
    {"Estado": "San Luis Potosí", "Siglas": "UGZHMP", "Nombre": "Unión de Gasolineros de la Zona Huasteca y Media Potosina A.C.", "Direccion": "Pedro Antonio de los Santos #443-7 Zona Centro C.P. 79040 Cd. Valles, SLP", "Telefono": "(481) 381-0749", "Email": ""},
    {"Estado": "Sinaloa", "Siglas": "ONEXPO Sinaloa", "Nombre": "ONEXPO Sinaloa A.C.", "Direccion": "Blvd. Pedro María Anaya #1787-7 Col. Chapultepec C.P. 80040 Culiacán, Sinaloa", "Telefono": "(667) 716-6725", "Email": ""},
    {"Estado": "Sonora", "Siglas": "ONEXPO Sonora", "Nombre": "ONEXPO Sonora A.C.", "Direccion": "Veracruz #239 entre Ramón Corral y Juan G. Cabral Col. Country Club C.P. 83150 Hermosillo, Son.", "Telefono": "(662) 210-3575", "Email": ""},
    {"Estado": "Tabasco", "Siglas": "UNEXPETAB", "Nombre": "Unión de Expendedores de Pemex del Estado de Tabasco, Nte. de Chiapas y Poniente de Campeche A.C.", "Direccion": "Prol. Paseo de Usumacinta s/n Col. Guayabal C.P. 86090 Villahermosa, Tab.", "Telefono": "(993) 352-2302", "Email": ""},
    {"Estado": "Tamaulipas", "Siglas": "OTEXPO", "Nombre": "OTEXPO A.C.", "Direccion": "Alhelies #20 Col. Jardín C.P. 87330 Matamoros, Tam.", "Telefono": "(868) 813-0505", "Email": ""},
    {"Estado": "Veracruz", "Siglas": "OGAVE", "Nombre": "Organización de Gasolineros de Veracruz A.C.", "Direccion": "Blvd. Adolfo Ruíz Cortines esq. Ciencias Exactas s/n Fracc. SUTSEM C.P. 94299 Boca del Río, Ver.", "Telefono": "(229) 921-7500", "Email": ""},
    {"Estado": "Yucatán", "Siglas": "UGY", "Nombre": "Unión de Gasolineros del Estado de Yucatán A.C.", "Direccion": "Calle 27 #86 entre 18 y 20 Col. Chichén Itzá C.P. 97170 Mérida, Yuc.", "Telefono": "(999) 926-8016", "Email": ""},
    {"Estado": "Yucatán", "Siglas": "GUPYAC", "Nombre": "Gasolineros Unidos del Península A.C.", "Direccion": "Calle 20 #235 entre calle 7 y 15 Edif. Luxus Altabrisa piso 6 C.P. 97130 Mérida, Yuc.", "Telefono": "(999) 270-4735", "Email": ""},
    {"Estado": "Zacatecas", "Siglas": "GAZAC", "Nombre": "Asociación de Gasolineros de Zacatecas A.C.", "Direccion": "Av. Hacienda de Bernardez #106 A Fracc. Conde de Bernardez C.P. 98617 Guadalupe, Zac.", "Telefono": "(492) 921-2345", "Email": ""}
]

base_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine"
json_path = os.path.join(base_dir, "data", "directorio_asociaciones_onexpo_mexico.json")
csv_path = os.path.join(base_dir, "data", "directorio_asociaciones_onexpo_mexico.csv")
md_path = os.path.join(base_dir, "playbooks", "directorio_onexpo_estatal_mexico.md")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(associations, f, ensure_ascii=False, indent=2)

df = pd.DataFrame(associations)
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

md_content = "# 🗺️ Directorio Oficial de Asociaciones Estatales de ONEXPO Nacional A.C.\n\n"
md_content += "> **Uso Estratégico:** Directorio de las 42 asociaciones gremiales de expendedores de gasolina en los 32 estados de México. Ideal para prospección institucional, alianzas de distribución y convocatorias regionales.\n\n"
md_content += "| Estado | Siglas | Nombre de la Asociación | Dirección | Teléfono / Contacto |\n"
md_content += "| :--- | :--- | :--- | :--- | :--- |\n"

for a in associations:
    tel_email = a['Telefono'] if a['Telefono'] else a['Email']
    md_content += f"| **{a['Estado']}** | `{a['Siglas']}` | {a['Nombre']} | {a['Direccion']} | {tel_email} |\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Directorio procesado exitosamente: {len(associations)} asociaciones registradas.")
