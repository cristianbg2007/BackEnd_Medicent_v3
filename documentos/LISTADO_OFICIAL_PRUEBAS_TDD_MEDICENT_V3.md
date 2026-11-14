# DOCUMENTO OFICIAL DE INGENIERÍA TDD
## Catálogo Exhaustivo y Detallado de Pruebas — Medicent Backend V3
**Especificación Minuciosa: 40 Pruebas Individuales (AAA Completo — Arrange / Act / Assert)**

- **Proyecto:** Backend_Medicent_v3
- **Equipo de Desarrollo:** Andrés & Cristian Beltrán
- **Total de Casos:** 40 Pruebas Exhaustivas Individuales
- **Estado Implementadas (en Verde / OK):** 29 Pruebas (`tests/`)
- **Estado Planificadas:** 11 Pruebas (Modelos aislados, asignación de cuidadores y E2E de flujos)
- **Framework de Ejecución:** `pytest` / `unittest`
- **Base de Datos de Pruebas:** SQLite en memoria (`sqlite:///:memory:`)

---

## 1. Resumen de la Matriz de Pruebas por Módulos y Niveles

| Nivel | Dominio / Módulo | Implementadas (OK) | Planificadas | Total Casos | Archivos Asociados |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Nivel 1: Unitarias** | Lógica de negocio pura (Auth, Criptografía, Cálculo de tomas, Modelos en memoria) | **5 casos** | **5 casos** | **10 casos** | `tests/unit/test_auth_service.py`<br>`tests/unit/test_calculo_tomas.py`<br>`tests/unit/test_modelos_unitarios.py` |
| **Nivel 2: Integración** | Base de datos SQLite, Servicios ORM, Prescripciones, Seguimiento de tomas y Endpoints REST | **24 casos** | **1 caso** | **25 casos** | `tests/integration/test_*.py` |
| **Nivel 3: End-to-End (E2E)** | Flujos completos de cliente HTTP (Healthcheck, Registro/Login JWT, Tratamiento integral, Auditoría) | **0 casos** | **5 casos** | **5 casos** | `tests/e2e/test_flujo_clinico_e2e.py` |
| **TOTAL GENERAL** | **Suite Completa del Sistema** | **29 IMPLEMENTADAS** | **11 PLANIFICADAS** | **40 CASOS** | **Cobertura Integral** |

---

## 2. Convención y Estructura de Registro por Caso (Patrón AAA)
Cada caso de prueba está registrado de manera estrictamente individual bajo el patrón estándar de la industria:
1. **Preparar (Arrange):** Define precondiciones, instancias de datos, tokens de sesión o mocks en memoria.
2. **Actuar (Act):** Especifica la invocación exacta del método, servicio o petición HTTP (`GET`, `POST`, `PATCH`).
3. **Verificar (Assert):** Especifica las aserciones obligatorias, códigos de estado HTTP, validación de excepciones o estado de persistencia.

---

## 3. Catálogo Detallado de Pruebas Unitarias (Nivel 1 — Funciones Aisladas)

### [U1] `test_registro_usuario_exitoso`
- **Nivel:** Unitaria
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/unit/test_auth_service.py`
- **Función probada:** `auth_service.registrar_usuario(...)`
- **Objetivo:** Validar que el servicio registre un nuevo usuario, cifre la contraseña en un hash Bcrypt válido (`$2b$`) y devuelva la entidad persistida con ID asignado.
- **PREPARAR (ARRANGE):**
  - Parámetros en memoria: `nombre="Juan Perez"`, `correo="juan@test.com"`, `contrasena="secret123"`, `rol="paciente"`.
- **ACTUAR (ACT):**
  - Invocar `auth_service.registrar_usuario(nombre, correo, contrasena, rol)`.
- **VERIFICAR (ASSERT):**
  - `usuario is not None`
  - `usuario.id is not None`
  - `usuario.correo == "juan@test.com"`
  - `usuario.contrasena_hash != "secret123"`
  - `usuario.contrasena_hash.startswith("$2b$") is True`

---

### [U2] `test_registro_correo_duplicado`
- **Nivel:** Unitaria
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/unit/test_auth_service.py`
- **Función probada:** `auth_service.registrar_usuario(...)`
- **Objetivo:** Asegurar que si un correo electrónico ya existe registrado en el sistema, el servicio rechace la operación devolviendo `None`.
- **PREPARAR (ARRANGE):**
  - Registrar previamente un usuario con correo `"duplicado@test.com"`.
