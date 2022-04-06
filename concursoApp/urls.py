from django.urls import path

from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('home/', home, name='home'),
    path('registro/', registro, name='registro'),
    path('logout/', loginView, name='login'),
    path('login/', logoutVista, name='logoutVista'),
    path('quiz/', quiz, name='quiz'),
    path('resultado/<int:preguntaRespondida_pk>/', resultadoPreguntas, name='resultado'),

    # path('formUsuario/', index, name='formRegistro'),
    # path('registroUser/', registrarUsuario, name='registro'),
    # path('preguntas/', preguntas, name='cuestionario'),

]
