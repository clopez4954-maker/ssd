-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-06-2026 a las 03:19:23
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ssd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Postulante');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Solicitud de Verificación', 7, 'add_solicitudverificacion'),
(26, 'Can change Solicitud de Verificación', 7, 'change_solicitudverificacion'),
(27, 'Can delete Solicitud de Verificación', 7, 'delete_solicitudverificacion'),
(28, 'Can view Solicitud de Verificación', 7, 'view_solicitudverificacion'),
(29, 'Can add Perfil de Usuario', 8, 'add_perfilusuario'),
(30, 'Can change Perfil de Usuario', 8, 'change_perfilusuario'),
(31, 'Can delete Perfil de Usuario', 8, 'delete_perfilusuario'),
(32, 'Can view Perfil de Usuario', 8, 'view_perfilusuario'),
(33, 'Can add Log de Acción', 9, 'add_logaccion'),
(34, 'Can change Log de Acción', 9, 'change_logaccion'),
(35, 'Can delete Log de Acción', 9, 'delete_logaccion'),
(36, 'Can view Log de Acción', 9, 'view_logaccion'),
(37, 'Can add Convocatoria', 10, 'add_convocatoria'),
(38, 'Can change Convocatoria', 10, 'change_convocatoria'),
(39, 'Can delete Convocatoria', 10, 'delete_convocatoria'),
(40, 'Can view Convocatoria', 10, 'view_convocatoria'),
(41, 'Can add Postulante', 11, 'add_postulante'),
(42, 'Can change Postulante', 11, 'change_postulante'),
(43, 'Can delete Postulante', 11, 'delete_postulante'),
(44, 'Can view Postulante', 11, 'view_postulante'),
(45, 'Can add Ficha Socioeconómica', 12, 'add_fichasocioeconomica'),
(46, 'Can change Ficha Socioeconómica', 12, 'change_fichasocioeconomica'),
(47, 'Can delete Ficha Socioeconómica', 12, 'delete_fichasocioeconomica'),
(48, 'Can view Ficha Socioeconómica', 12, 'view_fichasocioeconomica'),
(49, 'Can add Parámetro de Beca', 13, 'add_parametrobeca'),
(50, 'Can change Parámetro de Beca', 13, 'change_parametrobeca'),
(51, 'Can delete Parámetro de Beca', 13, 'delete_parametrobeca'),
(52, 'Can view Parámetro de Beca', 13, 'view_parametrobeca'),
(53, 'Can add Evaluación', 14, 'add_evaluacion'),
(54, 'Can change Evaluación', 14, 'change_evaluacion'),
(55, 'Can delete Evaluación', 14, 'delete_evaluacion'),
(56, 'Can view Evaluación', 14, 'view_evaluacion'),
(57, 'Can add Miembro Familiar', 15, 'add_miembrofamiliar'),
(58, 'Can change Miembro Familiar', 15, 'change_miembrofamiliar'),
(59, 'Can delete Miembro Familiar', 15, 'delete_miembrofamiliar'),
(60, 'Can view Miembro Familiar', 15, 'view_miembrofamiliar'),
(61, 'Can add Datos Académicos', 16, 'add_datosacademicos'),
(62, 'Can change Datos Académicos', 16, 'change_datosacademicos'),
(63, 'Can delete Datos Académicos', 16, 'delete_datosacademicos'),
(64, 'Can view Datos Académicos', 16, 'view_datosacademicos'),
(65, 'Can add Solicitud de Beca', 17, 'add_solicitudbeca'),
(66, 'Can change Solicitud de Beca', 17, 'change_solicitudbeca'),
(67, 'Can delete Solicitud de Beca', 17, 'delete_solicitudbeca'),
(68, 'Can view Solicitud de Beca', 17, 'view_solicitudbeca'),
(69, 'Can add Rango de Materias', 18, 'add_rangomaterias'),
(70, 'Can change Rango de Materias', 18, 'change_rangomaterias'),
(71, 'Can delete Rango de Materias', 18, 'delete_rangomaterias'),
(72, 'Can view Rango de Materias', 18, 'view_rangomaterias'),
(73, 'Can add Rango de PPS', 19, 'add_rangopps'),
(74, 'Can change Rango de PPS', 19, 'change_rangopps'),
(75, 'Can delete Rango de PPS', 19, 'delete_rangopps'),
(76, 'Can view Rango de PPS', 19, 'view_rangopps'),
(77, 'Can add Regla de Desempate', 20, 'add_regladesempate'),
(78, 'Can change Regla de Desempate', 20, 'change_regladesempate'),
(79, 'Can delete Regla de Desempate', 20, 'delete_regladesempate'),
(80, 'Can view Regla de Desempate', 20, 'view_regladesempate'),
(81, 'Can add Opción Socioeconómica', 21, 'add_opcionsocioeconomica'),
(82, 'Can change Opción Socioeconómica', 21, 'change_opcionsocioeconomica'),
(83, 'Can delete Opción Socioeconómica', 21, 'delete_opcionsocioeconomica'),
(84, 'Can view Opción Socioeconómica', 21, 'view_opcionsocioeconomica'),
(85, 'Can add Materia Cursada', 22, 'add_materiasemestre'),
(86, 'Can change Materia Cursada', 22, 'change_materiasemestre'),
(87, 'Can delete Materia Cursada', 22, 'delete_materiasemestre'),
(88, 'Can view Materia Cursada', 22, 'view_materiasemestre');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$720000$8vHuQffVz1k9FGEOjyX8MS$2f4ItGqnmsSB1gdC1rkAliXwtAy8N0Ms8Ok3AU9pi+o=', '2026-06-17 20:18:55.064687', 1, 'admin', 'Admin', 'Sistema', 'admin@becasuni.edu.co', 1, 1, '2026-06-12 04:27:57.371912'),
(2, 'pbkdf2_sha256$720000$hF4ZBMQ5jBINxHB5Y6WL1Y$sFfsTkx2kv4xkcAkjdiPEzbknzLL4o6AYulnjIt86Ls=', '2026-06-17 20:23:01.140472', 0, 'evaluador', 'Juan', 'Pérez', 'evaluador@becasuni.edu.co', 0, 1, '2026-06-12 04:27:58.402206'),
(3, 'pbkdf2_sha256$720000$yhk9y3nHECIBLA09c1kwln$rErupyqe9PEiV4u3pf/EX1+OP+ETihlizmfm6GYN8wM=', '2026-06-17 19:09:19.492451', 0, 'postulante1', 'María', 'Gómez', 'maria.gomez@becasuni.edu.co', 0, 1, '2026-06-12 04:27:59.471900'),
(4, 'pbkdf2_sha256$720000$VlZnGOQpclIvIg6uKjlTgv$Yx7gDb3D/InzBgKNYpe9tH3D0vvaj8H6voaZmvN/UDU=', '2026-06-12 21:04:38.161216', 0, 'postulante2', 'Carlos', 'Rodríguez', 'carlos.rodriguez@becasuni.edu.co', 0, 1, '2026-06-12 04:28:00.652780'),
(5, 'pbkdf2_sha256$720000$eK928gUlURbcd4Be6gm0z8$OtOqi6Z1Eaio1LtwLzMb0zE8gds8M3ODxGLUEzF7JvU=', '2026-06-17 03:13:39.497358', 0, 'postulante3', 'Laura', 'Castro', 'laura.castro@becasuni.edu.co', 0, 1, '2026-06-12 04:28:01.740008'),
(6, 'pbkdf2_sha256$720000$YaStn7rlHwqNx4R0bkDtzE$WdFCkRmWDkNkSHLU5tMwKbE/YjieUT4zpRvide3qZok=', NULL, 0, '13176943', 'Camilo', 'Lopez', 'clopez4954@gmail.com', 0, 1, '2026-06-12 18:19:20.914243'),
(7, 'pbkdf2_sha256$720000$kd54dilKjzG1YRi7iXjUNx$xy/jM8kLRdTbpJQ3ypVj57/H1bC5NCb6Cwqfd2/Bv0w=', NULL, 0, '11327216', 'Yeison', 'Vargas', 'yeisonvargas778@gmail.com', 0, 1, '2026-06-12 18:19:48.078440'),
(8, 'pbkdf2_sha256$720000$WGdodaV352bafcIc1cHYo0$77+220Fj+m7vZSvkx2UIaBno6tV7ootLqvlsZa7x638=', NULL, 0, '11327217', 'Leonel', 'Vargas', 'yevargasu778@gmail.com', 0, 1, '2026-06-12 18:38:09.245251'),
(9, 'pbkdf2_sha256$720000$odGvmR00iSBrd4fiwSFpZu$suXw+qux6f4ouU1zFjfu+oAA3G0vvjT+xM9dsZqAlNg=', '2026-06-17 20:16:34.123245', 0, '221185550', 'Yeison Leonel', 'Ayzacayo Vargas', 'leonel@gmail.com', 0, 1, '2026-06-17 20:12:29.647068');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 6, 1),
(2, 7, 1),
(3, 8, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `convocatorias_convocatoria`
--

CREATE TABLE `convocatorias_convocatoria` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `activa` tinyint(1) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `creada_por_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `convocatorias_convocatoria`
--

INSERT INTO `convocatorias_convocatoria` (`id`, `nombre`, `descripcion`, `fecha_inicio`, `fecha_fin`, `activa`, `fecha_creacion`, `creada_por_id`) VALUES
(1, 'Convocatoria Becas 2026-II', 'Programa de becas de matrícula para el segundo semestre del año 2026.', '2026-06-12', '2026-07-12', 1, '2026-06-12 04:27:59.464871', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(10, 'convocatorias', 'convocatoria'),
(14, 'evaluaciones', 'evaluacion'),
(21, 'parametros', 'opcionsocioeconomica'),
(13, 'parametros', 'parametrobeca'),
(18, 'parametros', 'rangomaterias'),
(19, 'parametros', 'rangopps'),
(20, 'parametros', 'regladesempate'),
(16, 'postulantes', 'datosacademicos'),
(12, 'postulantes', 'fichasocioeconomica'),
(22, 'postulantes', 'materiasemestre'),
(15, 'postulantes', 'miembrofamiliar'),
(11, 'postulantes', 'postulante'),
(17, 'postulantes', 'solicitudbeca'),
(6, 'sessions', 'session'),
(9, 'usuarios', 'logaccion'),
(8, 'usuarios', 'perfilusuario'),
(7, 'usuarios', 'solicitudverificacion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-06-12 04:27:43.729884'),
(2, 'auth', '0001_initial', '2026-06-12 04:27:44.580504'),
(3, 'admin', '0001_initial', '2026-06-12 04:27:44.819062'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-06-12 04:27:44.847522'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-06-12 04:27:44.869407'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-06-12 04:27:45.000157'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-06-12 04:27:45.097011'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-06-12 04:27:45.128378'),
(9, 'auth', '0004_alter_user_username_opts', '2026-06-12 04:27:45.144181'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-06-12 04:27:45.227934'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-06-12 04:27:45.231566'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-06-12 04:27:45.253579'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-06-12 04:27:45.283023'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-06-12 04:27:45.313531'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-06-12 04:27:45.349425'),
(16, 'auth', '0011_update_proxy_permissions', '2026-06-12 04:27:45.378093'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-06-12 04:27:45.417563'),
(18, 'convocatorias', '0001_initial', '2026-06-12 04:27:45.561527'),
(19, 'postulantes', '0001_initial', '2026-06-12 04:27:46.019445'),
(20, 'evaluaciones', '0001_initial', '2026-06-12 04:27:46.435088'),
(21, 'parametros', '0001_initial', '2026-06-12 04:27:46.623919'),
(22, 'sessions', '0001_initial', '2026-06-12 04:27:46.707132'),
(23, 'usuarios', '0001_initial', '2026-06-12 04:27:47.143411'),
(24, 'usuarios', '0002_solicitudverificacion_boleta_inscripcion_and_more', '2026-06-12 04:51:04.197581'),
(25, 'postulantes', '0002_remove_fichasocioeconomica_comprobante_ingresos_and_more', '2026-06-12 15:14:57.428104'),
(26, 'postulantes', '0003_fichasocioeconomica_infra_descripcion', '2026-06-12 15:39:15.185914'),
(27, 'postulantes', '0004_postulante_archivo_boleta_inscripcion_and_more', '2026-06-12 16:52:27.213057'),
(28, 'parametros', '0002_rangomaterias_rangopps_regladesempate_and_more', '2026-06-12 17:42:23.790121'),
(29, 'postulantes', '0005_datosacademicos_solicitudbeca_and_more', '2026-06-12 17:42:25.853217'),
(30, 'usuarios', '0003_alter_solicitudverificacion_comprobante_matricula_and_more', '2026-06-12 17:55:34.791543'),
(31, 'postulantes', '0006_fichasocioeconomica_archivo_boleta_inscripcion_and_more', '2026-06-12 18:50:08.484700'),
(32, 'postulantes', '0007_rename_pps_datosacademicos_ppa_materiasemestre', '2026-06-17 01:04:35.206869'),
(33, 'postulantes', '0008_datosacademicos_certificado_notas_pdf', '2026-06-17 01:14:24.405698'),
(34, 'postulantes', '0009_datosacademicos_puntaje_academico_total_and_more', '2026-06-17 01:32:52.230771'),
(35, 'postulantes', '0010_solicitudbeca_fecha_revision_and_more', '2026-06-17 02:16:17.977897'),
(36, 'postulantes', '0011_solicitudbeca_fecha_rechazo_and_more', '2026-06-17 02:25:48.260907'),
(37, 'postulantes', '0012_alter_fichasocioeconomica_ocupacion', '2026-06-17 03:18:03.975896'),
(38, 'postulantes', '0013_remove_fichasocioeconomica_discapacidad', '2026-06-17 15:47:57.663637'),
(39, 'postulantes', '0014_remove_postulante_solicitud_verificacion_and_more', '2026-06-17 19:29:42.904823'),
(40, 'usuarios', '0004_delete_solicitudverificacion', '2026-06-17 19:29:42.915784');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('354r9725to7p251fsmc782dl9x5xkgkv', '.eJxVjLsKwzAMAP9FczFWJPzI2L3fEGTLrtOWBPKYSv-9BDK0691xbxhk39qwr2UZRoUeCC6_LEl-lukQ-pDpPps8T9syJnMk5rSruc1aXtez_Rs0WRv04DlbwqCsojZKx5GQfUbsqBZxhMlTDII1dIyRa3XFek1sXSCkkuHzBcL0Nwg:1wY7JP:FOFDQU_Dvn7UTN8lqzlNxY-jXIaGY1wERAyeW7hXMrQ', '2026-06-26 19:13:03.492206'),
('v26x1ippxd9tgupol092eqpvf4kdguee', '.eJxVzMsKwjAQheF3mbWEZpqQSZfufYYyuYypSgK9rMR3l0AXuj3_x3nDzMde5mPL67wkmEDD5XcLHJ-59pAeXO9NxVb3dQmqE3XWTd1ayq_raf8OCm8FJhBkE0IWstFEGaJ2SKPTEg0ROiTywmQYxXq2OXVus8c0JPTeywifL_YQOCA:1wXuIU:IDp1Pp-yklSDPIv-f3yvTJYYyqw1Rnqdvb4kK-kVaTE', '2026-06-26 05:19:14.190254');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evaluaciones_evaluacion`
--

CREATE TABLE `evaluaciones_evaluacion` (
  `id` bigint(20) NOT NULL,
  `puntaje_academico` decimal(6,2) NOT NULL,
  `puntaje_socioeconomico` decimal(6,2) NOT NULL,
  `puntaje_total` decimal(6,2) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `observaciones` longtext NOT NULL,
  `fecha_evaluacion` datetime(6) DEFAULT NULL,
  `convocatoria_id` bigint(20) DEFAULT NULL,
  `evaluado_por_id` int(11) DEFAULT NULL,
  `postulante_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `evaluaciones_evaluacion`
--

INSERT INTO `evaluaciones_evaluacion` (`id`, `puntaje_academico`, `puntaje_socioeconomico`, `puntaje_total`, `estado`, `observaciones`, `fecha_evaluacion`, `convocatoria_id`, `evaluado_por_id`, `postulante_id`) VALUES
(1, 10.00, 65.00, 75.00, 'pendiente', '', '2026-06-17 02:10:41.732781', 1, 2, 1),
(2, 0.00, 66.00, 66.00, 'pendiente', '', '2026-06-12 21:16:54.056338', 1, 2, 2),
(3, 10.00, 2.00, 12.00, 'pendiente', '', '2026-06-17 02:20:28.265112', 1, 2, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametros_opcionsocioeconomica`
--

CREATE TABLE `parametros_opcionsocioeconomica` (
  `id` bigint(20) NOT NULL,
  `variable` varchar(50) NOT NULL,
  `opcion_texto` varchar(200) NOT NULL,
  `puntaje` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `parametros_opcionsocioeconomica`
--

INSERT INTO `parametros_opcionsocioeconomica` (`id`, `variable`, `opcion_texto`, `puntaje`) VALUES
(1, 'dependencia', 'Ambos padres', 5),
(2, 'dependencia', 'Pareja', 6),
(3, 'dependencia', 'Otro familiar', 8),
(4, 'dependencia', 'Solo padre o madre', 9),
(5, 'dependencia', 'Independiente', 10),
(6, 'ocupacion', 'Comerciante mayorista', 6),
(7, 'ocupacion', 'Asalariado formal', 7),
(8, 'ocupacion', 'Rentista', 8),
(9, 'ocupacion', 'Asalariado informal', 9),
(10, 'ocupacion', 'Comerciante minorista', 10),
(11, 'ocupacion', 'Agricultor', 10),
(12, 'rango_ingresos', 'Más de 6000 Bs.', 7),
(13, 'rango_ingresos', 'De 4001 a 6000 Bs.', 8),
(14, 'rango_ingresos', 'De 2501 a 4000 Bs.', 9),
(15, 'rango_ingresos', 'Hasta 2500 Bs.', 10),
(16, 'num_integrantes', 'Hasta 1 miembro', 2),
(17, 'num_integrantes', 'De 2 a 3 miembros', 3),
(18, 'num_integrantes', 'De 3 a 4 miembros', 4),
(19, 'num_integrantes', 'Más de 4 miembros', 5),
(20, 'num_hijos', 'Sin hijos', 0),
(21, 'num_hijos', '1 hijo', 4),
(22, 'num_hijos', 'Más de 1 hijo', 5),
(23, 'lugar_residencia', 'Hasta el segundo anillo', 2),
(24, 'lugar_residencia', 'Fuera del 2do anillo', 5),
(25, 'tenencia_vivienda', 'Por herencia', 2),
(26, 'tenencia_vivienda', 'De los padres', 2),
(27, 'tenencia_vivienda', 'Cedida por terceros', 3),
(28, 'tenencia_vivienda', 'Anticrético', 4),
(29, 'tenencia_vivienda', 'Alquiler', 5),
(30, 'tipo_vivienda', 'Casa', 2),
(31, 'tipo_vivienda', 'Departamento', 2),
(32, 'tipo_vivienda', 'Más de 4 hab.', 3),
(33, 'tipo_vivienda', 'Más de 2 hab.', 4),
(34, 'tipo_vivienda', '1 habitación o pieza', 5),
(35, 'procedencia', 'Ciudad', 13),
(36, 'procedencia', 'Otro departamento', 14),
(37, 'procedencia', 'Provincia', 15);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametros_parametrobeca`
--

CREATE TABLE `parametros_parametrobeca` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `valor` decimal(15,4) NOT NULL,
  `descripcion` longtext NOT NULL,
  `vigente` tinyint(1) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `modificado_por_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `parametros_parametrobeca`
--

INSERT INTO `parametros_parametrobeca` (`id`, `nombre`, `valor`, `descripcion`, `vigente`, `fecha_modificacion`, `modificado_por_id`) VALUES
(1, 'cupos_disponibles', 5.0000, 'Cantidad máxima de becas a asignar', 1, '2026-06-12 20:37:43.330526', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametros_rangomaterias`
--

CREATE TABLE `parametros_rangomaterias` (
  `id` bigint(20) NOT NULL,
  `desde` int(11) NOT NULL,
  `hasta` int(11) DEFAULT NULL,
  `puntaje` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `parametros_rangomaterias`
--

INSERT INTO `parametros_rangomaterias` (`id`, `desde`, `hasta`, `puntaje`) VALUES
(1, 6, NULL, 5),
(2, 4, 5, 4),
(3, 2, 3, 3),
(4, 1, 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametros_rangopps`
--

CREATE TABLE `parametros_rangopps` (
  `id` bigint(20) NOT NULL,
  `desde` double NOT NULL,
  `hasta` double NOT NULL,
  `puntaje` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `parametros_rangopps`
--

INSERT INTO `parametros_rangopps` (`id`, `desde`, `hasta`, `puntaje`) VALUES
(1, 60, 100, 25),
(2, 46, 59.99, 20),
(3, 32, 45.99, 15),
(4, 0, 31.99, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametros_regladesempate`
--

CREATE TABLE `parametros_regladesempate` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `campo_modelo` varchar(100) NOT NULL,
  `orden_ejecucion` int(10) UNSIGNED NOT NULL CHECK (`orden_ejecucion` >= 0),
  `direccion` varchar(10) NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `parametros_regladesempate`
--

INSERT INTO `parametros_regladesempate` (`id`, `nombre`, `campo_modelo`, `orden_ejecucion`, `direccion`, `activo`) VALUES
(1, 'Sin otro beneficio universitario', 'postulante__ficha_socioeconomica__otro_beneficio', 1, 'asc', 1),
(2, 'Mayor puntaje socioeconómico', 'puntaje_socioeconomico', 2, 'desc', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulantes_datosacademicos`
--

CREATE TABLE `postulantes_datosacademicos` (
  `id` bigint(20) NOT NULL,
  `ppa` double NOT NULL,
  `materias_aprobadas` int(11) NOT NULL,
  `postulante_id` bigint(20) NOT NULL,
  `certificado_notas_pdf` varchar(100) DEFAULT NULL,
  `puntaje_academico_total` double NOT NULL,
  `puntaje_materias` double NOT NULL,
  `puntaje_ppa` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `postulantes_datosacademicos`
--

INSERT INTO `postulantes_datosacademicos` (`id`, `ppa`, `materias_aprobadas`, `postulante_id`, `certificado_notas_pdf`, `puntaje_academico_total`, `puntaje_materias`, `puntaje_ppa`) VALUES
(1, 0, 0, 3, 'certificados/Trabajo_Final_2.pdf', 10, 0, 10),
(2, 0, 0, 1, '', 10, 0, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulantes_fichasocioeconomica`
--

CREATE TABLE `postulantes_fichasocioeconomica` (
  `id` bigint(20) NOT NULL,
  `postulante_id` bigint(20) NOT NULL,
  `dependencia` varchar(100) DEFAULT NULL,
  `otro_beneficio` tinyint(1) NOT NULL,
  `rango_ingresos` varchar(100) DEFAULT NULL,
  `descripcion_otro_beneficio` varchar(200) NOT NULL,
  `doc_ingresos` varchar(100) NOT NULL,
  `doc_ocupacion` varchar(100) NOT NULL,
  `doc_vivienda` varchar(100) NOT NULL,
  `fecha_llenado` datetime(6) NOT NULL,
  `lugar_residencia` varchar(100) DEFAULT NULL,
  `num_hijos` int(11) NOT NULL,
  `num_integrantes` int(11) NOT NULL,
  `ocupacion` varchar(100) NOT NULL,
  `procedencia` varchar(100) DEFAULT NULL,
  `tenencia_vivienda` varchar(100) DEFAULT NULL,
  `tipo_vivienda` varchar(100) DEFAULT NULL,
  `archivo_boleta_inscripcion` varchar(100) DEFAULT NULL,
  `archivo_carnet_identidad` varchar(100) DEFAULT NULL,
  `archivo_historico_academico` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `postulantes_fichasocioeconomica`
--

INSERT INTO `postulantes_fichasocioeconomica` (`id`, `postulante_id`, `dependencia`, `otro_beneficio`, `rango_ingresos`, `descripcion_otro_beneficio`, `doc_ingresos`, `doc_ocupacion`, `doc_vivienda`, `fecha_llenado`, `lugar_residencia`, `num_hijos`, `num_integrantes`, `ocupacion`, `procedencia`, `tenencia_vivienda`, `tipo_vivienda`, `archivo_boleta_inscripcion`, `archivo_carnet_identidad`, `archivo_historico_academico`) VALUES
(1, 1, 'Independiente', 1, 'Hasta 2500 Bs.', 'beca comedor', 'fichas/ingresos/descarga.jpeg', 'fichas/ocupacion/descarga.jpeg', 'fichas/vivienda/descarga.jpeg', '2026-06-12 17:42:24.662784', 'Hasta el segundo anillo', 2, 5, 'Agricultor', 'Provincia', 'Anticrético', 'Más de 2 hab.', 'fichas/boletas/descarga.jpeg', 'fichas/identidades/descarga.jpeg', 'fichas/historicos/descarga.jpeg'),
(2, 2, 'Independiente', 0, 'Hasta 2500 Bs.', '', '', '', '', '2026-06-12 17:42:24.662784', 'Hasta el segundo anillo', 2, 5, 'Agricultor', 'Provincia', 'Alquiler', 'Más de 2 hab.', 'fichas/boletas/descarga_McMckPX.jpeg', 'fichas/identidades/descarga_4TpKiFj.jpeg', 'fichas/historicos/descarga_gAWwYdG.jpeg'),
(3, 3, '', 0, '', '', '', '', '', '2026-06-12 17:42:24.662784', NULL, 0, 1, '', NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulantes_materiasemestre`
--

CREATE TABLE `postulantes_materiasemestre` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `sigla` varchar(10) NOT NULL,
  `nota` double NOT NULL,
  `semestre` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `postulante_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulantes_miembrofamiliar`
--

CREATE TABLE `postulantes_miembrofamiliar` (
  `id` bigint(20) NOT NULL,
  `nombre_completo` varchar(200) NOT NULL,
  `parentesco` varchar(100) NOT NULL,
  `edad` smallint(5) UNSIGNED NOT NULL CHECK (`edad` >= 0),
  `ocupacion` varchar(200) NOT NULL,
  `observacion` varchar(255) NOT NULL,
  `ficha_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulantes_postulante`
--

CREATE TABLE `postulantes_postulante` (
  `id` bigint(20) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `nombre_completo` varchar(200) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `direccion` longtext NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `datos_completos` tinyint(1) NOT NULL,
  `ficha_completada` tinyint(1) NOT NULL,
  `convocatoria_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `carrera` varchar(100) NOT NULL,
  `facultad` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `postulantes_postulante`
--

INSERT INTO `postulantes_postulante` (`id`, `cedula`, `nombre_completo`, `telefono`, `direccion`, `fecha_nacimiento`, `fecha_registro`, `datos_completos`, `ficha_completada`, `convocatoria_id`, `user_id`, `carrera`, `facultad`) VALUES
(1, '10102020', 'María Gómez', '3151111111', 'Calle 10 # 45-12, Bogotá', '2003-05-15', '2026-06-12 04:28:00.624997', 1, 1, 1, 3, '', 'Facultad Integral de los Valles Cruceños'),
(2, '30304040', 'Carlos Rodríguez', '3152222222', 'Carrera 7 # 100-20, Bogotá', '2003-05-15', '2026-06-12 04:28:01.721872', 1, 1, 1, 4, '', 'Facultad Integral de los Valles Cruceños'),
(3, '50506060', 'Laura Castro', '3153333333', 'Transversal 5 # 80-40, Bogotá', '2003-05-15', '2026-06-12 04:28:02.763337', 1, 0, 1, 5, '', 'Facultad Integral de los Valles Cruceños'),
(4, '13176943', 'Camilo Lopez', '71004954', '', NULL, '2026-06-12 18:19:21.647578', 0, 0, NULL, 6, '', 'Facultad Integral de los Valles Cruceños'),
(5, '11327216', 'Yeison Vargas', '71394021', '', NULL, '2026-06-12 18:19:48.760697', 0, 0, NULL, 7, '', 'Facultad Integral de los Valles Cruceños'),
(6, '11327217', 'Leonel Vargas', '71394021', '', NULL, '2026-06-12 18:38:09.939291', 0, 0, NULL, 8, '', 'Facultad Integral de los Valles Cruceños'),
(7, '221185550', 'Yeison Leonel Ayzacayo Vargas', '71394021', '', NULL, '2026-06-17 20:12:30.634633', 0, 0, NULL, 9, '', 'Facultad Integral de los Valles Cruceños');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulantes_solicitudbeca`
--

CREATE TABLE `postulantes_solicitudbeca` (
  `id` bigint(20) NOT NULL,
  `puntaje_total` double DEFAULT NULL,
  `puntaje_academico` double DEFAULT NULL,
  `puntaje_socioeconomico` double DEFAULT NULL,
  `estado` varchar(50) NOT NULL,
  `fecha_asignacion` datetime(6) DEFAULT NULL,
  `postulante_id` bigint(20) NOT NULL,
  `fecha_revision` datetime(6) DEFAULT NULL,
  `motivo_rechazo` longtext DEFAULT NULL,
  `observaciones_internas` longtext DEFAULT NULL,
  `fecha_rechazo` datetime(6) DEFAULT NULL,
  `notificado_rechazo` tinyint(1) NOT NULL,
  `rechazado` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `postulantes_solicitudbeca`
--

INSERT INTO `postulantes_solicitudbeca` (`id`, `puntaje_total`, `puntaje_academico`, `puntaje_socioeconomico`, `estado`, `fecha_asignacion`, `postulante_id`, `fecha_revision`, `motivo_rechazo`, `observaciones_internas`, `fecha_rechazo`, `notificado_rechazo`, `rechazado`) VALUES
(1, 75, 10, 65, 'Beca Asignada', '2026-06-17 02:43:29.483549', 1, '2026-06-17 02:43:17.936276', NULL, '', NULL, 0, 0),
(2, 66, 0, 66, 'Beca Asignada', '2026-06-17 02:43:29.483549', 2, NULL, NULL, NULL, NULL, 0, 0),
(3, 12, 10, 2, 'Postulación completada', NULL, 3, NULL, NULL, NULL, NULL, 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_logaccion`
--

CREATE TABLE `usuarios_logaccion` (
  `id` bigint(20) NOT NULL,
  `accion` varchar(50) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `detalles` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`detalles`)),
  `ip_address` char(39) DEFAULT NULL,
  `objeto_id` int(10) UNSIGNED DEFAULT NULL CHECK (`objeto_id` >= 0),
  `objeto_tipo` varchar(100) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios_logaccion`
--

INSERT INTO `usuarios_logaccion` (`id`, `accion`, `timestamp`, `detalles`, `ip_address`, `objeto_id`, `objeto_tipo`, `usuario_id`) VALUES
(1, 'login', '2026-06-12 04:33:43.053187', '{}', '127.0.0.1', NULL, '', 1),
(2, 'logout', '2026-06-12 04:37:26.415624', '{}', NULL, NULL, '', 1),
(3, 'login', '2026-06-12 04:38:05.771480', '{}', '127.0.0.1', NULL, '', 3),
(4, 'logout', '2026-06-12 04:39:30.101441', '{}', NULL, NULL, '', 3),
(5, 'login', '2026-06-12 05:19:14.187039', '{}', '127.0.0.1', NULL, '', 1),
(6, 'login', '2026-06-12 06:18:47.479470', '{}', '127.0.0.1', NULL, '', 1),
(7, 'logout', '2026-06-12 06:20:06.762551', '{}', NULL, NULL, '', 1),
(8, 'login', '2026-06-12 06:20:31.443526', '{}', '127.0.0.1', NULL, '', 1),
(9, 'logout', '2026-06-12 06:22:42.859061', '{}', NULL, NULL, '', 1),
(10, 'login', '2026-06-12 06:23:04.622325', '{}', '127.0.0.1', NULL, '', 2),
(11, 'logout', '2026-06-12 06:24:06.218132', '{}', NULL, NULL, '', 2),
(12, 'login', '2026-06-12 06:24:13.370228', '{}', '127.0.0.1', NULL, '', 1),
(13, 'logout', '2026-06-12 14:25:47.142271', '{}', NULL, NULL, '', 1),
(14, 'login', '2026-06-12 14:26:17.794566', '{}', '127.0.0.1', NULL, '', 1),
(15, 'logout', '2026-06-12 14:40:30.818693', '{}', NULL, NULL, '', 1),
(16, 'otro', '2026-06-12 14:41:55.894714', '{\"tipo\": \"contacto_landing\", \"nombre\": \"leonel vargas \", \"email\": \"leo@gmail.com\"}', NULL, NULL, '', NULL),
(17, 'login', '2026-06-12 14:42:17.476144', '{}', '127.0.0.1', NULL, '', 1),
(18, 'logout', '2026-06-12 14:44:14.683628', '{}', NULL, NULL, '', 1),
(19, 'login', '2026-06-12 14:45:45.123383', '{}', '127.0.0.1', NULL, '', 1),
(20, 'logout', '2026-06-12 14:46:06.474416', '{}', NULL, NULL, '', 1),
(21, 'login', '2026-06-12 14:46:19.829888', '{}', '127.0.0.1', NULL, '', 2),
(22, 'logout', '2026-06-12 14:46:39.221348', '{}', NULL, NULL, '', 2),
(23, 'login', '2026-06-12 14:47:33.630954', '{}', '127.0.0.1', NULL, '', 1),
(24, 'logout', '2026-06-12 14:48:08.592224', '{}', NULL, NULL, '', 1),
(25, 'login', '2026-06-12 14:48:25.859483', '{}', '127.0.0.1', NULL, '', 3),
(26, 'logout', '2026-06-12 14:51:14.625836', '{}', NULL, NULL, '', 3),
(27, 'login', '2026-06-12 14:54:49.286603', '{}', '127.0.0.1', NULL, '', 1),
(28, 'logout', '2026-06-12 14:55:37.030753', '{}', NULL, NULL, '', 1),
(29, 'login', '2026-06-12 14:55:49.409211', '{}', '127.0.0.1', NULL, '', 3),
(30, 'logout', '2026-06-12 16:56:06.392519', '{}', NULL, NULL, '', 3),
(31, 'login', '2026-06-12 17:00:44.534421', '{}', '127.0.0.1', NULL, '', 2),
(32, 'logout', '2026-06-12 17:49:19.358425', '{}', NULL, NULL, '', 1),
(33, 'login', '2026-06-12 17:49:28.914045', '{}', '127.0.0.1', NULL, '', 1),
(34, 'logout', '2026-06-12 17:52:04.660273', '{}', NULL, NULL, '', 1),
(35, 'login', '2026-06-12 17:53:00.000316', '{}', '127.0.0.1', NULL, '', 3),
(36, 'logout', '2026-06-12 17:53:46.321082', '{}', NULL, NULL, '', 3),
(37, 'login', '2026-06-12 17:57:59.365958', '{}', '127.0.0.1', NULL, '', 1),
(38, 'logout', '2026-06-12 18:15:32.007305', '{}', NULL, NULL, '', 1),
(39, 'login', '2026-06-12 18:17:38.047565', '{}', '127.0.0.1', NULL, '', 1),
(40, 'logout', '2026-06-12 18:36:47.503712', '{}', NULL, NULL, '', 1),
(41, 'login', '2026-06-12 18:37:56.068749', '{}', '127.0.0.1', NULL, '', 1),
(42, 'logout', '2026-06-12 18:42:51.862001', '{}', NULL, NULL, '', 1),
(43, 'login', '2026-06-12 18:43:18.922159', '{}', '127.0.0.1', NULL, '', 3),
(44, 'logout', '2026-06-12 19:12:49.081666', '{}', NULL, NULL, '', 3),
(45, 'login', '2026-06-12 19:13:03.486795', '{}', '127.0.0.1', NULL, '', 3),
(46, 'login', '2026-06-12 19:13:04.351998', '{}', '127.0.0.1', NULL, '', 3),
(47, 'logout', '2026-06-12 19:55:01.793915', '{}', NULL, NULL, '', 3),
(48, 'login', '2026-06-12 19:55:30.485860', '{}', '127.0.0.1', NULL, '', 2),
(49, 'logout', '2026-06-12 20:09:01.075903', '{}', NULL, NULL, '', 2),
(50, 'login', '2026-06-12 20:09:10.144097', '{}', '127.0.0.1', NULL, '', 1),
(51, 'modificar_parametro', '2026-06-12 20:09:51.115929', '{\"parametro\": \"cupos_disponibles\", \"valor\": \"2\", \"recalculados\": 3}', NULL, NULL, '', 1),
(52, 'modificar_parametro', '2026-06-12 20:14:59.358957', '{\"parametro\": \"cupos_disponibles\", \"valor\": \"2\", \"recalculados\": 3}', NULL, NULL, '', 1),
(53, 'login', '2026-06-12 20:23:01.434585', '{}', '127.0.0.1', NULL, '', 2),
(54, 'evaluacion', '2026-06-12 20:37:21.748956', '{\"mensaje\": \"Optimizaci\\u00f3n de becas ejecutada\", \"cupos\": 2, \"total_postulantes\": 1, \"seleccionados_count\": 1}', NULL, NULL, '', 1),
(55, 'modificar_parametro', '2026-06-12 20:37:43.489050', '{\"parametro\": \"cupos_disponibles\", \"valor\": \"5\", \"recalculados\": 3}', NULL, NULL, '', 1),
(56, 'evaluacion', '2026-06-12 20:37:55.635099', '{\"mensaje\": \"Optimizaci\\u00f3n de becas ejecutada\", \"cupos\": 5, \"total_postulantes\": 1, \"seleccionados_count\": 1}', NULL, NULL, '', 1),
(57, 'logout', '2026-06-12 20:38:53.621751', '{}', NULL, NULL, '', 1),
(58, 'logout', '2026-06-12 20:40:06.325251', '{}', NULL, NULL, '', 2),
(59, 'login', '2026-06-12 20:40:17.758790', '{}', '127.0.0.1', NULL, '', 1),
(60, 'logout', '2026-06-12 20:41:00.019715', '{}', NULL, NULL, '', 1),
(61, 'login', '2026-06-12 20:46:13.542588', '{}', '127.0.0.1', NULL, '', 2),
(62, 'logout', '2026-06-12 20:57:10.215996', '{}', NULL, NULL, '', 2),
(63, 'login', '2026-06-12 21:04:38.177992', '{}', '127.0.0.1', NULL, '', 4),
(64, 'logout', '2026-06-12 21:15:35.453884', '{}', NULL, NULL, '', 4),
(65, 'login', '2026-06-12 21:15:55.526999', '{}', '127.0.0.1', NULL, '', 2),
(66, 'evaluacion', '2026-06-12 21:17:26.993603', '{\"mensaje\": \"Optimizaci\\u00f3n de becas ejecutada\", \"cupos\": 5, \"total_postulantes\": 2, \"seleccionados_count\": 2}', NULL, NULL, '', 2),
(67, 'logout', '2026-06-12 21:18:19.136882', '{}', NULL, NULL, '', 2),
(68, 'login', '2026-06-12 21:18:28.644979', '{}', '127.0.0.1', NULL, '', 1),
(69, 'logout', '2026-06-16 14:43:10.212305', '{}', NULL, NULL, '', 1),
(70, 'login', '2026-06-16 14:44:38.881845', '{}', '127.0.0.1', NULL, '', 1),
(71, 'logout', '2026-06-16 14:56:15.136255', '{}', NULL, NULL, '', 1),
(72, 'login', '2026-06-16 14:56:47.456474', '{}', '127.0.0.1', NULL, '', 2),
(73, 'logout', '2026-06-17 00:38:43.099982', '{}', NULL, NULL, '', 2),
(74, 'login', '2026-06-17 00:43:20.585267', '{}', '127.0.0.1', NULL, '', 1),
(75, 'logout', '2026-06-17 00:46:10.172599', '{}', NULL, NULL, '', 1),
(76, 'login', '2026-06-17 00:46:24.716485', '{}', '127.0.0.1', NULL, '', 5),
(77, 'logout', '2026-06-17 01:50:54.093431', '{}', NULL, NULL, '', 5),
(78, 'login', '2026-06-17 01:51:18.684891', '{}', '127.0.0.1', NULL, '', 2),
(79, 'evaluacion', '2026-06-17 02:43:17.942152', '{\"postulante\": \"postulante1\", \"nuevo_estado\": \"Aprobado\"}', NULL, 1, 'Postulante', 2),
(80, 'evaluacion', '2026-06-17 02:43:29.542038', '{\"mensaje\": \"Optimizaci\\u00f3n de becas ejecutada\", \"cupos\": 5, \"total_postulantes\": 2, \"seleccionados_count\": 2}', NULL, NULL, '', 2),
(81, 'exportar', '2026-06-17 02:49:45.443397', '{\"formato\": \"Excel\"}', NULL, NULL, '', 2),
(82, 'logout', '2026-06-17 02:52:18.701228', '{}', NULL, NULL, '', 2),
(83, 'login', '2026-06-17 02:52:32.261024', '{}', '127.0.0.1', NULL, '', 1),
(84, 'logout', '2026-06-17 02:53:10.972401', '{}', NULL, NULL, '', 1),
(85, 'login', '2026-06-17 03:13:39.511380', '{}', '127.0.0.1', NULL, '', 5),
(86, 'logout', '2026-06-17 15:59:44.486372', '{}', NULL, NULL, '', 5),
(87, 'login', '2026-06-17 19:09:19.511852', '{}', '127.0.0.1', NULL, '', 3),
(88, 'logout', '2026-06-17 19:14:46.161619', '{}', NULL, NULL, '', 3),
(89, 'login', '2026-06-17 20:12:59.403951', '{}', '127.0.0.1', NULL, '', 9),
(90, 'logout', '2026-06-17 20:16:08.260005', '{}', NULL, NULL, '', 9),
(91, 'login', '2026-06-17 20:16:34.132821', '{}', '127.0.0.1', NULL, '', 9),
(92, 'logout', '2026-06-17 20:18:39.559137', '{}', NULL, NULL, '', 9),
(93, 'login', '2026-06-17 20:18:55.074878', '{}', '127.0.0.1', NULL, '', 1),
(94, 'logout', '2026-06-17 20:19:30.774709', '{}', NULL, NULL, '', 1),
(95, 'login', '2026-06-17 20:23:01.153321', '{}', '127.0.0.1', NULL, '', 2),
(96, 'logout', '2026-06-17 20:23:24.830504', '{}', NULL, NULL, '', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_perfilusuario`
--

CREATE TABLE `usuarios_perfilusuario` (
  `id` bigint(20) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios_perfilusuario`
--

INSERT INTO `usuarios_perfilusuario` (`id`, `rol`, `telefono`, `activo`, `fecha_creacion`, `user_id`) VALUES
(1, 'administrador', '3001234567', 1, '2026-06-12 04:27:58.393372', 1),
(2, 'evaluador', '3007654321', 1, '2026-06-12 04:27:59.449566', 2),
(3, 'postulante', '3151111111', 1, '2026-06-12 04:28:00.615114', 3),
(4, 'postulante', '3152222222', 1, '2026-06-12 04:28:01.712982', 4),
(5, 'postulante', '3153333333', 1, '2026-06-12 04:28:02.755621', 5),
(6, 'postulante', '', 1, '2026-06-12 18:19:21.643865', 6),
(7, 'postulante', '', 1, '2026-06-12 18:19:48.757667', 7),
(8, 'postulante', '', 1, '2026-06-12 18:38:09.935749', 8),
(9, 'postulante', '', 1, '2026-06-17 20:12:30.642773', 9);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `convocatorias_convocatoria`
--
ALTER TABLE `convocatorias_convocatoria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `convocatorias_convoc_creada_por_id_337e36a2_fk_auth_user` (`creada_por_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `evaluaciones_evaluacion`
--
ALTER TABLE `evaluaciones_evaluacion`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `postulante_id` (`postulante_id`),
  ADD KEY `evaluaciones_evaluac_convocatoria_id_0506493c_fk_convocato` (`convocatoria_id`),
  ADD KEY `evaluaciones_evaluacion_evaluado_por_id_61899584_fk_auth_user_id` (`evaluado_por_id`),
  ADD KEY `evaluaciones_evaluacion_puntaje_total_8db16101` (`puntaje_total`),
  ADD KEY `evaluaciones_evaluacion_estado_055491a5` (`estado`),
  ADD KEY `evaluacione_estado_d8585e_idx` (`estado`,`puntaje_total`);

--
-- Indices de la tabla `parametros_opcionsocioeconomica`
--
ALTER TABLE `parametros_opcionsocioeconomica`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `parametros_opcionsocioec_variable_opcion_texto_120af3af_uniq` (`variable`,`opcion_texto`);

--
-- Indices de la tabla `parametros_parametrobeca`
--
ALTER TABLE `parametros_parametrobeca`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`),
  ADD KEY `parametros_parametro_modificado_por_id_7cb0de26_fk_auth_user` (`modificado_por_id`);

--
-- Indices de la tabla `parametros_rangomaterias`
--
ALTER TABLE `parametros_rangomaterias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `parametros_rangopps`
--
ALTER TABLE `parametros_rangopps`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `parametros_regladesempate`
--
ALTER TABLE `parametros_regladesempate`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `postulantes_datosacademicos`
--
ALTER TABLE `postulantes_datosacademicos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `postulante_id` (`postulante_id`);

--
-- Indices de la tabla `postulantes_fichasocioeconomica`
--
ALTER TABLE `postulantes_fichasocioeconomica`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `postulante_id` (`postulante_id`);

--
-- Indices de la tabla `postulantes_materiasemestre`
--
ALTER TABLE `postulantes_materiasemestre`
  ADD PRIMARY KEY (`id`),
  ADD KEY `postulantes_materias_postulante_id_285ea973_fk_postulant` (`postulante_id`);

--
-- Indices de la tabla `postulantes_miembrofamiliar`
--
ALTER TABLE `postulantes_miembrofamiliar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `postulantes_miembrof_ficha_id_a607e88f_fk_postulant` (`ficha_id`);

--
-- Indices de la tabla `postulantes_postulante`
--
ALTER TABLE `postulantes_postulante`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cedula` (`cedula`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `postulantes_postulan_convocatoria_id_a8849ec4_fk_convocato` (`convocatoria_id`);

--
-- Indices de la tabla `postulantes_solicitudbeca`
--
ALTER TABLE `postulantes_solicitudbeca`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `postulante_id` (`postulante_id`);

--
-- Indices de la tabla `usuarios_logaccion`
--
ALTER TABLE `usuarios_logaccion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuarios_lo_usuario_9171f9_idx` (`usuario_id`,`timestamp`),
  ADD KEY `usuarios_lo_accion_c20457_idx` (`accion`,`timestamp`);

--
-- Indices de la tabla `usuarios_perfilusuario`
--
ALTER TABLE `usuarios_perfilusuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `convocatorias_convocatoria`
--
ALTER TABLE `convocatorias_convocatoria`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT de la tabla `evaluaciones_evaluacion`
--
ALTER TABLE `evaluaciones_evaluacion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `parametros_opcionsocioeconomica`
--
ALTER TABLE `parametros_opcionsocioeconomica`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT de la tabla `parametros_parametrobeca`
--
ALTER TABLE `parametros_parametrobeca`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `parametros_rangomaterias`
--
ALTER TABLE `parametros_rangomaterias`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `parametros_rangopps`
--
ALTER TABLE `parametros_rangopps`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `parametros_regladesempate`
--
ALTER TABLE `parametros_regladesempate`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `postulantes_datosacademicos`
--
ALTER TABLE `postulantes_datosacademicos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `postulantes_fichasocioeconomica`
--
ALTER TABLE `postulantes_fichasocioeconomica`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `postulantes_materiasemestre`
--
ALTER TABLE `postulantes_materiasemestre`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `postulantes_miembrofamiliar`
--
ALTER TABLE `postulantes_miembrofamiliar`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `postulantes_postulante`
--
ALTER TABLE `postulantes_postulante`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `postulantes_solicitudbeca`
--
ALTER TABLE `postulantes_solicitudbeca`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios_logaccion`
--
ALTER TABLE `usuarios_logaccion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;

--
-- AUTO_INCREMENT de la tabla `usuarios_perfilusuario`
--
ALTER TABLE `usuarios_perfilusuario`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `convocatorias_convocatoria`
--
ALTER TABLE `convocatorias_convocatoria`
  ADD CONSTRAINT `convocatorias_convoc_creada_por_id_337e36a2_fk_auth_user` FOREIGN KEY (`creada_por_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `evaluaciones_evaluacion`
--
ALTER TABLE `evaluaciones_evaluacion`
  ADD CONSTRAINT `evaluaciones_evaluac_convocatoria_id_0506493c_fk_convocato` FOREIGN KEY (`convocatoria_id`) REFERENCES `convocatorias_convocatoria` (`id`),
  ADD CONSTRAINT `evaluaciones_evaluac_postulante_id_c343584c_fk_postulant` FOREIGN KEY (`postulante_id`) REFERENCES `postulantes_postulante` (`id`),
  ADD CONSTRAINT `evaluaciones_evaluacion_evaluado_por_id_61899584_fk_auth_user_id` FOREIGN KEY (`evaluado_por_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `parametros_parametrobeca`
--
ALTER TABLE `parametros_parametrobeca`
  ADD CONSTRAINT `parametros_parametro_modificado_por_id_7cb0de26_fk_auth_user` FOREIGN KEY (`modificado_por_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `postulantes_datosacademicos`
--
ALTER TABLE `postulantes_datosacademicos`
  ADD CONSTRAINT `postulantes_datosaca_postulante_id_a507329a_fk_postulant` FOREIGN KEY (`postulante_id`) REFERENCES `postulantes_postulante` (`id`);

--
-- Filtros para la tabla `postulantes_fichasocioeconomica`
--
ALTER TABLE `postulantes_fichasocioeconomica`
  ADD CONSTRAINT `postulantes_fichasoc_postulante_id_d5b0c1c4_fk_postulant` FOREIGN KEY (`postulante_id`) REFERENCES `postulantes_postulante` (`id`);

--
-- Filtros para la tabla `postulantes_materiasemestre`
--
ALTER TABLE `postulantes_materiasemestre`
  ADD CONSTRAINT `postulantes_materias_postulante_id_285ea973_fk_postulant` FOREIGN KEY (`postulante_id`) REFERENCES `postulantes_postulante` (`id`);

--
-- Filtros para la tabla `postulantes_miembrofamiliar`
--
ALTER TABLE `postulantes_miembrofamiliar`
  ADD CONSTRAINT `postulantes_miembrof_ficha_id_a607e88f_fk_postulant` FOREIGN KEY (`ficha_id`) REFERENCES `postulantes_fichasocioeconomica` (`id`);

--
-- Filtros para la tabla `postulantes_postulante`
--
ALTER TABLE `postulantes_postulante`
  ADD CONSTRAINT `postulantes_postulan_convocatoria_id_a8849ec4_fk_convocato` FOREIGN KEY (`convocatoria_id`) REFERENCES `convocatorias_convocatoria` (`id`),
  ADD CONSTRAINT `postulantes_postulante_user_id_bfbebb4b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `postulantes_solicitudbeca`
--
ALTER TABLE `postulantes_solicitudbeca`
  ADD CONSTRAINT `postulantes_solicitu_postulante_id_f890b44c_fk_postulant` FOREIGN KEY (`postulante_id`) REFERENCES `postulantes_postulante` (`id`);

--
-- Filtros para la tabla `usuarios_logaccion`
--
ALTER TABLE `usuarios_logaccion`
  ADD CONSTRAINT `usuarios_logaccion_usuario_id_34fb5722_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `usuarios_perfilusuario`
--
ALTER TABLE `usuarios_perfilusuario`
  ADD CONSTRAINT `usuarios_perfilusuario_user_id_f03197c5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
