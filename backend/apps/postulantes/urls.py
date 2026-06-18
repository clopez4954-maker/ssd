from django.urls import path
from . import views

app_name = 'postulantes'

urlpatterns = [
    path('', views.PanelPostulanteView.as_view(), name='panel'),
    path('ficha-socioeconomica/', views.FichaSocioeconomicaView.as_view(), name='ficha_socioeconomica'),
    path('mi-postulacion/', views.MiPostulacionView.as_view(), name='mi_postulacion'),
    path('registro-materias/', views.RegistroMateriasView.as_view(), name='registro_materias'),
]

