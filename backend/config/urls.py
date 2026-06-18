from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from apps.usuarios.views import (
    RegistroPostulanteView,
)
from apps.evaluaciones.views import (
    PanelEvaluadorView,
    EjecutarOptimizacionView,
    ExportarExcelView,
    RankingPostulantesView,
    ExportarRankingExcelView
)
from apps.postulantes.views import RegistroMateriasView

urlpatterns = [
    # Registro de materias root-level path
    path('registro-materias/', RegistroMateriasView.as_view(), name='registro_materias'),

    # Vistas de Evaluador Personalizadas
    path('panel-evaluador/', PanelEvaluadorView.as_view(), name='panel_evaluador'),
    path('optimizar/', EjecutarOptimizacionView.as_view(), name='optimizar'),
    path('exportar-excel/', ExportarExcelView.as_view(), name='exportar_excel'),
    path('ranking/', RankingPostulantesView.as_view(), name='ranking_postulantes'),
    path('ranking/exportar/', ExportarRankingExcelView.as_view(), name='exportar_ranking_excel'),

    # Admin de Django
    path('admin/', admin.site.urls),

    # Landing page (página de inicio pública)
    path('', include('apps.landing.urls', namespace='landing')),
    path('registro/', RegistroPostulanteView.as_view(), name='registro'),



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
