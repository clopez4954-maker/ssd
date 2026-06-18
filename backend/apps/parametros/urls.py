from django.urls import path
from . import views

app_name = 'parametros'

urlpatterns = [
    path('',              views.ListaParametrosView.as_view(),  name='lista'),
    path('crear/',        views.CrearParametroView.as_view(),   name='crear'),
    path('<int:pk>/editar/', views.EditarParametroView.as_view(), name='editar'),
]
