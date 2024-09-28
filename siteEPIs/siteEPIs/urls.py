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
]