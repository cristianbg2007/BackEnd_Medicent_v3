use medicent_v3;

-- Insertar Usuarios (Valores de prueba iniciales)
INSERT INTO usuarios (nombre, correo, contrasena_hash, rol) VALUES 
("Admin", "admin@medicent.com", "admin123", "admin"),
("Paciente", "paciente@medicent.com", "paciente123", "paciente"),
("Cuidador", "cuidador@medicent.com", "cuidador123", "cuidador");

-- Insertar Pacientes_Cuidadores
INSERT INTO pacientes_cuidadores (cuidador_id, paciente_id) VALUES 
(3, 2);

-- Insertar Medicamentos
INSERT INTO medicamentos (nombre, descripcion, forma_farmaceutica) VALUES 
("Paracetamol", "Analgésico y antipirético", "Tableta"),
("Amoxicilina", "Antibiótico", "Cápsula");

-- Insertar Tratamientos
INSERT INTO tratamientos (paciente_id, medicamento_id, dosis, frecuencia_horas, fecha_inicio, fecha_fin, hora_inicial) VALUES 
(2, 1, "1 tableta", 6, "2022-01-01", "2022-01-07", "08:00:00"),
(2, 2, "1 cápsula", 8, "2022-01-01", "2022-01-07", "08:00:00");
