CREATE DATABASE IF NOT EXISTS desercion_escolar_ia;
USE desercion_escolar_ia;


CREATE TABLE estudiantes (

    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,

    nombres VARCHAR(100),

    apellidos VARCHAR(100),

    curso VARCHAR(50),

    edad INT,

    genero VARCHAR(20),

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


CREATE TABLE datos_sociales (

    id_social INT AUTO_INCREMENT PRIMARY KEY,

    id_estudiante INT,

    apoyo_familiar ENUM(
        'si',
        'no'
    ),

    situacion_economica ENUM(
        'baja',
        'media',
        'alta'
    ),

    acceso_internet ENUM(
        'si',
        'no'
    ),

    FOREIGN KEY (id_estudiante)
    REFERENCES estudiantes(id_estudiante)

);

ELECT * FROM estudiantes;

-- VER DATOS SOCIALES



SELECT * FROM datos_sociales;

-- VER RENDIMIENTO
