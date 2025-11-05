CREATE TABLE `Evento` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `horaClasificado` datetime NOT NULL,
  `horaSincronizado` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `duracion` float NOT NULL,
  `rutaImagen` varchar(255),
  `tipoClasificado` ENUM ('reciclable', 'noReciclable', 'organico') NOT NULL,
  `tipoReal` ENUM ('noRevisado', 'reciclable', 'noReciclable', 'organico') NOT NULL DEFAULT 'noRevisado' COMMENT 'Estado de la 		clasificación real',
  `admin_id` int DEFAULT null,
  `confianza` float DEFAULT null
);

CREATE TABLE `Error` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `hora` datetime NOT NULL,
  `fuente` varchar(255) NOT NULL,
  `mensaje` varchar(255) NOT NULL,
  `evento_id` int UNIQUE
);

CREATE TABLE `Administrador` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `usuario` varchar(255) UNIQUE NOT NULL,
  `contrasena` varchar(255) NOT NULL
);

CREATE TABLE `Estadistica` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `fn` float DEFAULT null,
  `fp` float DEFAULT null,
  `vn` float DEFAULT null,
  `vp` float DEFAULT null,
  `precision_global` float DEFAULT null,
  `recall` float DEFAULT null,
  `f1_score` float DEFAULT null,
  `auc` float DEFAULT null,
  `fecha_creacion` DATETIME DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `Error` ADD FOREIGN KEY (`evento_id`) REFERENCES `Evento` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Evento` ADD FOREIGN KEY (`admin_id`) REFERENCES `Administrador` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
