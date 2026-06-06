# 🎓 BecasUni — Sistema de Gestión y Asignación Automática de Becas

Sistema web premium para la gestión, postulación y evaluación automática de becas universitarias basado en un modelo matemático parametrizable.

## 🛠️ Stack Tecnológico
- **Backend**: Python 3.10+ & Django 5.x
- **Frontend**: Django Templates + Bootstrap 5.3 + HTMX 1.9 (actualizaciones parciales sin recargar)
- **Base de Datos**: SQLite (desarrollo local) y PostgreSQL ready
- **Estilos**: Paleta oscura (navy + gold) con micro-animaciones premium en CSS personalizado (`main.css`)

---

## 🚀 Instalación y Configuración Local

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

### 1. Clonar o descargar el repositorio
Asegúrate de estar dentro del directorio raíz `ssd/`.

### 2. Activar el Entorno Virtual
Si usas Windows, ejecuta en tu terminal:
```powershell
venv\Scripts\activate
```

### 3. Instalar Dependencias
Instala los paquetes de Python especificados en el archivo de requerimientos:
```bash
pip install -r backend/requirements.txt
```

### 4. Generar y Ejecutar Migraciones
Crea y aplica las tablas del sistema en la base de datos local:
```bash
python backend/manage.py makemigrations usuarios convocatorias postulantes parametros evaluaciones reportes
python backend/manage.py migrate
```

### 5. Cargar Parámetros Iniciales del Algoritmo
Carga los valores iniciales para el modelo de ponderación:
```bash
python backend/manage.py loaddata backend/fixtures/initial_data.json
```

### 6. Cargar Cuentas y Datos de Demostración
Puebla la base de datos con una convocatoria activa, superusuario, evaluador y postulantes de prueba ejecutando el script preconfigurado:
```bash
python backend/fixtures/create_demo_data.py
```

### 7. Iniciar el Servidor de Desarrollo
```bash
python backend/manage.py runserver
```
El sistema estará disponible en [http://localhost:8000](http://localhost:8000).

---

## 👥 Cuentas de Acceso (Demo)

Puedes iniciar sesión con cualquiera de los siguientes perfiles precargados:

| Rol | Usuario | Contraseña | Descripción |
|-----|---------|------------|-------------|
| **Administrador** | `admin` | `admin123` | Control total, logs de auditoría, gestión de parámetros e historial. |
| **Evaluador** | `evaluador` | `evaluador123` | Acceso a postulantes, evaluación en vivo, reevaluaciones masivas y reportes con gráficos. |
| **Postulante 1** | `postulante1` | `postulante123` | María Gómez (Datos Completos, estrato 1, promedio 4.65, estado Pendiente). |
| **Postulante 2** | `postulante2` | `postulante123` | Carlos Rodríguez (Datos Completos, estrato 2, promedio 3.80, trabaja, Pendiente). |
| **Postulante 3** | `postulante3` | `postulante123` | Laura Castro (Datos Completos, promedio 2.90, Pendiente). |

---

## 📐 Lógica del Modelo Matemático de Evaluación

El sistema calcula los puntajes académicos y socioeconómicos utilizando fórmulas configurables en tiempo real desde el **Panel de Parámetros**:

1. **Restricción de Entrada**: Si el promedio acumulado del postulante es inferior al parámetro `promedio_minimo` (defecto: `3.0`), la postulación se rechaza automáticamente.
2. **Puntaje Académico ($P_{Acad}$)**: Máximo 60 puntos.
   $$P_{Acad} = \left(\frac{\text{Promedio}}{5.0} \times 40\right) + \text{min}\left(\frac{\text{Créditos Aprobados}}{30} \times 20, 20\right)$$
3. **Puntaje Socioeconómico ($P_{Socio}$)**: Máximo 40 puntos.
   $$P_{Socio} = \left(1.0 - \text{min}\left(\frac{\text{Ingreso Familiar}}{\text{ingreso\_maximo}}, 0.95\right)\right) \times 25 + \text{Puntos por Estrato}$$
   *(Estrato 1 = 15 pts, Estrato 2 = 12 pts, Estrato 3 = 8 pts, Estrato 4 = 4 pts, Estrato 5/6 = 0 pts)*
4. **Puntaje Total ($P_{Total}$)**:
   $$P_{Total} = (P_{Acad} \times \text{peso\_academico}) + (P_{Socio} \times \text{peso\_socioeconomico})$$
5. **Aprobación**: Se aprueba si $P_{Total} \ge \text{puntaje\_corte\_aprobado}$ (defecto: `60.0`).

---

## 📂 Exportación de Base de Datos
La base de datos actual se almacena localmente en `backend/db.sqlite3`. Puedes abrirla o exportarla usando cualquier administrador de bases de datos como DB Browser for SQLite, DBeaver, o exportar su contenido directamente mediante comandos `dumpdata` de Django si deseas transferirla a PostgreSQL en producción.
