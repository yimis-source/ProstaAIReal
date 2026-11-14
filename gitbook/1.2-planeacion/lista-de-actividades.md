# Lista de actividades

Desglosa los ciclos en actividades concretas con identificador, descripción y responsables; alimenta el cronograma y el seguimiento TSP.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.2.2.1 |
| Fecha y versión | 11/10/2026; no indica versión |
| Responsable | Planeación y líder del proyecto |
| Formato | PDF de 7 páginas (plantilla ProjectManagementDocs) |

## Contenido principal

La lista contiene 81 actividades con ID, nombre, descripción del trabajo y dos responsables cada una. El primer dígito después del 1 indica el grupo (10 y 11 inicio y planeación, 12 a 18 ciclos 1 a 7, 19 gestión transversal).

| Grupo | Actividades (ID y nombre) |
|---|---|
| Inicio y planeación (28/09 a 12/10) | 1001 Aprobar el acta; 1002 Registro de interesados; 1003 Crear repositorio y carpeta compartida; 1004 Definir requisitos iniciales; 1101 Escribir la especificación de requisitos; 1102 Crear la matriz de trazabilidad; 1103 Armar el historial de tareas y el plan de ciclos; 1104 Hacer el cronograma; 1105 Completar el registro de riesgos; 1106 Hacer el plan de calidad y pruebas; 1107 Armar y aprobar los documentos de planeación |
| Ciclo 1, datos (13/10 a 25/10) | 1201 Definir qué estudios se usan; 1202 Buscar datasets públicos; 1203 Revisar licencias; 1204 Descargar y organizar los datasets; 1205 Verificar que los datos son anónimos; 1206 Analizar los datos; 1207 Revisar muestras en 3D Slicer; 1208 Hacer el informe de datos; 1209 Cerrar el Ciclo 1 |
| Ciclo 2, preprocesamiento y diseño (26/10 a 30/10) | 1301 Revisar la calidad de los datos; 1302 Unificar el formato; 1303 Dividir los datos por paciente; 1304 Verificar que no hay mezcla; 1305 Automatizar el preprocesamiento; 1306 Diseñar la arquitectura; 1307 Diseñar las pantallas; 1308 Definir el módulo de IA; 1309 Diseñar la base de datos; 1310 Cerrar el Ciclo 2 |
| Ciclo 3, modelo 3D (02/11 a 13/11) | 1401 Elegir el modelo; 1402 Configurar el entrenamiento en Colab; 1403 Cargar y preparar datos; 1404 Entrenar el modelo base; 1405 Mejorar el modelo; 1406 Registrar los experimentos; 1407 Crear el script de inferencia; 1408 Medir el tiempo de procesamiento; 1409 Probar el modelo; 1410 Cerrar el Ciclo 3 |
| Ciclo 4, ROI (16/11 a 20/11) | 1501 Limpiar la máscara para obtener la ROI; 1502 Diseñar cómo se muestra la ROI; 1503 Hacer el visor de la ROI; 1504 Escribir la explicación y el aviso; 1505 Revisar la ROI en 3D Slicer; 1506 Probar la ROI; 1507 Cerrar el Ciclo 4 |
| Ciclo 5, evaluación (23/11 a 25/11) | 1601 Calcular Dice e IoU; 1602 Analizar los errores; 1603 Documentar límites y sesgos; 1604 Confirmar la división por paciente; 1605 Mejorar si el Dice es bajo; 1606 Hacer el informe de métricas; 1607 Cerrar el Ciclo 5 |
| Ciclo 6, aplicación web (26/11 a 02/12) | 1701 API con FastAPI; 1702 Pantalla de carga en React; 1703 Conectar base de datos y almacenamiento; 1704 Conectar el modelo a la API; 1705 Pantalla de resultados; 1706 Acceso básico; 1707 Probar la integración; 1708 Pruebas funcionales; 1709 Pruebas de usabilidad; 1710 Pruebas de rendimiento; 1711 Verificar que no persisten datos personales; 1712 Reunir las evidencias de calidad; 1713 Cerrar el Ciclo 6 |
| Ciclo 7, cierre (03/12 a 09/12) | 1801 Ordenar el repositorio y la documentación; 1802 Documentar decisiones técnicas; 1803 Documentar riesgos pendientes; 1804 Escribir lecciones aprendidas y conclusiones; 1805 Armar la documentación final; 1806 Preparar la presentación y la demo; 1807 Revisar los criterios de aceptación; 1808 Obtener la aprobación del propietario; 1809 Cerrar el repositorio |
| Gestión transversal (05/10 a 09/12) | 1901 Gestionar los cambios; 1902 Controlar versiones de documentos; 1903 Revisar los pull requests; 1904 Informar el avance al docente; 1905 Revisar los supuestos |

Las actividades 1001 a 1003 figuran como finalizadas en la lista. Cada ciclo cierra con una revisión, la actualización de la matriz de trazabilidad y una etiqueta de versión en GitHub (v0.1 a v0.6 para los ciclos 1 a 6).

## Documento original

* [Lista de actividades (PDF)](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/docsf/1.2 Planeación/1.2.2.1 Lista de actividades.pdf`
