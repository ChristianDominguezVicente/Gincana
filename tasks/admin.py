from django.contrib import admin
from .models import Gincana, Profesor, Verificacion, GincanaJugada

class GincanaAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha", )

# Register your models here.
admin.site.register(Gincana, GincanaAdmin)
admin.site.register(Profesor)
admin.site.register(Verificacion)
admin.site.register(GincanaJugada)