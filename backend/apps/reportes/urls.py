from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('',          views.DashboardReportesView.as_view(), name='dashboard'),
    path('csv/',      views.ExportarCSVView.as_view(),       name='exportar_csv'),
    path('excel/',    views.ExportarExcelView.as_view(),     name='exportar_excel'),
]
