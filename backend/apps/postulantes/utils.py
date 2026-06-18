from .models import DatosAcademicos
from apps.parametros.models import RangoPPS

def calcular_puntaje_academico(postulante):
    """
    Calcula el puntaje académico del postulante según su PPA y la cantidad de materias aprobadas.
    """
    materias = postulante.materias.all()
    if materias.exists():
        promedio = sum(m.nota for m in materias) / materias.count()
        aprobadas = materias.filter(nota__gte=51.0).count()
    else:
        promedio = 0.0
        aprobadas = 0

    # 1. Puntaje por PPA (máx 25)
    rango_pps = RangoPPS.objects.filter(desde__lte=promedio, hasta__gte=promedio).first()
    puntaje_ppa = rango_pps.puntaje if rango_pps else 0.0

    # 2. Puntaje por materias aprobadas (máx 5)
    if aprobadas >= 6:
        puntaje_materias = 5.0
    elif aprobadas >= 4:
        puntaje_materias = 4.0
    elif aprobadas >= 2:
        puntaje_materias = 3.0
    elif aprobadas == 1:
        puntaje_materias = 2.0
    else:
        puntaje_materias = 0.0

    total = puntaje_ppa + puntaje_materias

    # Guardar en DatosAcademicos
    datos_acad, _ = DatosAcademicos.objects.get_or_create(
        postulante=postulante,
        defaults={'ppa': 0.0, 'materias_aprobadas': 0}
    )
    datos_acad.ppa = promedio
    datos_acad.materias_aprobadas = aprobadas
    datos_acad.puntaje_ppa = puntaje_ppa
    datos_acad.puntaje_materias = puntaje_materias
    datos_acad.puntaje_academico_total = total
    datos_acad.save()

    return {
        'promedio': promedio,
        'aprobadas': aprobadas,
        'puntaje_ppa': puntaje_ppa,
        'puntaje_materias': puntaje_materias,
        'total': total,
    }

def calcular_ppa_y_materias(postulante):
    # Wrapper para compatibilidad
    return calcular_puntaje_academico(postulante)
