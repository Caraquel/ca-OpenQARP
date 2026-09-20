# Conclusiones del tutorial 06 — MaxCut, simuladores y hardware

**Autor:** Carlos Araque / Caraquel · **Revisión:** 20 de septiembre de 2026.

El experimento completó la comparación local y recuperó resultados de hardware
de IBM Marrakesh e IQM Garnet. Demuestra portabilidad y ejecución de un circuito
QAOA entre herramientas y dispositivos. **No demuestra ventaja cuántica**:
el método clásico de búsqueda local encontró el óptimo en sus cinco intentos.

## Experimento y evidencia

- Problema sintético: MaxCut ponderado, cinco vértices y siete aristas.
- Óptimo certificado por enumeración: **10**; partición aleatoria: valor esperado **6**.
- QAOA con p=1; tres inicializaciones de optimización exacta y parámetros
  congelados antes de comparar las ejecuciones.
- Cinco repeticiones de 2.048 shots por ruta: **10.240 shots por proveedor**.
- Dos trabajos de benchmark en hardware, uno por proveedor; ambos figuran como
  `retrieved` en el registro exportado. Las cinco repeticiones de cada proveedor
  pertenecen a un mismo trabajo, no a cinco calibraciones o días independientes.
- Se comprobaron las diez filas de resultados de hardware contra los conteos
  originales, sus presupuestos de shots y los parámetros del experimento.

Fuente: `398931fcc280_20260920T075046640721Z.zip`. Su huella SHA-256 se conserva
en [provenance.json](hardware_run/provenance.json). La revisión valida la
consistencia del archivo exportado; no volvió a consultar los proveedores.

## Resultados

| Ruta | Corte medio | Fracción del óptimo | Probabilidad de medir una solución óptima |
| --- | ---: | ---: | ---: |
| Búsqueda local clásica | 10,0000 | 1,0000 | 5/5 inicializaciones alcanzaron el óptimo |
| Aer ideal | 8,3492 | 0,8349 | 40,99 % |
| Qrisp → Aer ideal | 8,3492 | 0,8349 | 40,99 % |
| OpenQARP ideal | 8,3372 | 0,8337 | 40,68 % |
| Modelo de ruido IBM Manila | 7,7448 | 0,7745 | 31,18 % |
| Modelo de ruido IQM Adonis | 7,3632 | 0,7363 | 28,21 % |
| **Hardware IBM Marrakesh** | **7,6877** | **0,7688** | **31,51 %** |
| **Hardware IQM Garnet** | **7,3410** | **0,7341** | **29,93 %** |

La búsqueda local produce una solución por inicio; las otras filas representan
distribuciones medidas. La última columna no equipara esos presupuestos.
Todas las repeticiones de hardware encontraron al menos una solución de valor 10,
pero eso no significa que todas las mediciones fueran óptimas.

## Qué podemos concluir

1. **El circuito es portable.** Los controles de convenciones y de distribución
   tras compilación pasaron; la versión de Colab produjo resultados compatibles
   con la prueba local. Aer y OpenQARP ideales dan valores cercanos, con distintas
   muestras aleatorias. Qrisp y Qiskit comparten Aer y no aportan dos motores
   independientes en este experimento.
2. **La ejecución real está demostrada por el archivo.** Hay identificadores de
   trabajos, dispositivos, fechas, conteos y resultados recuperados. La prueba
   adicional de un qubit en IQM es un diagnóstico de conexión; no forma parte
   del benchmark MaxCut exportado.
3. **Las rutas de hardware dan menor calidad que la simulación ideal en este caso.**
   IBM obtuvo un corte medio mayor que IQM para estos parámetros y compilaciones.
   Un solo problema de cinco qubits no permite ordenar proveedores en general.
4. **Los modelos de ruido no corresponden a los dispositivos ejecutados.**
   Manila no es Marrakesh y Adonis no es Garnet. La cercanía entre algunas medias
   no valida la calibración de un modelo ni permite atribuir toda la diferencia
   a un mecanismo concreto de ruido.
5. **La comparación temporal no mide ventaja cuántica.** Los aproximadamente
   58 minutos registrados abarcan desde el envío hasta la recuperación, incluyendo
   cola y demora en consultar. No son tiempo exclusivo de QPU. Las latencias
   locales tampoco incluyen todo el coste de instalación, entrenamiento y compilación.

## Limitaciones y lecciones de ingeniería

- Cinco qubits son suficientes para validar integración, pero demasiado pocos
  para poner a prueba la escalabilidad de los simuladores.
- La profundidad p=1 y el entrenamiento ideal compartido estudian transferencia
  de parámetros, no la mejor estrategia posible para cada dispositivo.
- Las incertidumbres de muestreo no incluyen deriva de calibración, variabilidad
  entre problemas o sesgos de selección de parámetros.
- La compilación IQM necesita el perfil validado sin MOVE para arquitecturas
  de acoplamiento directo. La conexión Qrisp a Sirius es una ruta diferente.
- El `pip check` de Colab registró conflictos con paquetes preinstalados. El
  benchmark terminó, pero no puede describirse ese entorno completo como limpio.
  El siguiente notebook instala sus dependencias en un entorno aislado.
- El registro de trabajos debe conservarse incluso antes de recuperar resultados;
  reiniciar Colab no debe llevar a reenviar trabajos por accidente.

## Siguiente investigación: tutorial 07

Cambiar QAOA por **simulación de evolución temporal Suzuki–Trotter** de una
cadena XXZ con campos longitudinal y transversal. Aumentar qubits y pasos,
comprobar casos pequeños contra exponenciación clásica y separar error de
aproximación, muestreo y compilación. Empezar sin ruido, sin credenciales y sin
hardware, midiendo preparación, ejecución, memoria y fallos de recursos.

La comparación será entre tres rutas de software identificadas explícitamente:
IBM/Aer, IQM compilado para su modelo local sobre Aer, y Fujitsu OpenQARP. IQM
y IBM comparten motor Aer; este hecho debe acompañar cualquier gráfico.

## Archivos de soporte

- [Resultados de hardware](hardware_run/hardware_runs.csv)
- [Conteos, dispositivos y trabajos recuperados](hardware_run/hardware_jobs.json)
- [Resumen de simuladores](hardware_run/simulator_summary.csv)
- [Configuración y versiones de Colab](hardware_run/manifest.json)
- [Resultados clásicos](hardware_run/classical_local_search.csv)
- [Conflictos de dependencias registrados](hardware_run/pip_check.txt)

**Texto para portfolio:** «Implementé y validé un benchmark reproducible de QAOA
para MaxCut con referencia clásica, simulación en Qiskit/Qrisp y OpenQARP, y
ejecución de 10.240 shots en cada uno de IBM Marrakesh e IQM Garnet. Analicé
calidad de solución, incertidumbre de muestreo y limitaciones de los modelos de
ruido, sin atribuir ventaja cuántica al caso pequeño».
