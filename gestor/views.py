from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout
#from .decorador import *
from .models import *
from collections import defaultdict
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone

## funciones propias
#from .mail import *
import random
import json
from datetime import datetime


def Login(request):
    # if request.user.is_authenticated:
    #     return redirect_to_appropriate_page(request, request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_to_appropriate_page(request, user)
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    return render(request, './user/login.html')


def Logout(request):
    logout(request)
    return redirect('main:login')


def redirect_to_appropriate_page(request, user):  # Asegúrate de que 'request' sea un parámetro de la función
    try:
        usuario = Usuario.objects.get(usuario=user)
        if usuario.rol == 'administrador':
            return redirect('main:inicio_administrator')
        elif usuario.rol == 'gerente':
            return redirect('main:inicio_manager', usuario.id)
        elif usuario.rol == 'miembro':
            return redirect('main:pagina_miembro')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')  # Asegúrate de usar 'request' aquí
    return redirect('main:login')

## admin

def inicio_administrador(request):
    gerentes = Usuario.objects.filter(rol='gerente')
    # Inicializar un diccionario para almacenar los conteos de proyectos por tipo para cada gerente
    project = Proyecto.objects.all()
    proyectos_por_gerente = []

    # Iterar sobre cada gerente
    for gerente in gerentes:
        tip1 = 0
        tip2 = 0
        tip3 = 0
        tip4 = 0

        proyectos = Proyecto.objects.filter(user=gerente)


        for proyecto in proyectos:
            if proyecto.tipo == 'Necesidades entrega operación':
                tip1 += 1
            elif proyecto.tipo == 'Necesidades':
                tip2 += 1
            elif proyecto.tipo == 'Proyectos Integración':
                tip3 += 1
            elif proyecto.tipo == 'Proyectos Producto Propio':
                tip4 += 1
            else:
                print("Error: Tipo de proyecto desconocido.")


        sumato = tip1 + tip2+ tip3 + tip4


        nombre_completo = f"{gerente.usuario.first_name} {gerente.usuario.last_name} "

        # Agregar los conteos al diccionario bajo la clave del gerente actual
        proyectos_por_gerente.append({
            'gerente': nombre_completo,
            'tip1': tip1,
            'tip2': tip2,
            'tip3': tip3,
            'tip4': tip4,
            'total': sumato
        })


    return render(request, "./user/inicio_administrador.html",{'gerentes':gerentes ,'proyectos_por_gerente':proyectos_por_gerente , 'proyecto': project })


def dobleasignar(request,codigo):
    gerentes = Usuario.objects.filter(rol='gerente')
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    print("protecto dir ", dir(proyecto))

    if request.method == 'POST':
        project_managers = request.POST.get('project-managers')
        manager = get_object_or_404(Usuario, id=project_managers)

        proyecto.user.add(manager)
        proyecto.save()

        #enviar_correo_post(usuario.id, proyecto1.codigo, 'tipo1')
        return redirect('main:inicio_administrator')

    return render(request, './user/reasignar.html', {'gerentes': gerentes ,'proyecto':proyecto })



def asignar(request):
    gerentes = Usuario.objects.filter(rol='gerente')
    if request.method == 'POST':
        project_name = request.POST.get('project-name')
        project_descrip = request.POST.get('project-descrip')
        project_type = request.POST.get('project-type')
        project_category = request.POST.get('project-category')
        project_managers = request.POST.get('project-managers')
        manager = get_object_or_404(Usuario, id=project_managers)
        while True:
            codigo = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            if not Proyecto.objects.filter(codigo=codigo).exists():
                break

        proyecto1 = Proyecto.objects.create(
            name=project_name,
            codigo=codigo,
            description=project_descrip,
            tipo=project_type,
            categoria=project_category,
            estado='abierto'
        )
        proyecto1.user.add(manager)
        proyecto1.save()
        # Llamar a la función para enviar el correo electrónico
        #enviar_correo_post(usuario.id, proyecto1.codigo, 'tipo1')
        return redirect('main:inicio_administrator')

    return render(request, './user/asignar.html', {'gerentes': gerentes})
## gerente
def inicio_gerente(request, id_gerente):
    gerente = Usuario.objects.get(id=id_gerente)
    proyectos = Proyecto.objects.filter(user=gerente)

    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',

    }
    return render(request, "./user/inicio_gerente.html", {'context':context , 'gerente':gerente , 'proyectos':proyectos} )






