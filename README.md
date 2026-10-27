# KPI Nestlé · Venejugos C.A.

Tablero de evaluación de los KPI de activación y volumen Nestlé de Venejugos, aliado comercial de Nestlé.
Se publica con GitHub Pages desde este repositorio (`Venejugosserver/kpi-nestle1`, rama `main`).

| Página | Enlace | Para qué |
|---|---|---|
| Performance | `https://venejugosserver.github.io/kpi-nestle1/performance.html` | El tablero: activación por categoría, equipos, clientes, rolling en kilos y déficit semanal |
| Resumen por asesor | `https://venejugosserver.github.io/kpi-nestle1/reporte.html` | Documento por coordinación y asesor, descargable en Word o PDF; adaptado a teléfonos |
| Panel administrativo | `https://venejugosserver.github.io/kpi-nestle1/admin.html` | Carga de archivos, parámetros y publicación |

No hay `index.html`: comparta siempre los enlaces directos. Ninguna página pide contraseña.

---

## Archivos del repositorio

| Archivo | Lo genera | Contenido |
|---|---|---|
| `admin.html`, `performance.html`, `reporte.html` | Desarrollo | Páginas autocontenidas (HTML, CSS y JavaScript en un solo archivo) |
| `dataset.json` | Panel → Publicar ventas y maestro | Ventas Nestlé del Reporte General del mes |
| `maestro.pub.json` | Panel → Publicar ventas y maestro | Maestro general de clientes, sin teléfonos, direcciones, coordenadas, deuda ni flujo de caja |
| `activacion.json` | Panel → Publicar matriz | Matriz oficial de activación de la coordinación (opcional) |
| `README.md` | Desarrollo | Este documento |

`maestro.enc.json` (maestro anterior, cifrado) ya no forma parte de la arquitectura y puede borrarse.

Para actualizar páginas, suba solo los `.html`. **No borre archivos antes de subir**: GitHub reemplaza los que tienen el mismo nombre, y los `.json` de datos los genera el panel.

---

## Flujo de actualización

1. **Ventas:** en el panel, cargue el Reporte General (`.xlsx`). Se leen subcategoría, fecha, cliente, RIF, zona, vendedor, kilos, cantidad, precio total, tipo de documento y la columna **CódigoDirecCliente** (sucursales). Solo entran líneas Nestlé.
2. **Maestro general:** cargue el Excel del maestro (hoja *CLIENTES MATRIZ NESTLE*). De él salen las bases, las coordinaciones y la validación de las activaciones. Luego pulse *Publicar ventas y maestro* en la sección Publicar en GitHub: sube `dataset.json` y `maestro.pub.json`.
3. **Matriz oficial (opcional):** cargue el Excel de la matriz de activación de la coordinación y pulse *Publicar matriz*. Se lee hasta la fila TOTAL.
4. Espere uno o dos minutos y recargue las páginas (Ctrl+F5, o cerrar y abrir en el teléfono).

Las páginas leen primero el archivo publicado en GitHub Pages; si responde 404 lo leen directo del repositorio, y como último recurso usan la copia guardada en el navegador.

---

## Reglas de medición

**Bases (desde el maestro general)**
- Cartera Nestlé del asesor: clientes con `ESTATUS NESTLE = ACTIVO`, por `ASESOR ACTUAL`. RECUPERACION queda fuera.
- Base A&B y base Confites: clientes de la cartera con la bandera `A&B` o `CONFITES`. Chocolates y Galletas se miden sobre Confites; el resto de categorías sobre A&B.
- Coordinación: la columna `SUPERVISOR` del maestro.

**Activación**
- Cliente de la base del asesor: cuenta para ese asesor si compró la categoría, se la haya facturado quien sea.
- Cliente fuera de la base (sin la bandera, sin estatus Nestlé activo o fuera del maestro): cuenta para el asesor que le vendió.
- Siempre con factura mayor a cero; las devoluciones NCTESO se restan y, si el cliente devolvió todo, no cuenta.
- Cada sucursal es un cliente aparte: `CódigoDirecCliente` 2, 3… en ventas; en el maestro general el RIF sin sufijo es la principal, `RIF-1` la dirección 2 y `RIF-2` la dirección 3.
- Las ventas del vendedor DIRECTO no se suman a Directo Oficina.

