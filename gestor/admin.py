from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(Equipo)
admin.site.register(Proyecto)
admin.site.register(Grupo)
admin.site.register(Hito)
admin.site.register(Tarea)
admin.site.register(ComentarioTarea)
admin.site.register(MatrizRiesgo)
admin.site.register(Documentos)
admin.site.register(Tablero)
admin.site.register(Columna)
admin.site.register(Tarjeta)
admin.site.register(Recurso)

## nuevos modelos
admin.site.register(Des)
admin.site.register(Comunicacion)
admin.site.register(Acti)

## modelos costos
admin.site.register(Costos)
admin.site.register(Costosingresos)
admin.site.register(Costoscostos)