- **ACTUAR (ACT):**
  - Intentar registrar un segundo usuario con idéntico correo `"duplicado@test.com"`.
- **VERIFICAR (ASSERT):**
  - `resultado is None`
  - La base de datos no duplica el registro ni genera inconsistencias.

---

### [U3] `test_login_exitoso`
- **Nivel:** Unitaria
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/unit/test_auth_service.py`
- **Función probada:** `auth_service.iniciar_sesion(...)`
- **Objetivo:** Validar que un usuario con credenciales correctas reciba un diccionario de autenticación con Token JWT firmado, claims de rol y sus datos de perfil.
- **PREPARAR (ARRANGE):**
  - Crear usuario con `correo="login@test.com"`, `contrasena="password123"` y `rol="cuidador"`.
- **ACTUAR (ACT):**
  - Invocar `auth_service.iniciar_sesion("login@test.com", "password123")`.
- **VERIFICAR (ASSERT):**
  - `resultado is not None`
  - `"token" in resultado`
  - `resultado["usuario"]["correo"] == "login@test.com"`
  - `resultado["usuario"]["rol"] == "cuidador"`

---

### [U4] `test_login_contrasena_incorrecta`
- **Nivel:** Unitaria
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/unit/test_auth_service.py`
- **Función probada:** `auth_service.iniciar_sesion(...)`
- **Objetivo:** Comprobar que si la contraseña provista no coincide con el hash almacenado, el inicio de sesión sea denegado retornando `None`.
- **PREPARAR (ARRANGE):**
  - Crear usuario registrado con contraseña `"correcta123"`.
- **ACTUAR (ACT):**
  - Invocar `auth_service.iniciar_sesion("login@test.com", "incorrecta999")`.
- **VERIFICAR (ASSERT):**
  - `resultado is None`
  - Ningún token JWT es generado ni devuelto.

---

