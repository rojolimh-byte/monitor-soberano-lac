# Continuidad del proyecto

## Objetivo
Terminar un portafolio de monitor macrofiscal y vulnerabilidad externa
para ARG, BRA, CHL, COL y PER. GitHub es el respaldo principal.

## Estado confirmado
- WDI: 480 filas.
- Selección WEO: 420 filas.
- Panel integrado WDI-WEO: 900 filas.
- Reservas oficiales: 5054 observaciones.
- Reservas, originales, script e informe publicados en commit 84e4f32.
- Validación WDI ejecutada: 433 filas pasan controles y 47 faltantes.
- validate.py ahora usa CSV y no modifica el panel de entrada.

## Limitaciones
- No rellenar faltantes ni interpolar reservas.
- Chile: frecuencia observada trimestral, metadatos indican mensual.
- Conservar fechas originales de reservas.
- No confundir deuda del gobierno central WDI con gobierno general WEO.
- No mezclar históricos con proyecciones.
- Deuda WEO 2025 de BRA y CHL figura como projection.
- El análisis de cinco países debe usar un año común por indicador.
- Etiqueta actual según fuente; no implica dato definitivo.

## Pendientes
1. Revisar o ejecutar el análisis y verificar gráficos y tablas.
2. Redactar hallazgos sustentados en los resultados.
3. Completar README, metodología e instrucciones reproducibles.
4. Completar código reproducible de selección WEO e integración.
5. Preparar dashboard y pruebas.
6. Respaldar cada bloque importante, sin duplicados ni credenciales.

## Copias locales excluidas del respaldo
- Originales duplicados en la raíz.
- reserves_official_native_review_*.csv provisional.
No son necesarios para reiniciar desde GitHub.

## Script de análisis
No existe src/analyze_macro.py; crearlo en la próxima sesión.