def nuevoproyecto(request, codigo , id_gerente):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    gluster = Grupo.objects.all()
    gerente = Usuario.objects.filter(id=id_gerente).first()


    context = {
        'codigo': proyecto.codigo,
        'name': proyecto.name ,
        'descr': proyecto.description,
    }


    if request.method == 'POST':
        if proyecto:
            proyecto.fecha_creacion =  timezone.now().strftime('%Y-%m-%d')
            proyecto.fecha_inicio_planeada = request.POST.get('project-start-date-planned')#*
            proyecto.fecha_finalizacion_planeada = request.POST.get('project-end-date-planned')
            proyecto.alcance = request.POST.get('project-scope')
            proyecto.estado = "abierto"
            proyecto.lider = request.POST.get('project-leader')
            proyecto.grupo = request.POST.get('project-group')
            proyecto.antecedentes = 'antecedentes'
            proyecto.fase = "ninguna"
            proyecto.comentarios = request.POST.get('project-comments')
            proyecto.porcentaje_completado = 0
            proyecto.columna = True
            proyecto.save()



        return redirect('main:inicio_manager', proyecto.user.id )
    # CLUSTER gluster
    return render(request, "./user/nuevoproyecto.html" , {'context':context , 'gerente': proyecto.user , 'gluster':gluster , 're':gerente} )


#* proyecto

def proyecto(request , codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    riesgos = MatrizRiesgo.objects.filter(proyecto=proyecto)
    ComentarioTareas = ComentarioTarea.objects.filter(proyecto=proyecto)

    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',

    }

    return render(request , './user/proyecto.html' ,{'context': context ,
                                                        'proyecto' : proyecto ,
                                                        'riesgos' : riesgos,
                                                        'ComentarioTareas' : ComentarioTareas,
                                                        })

##! parte oscar

def riesgos(request , codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    riesgo = MatrizRiesgo.objects.filter(proyecto=proyecto)
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',

    }

    return render(request , './user/riesgo.html' ,{'context': context , 'proyecto' : proyecto ,'riesgos':riesgo})

def nuevomatriz(request , codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',

    }

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_riesgo = request.POST.get('matriz-name')
        descripcion_riesgo = request.POST.get('matriz-descrip')
        causas_riesgo = request.POST.get('matriz-causas')
        plan = request.POST.get('matriz-mitigacion')
        descripcion_tiempo = request.POST.get('matriz-tiempo')
        descripcion_alcance = request.POST.get('matriz-impact')
        descripcion_costo = request.POST.get('matriz-costo')
        probabilidad = request.POST.get('matriz-probabilidad')
        gravedad = request.POST.get('matriz-gravedad')


        # Convertir probabilidad y gravedad a enteros
        probabilidad = int(probabilidad)
        gravedad = int(gravedad)

        riesgo_basico = (probabilidad * gravedad)

        if riesgo_basico >= 1 and riesgo_basico <= 2:
            nivel = 'Marginal'
        elif riesgo_basico >= 3 and riesgo_basico <= 8:
            nivel = 'Apreciable'
        elif riesgo_basico >= 9 and riesgo_basico <= 14:
            nivel = 'Importante'
        elif riesgo_basico >= 15 and riesgo_basico <= 25:
            nivel = 'Muy Grabe'
        else:
            nivel = 'Error'

        nuevo_riesgo = MatrizRiesgo(
            nombre=nombre_riesgo,
            descripcion=descripcion_riesgo,
            causas=causas_riesgo,
            plan=plan,
            descripcion_tiempo=descripcion_tiempo,
            descripcion_alcance=descripcion_alcance,
            descripcion_costo=descripcion_costo,
            probavilidad=probabilidad,
            gravedad=gravedad,
            proyecto=proyecto,
            riesgo = nivel
        )
        # Guardar el nuevo riesgo en la base de datos
        nuevo_riesgo.save()
        return redirect('main:riesgos', proyecto.codigo )

    return render(request , './user/nuevoriesgo.html' ,{'context': context , 'proyecto' : proyecto })

def editmatriz(request,codigo,id_riesgo):
    riesgo = get_object_or_404(MatrizRiesgo, pk=id_riesgo)
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    if request.method == 'POST':
        nuevo_materializo = request.POST.get('materializo', '')
        nuevo_acciones_mitigacion = request.POST.get('acciones_mitigacion', '')
        nuevo_consecuencias = request.POST.get('consecuencias', '')

        if nuevo_materializo:
            riesgo.materializo = actualizar_comentario(riesgo.materializo, nuevo_materializo)
        if nuevo_acciones_mitigacion:
            riesgo.acciones_mitigacion = actualizar_comentario(riesgo.acciones_mitigacion, nuevo_acciones_mitigacion)
        if nuevo_consecuencias:
            riesgo.consecuencias = actualizar_comentario(riesgo.consecuencias, nuevo_consecuencias)

        riesgo.save()
        return redirect('main:riesgos', proyecto.codigo)

    return render(request, "./user/editmatriz.html", {'proyecto': proyecto})

