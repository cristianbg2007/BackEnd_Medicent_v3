# DOCUMENTO OFICIAL DE INGENIERÍA TDD
## Catálogo y Matriz Unificada de Pruebas — Medicent V3 (Backend Flask + Mobile Flutter)
**Especificación Exhaustiva: 62 Pruebas Automatizadas Implementadas (100% Passing / en Verde)**

- **Proyecto:** Medicent V3 • Sistema de Gestión y Adherencia Farmacológica
- **Equipo de Desarrollo:** Andrés Pachón & Cristian Beltrán
- **Total de Pruebas Implementadas:** **62 Casos Automatizados**
  - **Backend Flask (Python):** 32 Pruebas (`pytest` / `unittest` sobre SQLite en memoria)
  - **Mobile App (Flutter/Dart):** 30 Pruebas (`flutter test` con patrón AAA)
- **Tasa de Aprobación:** **100% de Pruebas en Verde (0 Fallos)**
- **Metodología:** Desarrollo Guiado por Pruebas (Test-Driven Development - TDD)

---

## 1. Resumen Ejecutivo del Ecosistema de Pruebas

| Capa del Sistema | Tecnología | Pruebas Implementadas | Estado | Archivos Asociados |
| :--- | :--- | :---: | :---: | :--- |
| **Backend: Unitarias Puras** | Python / Pytest | **5 casos** | 🟢 100% OK | `tests/unit/test_auth_service.py`<br>`tests/unit/test_calculo_tomas.py` |
| **Backend: Integración & Endpoints** | Flask Client / SQLite | **27 casos** | 🟢 100% OK | `tests/integration/test_*.py` |
| **Mobile: Core API & Red** | Dart / HTTP Client | **4 casos** | 🟢 100% OK | `test/core/api/api_client_test.dart`<br>`test/core/api/api_endpoints_test.dart` |
| **Mobile: Alarmas & Notificaciones** | Local Notifications / Audio | **7 casos** | 🟢 100% OK | `test/core/services/notification_service_test.dart` |
| **Mobile: Utilidades & Validadores** | Dart Purt Functions | **5 casos** | 🟢 100% OK | `test/core/utils/utils_test.dart` |
| **Mobile: Autenticación & JWT** | Secure Storage / Models | **4 casos** | 🟢 100% OK | `test/features/auth/models/usuario_model_test.dart`<br>`test/features/auth/services/auth_service_test.dart` |
| **Mobile: Módulo Cuidador** | Services / Parsing | **1 caso** | 🟢 100% OK | `test/features/cuidador/services/cuidador_service_test.dart` |
| **Mobile: Medicamentos** | Catálogo / Null-Safety | **3 casos** | 🟢 100% OK | `test/features/medicamentos/models/`<br>`test/features/medicamentos/services/` |
| **Mobile: Tomas & Semáforo** | Tomas / Adherencia | **3 casos** | 🟢 100% OK | `test/features/tomas/models/`<br>`test/features/tomas/services/` |
| **Mobile: Prescripciones** | Tratamientos / Cronograma | **3 casos** | 🟢 100% OK | `test/features/tratamientos/models/`<br>`test/features/tratamientos/services/` |
| **TOTAL ECOSISTEMA** | **Flask + Flutter** | **62 CASOS** | 🟢 **100% VERDE** | **Cobertura Integral Full-Stack** |

---

## 2. Convención y Estructura por Caso (Patrón AAA)
Cada caso de prueba se rige estrictamente bajo el estándar de la industria:
1. **Preparar (Arrange):** Define precondiciones, instancias de datos, tokens JWT o mocks en memoria.
2. **Actuar (Act):** Invoca el método, servicio o petición HTTP (`GET`, `POST`, `PATCH`, `DELETE`).
3. **Verificar (Assert):** Comprueba aserciones obligatorias, códigos HTTP (200, 201, 400, 404), excepciones y mutaciones de estado.

---

## 3. Catálogo de Pruebas del Backend Flask (32 Casos en Verde)

### A. Algoritmos y Criptografía (`tests/unit/`)
1. **[B-U1] `test_registro_usuario_exitoso` (`test_auth_service.py`):**
   * *Arrange:* Parámetros `nombre="Juan Perez"`, `correo="juan@test.com"`, `contrasena="secret123"`, `rol="paciente"`.
   * *Act:* Invocar `auth_service.registrar_usuario(...)`.
   * *Assert:* Usuario persistido con ID, clave cifrada en hash Bcrypt `$2b$`.
2. **[B-U2] `test_registro_correo_duplicado` (`test_auth_service.py`):**
   * *Arrange:* Usuario registrado previamente con `duplicado@test.com`.
   * *Act:* Intentar registrar segundo usuario con el mismo correo.
   * *Assert:* Operación rechazada retornando `None`.