**Metas y porcentajes**
- Targets: Caldos 75 %, Sopas 75 %, Galletas 70 %, Chocolates 80 %, Cerelac 40 %, Nestum 30 %, Nestea 25 %, La Campesina 20 %, Leche condensada 20 %, Nutririnde 20 %, Fórmulas infantiles 0 %. Categorías principales (★): Galletas, Chocolates, Caldos y Sopas.
- Meta = base × target, redondeada al entero. Falta = meta − activados, con piso cero.
- En la coordinación y en el total, la falta es la del equipo: meta del equipo − activados del equipo (el asesor que supera su meta compensa).
- Cumplimiento = activados ÷ meta (medida por defecto); activación = activados ÷ base; brecha = falta ÷ meta. El color siempre sigue el cumplimiento: verde ≥ 100 %, ámbar ≥ 70 %, rojo < 70 %.

**Calendario**
- Días hábiles: lunes a viernes sin feriados nacionales de Venezuela (se calculan solos; el panel permite agregar feriados por decreto). Octubre 2026: 21 días, con el 12/10 feriado.
- Necesidad diaria = falta ÷ días hábiles restantes.
- Semanas: S0 es la semana parcial inicial (1 y 2 de octubre). Meta semanal = meta del mes ÷ días hábiles del mes × días de la semana, a un decimal.

**Matriz oficial**
- Sus montos aplican en el rango que va del día 1 al día de las ventas con que se armó (`ventasHasta`). Con más ventas, el tablero calcula con las reglas anteriores y ofrece el enlace *ver sus montos*.
- La matriz se ve solo en el panel administrativo.

**Rolling en kilos**
- Kilos facturados por asesor (sin NCTESO) contra su cuota del mes. Cuotas de octubre: 15.000 kg.

---

## Funciones del tablero

- Filtros: categoría, coordinación (varias a la vez), vendedor, medida, orden y rango de fechas (calendario *Desde / Hasta* y *Mes completo*).
- Pestañas: Equipos y categorías · Clientes activados (con validación contra el maestro y exportación CSV) · Rolling Nestlé (kilos) · Déficit semanal y meta semanal por categoría.
- Rótulos **Meta**, **Activados** y **Falta** sobre los números de cada coordinación y asesor.
- Resumen por asesor con listas desplegables, filtro por semana y descarga en Word o PDF.
- Vista adaptable a teléfonos de 5" a 6,7" (vertical y horizontal) y a pantallas de escritorio.

---

## Auditoría

Última auditoría: 27/10/2026, con los datos publicados ese día: ventas al 26/10/2026 (ReporteGeneral 58), maestro general del 27/10/2026 y matriz oficial con ventas al 26/10/2026.

| Verificación | Resultado |
|---|---|
| Recalculo independiente (Python) contra el motor de las páginas: calendario, bases de los 18 asesores, 216 celdas asesor × categoría y 48 filas de coordinación (cálculo con ventas del 1 al 25), 189 celdas de la matriz oficial (1 al 26), 54 celdas del filtro por fechas, 198 celdas del resumen, sucursales, devoluciones y rolling | 35 de 35 puntos sin diferencias |
| Aritmética del tablero (12 categorías × 3 medidas × 2 rangos) | 13.602 comprobaciones sin diferencias |
| Aritmética del resumen por asesor | 1.146 comprobaciones sin diferencias |
| Errores de JavaScript | Ninguno |

Corregido durante la auditoría: el resumen por asesor sumaba a Directo Oficina las ventas del vendedor DIRECTO, a diferencia del tablero; y en equipos con la llave antigua guardada podía leer el maestro cifrado anterior. Ahora ambos siguen la misma regla y usan siempre `maestro.pub.json`; el panel ya no publica `maestro.enc.json`.

---

## Notas técnicas

- Páginas estáticas, sin servidor: Chart.js y SheetJS van incluidos en los archivos.
- El panel publica en GitHub con la API de contenidos; necesita un token *fine-grained* con permiso *Contents: Read and write* solo sobre este repositorio, guardado únicamente en el navegador de quien publica.
- El repositorio es público: `dataset.json`, `maestro.pub.json` y `activacion.json` pueden ser vistos por quien tenga el enlace.
