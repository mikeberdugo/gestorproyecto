from django.urls import path

from . import views

urlpatterns = [
    path('',views.Login,name='login'),
    #admin
    path('project/administrator',views.inicio_administrador,name='inicio_administrator'),
    path('project/asignar/new',views.asignar,name='asignar'),
    path('project/asignar/reassign/<str:codigo>',views.dobleasignar,name='dobleasignar'),

    ## gerente
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

    path('project/project/<str:codigo>/financial/',views.costos,name='costos'),
    path('project/project/<str:codigo>/costs/new',views.nuevocosto,name='nuevocosto'),
    path('project/project/<str:codigo>/income/new',views.ingreso,name='ingreso'),
    path('project/project/<str:codigo>/costs/ingreso/',views.ingresobutton,name='ingresobutton'),
    path('project/project/<str:codigo>/costs/costo/',views.costobutton,name='costobutton'),
    path('project/project/<str:codigo>/costs/resumen/',views.resumenbutton,name='resumenbutton'),


    ## comunicacion
    path('project/project/<str:codigo>/documentation/',views.docu,name='docu'),
    path('project/project/<str:codigo>/documentation/new',views.nuevodocu,name='nuevodocu'),

    ## comunicacion
    path('project/project/<str:codigo>/communication/',views.comu,name='comu'),
    path('project/project/<str:codigo>/communication/new',views.formatocomunica,name='formatocomunica'),


    path('project/project/<str:codigo>/des/',views.des,name='des'),
    path('project/project/<str:codigo>/des/new',views.nuevoitems,name='nuevoitems'),
    path('project/project/<str:codigo>/des/gantt',views.gantt,name='gantt'),
    path('project/project/<str:codigo>/des/edit/<str:id_items>',views.edititems,name='edititems'),

    path('project/project/<str:codigo>/des/kanban/<str:titulo>',views.kanban,name='kanban'),
    #path('project/project/<str:codigo>/des/kanban/new/<str:columna_id>/',views.nuevahito,name='nuevohito'),
    #path('tarjeta/<int:tarjeta_id>/mover/<int:columna_id>/', views.mover_tarjeta, name='mover_tarjeta'),
    #path('project/project/<str:codigo>/des/gatt',views.nuevodocu,name='nuevodocu'),



    ## WORKFLOW
    path('prueba/WORKFLOW',views.word,name='word'),
    ## apis apiriesgo

    path('2f7bc198e14ca3e5d39bd4d14a12ff5b6d5f6842',views.apiproyecto),
    path('5f45e63af89a32b95c728671e0d4b7af',views.apitareas),
    path('a2b7f4e81d6c9e3a5f8b2d4c6e7a1b9f',views.apiriesgo),

    path('3c9a7e5b2f8d1a4c7e9b3d5c7f2e8a1',views.apicostos),
    path('b6d3f8a1e5c7f2b9d2a4c6e8b1f9d4',views.apiriesgo),
    path('8e1a5c7f3b6d9e2a4c7e8b1f9d3c5',views.apicarga),
    # power bi
    path('project/project/<str:codigo>/infor',views.informe,name='informe'),

    ## server
    path('logout/', views.Logout, name='logout'),
]

