3. **[B-U3] `test_login_exitoso` (`test_auth_service.py`):**
   * *Arrange:* Usuario con `correo="login@test.com"`, `contrasena="password123"`.
   * *Act:* `auth_service.iniciar_sesion("login@test.com", "password123")`.
   * *Assert:* Retorna token JWT firmado, claims de rol y datos de perfil.
4. **[B-U4] `test_login_contrasena_incorrecta` (`test_auth_service.py`):**
   * *Arrange:* Usuario con clave `"correcta123"`.
   * *Act:* `auth_service.iniciar_sesion("login@test.com", "incorrecta999")`.
   * *Assert:* Retorna `None`, denegando acceso.
5. **[B-U5] `test_algoritmo_calculo_tomas_intervalo_regular` (`test_calculo_tomas.py`):**
   * *Arrange:* Rango de 2 días (48h), inicio 08:00 AM, frecuencia cada 8 horas.
   * *Act:* Invocar `calcular_horarios_tomas(...)`.
   * *Assert:* Retorna exactamente 6 timestamps espaciados uniformemente por 8 horas.

### B. Servicios ORM e Integración (`tests/integration/`)
6. **[B-I1] `test_creacion_medicamento_service` (`test_medicamento_service.py`):** Persistencia en SQLite con campos clínicos.
7. **[B-I2] `test_creacion_medicamento_nombre_duplicado` (`test_medicamento_service.py`):** Lanza `ValueError` ante nombres repetidos.
8. **[B-I3] `test_listar_medicamentos_orden_alfabetico` (`test_medicamento_service.py`):** Retorno de catálogo ordenado.
9. **[B-I4] `test_obtener_medicamento_por_id_inexistente` (`test_medicamento_service.py`):** Retorna `None` al no encontrar el ID.
10. **[B-I5] `test_crear_tratamiento_exitoso_genera_tomas` (`test_tratamiento_service.py`):** Prescripción autogenera tomas pendientes.
11. **[B-I6] `test_crear_tratamiento_paciente_inexistente` (`test_tratamiento_service.py`):** Lanza `ValueError` al fallar FK paciente.
12. **[B-I7] `test_crear_tratamiento_medicamento_inexistente` (`test_tratamiento_service.py`):** Lanza `ValueError` al fallar FK fármaco.
13. **[B-I8] `test_crear_tratamiento_fechas_o_frecuencia_invalidas` (`test_tratamiento_service.py`):** Valida coherencia cronológica y frecuencia `> 0`.
14. **[B-I9] `test_obtener_tratamientos_por_paciente` (`test_tratamiento_service.py`):** Retorna historial completo del paciente.
15. **[B-I10] `test_eliminar_tratamiento_exitoso_y_en_cascada` (`test_tratamiento_service.py`):** Borra el tratamiento y elimina en cascada todas sus tomas asociadas.
16. **[B-I11] `test_marcar_toma_como_tomada_exitoso` (`test_marcar_toma.py`):** Actualiza estado a `tomada` y asigna `fecha_hora_toma`.
17. **[B-I12] `test_marcar_toma_estado_invalido_lanza_error` (`test_marcar_toma.py`):** Rechaza estados no autorizados con `ValueError`.
18. **[B-I13] `test_generacion_tomas_exactitud_fechas` (`test_generacion_tomas.py`):** Comprueba consistencia matemática del generador.
19. **[B-I14] `test_modelo_medicamento_to_dict` (`test_medicamento.py`):** Serialización de entidad Medicamento a JSON.
20. **[B-I15] `test_modelo_tratamiento_to_dict` (`test_tratamiento.py`):** Serialización de Tratamiento y relaciones.
21. **[B-I16] `test_modelo_registro_toma_to_dict` (`test_registro_toma.py`):** Serialización de toma individual.

