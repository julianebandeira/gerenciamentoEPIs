from django.contrib import admin
from django.urls import path, include
from epis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('colaboradores/', views.colaboradores, name='colaboradores'),
    path('epis/', views.epis, name='epis'),  # Corrigido
    path('entrega/', views.entrega, name='entrega'),  # Corrigido
    path('avisos/', views.avisos, name='avisos'),
    path('gerar-relatorio/', views.gerar_relatorio, name='gerar_relatorio'),
    path('editar-colaboradores/', views.editar_colaboradores, name='editar_colaboradores'),
    path('editar-colaborador/<int:colaborador_id>/', views.editar_colaborador, name='editar_colaborador'),
    path('excluir-colaborador/<int:colaborador_id>/', views.excluir_colaborador, name='excluir_colaborador'),
    path('editar-epis/', views.editar_epis, name='editar_epis'),
    path('editar-epi/<int:epi_id>/', views.editar_epi, name='editar_epi'),
    path('excluir-epi/<int:epi_id>/', views.excluir_epi, name='excluir_epi'),
    path('consultar-entrega/', views.consultar_entrega, name='consultar_entrega'),
    path('editar-entrega/<int:entrega_id>/', views.editar_entrega, name='editar_entrega'),
    path('gerar_relatorio/', views.gerar_relatorio, name='gerar_relatorio'),
    path('relatorio-entregas/', views.relatorio_entregas, name='relatorio_entregas'),
    
]