### [U5] `test_algoritmo_calculo_tomas_intervalo_regular`
- **Nivel:** Unitaria
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/unit/test_calculo_tomas.py`
- **Función probada:** `tratamiento_service.calcular_horarios_tomas(...)`
- **Objetivo:** Validar la exactitud matemática del motor de calendarización: tratamiento de 2 días (48 horas) cada 8 horas debe generar exactamente 6 timestamps con intervalos idénticos de 8 horas.
- **PREPARAR (ARRANGE):**
  - `fecha_inicio = date(2026, 11, 1)`, `fecha_fin = date(2026, 11, 2)`.
  - `hora_inicial = time(8, 0)`, `frecuencia_horas = 8`.
- **ACTUAR (ACT):**
  - Invocar `calcular_horarios_tomas(fecha_inicio, fecha_fin, hora_inicial, frecuencia_horas)`.
- **VERIFICAR (ASSERT):**
  - `len(horarios) == 6`
  - `horarios[0] == datetime(2026, 11, 1, 8, 0, 0)`
  - La diferencia temporal entre tomas consecutivas es exactamente `timedelta(hours=8)`.

---

### [U6] `test_validacion_algoritmo_tomas_frecuencia_invalida`
- **Nivel:** Unitaria
- **Estado:** PLANIFICADA
- **Archivo:** `tests/unit/test_calculo_tomas.py`
- **Función probada:** `tratamiento_service.calcular_horarios_tomas(...)`
- **Objetivo:** Garantizar que el motor matemático rechace frecuencias menores o iguales a cero (`<= 0`) evitando bucles infinitos.
- **PREPARAR (ARRANGE):**
  - Rango de fechas válido con `frecuencia_horas = 0` o `frecuencia_horas = -4`.
- **ACTUAR (ACT):**
  - Invocar `calcular_horarios_tomas(...)` dentro de `pytest.raises(ValueError)`.
- **VERIFICAR (ASSERT):**
  - Se lanza excepción `ValueError` indicando que la frecuencia en horas debe ser estrictamente mayor a 0.

---

### [U7] `test_modelo_usuario_instanciacion_y_atributos`
- **Nivel:** Unitaria
- **Estado:** PLANIFICADA
- **Archivo:** `tests/unit/test_modelos_unitarios.py`
- **Función probada:** `Usuario.to_dict()`
- **Objetivo:** Validar que la clase `Usuario` asigne sus propiedades en memoria y que su método de serialización oculte el hash de contraseña.
- **PREPARAR (ARRANGE):**
  - `Usuario(nombre='Carlos', correo='carlos@medicent.com', contrasena_hash='hash123', rol='cuidador')`.
- **ACTUAR (ACT):**
  - Ejecutar `usuario.to_dict()`.
- **VERIFICAR (ASSERT):**
  - Los campos coinciden y la clave `"contrasena_hash"` no está expuesta en el diccionario serializado.

---

### [U8] `test_modelo_medicamento_instanciacion`
- **Nivel:** Unitaria
- **Estado:** PLANIFICADA
- **Archivo:** `tests/unit/test_modelos_unitarios.py`
- **Función probada:** `Medicamento.to_dict()`
- **Objetivo:** Validar la instanciación en memoria del modelo `Medicamento` con sus atributos farmacológicos básicos.
- **PREPARAR (ARRANGE):**
  - `Medicamento(nombre='Loratadina', descripcion='Antihistamínico', forma_farmaceutica='Comprimido 10mg')`.
- **ACTUAR (ACT):**
  - Ejecutar `med.to_dict()`.
- **VERIFICAR (ASSERT):**
  - El diccionario contiene las claves `'nombre'`, `'descripcion'` y `'forma_farmaceutica'`.

---

### [U9] `test_modelo_tratamiento_instanciacion_y_defaults`
- **Nivel:** Unitaria
- **Estado:** PLANIFICADA
- **Archivo:** `tests/unit/test_modelos_unitarios.py`
- **Función probada:** `Tratamiento.__init__()`
- **Objetivo:** Comprobar que una instancia de `Tratamiento` mantenga la integridad de sus campos antes de ser persistida.
- **PREPARAR (ARRANGE):**
  - Datos de prescripción médica en memoria (paciente, medicamento, dosis, frecuencia y fechas).
- **ACTUAR (ACT):**
  - Instanciar objeto `Tratamiento(...)`.
- **VERIFICAR (ASSERT):**
  - Propiedades asignadas correctamente y coherencia de tipos de datos.

---

### [U10] `test_modelo_registro_toma_estado_inicial`
- **Nivel:** Unitaria
- **Estado:** PLANIFICADA
- **Archivo:** `tests/unit/test_modelos_unitarios.py`
- **Función probada:** `RegistroToma.__init__()`
- **Objetivo:** Confirmar que una instancia de `RegistroToma` inicie con estado predeterminado `'pendiente'` y fecha/hora real de toma nula.
- **PREPARAR (ARRANGE):**
  - `RegistroToma(tratamiento_id=1, fecha_hora_programada=datetime.now())`.
- **ACTUAR (ACT):**
  - Evaluar propiedades del objeto recién instanciado.
- **VERIFICAR (ASSERT):**
  - `toma.estado == 'pendiente'` y `toma.fecha_hora_toma is None`.

---

## 4. Catálogo Detallado de Pruebas de Integración (Nivel 2 — Servicios, BD y Rutas)

### [I1] `test_creacion_modelo_medicamento`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_medicamento.py`
- **Objetivo:** Persistir un medicamento en la base de datos de pruebas y verificar generación de su ID primario autoincremental.
- **PREPARAR (ARRANGE):** Instanciar `Medicamento(nombre="Paracetamol", descripcion="Analgésico", forma_farmaceutica="Comprimido")`.
- **ACTUAR (ACT):** `db.session.add(med); db.session.commit()`.
- **VERIFICAR (ASSERT):** `med.id is not None`, nombre persistido y `med.to_dict()` contiene las propiedades correctas.

---

### [I2] `test_crear_medicamento_exitoso`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_medicamento_service.py`
- **Objetivo:** Validar que `medicamento_service.crear_medicamento(...)` persista en BD un fármaco con atributos válidos.
- **PREPARAR (ARRANGE):** Parámetros `nombre="Ibuprofeno"`, `descripcion="Antiinflamatorio"`, `forma_farmaceutica="Cápsula"`.
- **ACTUAR (ACT):** Invocar `crear_medicamento(nombre, descripcion, forma_farmaceutica)`.
- **VERIFICAR (ASSERT):** Entidad devuelta con `id is not None`, nombre almacenado y forma farmacéutica exacta.

---

