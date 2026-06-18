-- 1. Tabla de Convocatorias
CREATE TABLE convocatorias_convocatoria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activa BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_creacion TIMESTAMPTZ NOT NULL,
    creada_por_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL
);

-- 2. Tabla Perfil de Usuario (Extensión de auth.User)
CREATE TABLE usuarios_perfilusuario (
    id SERIAL PRIMARY KEY,
    rol VARCHAR(20) NOT NULL DEFAULT 'postulante',
    telefono VARCHAR(20) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMPTZ NOT NULL,
    user_id INTEGER UNIQUE NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE
);

-- 3. Tabla de Postulantes
CREATE TABLE postulantes_postulante (
    id SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    direccion TEXT NOT NULL,
    fecha_nacimiento DATE,
    fecha_registro TIMESTAMPTZ NOT NULL,
    datos_completos BOOLEAN NOT NULL DEFAULT FALSE,
    convocatoria_id INTEGER REFERENCES convocatorias_convocatoria(id) ON DELETE SET NULL,
    user_id INTEGER UNIQUE NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE
);
CREATE INDEX idx_postulante_cedula ON postulantes_postulante(cedula);

-- 4. Tabla de Datos Académicos
CREATE TABLE postulantes_datosacademicos (
    id SERIAL PRIMARY KEY,
    institucion VARCHAR(200) NOT NULL,
    carrera VARCHAR(200) NOT NULL,
    semestre SMALLINT NOT NULL,
    promedio NUMERIC(3, 2) NOT NULL,
    creditos_aprobados INTEGER NOT NULL,
    creditos_totales INTEGER NOT NULL DEFAULT 0,
    postulante_id INTEGER UNIQUE NOT NULL REFERENCES postulantes_postulante(id) ON DELETE CASCADE
);

-- 5. Tabla de Datos Socioeconómicos
CREATE TABLE postulantes_datossocioeconomicos (
    id SERIAL PRIMARY KEY,
    ingreso_familiar NUMERIC(12, 2) NOT NULL,
    estrato SMALLINT NOT NULL,
    num_hermanos_universidad SMALLINT NOT NULL DEFAULT 0,
    tipo_vivienda VARCHAR(20) NOT NULL DEFAULT 'arrendada',
    trabaja BOOLEAN NOT NULL DEFAULT FALSE,
    numero_personas_hogar SMALLINT NOT NULL DEFAULT 1,
    es_cabeza_hogar BOOLEAN NOT NULL DEFAULT FALSE,
    postulante_id INTEGER UNIQUE NOT NULL REFERENCES postulantes_postulante(id) ON DELETE CASCADE
);

-- 6. Tabla de Evaluaciones
CREATE TABLE evaluaciones_evaluacion (
    id SERIAL PRIMARY KEY,
    puntaje_academico NUMERIC(6, 2) NOT NULL DEFAULT 0,
    puntaje_socioeconomico NUMERIC(6, 2) NOT NULL DEFAULT 0,
    puntaje_total NUMERIC(6, 2) NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    observaciones TEXT NOT NULL,
    fecha_evaluacion TIMESTAMPTZ,
    convocatoria_id INTEGER REFERENCES convocatorias_convocatoria(id) ON DELETE SET NULL,
    evaluado_por_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    postulante_id INTEGER UNIQUE NOT NULL REFERENCES postulantes_postulante(id) ON DELETE CASCADE
);
CREATE INDEX idx_evaluacion_estado_puntaje ON evaluaciones_evaluacion(estado, puntaje_total);

-- 7. Tabla de Parámetros de Beca
CREATE TABLE parametros_parametrobeca (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    valor NUMERIC(15, 4) NOT NULL,
    descripcion TEXT NOT NULL,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_modificacion TIMESTAMPTZ NOT NULL,
    modificado_por_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL
);
CREATE INDEX idx_parametro_nombre ON parametros_parametrobeca(nombre);

-- 8. Tabla de Logs de Auditoría
CREATE TABLE usuarios_logaccion (
    id SERIAL PRIMARY KEY,
    accion VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    detalles JSONB NOT NULL DEFAULT '{}'::jsonb,
    ip_address INET,
    objeto_id INTEGER,
    objeto_tipo VARCHAR(100) NOT NULL,
    usuario_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL
);
CREATE INDEX idx_logs_usuario_timestamp ON usuarios_logaccion(usuario_id, timestamp);
CREATE INDEX idx_logs_accion_timestamp ON usuarios_logaccion(accion, timestamp);