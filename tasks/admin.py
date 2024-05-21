from django.contrib import admin
from .models import Gincana, Profesor, Verificacion, GincanaJugada, Parada, Pregunta, Respuesta, Invitado, Puntuacion

class GincanaAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha", )

# Register your models here.
admin.site.register(Gincana, GincanaAdmin)
admin.site.register(Profesor)
admin.site.register(Verificacion)
admin.site.register(GincanaJugada)
admin.site.register(Parada)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Invitado)
admin.site.register(Puntuacion)