### [I3] `test_crear_medicamento_sin_nombre_lanza_error`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_medicamento_service.py`
- **Objetivo:** Validar que el servicio rechace la creación si el nombre del fármaco está vacío o ausente.
- **PREPARAR (ARRANGE):** `nombre=""` o compuesto de espacios en blanco.
- **ACTUAR (ACT):** Invocar `crear_medicamento(...)` dentro de `pytest.raises(ValueError)`.
- **VERIFICAR (ASSERT):** Se lanza `ValueError` conteniendo la palabra `"nombre"`.

---

### [I4] `test_obtener_medicamentos_retorna_lista`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_medicamento_service.py`
- **Objetivo:** Crear múltiples medicamentos en BD y comprobar que el servicio retorne la lista completa.
- **PREPARAR (ARRANGE):** Registrar en BD "Amoxicilina" y "Omeprazol".
- **ACTUAR (ACT):** Invocar `obtener_medicamentos()`.
- **VERIFICAR (ASSERT):** Longitud de lista igual a 2 y presencia de ambos medicamentos en los resultados.

---

### [I5] `test_obtener_medicamento_por_id_existente_e_inexistente`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_medicamento_service.py`
- **Objetivo:** Comprobar consulta por ID: retorna el objeto si existe o `None` si el ID no está registrado.
- **PREPARAR (ARRANGE):** Registrar fármaco con ID conocido; definir ID inexistente `9999`.
- **ACTUAR (ACT):** Ejecutar `obtener_medicamento_por_id(...)` para ambos identificadores.
- **VERIFICAR (ASSERT):** Retorna la entidad para el ID válido y `None` para el ID `9999`.

---

### [I6] `test_crear_medicamento_endpoint_exitoso`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_medicamento_routes.py`
- **Objetivo:** Petición HTTP POST a `/api/medicamentos` responde código 201 Created y JSON del fármaco registrado.
- **PREPARAR (ARRANGE):** Payload JSON con `nombre`, `descripcion` y `forma_farmaceutica`.
- **ACTUAR (ACT):** `client.post("/api/medicamentos", json=payload)`.
- **VERIFICAR (ASSERT):** Status HTTP 201, mensaje de éxito y datos del fármaco con ID asignado.

---

### [I7] `test_crear_medicamento_sin_nombre_retorna_400`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_medicamento_routes.py`
- **Objetivo:** Petición POST a `/api/medicamentos` sin nombre obligatorio debe responder 400 Bad Request.
- **PREPARAR (ARRANGE):** Payload omitiendo la clave `"nombre"`.
- **ACTUAR (ACT):** `client.post("/api/medicamentos", json=payload)`.
- **VERIFICAR (ASSERT):** Status HTTP 400 y mensaje de error en JSON.

---

### [I8] `test_listar_medicamentos_endpoint`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_medicamento_routes.py`
- **Objetivo:** Petición GET a `/api/medicamentos` responde 200 OK y el catálogo farmacológico completo.
- **PREPARAR (ARRANGE):** 2 medicamentos persistidos previamente en la base de datos.
- **ACTUAR (ACT):** `client.get("/api/medicamentos")`.
- **VERIFICAR (ASSERT):** Status HTTP 200 y array JSON con 2 elementos coincidentes.

---

### [I9] `test_creacion_modelo_tratamiento`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento.py`
- **Objetivo:** Comprobar la integridad de claves foráneas entre `Tratamiento`, `Usuario` (paciente) y `Medicamento`.
- **PREPARAR (ARRANGE):** Paciente y medicamento persistidos en SQLite.
- **ACTUAR (ACT):** Crear y guardar `Tratamiento` vinculando ambos IDs.
- **VERIFICAR (ASSERT):** `tratamiento.id is not None`, relación `tratamiento.paciente` y `tratamiento.medicamento` resuelven adecuadamente.

---

### [I10] `test_crear_tratamiento_exitoso_genera_tomas`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento_service.py`
- **Objetivo:** Al invocar `tratamiento_service.crear_tratamiento(...)`, deben persistirse en cascada automática todas las tomas del calendario.
- **PREPARAR (ARRANGE):** Prescripción de 2 días cada 8 horas para un paciente y fármaco válidos.
- **ACTUAR (ACT):** Invocar `crear_tratamiento(...)`.
- **VERIFICAR (ASSERT):** Tratamiento con ID generado, `len(tratamiento.tomas) == 6` y tomas en estado inicial `'pendiente'`.

