from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('project/project/<str:id_proyect>/',proyecto,name='project'),
    path('project/project/<str:id_project>/kanban', kanban, name='kanban'),
     path('tarjeta/<int:tarjeta_id>/mover/<int:columna_id>/', mover_tarjeta, name='mover_tarjeta'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


### administrador , inicio_gerete
