from django.contrib import admin


from .models import *
from .forms import *

class ElegirRespuestaInLine(admin.TabularInline):
    model      = ElegirRespuesta 
    can_delete = False
    max_num    = ElegirRespuesta.MAX_RESPUESTA
    min_num    = ElegirRespuesta.MAX_RESPUESTA
    formset    = ElegirInlineFormser

class PreguntaAdmin(admin.ModelAdmin):
    model         = Pregunta
    inlines       = (ElegirRespuestaInLine,)
    list_display  = ['textoPregunta',]
    search_fields = ['textoPregunta', 'preguntas__textoRespuesta']

class PreguntaRespondidaAdmin(admin.ModelAdmin):
    list_display = ['pregunta','respuesta', 'correcta', 'puntajeOtenido']

    class meta:
        model = PreguntasRespondida



admin.site.register(PreguntasRespondida)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(Categoria)
admin.site.register(QuizUsuario)