---

### [I11] `test_crear_tratamiento_paciente_inexistente_lanza_error`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento_service.py`
- **Objetivo:** Rechazar la prescripción si el `paciente_id` no existe en la base de datos.
- **PREPARAR (ARRANGE):** `paciente_id = 9999` inexistente y medicamento válido.
- **ACTUAR (ACT):** Invocar `crear_tratamiento(...)` dentro de bloque de excepción.
- **VERIFICAR (ASSERT):** Se lanza `ValueError` indicando que el paciente no existe.

---

### [I12] `test_crear_tratamiento_medicamento_inexistente_lanza_error`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento_service.py`
- **Objetivo:** Rechazar la prescripción si el `medicamento_id` no existe en el catálogo.
- **PREPARAR (ARRANGE):** Paciente válido y `medicamento_id = 9999` inexistente.
- **ACTUAR (ACT):** Invocar `crear_tratamiento(...)`.
- **VERIFICAR (ASSERT):** Se lanza `ValueError` conteniendo la palabra `"medicamento"`.

---

### [I13] `test_crear_tratamiento_fechas_o_frecuencia_invalidas`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento_service.py`
- **Objetivo:** Validar que la fecha de fin no sea anterior a la de inicio y que la frecuencia sea mayor a 0.
- **PREPARAR (ARRANGE):** Fechas invertidas (inicio posterior a fin) o frecuencia `= 0`.
- **ACTUAR (ACT):** Ejecutar el servicio creador para ambos casos inválidos.
- **VERIFICAR (ASSERT):** En ambos casos se lanza `ValueError` impidiendo la inserción.

---

### [I14] `test_obtener_tratamientos_por_paciente`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento_service.py`
- **Objetivo:** Retornar únicamente las prescripciones del paciente consultado y lista vacía para pacientes sin tratamientos.
- **PREPARAR (ARRANGE):** Tratamiento para Paciente A; Paciente B sin registros.
- **ACTUAR (ACT):** Invocar `obtener_tratamientos_por_paciente(...)` para ambos IDs.
- **VERIFICAR (ASSERT):** Longitud 1 para el paciente con datos y longitud 0 para el paciente sin datos.

---

### [I15] `test_crear_tratamiento_endpoint_exitoso`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento_routes.py`
- **Objetivo:** POST a `/api/tratamientos` responde 201 Created con el tratamiento y conteo de tomas autogeneradas.
- **PREPARAR (ARRANGE):** Payload JSON completo (paciente_id, medicamento_id, dosis, frecuencia 8h, fechas, hora_inicial).
- **ACTUAR (ACT):** `client.post("/api/tratamientos", json=payload)`.
- **VERIFICAR (ASSERT):** Status HTTP 201, objeto tratamiento y `total_tomas_generadas == 6`.

---

### [I16] `test_crear_tratamiento_datos_faltantes_retorna_400`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento_routes.py`
- **Objetivo:** POST a `/api/tratamientos` con campos obligatorios omitidos responde 400 Bad Request.
- **PREPARAR (ARRANGE):** Payload incompleto (únicamente `paciente_id`).
- **ACTUAR (ACT):** `client.post("/api/tratamientos", json=payload)`.
- **VERIFICAR (ASSERT):** Status HTTP 400 y mensaje de error descriptivo en JSON.

---

### [I17] `test_listar_tratamientos_por_paciente_endpoint`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_tratamiento_routes.py`
- **Objetivo:** GET a `/api/tratamientos/paciente/<id>` responde 200 OK con la lista de tratamientos del paciente.
- **PREPARAR (ARRANGE):** Tratamiento creado previamente en BD para la paciente Laura.
- **ACTUAR (ACT):** `client.get(f"/api/tratamientos/paciente/{paciente_id}")`.
- **VERIFICAR (ASSERT):** Status HTTP 200, array JSON con longitud 1 y dosis correspondiente.

---

### [I18] `test_creacion_modelo_registro_toma`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_registro_toma.py`
- **Objetivo:** Validar la persistencia de un `RegistroToma` vinculado a su tratamiento padre con estado inicial `'pendiente'`.
- **PREPARAR (ARRANGE):** Tratamiento persistido en base de datos.
- **ACTUAR (ACT):** Crear y persistir `RegistroToma` con fecha/hora programada.
- **VERIFICAR (ASSERT):** `toma.id is not None`, `toma.estado == 'pendiente'` y relación `toma.tratamiento` resuelve bien.

