from django.urls import path 
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('publicar', views.publicar, name='publicar')
]