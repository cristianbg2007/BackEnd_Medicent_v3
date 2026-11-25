# Mapa de archivos y plan para completar Medicent Backend V3

**Guía de trabajo individual para Cristian**  
**Fecha:** 22 de octubre de 2026

Esta guía explica qué carpetas y archivos hacen falta, para qué sirve cada uno y en qué orden conviene completarlos. No necesitas aprender todo el proyecto antes de empezar: trabaja una casilla, entiéndela y compruébala antes de pasar a la siguiente.

## 1. Antes de empezar: una regla importante

En el repositorio hay documentos que no coinciden entre sí sobre algunos campos de la base de datos. Por eso, antes de completar los modelos, confirma cuál diseño van a usar: compara `database/schema.sql`, el diagrama y el diccionario de datos de la Guía Maestra. Si acuerdan cambiar la base, actualicen también los demás documentos y la migración. No ejecutes scripts con `DROP TABLE` sobre una base que tenga datos que quieras conservar.

La primera guía, [GUIA_PASO_A_PASO_BACKEND_MEDICENT.md](GUIA_PASO_A_PASO_BACKEND_MEDICENT.md), contiene los problemas detectados en la rama de tu compañero. Resuélvelos antes de tomar la rama como base definitiva.

## 2. El mapa completo del proyecto

Esta es la estructura objetivo. Los archivos que ya existen o que aparecen en la rama remota de tu compañero se marcan más abajo; los demás todavía deben crearse. `__init__.py` es un archivo que le indica a Python que una carpeta se puede importar como parte del proyecto.

