from django.urls import path
from . import views

app_name = 'evaluaciones'

urlpatterns = [
    path('',                         views.ListaPostulantesView.as_view(),    name='lista'),
    path('panel-evaluador/',         views.PanelEvaluadorView.as_view(),      name='panel_evaluador'),
    path('optimizar/',               views.EjecutarOptimizacionView.as_view(), name='optimizar'),
    path('exportar-excel/',          views.ExportarExcelView.as_view(),       name='exportar_excel'),
    path('ranking/',                 views.RankingPostulantesView.as_view(),  name='ranking_postulantes'),
    path('ranking/exportar/',        views.ExportarRankingExcelView.as_view(), name='exportar_ranking_excel'),
    path('<int:pk>/',                 views.DetallePostulanteView.as_view(),   name='detalle'),
    path('<int:pk>/evaluar/',         views.EvaluarPostulanteView.as_view(),   name='evaluar'),
    path('<int:pk>/editar/',          views.EditarPostulanteStaffView.as_view(), name='editar_postulante'),
    path('<int:pk>/rechazar-postulante/', views.rechazar_postulante,            name='rechazar_postulante'),
    path('<int:pk>/reactivar-postulante/', views.reactivar_postulante,          name='reactivar_postulante'),
    path('reevaluar-masivo/',         views.ReevaluarMasivoView.as_view(),    name='reevaluar_masivo'),
]

