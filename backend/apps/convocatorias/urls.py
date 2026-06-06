from django.urls import path
from . import views

app_name = 'convocatorias'

urlpatterns = [
    path('',              views.ListaConvocatoriasView.as_view(), name='lista'),
    path('crear/',        views.CrearConvocatoriaView.as_view(),  name='crear'),
    path('<int:pk>/editar/', views.EditarConvocatoriaView.as_view(), name='editar'),
]