### C. Endpoints y Controladores HTTP REST (`tests/integration/`)
22. **[B-R1] `test_post_medicamentos_201_creado` (`test_medicamento_routes.py`):** `POST /api/medicamentos` retorna 201 y recurso creado.
23. **[B-R2] `test_post_medicamentos_faltan_campos_400` (`test_medicamento_routes.py`):** `POST` sin campos requeridos retorna 400.
24. **[B-R3] `test_get_medicamentos_lista_200` (`test_medicamento_routes.py`):** `GET /api/medicamentos` retorna array de fármacos.
25. **[B-R4] `test_post_tratamientos_201_con_tomas` (`test_tratamiento_routes.py`):** `POST /api/tratamientos` retorna 201 y total de tomas creadas.
26. **[B-R5] `test_post_tratamientos_datos_invalidos_400` (`test_tratamiento_routes.py`):** `POST` con payload inválido retorna 400.
27. **[B-R6] `test_get_tratamientos_paciente_200` (`test_tratamiento_routes.py`):** `GET /api/tratamientos/paciente/<id>` retorna lista.
28. **[B-R7] `test_delete_tratamiento_endpoint_200` (`test_tratamiento_routes.py`):** `DELETE /api/tratamientos/<id>` retorna 200 y 404 si ya no existe.
29. **[B-R8] `test_patch_marcar_toma_nuevo_estado_200` (`test_toma_routes.py`):** `PATCH /api/tomas/<id>` con `nuevo_estado='tomada'` retorna 200.
30. **[B-R9] `test_patch_marcar_toma_campo_estado_200` (`test_toma_routes.py`):** `PATCH /api/tomas/<id>` con `estado='tomada'` (app móvil) retorna 200.
31. **[B-R10] `test_patch_marcar_toma_estado_invalido_400` (`test_toma_routes.py`):** `PATCH` con estado desconocido retorna 400.
32. **[B-R11] `test_get_tomas_paciente_cronologico_200` (`test_toma_routes.py`):** `GET /api/tomas/paciente/<id>` retorna agenda de dosis ordenada.

---

## 4. Catálogo de Pruebas de la App Móvil Flutter (30 Casos en Verde)

### A. Core API y Comunicación HTTP (`test/core/api/`)
33. **[F-API1] `Debe generar encabezados JSON estándar sin token` (`api_client_test.dart`):**  
    * *Arrange:* Invocación sin credenciales activas.  
    * *Act:* `ApiClient.headers()`.  
    * *Assert:* Cabecera `Content-Type: application/json` presente, sin `Authorization`.
34. **[F-API2] `Debe inyectar el encabezado Authorization cuando se proporciona un token JWT` (`api_client_test.dart`):**  
    * *Arrange:* Token JWT de sesión `"token.jwt.mock"`.  
    * *Act:* `ApiClient.headers(token: "token.jwt.mock")`.  
    * *Assert:* `Authorization: Bearer token.jwt.mock` inyectado automáticamente.
35. **[F-API3] `Las rutas de autenticación deben tener la estructura correcta` (`api_endpoints_test.dart`):**  
    * *Assert:* `login` apunta a `/api/auth/login`, `registro` a `/api/auth/registro`.
36. **[F-API4] `Las rutas parametrizadas deben inyectar los IDs correctamente` (`api_endpoints_test.dart`):**  
    * *Assert:* `tomasPaciente(6)` -> `/api/tomas/paciente/6`, `marcarToma(13)` -> `/api/tomas/13`, `eliminarTratamiento(2)` -> `/api/tratamientos/2`.

### B. Módulo de Alarmas, Notificaciones y Audio (`test/core/services/`)
37. **[F-NOT1] `Debe programar una alarma para una toma pendiente` (`notification_service_test.dart`):**  
    * *Arrange:* Toma con estado `pendiente` programada a futuro.  
    * *Act:* `programarAlarmaToma(toma)`.  
    * *Assert:* Retorna `true`, total alarmas activas incrementa a 1.
38. **[F-NOT2] `NO debe programar alarma si la toma ya fue tomada` (`notification_service_test.dart`):**  
    * *Arrange:* Toma con estado `tomada`.  
    * *Act:* `programarAlarmaToma(tomaTomada)`.  
    * *Assert:* Retorna `false`, total alarmas activas permanece en 0 (filtro inteligente).
39. **[F-NOT3] `Debe cancelar la alarma cuando la toma se confirma` (`notification_service_test.dart`):**  
    * *Arrange:* Alarma activa en memoria para toma #103.  
    * *Act:* `cancelarAlarma(103)`.  
    * *Assert:* Retorna `true`, total alarmas activas desciende a 0.
40. **[F-NOT4] `Debe posponer una alarma por 15 minutos según especificación` (`notification_service_test.dart`):**  
    * *Arrange:* Alarma agendada a las 08:00 AM.  
    * *Act:* `posponerAlarma(104, minutos: 15)`.  
    * *Assert:* Nueva hora es exactamente 08:15 AM (`+15 minutos`).
41. **[F-NOT5] `Debe sincronizar lista de tomas programando solo las pendientes` (`notification_service_test.dart`):**  
    * *Arrange:* Lista mixta con 2 dosis pendientes y 1 dosis tomada.  
    * *Act:* `sincronizarAlarmasConTomas(tomas)`.  
    * *Assert:* Total activas es 2; la tomada es ignorada.
42. **[F-NOT6] `Debe verificar permisos nativos sin lanzar excepciones` (`notification_service_test.dart`):**  
    * *Assert:* `estanNotificacionesPermitidas()` retorna tipo booleano de forma segura.