---

### [I19] `test_tomas_generadas_estado_inicial_pendiente`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_generacion_tomas.py`
- **Objetivo:** Confirmar que el 100% de las tomas autogeneradas nazcan en estado `'pendiente'` y fecha real de toma nula.
- **PREPARAR (ARRANGE):** Tratamiento persistido de 2 días cada 8 horas.
- **ACTUAR (ACT):** Invocar `generar_tomas_tratamiento(tratamiento.id)`.
- **VERIFICAR (ASSERT):** 6 tomas creadas, todas con `estado == 'pendiente'` y `fecha_hora_toma is None`.

---

### [I20] `test_transicion_estado_toma_valida`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_marcar_toma.py`
- **Objetivo:** `toma_service.marcar_toma(...)` debe actualizar el estado a `'tomada'` y fijar timestamp real de consumo.
- **PREPARAR (ARRANGE):** `RegistroToma` en estado `'pendiente'`.
- **ACTUAR (ACT):** Invocar `marcar_toma(toma_id, nuevo_estado="tomada")`.
- **VERIFICAR (ASSERT):** `estado == 'tomada'`, `fecha_hora_toma is not None` tanto en el objeto devuelto como en la BD.

---

### [I21] `test_marcar_toma_endpoint_exitoso`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_toma_routes.py`
- **Objetivo:** PATCH a `/api/tomas/<id>` con `{"nuevo_estado": "tomada"}` responde 200 OK y persiste el cambio.
- **PREPARAR (ARRANGE):** Toma pendiente creada en la base de datos.
- **ACTUAR (ACT):** `client.patch(f"/api/tomas/{toma_id}", json={"nuevo_estado": "tomada"})`.
- **VERIFICAR (ASSERT):** Status HTTP 200 y JSON confirmando estado `'tomada'` con timestamp asignado.

---

### [I22] `test_marcar_toma_estado_invalido_retorna_400`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_toma_routes.py`
- **Objetivo:** PATCH a `/api/tomas/<id>` con estado no permitido responde 400 Bad Request.
- **PREPARAR (ARRANGE):** Toma existente; payload con `{"nuevo_estado": "inventado"}`.
- **ACTUAR (ACT):** `client.patch(...)` enviando el estado inválido.
- **VERIFICAR (ASSERT):** Status HTTP 400 y mensaje de error en JSON.

---

### [I23] `test_marcar_toma_inexistente_retorna_404`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_toma_routes.py`
- **Objetivo:** PATCH a `/api/tomas/99999` (toma inexistente) responde 404 Not Found.
- **PREPARAR (ARRANGE):** ID inexistente `99999`.
- **ACTUAR (ACT):** `client.patch("/api/tomas/99999", json={"nuevo_estado": "tomada"})`.
- **VERIFICAR (ASSERT):** Status HTTP 404 y mensaje de error en JSON.

---

### [I24] `test_listar_tomas_por_paciente_endpoint`
- **Nivel:** Integración
- **Estado:** IMPLEMENTADA (OK)
- **Archivo:** `tests/integration/test_toma_routes.py`
- **Objetivo:** GET a `/api/tomas/paciente/<id>` responde 200 OK y el listado de tomas del paciente.
- **PREPARAR (ARRANGE):** Paciente con prescripción de 6 tomas generadas.
- **ACTUAR (ACT):** `client.get(f"/api/tomas/paciente/{paciente_id}")`.
- **VERIFICAR (ASSERT):** Status HTTP 200, array JSON con 6 tomas y estados correspondientes.

---

### [I25] `test_asignar_paciente_a_cuidador_tabla_asociativa`
- **Nivel:** Integración
- **Estado:** PLANIFICADA
- **Archivo:** `tests/integration/test_asignacion_cuidador.py`
- **Objetivo:** `auth_service.asignar_paciente(...)` debe persistir la relación en la tabla intermedia `pacientes_cuidadores` y evitar duplicados.
- **PREPARAR (ARRANGE):** 1 usuario cuidador y 1 usuario paciente en BD.
- **ACTUAR (ACT):** Invocar `asignar_paciente(cuidador.id, paciente.id)` dos veces seguidas.
- **VERIFICAR (ASSERT):** La primera llamada vincula exitosamente; la segunda llamada devuelve `None` evitando registros duplicados.

