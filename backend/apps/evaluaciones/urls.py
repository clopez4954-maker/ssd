from django.urls import path
from . import views

app_name = 'evaluaciones'

urlpatterns = [
    path('',                         views.ListaPostulantesView.as_view(),    name='lista'),
    path('<int:pk>/',                 views.DetallePostulanteView.as_view(),   name='detalle'),
    path('<int:pk>/evaluar/',         views.EvaluarPostulanteView.as_view(),   name='evaluar'),
    path('<int:pk>/editar/',          views.EditarPostulanteStaffView.as_view(), name='editar_postulante'),
    path('reevaluar-masivo/',         views.ReevaluarMasivoView.as_view(),    name='reevaluar_masivo'),
]