```text
BackEnd_Medicent_v3/
├── app/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── paciente_cuidador.py
│   │   ├── medicamento.py
│   │   ├── tratamiento.py
│   │   └── registro_toma.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── medicamento_service.py
│   │   ├── tratamiento_service.py
│   │   └── toma_service.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── medicamento_controller.py
│   │   ├── tratamiento_controller.py
│   │   └── toma_controller.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── medicamento_routes.py
│   │   ├── tratamiento_routes.py
│   │   └── toma_routes.py
│   └── middlewares/
│       ├── __init__.py
│       └── auth_middleware.py
├── database/
│   ├── schema.sql
│   └── seed.sql
├── migrations/                 # archivos gestionados por Flask-Migrate
├── tests/
│   ├── __init__.py
│   ├── base_test.py
│   ├── test_modelos.py
│   ├── test_servicios.py
│   └── test_rutas_api.py
├── documentos/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

No crees todos los archivos vacíos el primer día. Crea cada uno cuando llegues a la etapa que lo necesita; así es más fácil entender para qué sirve.

## 3. Qué hace cada carpeta

Piensa en una solicitud como una nota que viaja por varias mesas:

1. **`routes/` recibe la dirección y el método HTTP.** Ejemplo: alguien manda un `POST` a `/api/auth/login`.
2. **`controllers/` recibe los datos de esa solicitud y prepara la respuesta HTTP.**
3. **`services/` hace el trabajo y las reglas del negocio.** Por ejemplo, buscar al usuario y comparar su contraseña.
4. **`models/` describe cómo se guardan los datos en las tablas.**
5. **`middlewares/` revisa si la persona tiene una llave válida y el permiso correcto.**

Una ruta no debería calcular horarios, y un servicio no debería leer directamente la petición web. Mantener estas tareas separadas facilita encontrar errores y probar cada pieza.

## 4. Orden de trabajo recomendado

### Etapa 0: saber en qué versión estás

Antes de escribir:

- Confirma el nombre de tu rama y que no tienes cambios sin guardar.
- Trae las ramas del servidor y acuerda con tu compañero cuál será la rama base.
- La rama remota del módulo clínico tiene trabajo de tu compañero; todavía debe revisarse e integrarse con `develop`.
- Cada tarea nueva debe ir en una rama `feature/...` creada desde la versión acordada. No sigas trabajando sobre una copia antigua sin actualizarla.

**Terminado cuando:** puedes decir qué rama contiene tu trabajo, cuál contiene el de tu compañero y cuál se usará como base.

### Etapa 1: preparar el computador

1. Usa la versión de Python acordada para el equipo.
2. Crea y activa el entorno virtual del proyecto.
3. Instala las dependencias que aparecen en `requirements.txt`.
4. Crea `.env` local copiando `.env.example`; completa tu conexión de MySQL. `.env` no debe guardarse en Git.
5. En Workbench, crea o importa `medicent_v3` y confirma que aparecen las cinco tablas.
6. Arranca el servidor y comprueba primero el endpoint de salud y luego la conexión a MySQL.

**Archivos implicados:** `requirements.txt`, `.env.example`, `.gitignore`, `app/config/settings.py`, `run.py`.  
**Terminado cuando:** Flask responde, MySQL responde y `git status` no muestra `.env`.

### Etapa 2: acordar y documentar las tablas

Haz una hoja de control con una fila por campo de cada tabla. Anota nombre, tipo, si permite vacío, clave principal y relación. Compara con:

- `database/schema.sql`: estructura que MySQL crea.
- `documentos/diagrama_relacional.png`: dibujo de tablas y relaciones.
- `documentos/Guia_Maestra_Desarrollo_Medicent_V3.pdf`: explicación de campos y reglas.

Marca diferencias y resuélvelas con tu compañero. Por ejemplo, el esquema actual exige `forma_farmaceutica`, pero el modelo de la otra rama la permite vacía; el diagrama también muestra columnas de fecha que el SQL no tiene.

**Terminado cuando:** SQL, diagrama y lista de modelos describen la misma versión. Antes de cambiar una base existente, guarda una copia; no vuelvas a importar un script que borra tablas.

### Etapa 3: dejar lista la fábrica de la aplicación

Completa estos archivos antes de empezar los módulos:

| Archivo | Qué debe contener o hacer | Cómo sabes que está listo |
|---|---|---|
| `app/config/__init__.py` | Permitir importar la configuración. | Python puede importar la carpeta `config`. |
| `app/config/settings.py` | Configuración normal desde `.env` y configuración aislada de pruebas en SQLite en memoria. | La app de pruebas no apunta a MySQL ni usa datos reales. |
| `app/database/__init__.py` | Inicializar el paquete de base de datos. | Los módulos pueden importar sus extensiones desde esta carpeta. |
| `app/database/connection.py` | Crear una sola instancia de SQLAlchemy y las extensiones previstas: migraciones, hash de contraseñas y JWT. | Las extensiones se conectan a la app en la fábrica, sin crear varias instancias. |
| `app/__init__.py` | Crear la app, cargar la configuración, inicializar extensiones y registrar Blueprints. | Se puede crear la app normal y también la app de pruebas cambiando la configuración. |
| `run.py` | Arrancar la app para desarrollo local. | El comando de inicio levanta Flask. |

La configuración de pruebas se llama `TestConfig` en los documentos. El código de preparación de pruebas la importa, así que debe estar definida antes de ejecutar la suite.

### Etapa 4: resolver migraciones sin dañar la base

Una migración es una instrucción versionada para cambiar la estructura de una base de datos. Como ya importaste el SQL y la tabla `medicamentos` existe, la primera migración de la rama clínica podría intentar crearla de nuevo.

Antes de ejecutar migraciones en tu base:

1. Comprende si el equipo manejará el esquema desde `schema.sql`, desde migraciones, o cómo convertirán el SQL inicial en una migración base.
2. Prueba la decisión en una base vacía de práctica.
3. Revisa qué tablas propone cambiar la migración antes de aplicarla.
4. Haz copia de seguridad y confirma que no elimina información útil.

**Archivos:** `migrations/` y `app/database/connection.py`. Los archivos internos de `migrations/` suelen generarse o administrarse con Flask-Migrate; no los edites sin entender qué cambio describen.

### Etapa 5: modelos y pruebas de modelos

Un modelo es la descripción en Python de una tabla. Crea los modelos en este orden porque las relaciones dependen unas de otras:

| Orden | Archivo | Debe representar | Prueba en `tests/test_modelos.py` |
|---:|---|---|---|
| 1 | `app/models/usuario.py` | `usuarios`: nombre, correo único, hash de contraseña y rol permitido. | Se puede crear un usuario; el correo duplicado se rechaza; la salida pública no muestra el hash. |
| 2 | `app/models/paciente_cuidador.py` | `pacientes_cuidadores`: dos claves foráneas y relación muchos a muchos. | Un cuidador puede relacionarse con varios pacientes y no duplicar el mismo vínculo. |
| 3 | `app/models/medicamento.py` | `medicamentos`: nombre, descripción opcional y forma farmacéutica según el esquema acordado. | Se guarda y se puede convertir a una respuesta pública segura. |
| 4 | `app/models/tratamiento.py` | `tratamientos`: paciente, medicamento, dosis, frecuencia, fechas y hora inicial. | Las referencias existen y la frecuencia debe ser mayor que cero. |
| 5 | `app/models/registro_toma.py` | `registros_tomas`: tratamiento, hora programada, hora real y estado. | Una toma inicia pendiente y una hora real puede quedar vacía hasta registrarla. |

`app/models/__init__.py` debe importar los modelos que necesiten conocer la aplicación y las migraciones. Los nombres de tabla y de campos deben coincidir exactamente con el SQL ya acordado.

Para cada fila de la tabla de arriba, haz primero una prueba sencilla: preparar datos, guardar una instancia, consultarla y comprobar el resultado. Luego agrega un caso inválido. No avances si no entiendes por qué la prueba pasa o falla.

### Etapa 6: servicios y sus pruebas

Los servicios contienen decisiones del negocio. No reciben directamente objetos `request` de Flask.

| Archivo | Trabajo | Casos que debes comprobar en `tests/test_servicios.py` |
|---|---|---|
| `app/services/auth_service.py` | Registrar, comprobar credenciales, generar hash y entregar JWT. | Contraseña correcta, incorrecta, correo inexistente, registro repetido. |
| `app/services/medicamento_service.py` | Validar y consultar el catálogo. | Datos requeridos, descripción opcional, listado y duplicados si aplica. |
| `app/services/tratamiento_service.py` | Validar una prescripción y calcular los horarios de tomas. | Intervalo positivo, rango de fechas, hora inicial y cantidad exacta de tomas. |
| `app/services/toma_service.py` | Consultar tomas y registrar cambio de estado. | Estados válidos, estado inventado, marca de hora real y toma inexistente. |

Para el calendario, define primero con palabras qué significa `fecha_fin`: por ejemplo, si incluye todo ese día. Decide también qué ocurre si el intervalo supera el tiempo restante. Luego escribe ejemplos concretos y prueba esos resultados. El PDF propone una terapia de dos días cada ocho horas que genera seis tomas.

### Etapa 7: controladores, rutas y seguridad

Cada endpoint debe tener un contrato antes de programarlo: método, dirección, datos que recibe, JSON que devuelve, quién puede usarlo y código HTTP esperado.

| Archivos | Responsabilidad |
|---|---|
| `app/controllers/auth_controller.py` y `app/routes/auth_routes.py` | Registro, login y asignación de paciente. |
| `app/controllers/medicamento_controller.py` y `app/routes/medicamento_routes.py` | Crear y listar medicamentos. |
| `app/controllers/tratamiento_controller.py` y `app/routes/tratamiento_routes.py` | Crear tratamientos y consultar por paciente. |
| `app/controllers/toma_controller.py` y `app/routes/toma_routes.py` | Consultar calendario y cambiar el estado de una toma. |
| `app/middlewares/auth_middleware.py` | Revisar JWT y permitir o negar según el rol. |
| `app/routes/__init__.py` | Reunir los Blueprints para que `create_app` los registre. |

Rutas que aparecen en el catálogo oficial: `GET /api/salud`, `POST /api/auth/registro`, `POST /api/auth/login`, `POST /api/auth/asignar-paciente`, `GET` y `POST /api/medicamentos`, `POST /api/tratamientos`, `GET /api/tratamientos/paciente/<id>`, `PATCH /api/tomas/<id>` y `GET /api/tomas/paciente/<id>`.

Usa el flujo recomendado: ruta recibe, controlador traduce HTTP, servicio decide, modelo lee o guarda. En respuestas públicas nunca envíes contraseñas ni hashes. Comprueba tanto el permiso concedido como el acceso rechazado.

### Etapa 8: pruebas de rutas y recorrido completo

`tests/test_rutas_api.py` utiliza el cliente de pruebas de Flask y verifica el comportamiento HTTP. Empieza por salud y luego prueba, en orden:

1. Registro de usuario válido y datos inválidos.
2. Login correcto y login con clave incorrecta.
3. Endpoint protegido sin token, con token inválido y con rol insuficiente.
4. Crear y listar medicamento.
5. Crear tratamiento y comprobar que se generen las tomas esperadas.
6. Consultar calendario y marcar una toma.
7. Repetir el flujo con identificadores inexistentes y datos incorrectos.

El resultado final debe ser un recorrido completo: registrar, iniciar sesión, recibir JWT, usar permisos, crear o consultar el medicamento, prescribir tratamiento, ver calendario y marcar una toma.

## 5. Archivos de pruebas: qué va en cada uno

| Archivo | Qué se prueba |
|---|---|
| `tests/__init__.py` | Hace explícito que `tests` es un paquete que se puede importar. |
| `tests/base_test.py` | Crea la app de prueba, cliente HTTP, contexto y tablas temporales; limpia todo después. |
| `tests/test_modelos.py` | Campos, restricciones, relaciones y serialización de modelos. |
| `tests/test_servicios.py` | Reglas de negocio, autenticación y cálculo de horarios. |
| `tests/test_rutas_api.py` | Respuestas HTTP y recorrido de la API desde el cliente Flask. |

Los documentos proponen 17 casos: 8 unitarios, 4 de integración y 5 de extremo a extremo. No es necesario escribirlos todos el primer día; sí conviene cubrir cada regla antes de declarar terminado el módulo.

## 6. Cómo saber si una tarea está completa

Usa esta lista al cerrar cada tarea:

- [ ] Sé explicar con mis palabras qué problema resuelve el archivo.
- [ ] Los nombres están en español y coinciden con el esquema acordado.
- [ ] Escribí primero una prueba que describe el resultado esperado.
- [ ] La prueba pasa y las pruebas que ya pasaban siguen pasando.
- [ ] Revisé el caso correcto y al menos un caso inválido.
- [ ] No guardé secretos en el código ni en Git.
- [ ] Mi compañero puede revisar el cambio y entender el commit.

Cuando termines una etapa, guarda cambios pequeños en tu rama `feature/...` y abre un Pull Request hacia `develop` para revisión. No lleves a `main` algo que no haya sido revisado.

## 7. Tu próxima sesión: un plan de una hora

1. **10 minutos:** confirma que estás en la rama correcta y que ves los cambios remotos de tu compañero.
2. **20 minutos:** compara `schema.sql`, el diagrama y la tabla `medicamentos`; acuerda qué campos son obligatorios y cuáles existen.
3. **20 minutos:** revisa `settings.py`, `requirements.txt` y `tests/base_test.py`; anota qué falta para que las pruebas puedan arrancar.
4. **10 minutos:** escribe una lista corta de los acuerdos y elige una única tarea para la próxima sesión. Una buena primera tarea tuya es terminar la configuración de pruebas y entender cada línea de `BaseTestCase`.

Después de eso, empieza por Usuario y su primera prueba. No empieces simultáneamente modelos, rutas, JWT y algoritmos: cuando algo falle, sería difícil saber cuál pieza causó el problema.

## 8. Documentación de referencia

En `documentos/` están el árbol de archivos, la Guía Maestra, el catálogo de pruebas, la metodología de trabajo y el diagrama relacional. En la copia revisada aparecen cuatro PDF y un PNG. Si el equipo tiene un quinto PDF, deben subirlo al repositorio para agregarlo a esta lista.
