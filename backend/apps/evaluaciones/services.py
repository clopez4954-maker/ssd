"""
Servicio de evaluación automática de becas.
Contiene la lógica del modelo matemático parametrizable.
"""
from decimal import Decimal
from django.utils import timezone
from apps.parametros.models import ParametroBeca
from apps.evaluaciones.models import Evaluacion


PUNTOS_ESTRATO = {1: 15, 2: 12, 3: 8, 4: 4, 5: 0, 6: 0}


def calcular_puntaje(postulante, parametros: dict) -> dict:
    """
    Calcula el puntaje de un postulante según el modelo parametrizable.

    Args:
        postulante: instancia de Postulante con datos_academicos y datos_socioeconomicos.
        parametros: dict {nombre_parametro: valor_float}

    Returns:
        dict con p_academico, p_socioeconomico, p_total, estado
    """
    acad = postulante.datos_academicos
    socio = postulante.datos_socioeconomicos

    promedio_min = parametros.get('promedio_minimo', 3.0)
    ingreso_max = parametros.get('ingreso_maximo', 4000000)
    peso_acad = parametros.get('peso_academico', 1.0)
    peso_socio = parametros.get('peso_socioeconomico', 1.0)
    corte = parametros.get('puntaje_corte_aprobado', 60.0)

    promedio = float(acad.promedio)

    # Restricción: promedio mínimo
    if promedio < promedio_min:
        return {
            'p_academico': Decimal('0.00'),
            'p_socioeconomico': Decimal('0.00'),
            'p_total': Decimal('0.00'),
            'estado': Evaluacion.ESTADO_RECHAZADO,
        }

    # ── Puntaje Académico ──────────────────────────────────────────────
    # Hasta 40 pts por promedio + hasta 20 pts por créditos
    p_promedio = (promedio / 5.0) * 40.0
    p_creditos = min((float(acad.creditos_aprobados) / 30.0) * 20.0, 20.0)
    p_academico = p_promedio + p_creditos  # máximo 60

    # ── Puntaje Socioeconómico ─────────────────────────────────────────
    # Hasta 25 pts por ingreso + hasta 15 pts por estrato
    ratio_ingreso = float(socio.ingreso_familiar) / ingreso_max
    ratio_ingreso = min(ratio_ingreso, 0.95)
    p_ingreso = (1.0 - ratio_ingreso) * 25.0

    p_estrato = PUNTOS_ESTRATO.get(socio.estrato, 0)
    p_socioeconomico = p_ingreso + p_estrato  # máximo 40

    # ── Puntaje Total ──────────────────────────────────────────────────
    p_total = (p_academico * peso_acad) + (p_socioeconomico * peso_socio)

    estado = (
        Evaluacion.ESTADO_APROBADO
        if p_total >= corte
        else Evaluacion.ESTADO_RECHAZADO
    )

    return {
        'p_academico': Decimal(str(round(p_academico, 2))),
        'p_socioeconomico': Decimal(str(round(p_socioeconomico, 2))),
        'p_total': Decimal(str(round(p_total, 2))),
        'estado': estado,
    }


class EvaluacionService:
    """Servicio de alto nivel para evaluar postulantes."""

    @classmethod
    def evaluar(cls, postulante, evaluado_por=None):
        """
        Evalúa un postulante individual y guarda/actualiza su Evaluacion.
        Retorna la instancia de Evaluacion guardada.
        """
        if not hasattr(postulante, 'datos_academicos') or \
           not hasattr(postulante, 'datos_socioeconomicos'):
            raise ValueError(
                f'El postulante {postulante} no tiene datos académicos o socioeconómicos completos.'
            )

        parametros = ParametroBeca.get_dict()
        resultado = calcular_puntaje(postulante, parametros)

        evaluacion, _ = Evaluacion.objects.get_or_create(
            postulante=postulante,
            defaults={'convocatoria': postulante.convocatoria},
        )
        evaluacion.puntaje_academico = resultado['p_academico']
        evaluacion.puntaje_socioeconomico = resultado['p_socioeconomico']
        evaluacion.puntaje_total = resultado['p_total']
        evaluacion.estado = resultado['estado']
        evaluacion.fecha_evaluacion = timezone.now()
        evaluacion.evaluado_por = evaluado_por
        evaluacion.save()

        # Marcar datos completos en el postulante
        postulante.datos_completos = True
        postulante.save(update_fields=['datos_completos'])

        return evaluacion

    @classmethod
    def reevaluar_masivo(cls, queryset, evaluado_por=None):
        """
        Reevalúa todos los postulantes de un queryset.
        Retorna (evaluados, errores) como listas.
        """
        evaluados = []
        errores = []

        for postulante in queryset.prefetch_related(
            'datos_academicos', 'datos_socioeconomicos'
        ):
            try:
                ev = cls.evaluar(postulante, evaluado_por=evaluado_por)
                evaluados.append(ev)
            except Exception as exc:
                errores.append({'postulante': postulante, 'error': str(exc)})

        return evaluados, errores
