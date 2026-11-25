# Guía paso a paso para terminar Medicent Backend V3

**Para:** Cristian y su compañero  
**Fecha de revisión:** 22 de octubre de 2026  
**Objetivo:** saber qué falta, quién lo hace y en qué orden, sin tener que entender todo el proyecto de una vez.

## 1. Cómo usar esta guía

Trabajen una tarea pequeña por vez. Para cada tarea:

1. Lean juntos qué debe hacer la función.
2. Escriban una prueba que describa el resultado esperado.
3. Ejecuten esa prueba y miren el error. Al principio debe fallar porque la función todavía no está hecha.
4. Escriban solo lo necesario para que pase.
5. Vuelvan a ejecutar la prueba y luego las pruebas anteriores.
6. Cuando todo esté claro, guarden el cambio en su rama y súbanlo.

En pareja, quien escribe es el **conductor** y quien revisa y piensa en los casos difíciles es el **navegador**. Cambien de rol cada 25 o 30 minutos. La prueba debe ser entendible para ambos; si no pueden explicar qué comprueba, todavía no está lista.

## 2. Qué encontré en el repositorio

### Código de tu compañero

Los cambios de la rama remota `feature/tratamientos-tomas` incluyen un modelo `Medicamento`, la inicialización de Flask-Migrate, una migración y una base para pruebas. El modelo está empezado, pero aún no está listo para considerarlo terminado.

Antes de continuar, atiendan estos puntos:

1. **Modelo frente a tabla:** en `database/schema.sql`, `medicamentos.forma_farmaceutica` es obligatorio (`NOT NULL`); en el modelo aparece como opcional. Deben acordar que ambos digan lo mismo.
2. **Campos de fecha:** el diagrama muestra campos `creado_en` en varias tablas, pero el `schema.sql` actual no los incluye. El catálogo de pruebas también espera `creado_en` para un medicamento. Decidan en pareja si esos campos se agregan a la base, al diagrama y a los modelos, o si se quitan de los documentos y pruebas.
3. **Campos clínicos adicionales:** el diagrama y el archivo `PASOS_TRABAJO_EN_CASA.md` mencionan `instrucciones`, `esta_activo`, `notas` y otros campos que no aparecen en `schema.sql`. No los agreguen solo porque aparecen en una guía: primero acuerden el diseño y actualicen todas las referencias.
4. **Configuración de pruebas:** `tests/base_test.py` importa `TestConfig`, pero la versión revisada de `app/config/settings.py` solo declara `Config`. La configuración de SQLite en memoria debe existir antes de que esa base de pruebas pueda usarse.
5. **Dependencia de migraciones:** el código de conexión importa Flask-Migrate, pero `requirements.txt` no lista `Flask-Migrate`. Sin esa dependencia, otra persona no podrá instalar el proyecto siguiendo únicamente ese archivo.
6. **Primera migración:** la migración revisada intenta crear la tabla `medicamentos`, que ya está en el `schema.sql` y en la base que Cristian importó. No ejecuten `flask db upgrade` sobre esa base hasta decidir cómo registrar el esquema existente como punto de partida; de lo contrario puede intentar crear una tabla que ya existe.
7. **Prueba de modelo:** `tests/test_modelos.py` está vacío. La prueba de Medicamento descrita en `PASOS_TRABAJO_EN_CASA.md` todavía no está guardada ahí.
8. **Ruta de salud:** el código actual responde en `/api/estado`; el catálogo oficial de pruebas pide `/api/salud`. Acuerden un nombre y manténganlo igual en la ruta y su prueba.
9. **Paquetes y extensiones pendientes:** el árbol oficial también espera `app/database/__init__.py` y `tests/__init__.py`. Además, la fábrica todavía no inicializa todas las extensiones previstas en la guía (Bcrypt, JWT y CORS). Completen esto cuando lleguen a la configuración de autenticación y rutas, siguiendo una pieza a la vez.

La rama remota `feature/tratamientos-tomas` todavía está separada de los cambios más recientes de `develop`. Antes de integrarla, actualicen la rama con `develop` mediante el flujo acordado y resuelvan los cambios compartidos de `app/__init__.py`, configuración y conexión. No mezclen ramas a ciegas.

