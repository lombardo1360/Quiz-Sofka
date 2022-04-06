from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroFormulario, UsuarioLoginFormulario
from django.contrib.auth import authenticate, login, logout
import random
from .models import QuizUsuario, Pregunta, PreguntasRespondida

def inicio(request):
    return render(request, 'paginas/inicio.html')

def home(request):
    return render(request, 'paginas/home.html')

def quiz(request):
    
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        pregunta_pk        = request.POST.get('pregunta_pk')
        preguntaRespondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk       = request.POST.get('respuesta_pk')
        
        try:
            optionSeleccionada = preguntaRespondida.pregunta.opciones.get(pk=respuesta_pk) 
        except ObjectDoesNotExiste:
            raise Http404  
        
        QuizUser.validarIntentos(preguntaRespondida, optionSeleccionada)
        
        return redirect('resultado', preguntaRespondida.pk)
    
    else:
        pregunta = QuizUser.obtenerPreguntas()
        if pregunta is not None:
            QuizUser.crearIntento(pregunta)
            
        context = {
            'pregunta':pregunta
        }  
    return render(request, 'play/jugar.html', context)     

def resultadoPreguntas(request, preguntaRespondida_pk):
    respondida = get_object_or_404(PreguntasRespondida, pk=preguntaRespondida_pk )
    
    context={
        'respondida': respondida
    }
    
    return render(request, 'play/resultados.html', context)


def loginView(request):
    titulo = "login"
    form = UsuarioLoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect('home')        
    context = {
        'form':form,
        'titulo': titulo
    } 
    return render(request, 'paginas/login.html', context)

def registro(request):
    titulo = 'Crear cuenta'
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroFormulario()
    
    context = {
        'form':form,
        'titulo': titulo
    } 
    
    return render(request, 'paginas/registro.html', context)

def logoutVista(request):
    logout(request)
    return redirect('inicio')
        


    
