from django.urls import path

from . import views

urlpatterns = [
    path('',views.Login,name='login'),
    #admin
    path('project/administrator',views.inicio_administrador,name='inicio_administrator'),
    path('project/asignar/new',views.asignar,name='asignar'),
    path('project/asignar/reassign/<str:codigo>',views.dobleasignar,name='dobleasignar'),

    ## gerente
    path('project/comunicaciones',views.comunicacion,name='comunicaciones'),
    path('project/manager/<str:id_gerente>/', views.inicio_gerente, name='inicio_manager'),
    path('project/new/<str:codigo>/<str:id_gerente>/',views.nuevoproyecto,name='nuevoproyecto'),

    path('project/project/<str:codigo>/',views.proyecto,name='project'),
    #! falta kanbas rama test
    path('project/project/<str:codigo>/risks/',views.riesgos,name='riesgos'),
    path('project/project/<str:codigo>/risks/new',views.nuevomatriz,name='nuevomatriz'),
    path('project/project/<str:codigo>/risks/edit/<str:id_riesgo>',views.editmatriz,name='editmatriz'),



    path('project/project/<str:codigo>/lessons/',views.leccionesprojec,name='leccionesprojec'),
    path('project/project/<str:codigo>/lessons/edit/<str:id_lesson>',views.leccioneseditar,name='leccioneseditar'),
    path('project/project/lessons/all/<str:id_gerente>',views.leccionesprojecall,name='leccionesprojecall'),
    path('project/project/<str:codigo>/lessons/new',views.nuevalencion,name='nuevalencion'),

    path('project/project/<str:codigo>/costs/',views.costos,name='costos'),
    path('project/project/<str:codigo>/costs/new',views.nuevocosto,name='nuevocosto'),

    ## comunicacion
    path('project/project/<str:codigo>/documentation/',views.docu,name='docu'),
    path('project/project/<str:codigo>/documentation/new',views.nuevodocu,name='nuevodocu'),

    ## comunicacion
    path('project/project/<str:codigo>/communication/',views.comu,name='comu'),
    path('project/project/<str:codigo>/communication/new',views.nuevacomu,name='nuevacomu'),
    path('project/project/<str:codigo>/communication/formulario',views.formatocomunica,name='formatocomunica'),


    path('project/project/<str:codigo>/des/',views.des,name='des'),
    path('project/project/<str:codigo>/des/new',views.nuevoitems,name='nuevoitems'),
    path('project/project/<str:codigo>/des/gantt',views.gantt,name='gantt'),
    path('project/project/<str:codigo>/des/edit/<str:id_items>',views.edititems,name='edititems'),

    path('project/project/<str:codigo>/des/kanban/<str:titulo>',views.kanban,name='kanban'),
    #path('project/project/<str:codigo>/des/kanban/new/<str:columna_id>/',views.nuevahito,name='nuevohito'),
    #path('tarjeta/<int:tarjeta_id>/mover/<int:columna_id>/', views.mover_tarjeta, name='mover_tarjeta'),
    #path('project/project/<str:codigo>/des/gatt',views.nuevodocu,name='nuevodocu'),



    ## server
    path('logout/', views.Logout, name='logout'),
]