### Documentos encontrados

En las ramas de GitHub revisadas encontré **cuatro archivos PDF**, además de `diagrama_relacional.png`. No encontré un quinto PDF. También existe un archivo de pasos en la rama de tu compañero; tiene buenas indicaciones para retomar, pero algunas afirmaciones no coinciden con el código actual, en especial las de `TestConfig` y la migración.

## 3. Fase cero: ponerse de acuerdo en la base de datos

Antes de crear más modelos, siéntense juntos y comparen estas tres cosas: `database/schema.sql`, `documentos/diagrama_relacional.png` y el diccionario de datos de la Guía Maestra.

Para cada tabla, anoten el nombre de cada campo, su tipo, si puede quedar vacío, su clave principal y sus relaciones. Marquen cada diferencia. Acuerden una sola versión y actualicen los archivos necesarios para que todos describan el mismo diseño.

La base actual tiene estas cinco tablas:

| Tabla | Para qué sirve |
|---|---|
| `usuarios` | Pacientes, cuidadores y administradores. |
| `pacientes_cuidadores` | Une cuidadores con uno o varios pacientes. |
| `medicamentos` | Catálogo de medicamentos. |
| `tratamientos` | Prescripción de un medicamento a un paciente. |
| `registros_tomas` | Cada toma programada y su estado. |

**Protejan la base que ya importaron.** `schema.sql` contiene instrucciones `DROP TABLE`; no vuelvan a importarlo sobre una base con datos que quieran conservar. Antes de cambiar tablas, hagan una copia de seguridad y prueben los cambios en una base desechable. `seed.sql` también debe revisarse antes de usarlo: las contraseñas de usuarios de prueba deben guardarse como hashes, no como contraseñas legibles.

## 4. Fase uno: preparar el mismo proyecto en los dos computadores

Cada computador necesita su propia instalación de Python, entorno virtual, dependencias, MySQL, base de datos y archivo `.env`. Git comparte archivos del proyecto; **no comparte la base local ni el `.env`**. No suban la contraseña.

En el computador nuevo:

1. Clonen el repositorio o actualicen la copia que ya existe.
2. Traigan las ramas remotas y elijan juntos la rama que corresponde al trabajo actual.
3. Activen el entorno virtual e instalen lo que aparece en `requirements.txt`.
4. Creen localmente el `.env` a partir de `.env.example` y escriban ahí sus credenciales locales.
5. Creen o importen la base `medicent_v3` en MySQL Workbench. Comprueben que aparecen las cinco tablas.
6. Arranquen Flask y visiten las rutas de estado. La ruta de salud confirma que Flask responde; la ruta de base de datos confirma que MySQL responde.

Si el servidor da un error, lean las últimas líneas de la terminal. No copien el contenido de `.env` al chat ni lo suban a GitHub.

## 5. Fase dos: dejar lista la base del backend y de las pruebas

Hagan y expliquen estos cambios pequeños antes de agregar lógica de negocio:

- Completar la configuración normal y la configuración de prueba. La de prueba debe apuntar a SQLite en memoria y activar el modo de pruebas.
- Declarar una sola vez las extensiones que el proyecto usa: base de datos, hash de contraseñas, JWT y migraciones. Añadir sus dependencias al archivo de requisitos.
- Mantener el orden de inicio: leer configuración, conectar las extensiones a la aplicación y después registrar rutas.
- Decidir cómo manejar las migraciones partiendo de la base que ya existe. Ensayar primero en una base vacía de prueba; no ejecutar la primera migración directamente sobre la base importada hasta resolver el choque descrito arriba.
- Corregir la ruta de salud para que coincida con el nombre acordado y con el documento de pruebas.

La base de pruebas debe crear las tablas al iniciar cada prueba y limpiarlas al terminar. Así las pruebas no dependen de que MySQL esté encendido y una prueba no deja datos que afecten a la siguiente.

## 6. Fase tres: crear los modelos, uno por uno

Un modelo es la clase de Python que describe una tabla. Para cada modelo comparen el archivo con el SQL antes de escribirlo.

### Trabajo de Cristian: usuarios y permisos

