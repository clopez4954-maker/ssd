import os
import sys
import django
from decimal import Decimal
from django.utils import timezone
from datetime import date

# Configurar entorno Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.usuarios.models import PerfilUsuario
from apps.convocatorias.models import Convocatoria
from apps.postulantes.models import Postulante, DatosAcademicos, DatosSocioeconomicos
from apps.evaluaciones.models import Evaluacion

def create_demo():
    print("Creando datos de demostración...")

    # 1. Crear Superusuario / Administrador
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@becasuni.edu.co', 'admin123')
        admin_user.first_name = "Admin"
        admin_user.last_name = "Sistema"
        admin_user.save()
        
        # PerfilUsuario se suele crear automáticamente por señales, pero nos aseguramos
        perfil, _ = PerfilUsuario.objects.get_or_create(user=admin_user)
        perfil.rol = PerfilUsuario.ROL_ADMINISTRADOR
        perfil.telefono = "3001234567"
        perfil.save()
        print("Administrador creado: admin / admin123")
    else:
        print("Administrador ya existe.")

    # 2. Crear Evaluador
    if not User.objects.filter(username='evaluador').exists():
        eval_user = User.objects.create_user('evaluador', 'evaluador@becasuni.edu.co', 'evaluador123')
        eval_user.first_name = "Juan"
        eval_user.last_name = "Pérez"
        eval_user.save()
        
        perfil, _ = PerfilUsuario.objects.get_or_create(user=eval_user)
        perfil.rol = PerfilUsuario.ROL_EVALUADOR
        perfil.telefono = "3007654321"
        perfil.save()
        print("Evaluador creado: evaluador / evaluador123")
    else:
        print("Evaluador ya existe.")

    # 3. Crear Convocatoria Activa
    hoy = timezone.now().date()
    convocatoria, _ = Convocatoria.objects.get_or_create(
        nombre="Convocatoria Becas 2026-II",
        defaults={
            'descripcion': "Programa de becas de matrícula para el segundo semestre del año 2026.",
            'fecha_inicio': hoy,
            'fecha_fin': hoy + timezone.timedelta(days=30),
            'activa': True,
        }
    )
    print(f"Convocatoria activa: {convocatoria.nombre}")

    # 4. Crear Postulantes de prueba
    postulantes_data = [
        {
            'username': 'postulante1',
            'pass': 'postulante123',
            'email': 'maria.gomez@becasuni.edu.co',
            'first_name': 'María',
            'last_name': 'Gómez',
            'cedula': '10102020',
            'telefono': '3151111111',
            'direccion': 'Calle 10 # 45-12, Bogotá',
            'promedio': Decimal('4.65'),
            'creditos_aprobados': 45,
            'creditos_totales': 160,
            'semestre': 3,
            'carrera': 'Ingeniería de Sistemas',
            'institucion': 'Universidad de Becas',
            'ingreso': Decimal('1500000.00'),
            'estrato': 1,
            'hermanos': 1,
            'vivienda': 'arrendada',
            'trabaja': False,
        },
        {
            'username': 'postulante2',
            'pass': 'postulante123',
            'email': 'carlos.rodriguez@becasuni.edu.co',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'cedula': '30304040',
            'telefono': '3152222222',
            'direccion': 'Carrera 7 # 100-20, Bogotá',
            'promedio': Decimal('3.80'),
            'creditos_aprobados': 90,
            'creditos_totales': 160,
            'semestre': 6,
            'carrera': 'Medicina',
            'institucion': 'Universidad de Becas',
            'ingreso': Decimal('2800000.00'),
            'estrato': 2,
            'hermanos': 0,
            'vivienda': 'propia',
            'trabaja': True,
        },
        {
            'username': 'postulante3',
            'pass': 'postulante123',
            'email': 'laura.castro@becasuni.edu.co',
            'first_name': 'Laura',
            'last_name': 'Castro',
            'cedula': '50506060',
            'telefono': '3153333333',
            'direccion': 'Transversal 5 # 80-40, Bogotá',
            'promedio': Decimal('2.90'), # Menor al mínimo
            'creditos_aprobados': 12,
            'creditos_totales': 160,
            'semestre': 1,
            'carrera': 'Derecho',
            'institucion': 'Universidad de Becas',
            'ingreso': Decimal('900000.00'),
            'estrato': 1,
            'hermanos': 2,
            'vivienda': 'familiar',
            'trabaja': False,
        }
    ]

    for p in postulantes_data:
        if not User.objects.filter(username=p['username']).exists():
            user = User.objects.create_user(p['username'], p['email'], p['pass'])
            user.first_name = p['first_name']
            user.last_name = p['last_name']
            user.save()
            
            perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
            perfil.rol = PerfilUsuario.ROL_POSTULANTE
            perfil.telefono = p['telefono']
            perfil.save()

            postulante = Postulante.objects.create(
                user=user,
                cedula=p['cedula'],
                nombre_completo=f"{p['first_name']} {p['last_name']}",
                telefono=p['telefono'],
                direccion=p['direccion'],
                fecha_nacimiento=date(2003, 5, 15),
                convocatoria=convocatoria,
                datos_completos=True
            )

            DatosAcademicos.objects.create(
                postulante=postulante,
                institucion=p['institucion'],
                carrera=p['carrera'],
                semestre=p['semestre'],
                promedio=p['promedio'],
                creditos_aprobados=p['creditos_aprobados'],
                creditos_totales=p['creditos_totales']
            )

            DatosSocioeconomicos.objects.create(
                postulante=postulante,
                ingreso_familiar=p['ingreso'],
                estrato=p['estrato'],
                num_hermanos_universidad=p['hermanos'],
                tipo_vivienda=p['vivienda'],
                trabaja=p['trabaja']
            )

            # Iniciar evaluación en estado pendiente
            Evaluacion.objects.create(
                postulante=postulante,
                convocatoria=convocatoria,
                estado=Evaluacion.ESTADO_PENDIENTE
            )
            print(f"Postulante creado: {p['username']} / {p['pass']} (Pendiente)")

if __name__ == "__main__":
    create_demo()