43. **[F-NOT7] `Debe solicitar permisos nativos de forma segura en tests` (`notification_service_test.dart`):**  
    * *Assert:* `solicitarPermisosNativos()` gestiona la ausencia de plugins en runtime de tests sin romperse.

### C. Utilidades y Validadores (`test/core/utils/`)
44. **[F-UT1] `Validar correo correctamente` (`utils_test.dart`):** Acepta correos válidos y rechaza entradas sin arroba o sin dominio.
45. **[F-UT2] `Validar contrasena correctamente` (`utils_test.dart`):** Exige longitud mínima de 6 caracteres.
46. **[F-UT3] `Validar campo obligatorio` (`utils_test.dart`):** Detecta cadenas vacías o espacios en blanco.
47. **[F-UT4] `Formatear fecha y hora para visualización de tomas` (`utils_test.dart`):** Convierte timestamps a formato legible (`"08:00 AM - 14 Nov"`).
48. **[F-UT5] `Detectar si una toma está vencida/retrasada` (`utils_test.dart`):** Semáforo cromático: retorna `true` si la hora programada ya pasó y la dosis no está tomada.

### D. Autenticación y Perfil (`test/features/auth/`)
49. **[F-AUT1] `Debe instanciar correctamente un UsuarioModel desde JSON con token` (`usuario_model_test.dart`):** Mapeo de `id`, `nombre`, `correo`, `rol` y `token`.
50. **[F-AUT2] `Debe serializar UsuarioModel a JSON correctamente` (`usuario_model_test.dart`):** Conversión bidireccional a Map/JSON.
51. **[F-AUT3] `Debe guardar el token y retornar UsuarioModel cuando el login es simulado con éxito` (`auth_service_test.dart`):** Persistencia en `flutter_secure_storage`.
52. **[F-AUT4] `Debe eliminar el token al cerrar sesión (logout)` (`auth_service_test.dart`):** Limpieza de llaves de sesión en el dispositivo.

### E. Módulo Cuidador (`test/features/cuidador/`)
53. **[F-CUI1] `Debe deserializar correctamente una lista de pacientes asignados` (`cuidador_service_test.dart`):** Mapea usuarios vinculados con rol paciente.

### F. Medicamentos (`test/features/medicamentos/`)
54. **[F-MED1] `Debe instanciar correctamente un MedicamentoModel desde JSON de Flask` (`medicamento_model_test.dart`):** Mapeo de campos clínicos.
55. **[F-MED2] `Debe soportar descripcion nula sin romperse` (`medicamento_model_test.dart`):** Resistencia a campos `null` devueltos por el backend.
56. **[F-MED3] `Debe deserializar correctamente una lista de medicamentos desde JSON` (`medicamento_service_test.dart`):** Conversión masiva de catálogo.

### G. Tomas y Adherencia (`test/features/tomas/`)
57. **[F-TOM1] `Debe instanciar correctamente una TomaModel desde JSON de Flask` (`toma_model_test.dart`):** Mapeo de IDs, medicamento, fecha y estado.
58. **[F-TOM2] `Debe detectar correctamente si la toma ya fue tomada` (`toma_model_test.dart`):** Evaluación de la propiedad booleana `estaTomada`.
59. **[F-TOM3] `Debe deserializar correctamente una lista de tomas en formato JSON` (`tomas_service_test.dart`):** Parseo seguro de cronograma de tomas.

### H. Tratamientos y Prescripciones (`test/features/tratamientos/`)
60. **[F-TRA1] `Debe instanciar correctamente un TratamientoModel desde JSON de Flask` (`tratamiento_model_test.dart`):** Lectura de prescripción.
61. **[F-TRA2] `Debe serializar TratamientoModel a JSON para POST /api/tratamientos` (`tratamiento_model_test.dart`):** Generación de payload exacto para Flask.
62. **[F-TRA3] `Debe deserializar correctamente una lista de tratamientos desde JSON` (`tratamiento_service_test.dart`):** Lectura de historial de recetas del paciente.

---

## 5. Comandos Oficiales de Ejecución y Validación

### Ejecutar Suite del Backend Flask (32 Pruebas):
```powershell
cd c:\Users\pacho\OneDrive\Escritorio\BackEnd_Medicent_v3
.\venv\Scripts\pytest -v
```
> **Resultado:** `32 passed, 1 warning in 2.90s` (100% Verde).

### Ejecutar Suite de la App Móvil Flutter (30 Pruebas):
```powershell
cd c:\Users\pacho\OneDrive\Escritorio\AppMovil_Medicent_v3
flutter test
```
> **Resultado:** `00:03 +30: All tests passed!` (100% Verde).

---

**Proyecto Medicent V3 • Sistema Integral de Salud • SENA 2026**  
*Documento de Calidad y Aseguramiento de Software (QA / TDD)*
