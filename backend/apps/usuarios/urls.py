from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/',    views.LoginPersonalizadoView.as_view(),  name='login'),
    path('logout/',   views.LogoutPersonalizadoView.as_view(), name='logout'),
    path('registro/', views.RegistroPostulanteView.as_view(), name='registro'),

    # Gestión de usuarios (administrador)
    path('gestion/',              views.GestionUsuariosView.as_view(),   name='gestion'),
    path('gestion/crear/',        views.CrearUsuarioStaffView.as_view(), name='crear_usuario'),
    path('gestion/<int:pk>/editar/', views.EditarUsuarioView.as_view(),  name='editar_usuario'),
    path('gestion/<int:pk>/toggle/', views.ToggleUsuarioView.as_view(),  name='toggle_usuario'),

    # Logs
    path('logs/', views.LogsView.as_view(), name='logs'),
]