---

## 5. Catálogo Detallado de Pruebas End-to-End (Nivel 3 — Flujos Completos de la API)

### [E1] `test_e2e_healthcheck_servidor_y_base_de_datos`
- **Nivel:** End-to-End (E2E)
- **Estado:** PLANIFICADA
- **Archivo:** `tests/e2e/test_flujo_clinico_e2e.py`
- **Objetivo:** Peticiones GET a `/api/estado` y `/api/estado-db` confirman servidor activo y conexión a base de datos.
- **PREPARAR (ARRANGE):** Cliente de pruebas de la aplicación inicializado.
- **ACTUAR (ACT):** Ejecutar peticiones GET a ambos endpoints.
- **VERIFICAR (ASSERT):** Código HTTP 200 en ambos endpoints y respuestas JSON con confirmación de estado activo.

---

### [E2] `test_e2e_flujo_registro_login_y_obtencion_jwt`
- **Nivel:** End-to-End (E2E)
- **Estado:** PLANIFICADA
- **Archivo:** `tests/e2e/test_flujo_clinico_e2e.py`
- **Objetivo:** Ciclo completo de cuenta: registrar usuario vía HTTP POST y autenticarse en `/api/auth/login` para recibir token JWT.
- **PREPARAR (ARRANGE):** Payload de registro con datos válidos.
- **ACTUAR (ACT):** 1) POST `/api/auth/registro`. 2) POST `/api/auth/login`.
- **VERIFICAR (ASSERT):** Registro responde 201 Created; Login responde 200 OK y entrega token JWT utilizable.

---

### [E3] `test_e2e_login_invalido_rechazado_con_401`
- **Nivel:** End-to-End (E2E)
- **Estado:** PLANIFICADA
- **Archivo:** `tests/e2e/test_flujo_clinico_e2e.py`
- **Objetivo:** Validar que una petición de login con contraseña incorrecta sea rechazada con código HTTP 401 Unauthorized.
- **PREPARAR (ARRANGE):** Usuario previamente registrado en base de datos.
- **ACTUAR (ACT):** POST `/api/auth/login` con clave errónea.
- **VERIFICAR (ASSERT):** Código HTTP 401 Unauthorized y ningún token retornado.

---

### [E4] `test_e2e_ciclo_completo_prescripcion_y_consumo_tomas`
- **Nivel:** End-to-End (E2E)
- **Estado:** PLANIFICADA
- **Archivo:** `tests/e2e/test_flujo_clinico_e2e.py`
- **Objetivo:** Flujo integral: prescribir tratamiento (3 días cada 12h = 6 tomas), consultar calendario por GET y marcar primera toma por PATCH.
- **PREPARAR (ARRANGE):** Paciente y medicamento existentes en base de datos.
- **ACTUAR (ACT):** 1) POST `/api/tratamientos`. 2) GET `/api/tomas/paciente/<id>`. 3) PATCH `/api/tomas/<id>`.
- **VERIFICAR (ASSERT):** Tratamiento 201 con 6 tomas generadas; GET retorna 6 tomas pendientes; PATCH responde 200 y el calendario refleja 1 tomada y 5 pendientes.

---

### [E5] `test_e2e_auditoria_de_adherencia_paciente`
- **Nivel:** End-to-End (E2E)
- **Estado:** PLANIFICADA
- **Archivo:** `tests/e2e/test_flujo_clinico_e2e.py`
- **Objetivo:** Comprobar trazabilidad clínica: cuidador consulta tomas y audita timestamps reales y estados de cumplimiento.
- **PREPARAR (ARRANGE):** Paciente con tomas en estados mixtos (`tomada`, `omitida`, `retrasada`).
- **ACTUAR (ACT):** GET `/api/tomas/paciente/<id>`.
- **VERIFICAR (ASSERT):** Status HTTP 200 y cada elemento del reporte contiene `fecha_hora_programada`, `fecha_hora_toma` y `estado`.

---

## 6. Comandos Oficiales de Ejecución y Verificación

### Ejecución de la suite completa con Pytest:
```powershell
.\venv\Scripts\pytest -v
```

### Ejecución con Unittest estándar:
```powershell
.\venv\Scripts\python -m unittest discover -v -s tests -p "test_*.py"
```

