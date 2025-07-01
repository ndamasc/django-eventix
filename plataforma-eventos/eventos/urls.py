from django.urls import path
from .views import TrocarSenhaView
from . import views


urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('increver/<int:evento_id>/', views.inscrever, name='inscrever'),
    path('meus-eventos/', views.meus_eventos, name='meus_eventos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('evento/<int:id>/ingresso', views.gerar_ingresso, name='gerar_ingresso'),
    path('evento/<int:id>/solicitar-cancelamento/', views.solicitar_cancelamento, name='solicitar_cancelamento'),
    path('evento/<int:id>/confirmar-cancelamento/', views.confirmar_cancelamento, name='confirmar_cancelamento'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/senha/', TrocarSenhaView.as_view(), name='alterar_senha'),

]