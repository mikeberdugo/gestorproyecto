from django.contrib import admin
from django.urls import path
from gestor.views import *
from gestor.pruebas import * 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Login, name='login'),
    path('project/administrator',inicio_administrador,name='inicio_administrator'),
    path('project/manager/<str:id_gerente>/', inicio_gerente, name='inicio_manager'),
    path('project/new/<str:codigo>',nuevoproyecto,name='nuevoproyecto'),
    path('project/create',crearprojecto,name='crearprojecto'),
    path('project/asignar/new',asignar,name='asignar'),
    path('project/12',diagrama,name='diagrama'),
    ## gestor de kanban 
    path('prueba',gestion,name='gesstion'),
    
    
]


### administrador , inicio_gerete  
