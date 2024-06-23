from django.urls import path 
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cerrarSesion', views.cerrarSesion, name='cerrarSesion'),
    path('registroUsuario', views.registroUsuario, name='registroUsuario'),
    path('registrando1', views.registrando1, name='registrando1'),
    path('registrando2', views.registrando2, name='registrando2'),
    path('perfil', views.perfil, name='perfil'),
    path('editarPerfil', views.editarPerfil, name='editarPerfil'),
    path('publicacion/<int:publi_id>', views.publicacion, name='publicacion')
]