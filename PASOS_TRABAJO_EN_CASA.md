# 📋 Guía de Trabajo en Casa: Medicent Backend V3
**Desarrollador:** Andrés (Módulo Clínico y Motor de Tomas)  
**Proyecto:** `Backend_Medicent_v3`  
**Fecha:** Octubre 2026  

---

## 📍 1. ¿Dónde Quedamos Hoy? (Estado Actual)

1. **Base de Datos y Migraciones:**
   - La base de datos `medicent_v3` está creada en MySQL Workbench.
   - Flask-Migrate está configurado (`flask db init`).
   - Se creó y migró exitosamente la tabla **`medicamentos`** a MySQL Workbench (`app/models/medicamento.py`).
2. **Entorno de Pruebas (TDD):**
   - Se configuró `TestConfig` con SQLite en memoria (`sqlite:///:memory:`).
   - Se configuró la base de pruebas en `tests/base_test.py`.
   - El archivo `tests/test_modelos.py` está creado y listo para escribir la primera prueba.
3. **Control de Versiones (Git):**
   - Estás en la rama de trabajo: `feature/tratamientos-tomas`.
   - Tienes cambios locales pendientes de guardar en Git.

---

## 💾 2. ANTES DE APAGAR TU PC HOY: Guardar tu trabajo en GitHub

Para que no pierdas nada y puedas clonar o continuar en tu casa con total seguridad:

Abre tu terminal en `Backend_Medicent_v3` y corre estos 3 comandos:

```bash
# 1. Agregar todos los archivos nuevos y modificados
git add .

# 2. Hacer el commit registrando el avance del día
git commit -m "feat(clinico): configurar migraciones, modelo medicamento y base de pruebas TDD

- Migracion inicial de tabla medicamentos
- Configuracion de BaseTestCase con SQLite en memoria

Co-authored-by: Cristian <cristianbg2007@github.com>
Co-authored-by: Andres <tu_correo@medicent.com>"

# 3. Subir tu rama a GitHub
git push -u origin feature/tratamientos-tomas
```

---

## 🏠 3. CUANDO LLEGUES A TU CASA: ¿Cómo empezar?

### Si trabajas en otra computadora en tu casa:
1. Clona el repositorio:
   ```bash
   git clone https://github.com/cristianbg2007/BackEnd_Medicent_v3.git
   cd BackEnd_Medicent_v3
   ```
2. Cambia a tu rama de trabajo:
   ```bash
   git checkout feature/tratamientos-tomas
   ```
3. Crea tu archivo `.env` en la raíz (con tu usuario y clave local de MySQL):
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   DATABASE_URL=mysql+pymysql://root:TU_PASSWORD@localhost:3306/medicent_v3
   ```
4. Instala las dependencias:
   ```bash
   py -m pip install -r requirements.txt
   ```

---

## 🎯 4. Tu Lista de Tareas Paso a Paso en Casa (Roadmap)

### Paso 1: Escribir la Primera Prueba Unitaria en `tests/test_modelos.py`
Abre `tests/test_modelos.py` y pega la prueba del modelo `Medicamento`:

```python
from tests.base_test import BaseTestCase
from app.models.medicamento import Medicamento
from app.database.connection import db

class TestModelosClinicos(BaseTestCase):

    def test_creacion_modelo_medicamento(self):
        """Prueba que un Medicamento se cree en BD y devuelva to_dict()"""
        # 1. Preparar (Arrange)
        nuevo_medicamento = Medicamento(
            nombre="Paracetamol",
            descripcion="Analgésico y antipirético",
            forma_farmaceutica="Comprimido 500mg"
        )

        # 2. Actuar (Act)
        db.session.add(nuevo_medicamento)
        db.session.commit()

        # 3. Verificar (Assert)
        medicamento_guardado = Medicamento.query.filter_by(nombre="Paracetamol").first()
        self.assertIsNotNone(medicamento_guardado)
        self.assertEqual(medicamento_guardado.forma_farmaceutica, "Comprimido 500mg")
        
        datos_dict = medicamento_guardado.to_dict()
        self.assertEqual(datos_dict["nombre"], "Paracetamol")
```

Ejecuta el comando en terminal:
```bash
py -m unittest discover -s tests -p "test_*.py"
```
👉 **Meta:** Debe salir `Ran 1 test ... OK` en verde.

---

### Paso 2: Crear el Modelo `Tratamiento` (`app/models/tratamiento.py`)
Según el diagrama relacional, representa la prescripción médica:
- `id` (INT, PK)
- `paciente_id` (INT, FK -> usuarios.id)
- `medicamento_id` (INT, FK -> medicamentos.id)
- `dosis` (VARCHAR(100))
- `frecuencia_horas` (INT)
- `fecha_inicio` (DATE)
- `fecha_fin` (DATE)
- `hora_inicial` (TIME)
- `instrucciones` (TEXT)
- `esta_activo` (BOOLEAN / TINYINT)
- `creado_en` (TIMESTAMP)

---

### Paso 3: Crear el Modelo `RegistroToma` (`app/models/registro_toma.py`)
Controla el seguimiento de cada toma individual:
- `id` (BIGINT, PK)
- `tratamiento_id` (INT, FK -> tratamientos.id)
- `fecha_hora_programada` (DATETIME)
- `fecha_hora_toma` (DATETIME, nullable)
- `estado` (ENUM: `'pendiente'`, `'tomada'`, `'omitida'`, `'retrasada'`)
- `notas` (VARCHAR(255), nullable)
- `creado_en` (TIMESTAMP)

---

### Paso 4: Migrar las nuevas tablas a MySQL Workbench
Cada vez que crees o modifiques modelos, en tu terminal ejecutas:
```bash
py -m flask db migrate -m "crear tablas tratamientos y tomas"
py -m flask db upgrade
```

---

## 📌 Documentos de Referencia en tu Proyecto
Tienes toda la arquitectura y el diseño en tu carpeta `documentos/`:
- `documentos/Arbol_Estructura_Archivos_Medicent_V3.pdf` (nombres exactos de carpetas y archivos).
- `documentos/Listado_Oficial_de_Pruebas_TDD_Medicent_V3.pdf` (todas las pruebas explicadas).
- `documentos/diagrama_relacional.png` (imagen de las 5 tablas).
