# INFORME TÉCNICO Y AUDITORÍA DE PRUEBAS TDD
## Análisis y Reclasificación Real de la Suite de Pruebas — Medicent Backend V3

- **Proyecto:** Backend_Medicent_v3
- **Equipo de Desarrollo:** Andrés Pachón & Cristian Beltrán
- **Rama:** `develop`
- **Total de Pruebas Implementadas:** 29 Pruebas (100% Passing / en Verde)
- **Framework:** `pytest` 9.1.1 sobre Python 3.12 (Virtualenv)
- **Base de Datos de Test:** SQLite en memoria (`sqlite:///:memory:`)

---

## 1. El Dilema: ¿Por qué en la carpeta `tests/unit/` solo aparecen 5 pruebas?

Al revisar la estructura física de directorios del proyecto:
```text
tests/
├── unit/           -> Contiene 5 pruebas
└── integration/    -> Contiene 24 pruebas
```

Se generaba la duda de si entre Andrés y Cristian únicamente habían desarrollado 5 pruebas unitarias.

### Hallazgo de la Auditoría Técnica:
**La respuesta es NO.** El equipo desarrolló en realidad **18 pruebas unitarias** y **11 pruebas de integración HTTP**.

La discrepancia ocurrió durante el commit `71290a0` (*"(feat)division pruebas unitarias e integracion"*), donde se tomó como criterio de separación:
- **`tests/unit/`:** Archivos que no inicializan la base de datos de ninguna forma.
- **`tests/integration/`:** Archivos que importan `base_test.py` o ejecutan operaciones con `db.session` (incluso si se trata de SQLite en memoria probando funciones aisladas de servicios).

---

## 2. Reclasificación Rigurosa según Estándares de la Industria

En la ingeniería de software profesional:
1. **Prueba Unitaria de Modelo:** Evalúa una entidad aislada, sus campos, tipos de datos y método `to_dict()`.
2. **Prueba Unitaria de Servicio (Lógica de Negocio):** Evalúa una función o método de servicio específico (`crear_medicamento`, `validar_nombre`, `generar_tomas`, `marcar_toma`, `registrar_usuario`, etc.), comprobando validaciones, reglas de negocio y excepciones (`ValueError`), sin involucrar servidor web ni controladores HTTP.
3. **Prueba de Integración (Capa de Rutas / Endpoints HTTP):** Evalúa la colaboración completa entre el cliente de pruebas HTTP de Flask (`client.post`, `client.get`, `client.patch`), serialización JSON, códigos de estado HTTP (200, 201, 400, 404) y persistencia.

---

## 3. Desglose Real de las 29 Pruebas Implementadas

### A. Pruebas Unitarias de Algoritmos y Criptografía (5 Casos — Carpeta `tests/unit/`)
Ubicadas en `tests/unit/`:
1. `test_registro_usuario_exitoso` (`test_auth_service.py`): Creación y hashing seguro con Bcrypt (`$2b$`).
2. `test_registro_correo_duplicado` (`test_auth_service.py`): Control de unicidad de correo.
3. `test_login_exitoso` (`test_auth_service.py`): Verificación de clave y generación de Token JWT.
4. `test_login_contrasena_incorrecta` (`test_auth_service.py`): Rechazo de credenciales erradas.
5. `test_algoritmo_calculo_tomas_intervalo_regular` (`test_calculo_tomas.py`): Matemática de calendarización temporal.

### B. Pruebas Unitarias de Modelos de Datos (3 Casos — Clasificadas en `tests/integration/`)
Prueban la entidad pura y sus métodos:
6. `test_creacion_modelo_medicamento` (`test_medicamento.py`): Atributos y serialización `to_dict()`.
7. `test_creacion_modelo_tratamiento` (`test_tratamiento.py`): Atributos, fechas y relaciones ORM.
8. `test_creacion_modelo_registro_toma` (`test_registro_toma.py`): Estado por defecto `pendiente` y llaves foráneas.