1. `app/models/usuario.py`: relacionar el modelo con `usuarios`; representar nombre, correo único, hash de contraseña y rol permitido.
2. `app/models/paciente_cuidador.py`: representar la tabla de relación con las dos claves foráneas y su clave compuesta.
3. `app/models/__init__.py`: dejar que el paquete conozca los modelos necesarios.
4. En cada modelo, decidir con el diseño si hace falta conversión a diccionario. Nunca incluir el hash en la respuesta pública.

### Trabajo del compañero: catálogo y módulo clínico

1. Completar `app/models/medicamento.py` de acuerdo con el esquema acordado.
2. Crear `app/models/tratamiento.py` y revisar sus claves hacia paciente y medicamento.
3. Crear `app/models/registro_toma.py` y revisar la relación con tratamiento, fecha programada, fecha real y estado permitido.
4. Revisar con Cristian que nombres, tipos, campos obligatorios y relaciones sean iguales en SQL, diagrama y modelos.

Después de cada modelo, escriban y ejecuten su prueba de modelo antes de continuar con el siguiente. No creen los cinco modelos de una sola vez para probarlos al final.

## 7. Fase cuatro: TDD y las pruebas

El catálogo oficial propone 17 comprobaciones: 8 unitarias de modelos y lógica, 4 de integración y 5 de la API completa. Úsenlas como lista de aceptación, empezando por una sola prueba. El patrón **AAA** significa Preparar los datos, Actuar llamando al código y Verificar el resultado.

### Pruebas de Cristian

- Crear un usuario válido y comprobar su rol y sus datos públicos.
- Rechazar un correo duplicado sin dejar una sesión de base de datos dañada.
- Vincular un cuidador con varios pacientes.
- Comprobar que la contraseña se transforma en un hash y que la verificación distingue la contraseña correcta de una incorrecta.
- Iniciar sesión y comprobar que el JWT contiene identidad y rol.
- Rechazar token ausente, inválido o vencido, y rechazar un rol que no tiene permiso.
- Probar registro, inicio de sesión y asignación desde la API con los códigos HTTP acordados.

### Pruebas del compañero

- Crear y consultar un medicamento.
- Validar fechas, dosis e intervalo de un tratamiento.
- Calcular tomas empezando en `fecha_inicio + hora_inicial`, avanzando por `frecuencia_horas` y sin pasar del límite acordado.
- Guardar el tratamiento y sus tomas relacionadas; comprobar la cantidad de tomas y el estado inicial `pendiente`.
- Permitir transiciones válidas de estado y rechazar un estado inventado sin guardar cambios.
- Probar la creación/listado de medicamentos y el flujo clínico completo desde la API.

Antes de probar el algoritmo, decidan si `fecha_fin` cuenta como día completo y qué debe pasar cuando la frecuencia no divide exactamente el día. La prueba debe expresar la decisión del equipo, no adivinarla.

El PDF indica `unittest` y SQLite en memoria. Cuando la base de pruebas esté reparada, el comando general es:

```text
python -m unittest discover -s tests -p "test_*.py"
```

Si usan el lanzador `py` en Windows, pueden anteponerlo al mismo comando. Empiecen ejecutando una sola prueba y luego ejecuten todas. Un punto significa aprobada; `FAIL` significa que el resultado no coincide; `ERROR` suele indicar que el código no pudo ejecutarse. No consideren terminada una tarea solo porque Flask arranca.

## 8. Fase cinco: servicios, rutas y control de acceso

Construyan el sistema por capas para que cada parte tenga un trabajo sencillo:

1. **Servicio:** hace la lógica; por ejemplo, verificar contraseña o calcular horarios. No depende de una petición HTTP.
2. **Controlador:** recibe los datos de la petición, llama al servicio y decide la respuesta.
3. **Ruta:** define la dirección HTTP y el método, y conecta con el controlador.
4. **Middleware:** comprueba JWT y permisos antes de dejar pasar una petición protegida.

Cristian implementa primero `auth_service.py`, `auth_controller.py`, `auth_routes.py` y `auth_middleware.py`: registro, login, token y asignación de cuidador. El compañero implementa servicios, controladores y rutas de medicamentos, tratamientos y tomas. Las rutas de ambos se registran juntos en `create_app`.

