from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from apps.convocatorias.models import Convocatoria
from apps.usuarios.models import LogAccion


def home(request):
    # Obtener la convocatoria activa actual (o la más reciente si no hay activa)
    convocatoria = Convocatoria.objects.filter(activa=True).first()
    if not convocatoria:
        convocatoria = Convocatoria.objects.order_by('-fecha_inicio').first()

    # No POST request handling needed as contact form was removed

    # Fechas por defecto si no hay convocatoria en base de datos
    cronograma = []
    if convocatoria:
        cronograma = [
            {'evento': 'Apertura de Convocatoria', 'fecha': convocatoria.fecha_inicio},
            {'evento': 'Cierre de Inscripciones', 'fecha': convocatoria.fecha_fin},
            {'evento': 'Evaluación de Solicitudes', 'fecha': convocatoria.fecha_fin + timezone.timedelta(days=7)},
            {'evento': 'Publicación de Resultados', 'fecha': convocatoria.fecha_fin + timezone.timedelta(days=12)},
        ]
    else:
        hoy = timezone.now().date()
        cronograma = [
            {'evento': 'Apertura de Convocatoria', 'fecha': hoy},
            {'evento': 'Cierre de Inscripciones', 'fecha': hoy + timezone.timedelta(days=30)},
            {'evento': 'Evaluación de Solicitudes', 'fecha': hoy + timezone.timedelta(days=37)},
            {'evento': 'Publicación de Resultados', 'fecha': hoy + timezone.timedelta(days=42)},
        ]

    context = {
        'convocatoria': convocatoria,
        'cronograma': cronograma,
    }
    return render(request, 'landing/home.html', context)