### C. Pruebas Unitarias de Servicios y Lógica de Negocio (10 Casos — Clasificadas en `tests/integration/`)
Prueban exclusivamente los métodos de servicio y sus reglas de negocio:
9. `test_crear_medicamento_exitoso` (`test_medicamento_service.py`): Lógica de inserción de fármaco.
10. `test_crear_medicamento_sin_nombre_lanza_error` (`test_medicamento_service.py`): Validación de campo obligatorio (`ValueError`).
11. `test_obtener_medicamentos_retorna_lista` (`test_medicamento_service.py`): Consulta de colección completa.
12. `test_obtener_medicamento_por_id_existente_e_inexistente` (`test_medicamento_service.py`): Casos frontera de búsqueda por ID.
13. `test_crear_tratamiento_exitoso_genera_tomas` (`test_tratamiento_service.py`): Disparo en cascada de generación de tomas.
14. `test_crear_tratamiento_paciente_inexistente_lanza_error` (`test_tratamiento_service.py`): Validación de existencia del paciente.
15. `test_crear_tratamiento_medicamento_inexistente_lanza_error` (`test_tratamiento_service.py`): Validación de catálogo farmacológico.
16. `test_crear_tratamiento_fechas_o_frecuencia_invalidas` (`test_tratamiento_service.py`): Regla de negocio de coherencia temporal y frecuencia.
17. `test_obtener_tratamientos_por_paciente` (`test_tratamiento_service.py`): Filtro de prescripciones por paciente.
18. `test_tomas_generadas_estado_inicial_pendiente` (`test_generacion_tomas.py`): Verificación del estado de creación de tomas.
19. `test_transicion_estado_toma_valida` (`test_marcar_toma.py`): Máquina de estados de toma (`pendiente` -> `tomada`) y timestamp.

### D. Pruebas de Integración de Endpoints RESTful (10 Casos — Carpeta `tests/integration/`)
Prueban peticiones HTTP reales a la API de Flask:
20. `test_crear_medicamento_endpoint_exitoso` (`test_medicamento_routes.py`): POST /api/medicamentos (201 Created).
21. `test_crear_medicamento_sin_nombre_retorna_400` (`test_medicamento_routes.py`): POST /api/medicamentos error (400 Bad Request).
22. `test_listar_medicamentos_endpoint` (`test_medicamento_routes.py`): GET /api/medicamentos (200 OK).
23. `test_crear_tratamiento_endpoint_exitoso` (`test_tratamiento_routes.py`): POST /api/tratamientos (201 Created).
24. `test_crear_tratamiento_datos_faltantes_retorna_400` (`test_tratamiento_routes.py`): POST /api/tratamientos error (400 Bad Request).
25. `test_listar_tratamientos_por_paciente_endpoint` (`test_tratamiento_routes.py`): GET /api/tratamientos/paciente/<id> (200 OK).
26. `test_marcar_toma_endpoint_exitoso` (`test_toma_routes.py`): PATCH /api/tomas/<id> (200 OK).
27. `test_marcar_toma_estado_invalido_retorna_400` (`test_toma_routes.py`): PATCH /api/tomas/<id> estado erróneo (400 Bad Request).
28. `test_marcar_toma_inexistente_retorna_404` (`test_toma_routes.py`): PATCH /api/tomas/99999 (404 Not Found).
29. `test_listar_tomas_por_paciente_endpoint` (`test_toma_routes.py`): GET /api/tomas/paciente/<id> (200 OK).

---

## 4. Resumen Comparativo de Métricas

| Criterio | Por Ubicación Física de Carpetas | Por Naturaleza Real del Código |
| :--- | :---: | :---: |
| **Pruebas Unitarias** | 5 (17.2%) | **19 (65.5%)** |
| **Pruebas de Integración HTTP** | 24 (82.8%) | **10 (34.5%)** |
| **Total de Pruebas en Verde** | **29 (100%)** | **29 (100%)** |

---

## 5. Conclusión y Recomendación
El trabajo realizado por el equipo abarca una **cobertura unitaria robusta (65.5% de la suite)**, blindando todas las capas críticas: cálculo matemático, modelos ORM, servicios de negocio, cifrado Bcrypt y tokens JWT, complementado con una **capa de integración sólida (34.5%)** que certifica los contratos HTTP de la API REST.