Para cada endpoint acuerden los datos que recibe, el JSON que devuelve y el código HTTP. Los documentos nombran, entre otros, `200`, `201`, `400`, `401`, `403` y `404`. No devuelvan contraseñas ni hashes.

## 9. Fase seis: terminar e integrar sin perder trabajo

Usen Git Flow de forma simple: `main` guarda entregas estables; `develop` integra el trabajo revisado; cada tarea vive en una rama `feature/...`. No trabajen los dos en la misma rama al mismo tiempo.

1. Antes de empezar, traigan cambios remotos y confirmen en qué rama están.
2. Cristian trabaja su módulo IAM en una rama de feature; el compañero mantiene la rama clínica.
3. Cada quien guarda commits pequeños con mensajes que digan qué hizo.
4. Antes de solicitar integración, cada persona ejecuta las pruebas que corresponden y comparte el resultado.
5. Revisen los cambios del otro mediante Pull Request. Integren primero en `develop`; lleven a `main` solo una versión acordada y estable.
6. Antes de actualizar una rama, confirmen que sus cambios están guardados. Si ambos tocaron `app/__init__.py`, resuelvan juntos el conflicto revisando ambas necesidades.

El documento de metodología menciona coautoría obligatoria en los commits. Acuerden entre ustedes cómo usarla y qué correo público de GitHub corresponde; no inventen correos ni publiquen datos personales sin querer.

## 10. Qué significa que el backend está terminado

- SQL, diagrama, modelos y documentos describen las mismas tablas y campos.
- Están creados los cinco modelos y sus relaciones.
- El registro y login almacenan hashes, entregan JWT y respetan los roles.
- El cuidador solo puede operar con pacientes que tiene asignados.
- Los tratamientos generan las tomas correctas y las tomas aceptan solo estados permitidos.
- Las rutas devuelven JSON consistente y códigos HTTP acordados.
- Las pruebas de modelos, servicios, seguridad y rutas pasan en SQLite en memoria.
- El flujo principal funciona de principio a fin: registro, login, medicamento, tratamiento, calendario y marcar una toma.
- `.env` no aparece en Git; cada integrante tiene su configuración local.
- El trabajo está revisado e integrado mediante Pull Request.

## 11. Tu siguiente sesión: haz solo esto primero

1. Habla con tu compañero y acuerden el diseño oficial de las cinco tablas mirando juntos `schema.sql`, el diagrama y la Guía Maestra.
2. Corrijan la lista de diferencias de la sección 2, sobre todo campos `creado_en`, `forma_farmaceutica` y la estrategia de migración.
3. Pídele que te muestre la prueba de Medicamento en su computador y luego revisen por qué `TestConfig` aún no aparece en el archivo de configuración de la rama.
4. Cuando eso esté resuelto, tú comienzas `Usuario`: primero un caso de prueba válido, después la unicidad del correo y luego la relación con cuidadores.

No hace falta terminar todo en una tarde. Cada casilla que pase su prueba es un avance que ambos pueden explicar.

## 12. Documentos revisados

- `documentos/Arbol_Estructura_Archivos_Medicent_V3.pdf`: nombres y responsabilidades de archivos.
- `documentos/Guia_Maestra_Desarrollo_Medicent_V3.pdf`: tablas, arquitectura, endpoints y algoritmo de tomas.
- `documentos/Listado_Oficial_de_Pruebas_TDD_Medicent_V3.pdf`: las 17 pruebas sugeridas y cómo interpretarlas.
- `documentos/Metodologia_Pair_Programming_y_TDD.pdf`: turnos de pareja, ciclo TDD y estrategia Git.
- `documentos/diagrama_relacional.png`: relaciones y campos dibujados; debe reconciliarse con el SQL.
- `PASOS_TRABAJO_EN_CASA.md` en `feature/tratamientos-tomas`: notas del compañero para retomar. Es una referencia de trabajo, no sustituye los archivos que deben coincidir ni la verificación de las pruebas.

**Falta por localizar:** si el equipo tiene un quinto PDF distinto de estos cuatro, no está guardado en ninguna de las ramas remotas revisadas. Agréguenlo al repositorio para que ambos puedan consultarlo.
