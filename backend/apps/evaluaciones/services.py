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

    NOTA: La Ficha Socioeconómica IDH ha cambiado todos sus campos (ahora son de 10 puntos).
    Por ahora, el cálculo automático se suspende y retorna 0 hasta que se definan 
    nuevos parámetros de evaluación para este nuevo formato.
    """
    return {
        'p_academico': Decimal('0.00'),
        'p_socioeconomico': Decimal('0.00'),
        'p_total': Decimal('0.00'),
        'estado': Evaluacion.ESTADO_PENDIENTE,
    }


class EvaluacionService:
    """Servicio de alto nivel para evaluar postulantes."""

    @classmethod
    def evaluar(cls, postulante, evaluado_por=None):
        """
        Evalúa un postulante individual y guarda/actualiza su Evaluacion.
        Retorna la instancia de Evaluacion guardada.
        """
        if not hasattr(postulante, 'ficha_socioeconomica'):
            raise ValueError(
                f'El postulante {postulante} no tiene ficha socioeconómica completa.'
            )

        parametros = ParametroBeca.get_dict()
        resultado = calcular_puntaje(postulante, parametros)

        from apps.postulantes.views import calcular_y_guardar_puntaje
        sol = calcular_y_guardar_puntaje(postulante)
        
        # Guardar una copia compatible en Evaluacion para evitar errores en otras partes
        evaluacion, _ = Evaluacion.objects.get_or_create(
            postulante=postulante,
            defaults={'convocatoria': postulante.convocatoria},
        )
        evaluacion.puntaje_academico = sol.puntaje_academico
        evaluacion.puntaje_socioeconomico = sol.puntaje_socioeconomico
        evaluacion.puntaje_total = sol.puntaje_total
        evaluacion.estado = 'aprobado' if sol.estado == 'Beca Asignada' else 'pendiente'
        evaluacion.fecha_evaluacion = timezone.now()
        evaluacion.evaluado_por = evaluado_por
        evaluacion.save()

        return sol

    @classmethod
    def reevaluar_masivo(cls, queryset, evaluado_por=None):
        """
        Reevalúa todos los postulantes de un queryset.
        Retorna (evaluados, errores) como listas.
        """
        evaluados = []
        errores = []

        for postulante in queryset:
            try:
                ev = cls.evaluar(postulante, evaluado_por=evaluado_por)
                evaluados.append(ev)
            except Exception as exc:
                errores.append({'postulante': postulante, 'error': str(exc)})

        return evaluados, errores
