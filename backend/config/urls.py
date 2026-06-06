from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),

    # Redirección de raíz al dashboard o login
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),

    # Apps
    path('usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('dashboard/', include('apps.postulantes.urls', namespace='postulantes')),
    path('evaluador/', include('apps.evaluaciones.urls', namespace='evaluaciones')),
    path('parametros/', include('apps.parametros.urls', namespace='parametros')),
    path('reportes/', include('apps.reportes.urls', namespace='reportes')),
    path('convocatorias/', include('apps.convocatorias.urls', namespace='convocatorias')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
