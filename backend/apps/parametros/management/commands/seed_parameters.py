from django.core.management.base import BaseCommand
from apps.parametros.models import RangoPPS, RangoMaterias, OpcionSocioeconomica, ReglaDesempate, ParametroBeca


class Command(BaseCommand):
    help = 'Poblar base de datos con los parámetros por defecto de la Beca Albergue'

    def handle(self, *args, **options):
        self.stdout.write('Poblando rangos de PPS...')
        RangoPPS.objects.all().delete()
        RangoPPS.objects.create(desde=60.0, hasta=100.0, puntaje=25)
        RangoPPS.objects.create(desde=46.0, hasta=59.99, puntaje=20)
        RangoPPS.objects.create(desde=32.0, hasta=45.99, puntaje=15)
        RangoPPS.objects.create(desde=0.0, hasta=31.99, puntaje=10)

        self.stdout.write('Poblando rangos de Materias Aprobadas...')
        RangoMaterias.objects.all().delete()
        RangoMaterias.objects.create(desde=6, hasta=None, puntaje=5)
        RangoMaterias.objects.create(desde=4, hasta=5, puntaje=4)
        RangoMaterias.objects.create(desde=2, hasta=3, puntaje=3)
        RangoMaterias.objects.create(desde=1, hasta=1, puntaje=2)

        self.stdout.write('Poblando opciones socioeconómicas (X1 a X9)...')
        OpcionSocioeconomica.objects.all().delete()

        # X1: Tipo de dependencia
        x1_opts = [
            ('Ambos padres', 5),
            ('Pareja', 6),
            ('Otro familiar', 8),
            ('Solo padre o madre', 9),
            ('Independiente', 10),
        ]
        for opt, pts in x1_opts:
            OpcionSocioeconomica.objects.create(variable='dependencia', opcion_texto=opt, puntaje=pts)

        # X2: Tipo de ocupación
        x2_opts = [
            ('Comerciante mayorista', 6),
            ('Asalariado formal', 7),
            ('Rentista', 8),
            ('Asalariado informal', 9),
            ('Comerciante minorista', 10),
            ('Agricultor', 10),
        ]
        for opt, pts in x2_opts:
            OpcionSocioeconomica.objects.create(variable='ocupacion', opcion_texto=opt, puntaje=pts)

        # X3: Ingresos
        x3_opts = [
            ('Más de 6000 Bs.', 7),
            ('De 4001 a 6000 Bs.', 8),
            ('De 2501 a 4000 Bs.', 9),
            ('Hasta 2500 Bs.', 10),
        ]
        for opt, pts in x3_opts:
            OpcionSocioeconomica.objects.create(variable='rango_ingresos', opcion_texto=opt, puntaje=pts)

        # X4: Número de integrantes familiares
        x4_opts = [
            ('Hasta 1 miembro', 2),
            ('De 2 a 3 miembros', 3),
            ('De 3 a 4 miembros', 4),
            ('Más de 4 miembros', 5),
        ]
        for opt, pts in x4_opts:
            OpcionSocioeconomica.objects.create(variable='num_integrantes', opcion_texto=opt, puntaje=pts)

        # X5: Descendencia
        x5_opts = [
            ('Sin hijos', 0),
            ('1 hijo', 4),
            ('Más de 1 hijo', 5),
        ]
        for opt, pts in x5_opts:
            OpcionSocioeconomica.objects.create(variable='num_hijos', opcion_texto=opt, puntaje=pts)

        # X6: Lugar de residencia
        x6_opts = [
            ('Hasta el segundo anillo', 2),
            ('Fuera del 2do anillo', 5),
        ]
        for opt, pts in x6_opts:
            OpcionSocioeconomica.objects.create(variable='lugar_residencia', opcion_texto=opt, puntaje=pts)

        # X7: Tenencia de vivienda
        x7_opts = [
            ('Por herencia', 2),
            ('De los padres', 2),
            ('Cedida por terceros', 3),
            ('Anticrético', 4),
            ('Alquiler', 5),
        ]
        for opt, pts in x7_opts:
            OpcionSocioeconomica.objects.create(variable='tenencia_vivienda', opcion_texto=opt, puntaje=pts)

        # X8: Tipo de vivienda
        x8_opts = [
            ('Casa', 2),
            ('Departamento', 2),
            ('Más de 4 hab.', 3),
            ('Más de 2 hab.', 4),
            ('1 habitación o pieza', 5),
        ]
        for opt, pts in x8_opts:
            OpcionSocioeconomica.objects.create(variable='tipo_vivienda', opcion_texto=opt, puntaje=pts)

        # X9: Lugar de procedencia
        x9_opts = [
            ('Ciudad', 13),
            ('Otro departamento', 14),
            ('Provincia', 15),
        ]
        for opt, pts in x9_opts:
            OpcionSocioeconomica.objects.create(variable='procedencia', opcion_texto=opt, puntaje=pts)

        self.stdout.write('Poblando reglas de desempate por defecto...')
        ReglaDesempate.objects.all().delete()
        ReglaDesempate.objects.create(nombre='Sin otro beneficio universitario', campo_modelo='postulante__ficha_socioeconomica__otro_beneficio', orden_ejecucion=1, direccion='asc')
        ReglaDesempate.objects.create(nombre='Mayor puntaje socioeconómico', campo_modelo='puntaje_socioeconomico', orden_ejecucion=2, direccion='desc')


        self.stdout.write('Inicializando parámetros globales...')
        ParametroBeca.objects.get_or_create(nombre='cupos_disponibles', defaults={'valor': 10.0, 'descripcion': 'Cantidad máxima de becas a asignar'})

        self.stdout.write(self.style.SUCCESS('¡Seeding completado con éxito!'))