def actualizar_comentario(comentario_existente, nuevo_texto):
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if comentario_existente:
        return f"{comentario_existente}\n{fecha_actual}: {nuevo_texto}"
    else:
        return f"{fecha_actual}: {nuevo_texto}"


##! parte brayan

def leccionesprojec(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    info = ComentarioTarea.objects.filter(proyecto=proyecto)
    return render(request, "./user/leccionesproject.html",{'ComentarioTareas': info,'proyecto' : proyecto })

def nuevalencion(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    if request.method == 'POST':
        nombre_riesgo = request.POST.get('identificando_problema')
        descripcion_riesgo = request.POST.get('causa')
        plan = request.POST.get('solucion')
        descripcion_tiempo = request.POST.get('planes_mejora_aplicados')
        descripcion_costo = request.POST.get('resultados_planes_mejora')
        fecha_creacion = timezone.now().strftime('%Y-%m-%d')
        # YYYY-MM-DD.

        nueva = ComentarioTarea (
            proyecto = proyecto,
            identificando_problema = nombre_riesgo,
            causa = descripcion_riesgo ,
            solucion = plan ,
            planes_mejora_aplicados = descripcion_tiempo,
            resultados_planes_mejora = descripcion_costo,
            fecha_creacion = fecha_creacion
            )
        nueva.save()

        return redirect('main:leccionesprojec', proyecto.codigo )
    return render(request, "./user/nuevaLeccion.html",{'proyecto' : proyecto })

def leccioneseditar(request, codigo, id_lesson):
    comentario = get_object_or_404(ComentarioTarea, pk=id_lesson)
    proyecto = Proyecto.objects.filter(codigo=codigo).first()

    if request.method == 'POST':
        nuevo_plan = request.POST.get('solucion', '')
        nuevo_descripcion_tiempo = request.POST.get('planes_mejora_aplicados', '')
        nuevo_descripcion_costo = request.POST.get('resultados_planes_mejora', '')

        if nuevo_plan:
            comentario.solucion = actualizar_comentario(comentario.solucion, nuevo_plan)

        if nuevo_descripcion_tiempo:
            comentario.planes_mejora_aplicados = actualizar_comentario(comentario.planes_mejora_aplicados, nuevo_descripcion_tiempo)

        if nuevo_descripcion_costo:
            comentario.resultados_planes_mejora = actualizar_comentario(comentario.resultados_planes_mejora, nuevo_descripcion_costo)

        comentario.save()
        return redirect('main:leccionesprojec', proyecto.codigo)

    return render(request, "./user/editlessons.html", {'proyecto': proyecto})

def actualizar_comentario(comentario_existente, nuevo_texto):
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if comentario_existente:
        return f"{comentario_existente}\n{fecha_actual}: {nuevo_texto}"
    else:
        return f"{fecha_actual}: {nuevo_texto}"



def leccionesprojecall(request,id_gerente):
    gerente = Usuario.objects.get(id=id_gerente)
    info = ComentarioTarea.objects.all()
    return render(request, "./user/leccionesall.html",{'ComentarioTareas': info,'gerente':gerente })

##* costos

def costos(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    costo = Costos.objects.filter(proyecto=proyecto).filter()
    return render(request, "./user/costos.html",{'costos':costo ,'proyecto' : proyecto })


def nuevocosto(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()

    if request.method == 'POST':
        contrato = request.POST.get('contrato')
        objeto = request.POST.get('objeto')
        tipo = request.POST.get('tipo')
        aliado = request.POST.get('aliado')
        contrato_aliado = request.POST.get('contrato_aliado')
        backlog = request.POST.get('backlog')
        one_time = request.POST.get('one_time')
        recurrente = request.POST.get('recurrente')
        meses = request.POST.get('meses')

        # Crear el objeto Costos y guardarlo en la base de datos
        costo = Costos.objects.create(
            contrato=contrato,
            objeto=objeto,
            tipo=tipo,
            aliado=aliado,
            contrato_aliado=contrato_aliado,
            backlog=backlog,
            one_time=one_time,
            recurrente=recurrente,
            meses=meses,
            proyecto = proyecto
        )

        costo.save()
        return redirect('main:costos', proyecto.codigo )


    return render(request, "./user/neuvocosto.html",{'proyecto' : proyecto })

def docu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    docus = Documentos.objects.filter(proyecto=proyecto)
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        link = request.POST.get('url')

        documento = Documentos(titulo=titulo,
                            descriocion=descripcion,
                            link=link,
                            proyecto=proyecto)
        documento.save()

        return redirect('main:docu', proyecto.codigo )
    return render(request, "./user/docu.html",{'docus':docus ,'proyecto' : proyecto })

def nuevodocu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    costo = Costos.objects.filter(proyecto=proyecto)
    return render(request, "./user/costos.html",{'costos':costo ,'proyecto' : proyecto })

## comunicaciones
def comu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    return render(request, "./user/comu.html",{'proyecto' : proyecto })

def nuevacomu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    return render(request, "./user/comunicaciones.html",{'proyecto' : proyecto })

def comunicacion(request):
    return render(request, "./user/comunicaciones.html")

def formatocomunica(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    return render(request, "./user/formatocomunica.html",{'proyecto' : proyecto })

#nueva gestion

def gantt(request, codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    des = Des.objects.filter(codigo=codigo)
    datos_tareas = []

    for tarea in des:
        datos_tarea = {
            "id": tarea.titulo,
            "name": tarea.titulo,
            "start": tarea.fecha_inicio.strftime("%Y-%m-%d"),
            "end": tarea.fecha_fin.strftime("%Y-%m-%d"),
            "dependencies": tarea.dependencias,
            "description": tarea.descripcion,
        }
        datos_tareas.append(datos_tarea)
    datos_tareas_json = json.dumps(datos_tareas)


    return render(request, "./user/gantt.html", {'proyecto': proyecto,'datos_tareas': datos_tareas_json})


def estado_porcentaje(porcentaje):
    if porcentaje == 0:
        return "No ha iniciado"
    elif porcentaje > 0 and porcentaje < 100:
        return "En proceso"
    elif porcentaje == 100:
        return "Completado"
    else:
        return "Valor de porcentaje inválido"

def nuevoitems(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    des = Des.objects.filter(codigo=codigo)

    if request.method == 'POST':
        nombre = request.POST.get('actividad-nombre')
        descripcion = request.POST.get('actividad-descripcion')
        fase = request.POST.get('actividad-fase')
        subfase = request.POST.get('subfase')
        fecha_inicio = request.POST.get('actividad-fecha-inicio')
        fecha_fin = request.POST.get('actividad-fecha-fin')
        horas_estimadas = request.POST.get('horas-estimadas')
        observaciones = request.POST.get('observaciones')
        porcentaje = request.POST.get('porcentaje')
        dependencia = request.POST.get('dependencia')
        complejidad = request.POST.get('actividad-complejidad')

        estado = estado_porcentaje(int(porcentaje))


        # Crea una instancia del modelo Actividad con los datos del formulario
        des_instance = Des.objects.create(
            codigo=codigo,
            titulo=nombre,
            descripcion=descripcion,
            fase=fase,
            subfase=subfase,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tiempo_estimado=horas_estimadas,
            observaciones=observaciones,
            procentaje=porcentaje,
            dependencias = dependencia,
            estado = estado,
            peso = int(complejidad)
        )
        des_instance.save()
        return redirect('main:des', proyecto.codigo )


    return render(request, "./user/nuevaactividad.html",{'proyecto' : proyecto, 'des':des})

def edititems(request,codigo,id_items):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    item = get_object_or_404(Des, pk=id_items)

    return render(request, "./user/edittarea.html",{'proyecto' : proyecto, 'item':item})

## kanbas

"""
<option value="inicio"> Inicio </option>
<option value="planeacion"> Planeación </option>
<option value="planeacion"> Ejecución </option>
<option value="monitoreo"> Monitoreo y Control </option>
<option value="cierre"> Cierre </option>

"""

def des(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    inicio = Des.objects.filter(codigo=codigo,fase='inicio')
    planeacion = Des.objects.filter(codigo=codigo,fase='planeacion')
    ejecucion = Des.objects.filter(codigo=codigo,fase='ejecucion')
    monitoreo = Des.objects.filter(codigo=codigo,fase='monitoreo')
    cierre = Des.objects.filter(codigo=codigo,fase='cierre')

    return render(request, "./user/des.html",{'proyecto' : proyecto,
                                                'inicio':inicio,
                                                'planeacion':planeacion,
                                                'ejecucion':ejecucion,
                                                'monitoreo':monitoreo,
                                                'cierre':cierre,
                                            })


def kanban(request , codigo , titulo ):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    tablero = Tablero.objects.filter(titulo=titulo).first()

    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',
    }

    return render(request , './user/kanban.html', {'context':context , 'tablero':tablero , 'proyecto' : proyecto } )


def mover_tarjeta(request, tarjeta_id, columna_id):
    tarjeta = get_object_or_404(Tarjeta, id=tarjeta_id)
    columna = get_object_or_404(Columna, id=columna_id)
    tarjeta.columna = columna
    tarjeta.save()
    return HttpResponse("Ok")

##*  {% url 'main:nuevoproyecto' codigo=proyecto.codigo %}
##*  {% url 'main:project' codigo=proyecto.codigo %}
##*  {% url 'main:riesgos' codigo=proyecto.codigo %}
##* {% url 'main:nuevomatriz' codigo=proyecto.codigo %}