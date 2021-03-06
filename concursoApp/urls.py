from django.urls import path
from .views      import *

urlpatterns = [
    path('', inicio, name='inicio'),
    
    path('home/', home, name='home'),
    path('registro/', registro, name='registro'),
    path('login/', loginView, name='login'),
    path('logout/', logoutVista, name='logout'),
    
    path('quiz/', quiz, name='quiz'),
    path('salir/', retirarse, name='salir'),
    path('tablero/', tablero, name='tablero'),
    path('resultado/<int:preguntaRespondida_pk>', resultadoPreguntas, name='resultado'),

]
