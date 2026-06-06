from django.urls import path
from . import views

app_name = 'postulantes'

urlpatterns = [
    path('',                  views.PanelPostulanteView.as_view(),       name='panel'),
    path('datos-personales/', views.DatosPersonalesView.as_view(),       name='datos_personales'),
    path('datos-academicos/', views.DatosAcademicosView.as_view(),       name='datos_academicos'),
    path('datos-socioeconomicos/', views.DatosSocioeconomicosView.as_view(), name='datos_socioeconomicos'),
]
