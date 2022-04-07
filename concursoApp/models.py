from django.db                  import models
from django.conf                import settings 
from django.contrib.auth.models import User
import random 

#Modelos que formaran las tablas 

# Categoria de las preguntas
class Categoria(models.Model):
    nombreCategoria = models.TextField(max_length= 200, verbose_name='Categoria', null=False)

    def __str__(self):
        return self.nombreCategoria
    
# Preguntas con su categoria 
class Pregunta(models.Model):
    NUMERO_DE_RESPUESTAS_PERMITIDAS = 1
    textoPregunta     = models.TextField(verbose_name='Texto de la pregunta')
    categoriaPregunta = models.ForeignKey(Categoria, related_name="categorias", on_delete=models.CASCADE)
    max_puntaje       = models.DecimalField(verbose_name='maximo puntaje', default=3, decimal_places=2, max_digits=6)
    

    def __str__(self):
        
        return (self.textoPregunta)

#Elegir respuesta
class ElegirRespuesta(models.Model):
    MAX_RESPUESTA  = 4
    pregunta       = models.ForeignKey(Pregunta, related_name='opciones' ,on_delete=models.CASCADE) 
    textoRespuesta = models.TextField(verbose_name= 'Texto de la respuesta')
    correcta       = models.BooleanField(verbose_name= '¿Esta es la respuesta correcta?', default=False, null=False )

    def __str__(self):
        return self.textoRespuesta

#Clase que identifica el usuario con su puntaje obtenido
class QuizUsuario(models.Model):
    usuario      = models.OneToOneField(User, on_delete=models.CASCADE)
    puntajeTotal = models.DecimalField(verbose_name="Puntaje total", default=0, decimal_places=2, max_digits=10) 

    def crearIntento(self, pregunta):
        intento = PreguntasRespondida(pregunta=pregunta, usuario=self)
        intento.save()
                

    #Funcion que obtiene de todas las preguntas una al azar            
    def obtenerPreguntas(self):   
        categoria           = PreguntasRespondida.objects.filter(usuario=self).values_list('pregunta__categoriaPregunta', flat=True).distinct()
        preguntasRestantes  =Pregunta.objects.exclude(categoriaPregunta__in=categoria
                                                      )
        print(preguntasRestantes)
        if not preguntasRestantes.exists():
            return None
        return random.choice(preguntasRestantes)
    
    def validarIntentos(self, preguntaRespondida, respuestaSeleccionada):
        if preguntaRespondida.pregunta_id != respuestaSeleccionada.pregunta_id:
            return
        
        preguntaRespondida.respuestaSeleccionada = respuestaSeleccionada
        if respuestaSeleccionada.correcta is True:
            preguntaRespondida.correcta = True
            preguntaRespondida.puntajeObtenido = respuestaSeleccionada.pregunta.max_puntaje
            preguntaRespondida.respuesta = respuestaSeleccionada
        
        else:
            preguntaRespondida.respuesta = respuestaSeleccionada
        
        preguntaRespondida.save()
        
        self.actualizarPuntaje()
        
    def actualizarPuntaje(self):
        puntajeActualizado = self.intentos.filter(correcta=True).aggregate(
            models.Sum('puntajeObtenido'))['puntajeObtenido__sum']
        
        if puntajeActualizado == None:
            self.puntajeTotal = 0
            self.save
        else:           
            self.puntajeTotal = puntajeActualizado
            self.save()
            
# Clase que integra los demas modelos
class PreguntasRespondida(models.Model):
    usuario         = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
    pregunta        = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta       = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE,  null=True)
    correcta        = models.BooleanField(verbose_name='¿Esta es la respuesta correcta?',default=False, null=False)
    puntajeObtenido = models.DecimalField(verbose_name='Puntaje obtenido', default=1, decimal_places=2, max_digits=6)   


    
    