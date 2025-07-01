from django.urls import path
from . import views


urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('increver/<int:evento_id>/', views.inscrever, name='inscrever'),
    path('meus-eventos/', views.meus_eventos, name='meus_eventos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('evento/<int:id>/ingresso', views.gerar_ingresso, name='gerar_ingresso'),
    path('evento/<int:id>/cancelar-inscricao/', views.cancelar_inscricao, name='cancelar_inscricao'),   
]