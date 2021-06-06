from django.urls import path, include
from aplicaciones.principal import views

urlpatterns = [
    path('', views.diario, name='index'),
    path('reporteDiario', views.reporteDiarioDetail, name='reporteDiario'),
    path('reporteFechas', views.reporteFechas, name='reporteFechas'),
    path('reporteGeneral', views.reporteGeneral, name='reporteGeneral'),
    path('listarReportes', views.reportesList, name='listarReportes'),
    path('detalleReporte/<int:pk>',
         views.reportesDiariosDetail, name='detalleReporte'),
    path('eliminarReporte/<int:pk>',
         views.reporteDiarioDelete, name='eliminarReporte'),
    path('listarReportesGen', views.reportesGenList, name='listarReportesGen'),
    path('detalleReporteGen/<int:pk>',
         views.reportesGenDetail, name='detalleReporteGen'),
    path('eliminarReporteGen/<int:pk>',
         views.reporteGenDelete, name='eliminarReporteGen'),
    path('updateAgua/<int:pk>',
         views.updateAgua, name='updateAgua'),
    path('updateEjercicio/<int:pk>',
         views.updateEjercicio, name='updateEjercicio'),
    path('updateSleep/<int:pk>',
         views.updateSleep, name='updateSleep'),
    path('notificacionAgua/<int:pk>',
         views.notificacionAgua, name='notificacionAgua'),
]
