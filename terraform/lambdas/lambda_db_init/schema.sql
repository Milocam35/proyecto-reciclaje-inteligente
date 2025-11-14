-- =========================
--  Tabla Administrador
-- =========================
CREATE TABLE Administrador (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  usuario VARCHAR(255) UNIQUE NOT NULL,
  contrasena VARCHAR(255) NOT NULL
);

-- =========================
--  Tabla Evento
-- =========================
CREATE TABLE Evento (
  id INT AUTO_INCREMENT PRIMARY KEY,
  horaClasificado DATETIME NOT NULL,
  horaSincronizado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  duracion FLOAT NOT NULL CHECK (duracion >= 0),
  rutaImagen VARCHAR(255) DEFAULT NULL,
  tipoClasificado ENUM('reciclable', 'noReciclable', 'organico') NOT NULL,
  tipoReal ENUM('noRevisado', 'reciclable', 'noReciclable', 'organico') 
            NOT NULL DEFAULT 'noRevisado' COMMENT 'Estado de la clasificación real',
  admin_id INT DEFAULT NULL,
  confianza FLOAT DEFAULT NULL CHECK (confianza >= 0 AND confianza <= 1),
  CONSTRAINT fk_evento_admin FOREIGN KEY (admin_id) 
    REFERENCES Administrador(id)
    ON DELETE SET NULL 
    ON UPDATE CASCADE,
  INDEX (tipoClasificado),
  INDEX (tipoReal),
  INDEX (horaSincronizado)
);

-- =========================
--  Tabla Notificaciones
-- =========================
CREATE TABLE Notificaciones (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tipo ENUM('success', 'error') NOT NULL,
  mensaje VARCHAR(255) NOT NULL,
  origen VARCHAR(100),
  evento_id INT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_notificacion_evento FOREIGN KEY (evento_id)
    REFERENCES Evento(id)
    ON DELETE CASCADE,
  INDEX (tipo),
  INDEX (fecha)
);

-- =========================
--  Tabla Estadistica
-- =========================
CREATE TABLE Estadistica (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fn FLOAT DEFAULT NULL,
  fp FLOAT DEFAULT NULL,
  vn FLOAT DEFAULT NULL,
  vp FLOAT DEFAULT NULL,
  precision_global FLOAT DEFAULT NULL CHECK (precision_global >= 0 AND precision_global <= 1),
  recall FLOAT DEFAULT NULL CHECK (recall >= 0 AND recall <= 1),
  f1_score FLOAT DEFAULT NULL CHECK (f1_score >= 0 AND f1_score <= 1),
  auc FLOAT DEFAULT NULL CHECK (auc >= 0 AND auc <= 1),
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
