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
from django.http import JsonResponse
from datetime import datetime, timedelta


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
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    gerentesAsignados = proyecto.user.all()
    gerentes = Usuario.objects.filter(rol='gerente').exclude(pk__in=[gerentes.pk for gerentes in gerentesAsignados])

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
        project_contrato = request.POST.get('project-contrato')
        project_objeto = request.POST.get('project-objeto')
        project_cliente = request.POST.get('project-cliente')
        project_valor = request.POST.get('project-valor',0.0)
        project_descrip = request.POST.get('project-descrip')
        project_type = request.POST.get('project-type')
        project_category = request.POST.get('project-category')
        project_managers = request.POST.get('project-managers')
        project_name_contractor = request.POST.get('project-name-contractor')
        manager = get_object_or_404(Usuario, id=project_managers)
        while True:
            codigo = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            if not Proyecto.objects.filter(codigo=codigo).exists():
                break

        project_valor = request.POST.get('project-valor')
        if not project_valor:  # Si el campo está vacío
            # Establecer el valor a cero
            project_valor = 0
        """
        project_contrato
        project_objeto
        project_cliente
        project_valor
        fecha_inicio #
        fecha_finalizacion #
        """

        proyecto1 = Proyecto.objects.create(
            name=project_name,
            codigo=codigo,
            description=project_descrip,
            tipo=project_type,
            categoria=project_category,
            estado='abierto',
            contrato = project_contrato,
            objeto = project_objeto,
            cliente = project_cliente,
            valor = project_valor ,
            name_contractor = project_name_contractor
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
            proyecto.fecha_creacion = timezone.now().strftime('%Y-%m-%d')
            proyecto.fecha_inicio_planeada = request.POST.get('fecha-inicio')
            proyecto.fecha_finalizacion_planeada = request.POST.get('fecha-finalizacion')
            proyecto.alcance = request.POST.get('project-description')
            proyecto.estado = "abierto"
            proyecto.lider = request.POST.get('project-leader')
            proyecto.grupo = request.POST.get('project-group')
            proyecto.antecedentes = 'antecedentes'
            proyecto.fase = "ninguna"
            proyecto.comentarios = request.POST.get('project-comments')
            proyecto.porcentaje_completado = 0
            proyecto.columna = True
            proyecto.contrato = request.POST.get('project-contract-number')
            proyecto.objeto = request.POST.get('project-contract-object')
            proyecto.cliente = request.POST.get('project-client')
            proyecto.valor = request.POST.get('project-value')
            proyecto.name_contractor = request.POST.get('project-contractor-manager')
            proyecto.save()




        return redirect('main:inicio_manager', id_gerente )
    # CLUSTER gluster
    return render(request, "./user/nuevoproyecto.html" , {'context':context , 'gerente': proyecto.user , 'gluster':gluster , 're':gerente , 'proyecto':proyecto } )


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
            nivel = 'Muy Grave'
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
    costo = Costos.objects.filter(codigo=codigo).first
    if request.method == 'POST':
        contrato = request.POST.get('contrato')
        cliente = request.POST.get('cliente')
        valor_total_ingreso = request.POST.get('valor_total_ingreso')
        costo_presupuestado = request.POST.get('costo_presupuestado')

        nuevo = Costos.objects.create(
            codigo = codigo,
            contrato = contrato,
            cliente = cliente,
            valor_total_ingreso = int(valor_total_ingreso) ,
            costo_presupuestado = int(costo_presupuestado),
            bloqueo = True
            )

        nuevo.save()

    return render(request, "./user/costos.html",{'costos':costo ,'proyecto' : proyecto })


def ingresobutton (request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    ingreso = Costosingresos.objects.filter(codigo=codigo)

    return render(request, "./user/ingresobutton.html",{'proyecto' : proyecto , 'ingreso':ingreso})


def ingreso(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    if request.method == 'POST':
        tipo_ingreso = request.POST.get('tipo-ingreso')
        fecha_planeada = request.POST.get('fecha-planeada')
        valor_planeado = request.POST.get('valor-planeado')

        # Convertir la cadena de fecha en un objeto datetime
        fecha_planeada = datetime.strptime(fecha_planeada, '%Y-%m-%d').date()

        if tipo_ingreso == 'One Time':
            ingreso = Costosingresos.objects.create(
                codigo=codigo,
                tipo=tipo_ingreso,
                fecha_planeada=fecha_planeada,
                valor_planeado=valor_planeado
            )
            ingreso.save()
            return redirect('main:ingresobutton', proyecto.codigo)


        if tipo_ingreso == 'Recurrente1':
            n = int(request.POST.get('recurrencia-fija'))  # Convertir a entero
            valor_aux = float(valor_planeado) / n  # Convertir a flotante
            for _ in range(n):
                fecha_planeada += timedelta(days=30)
                ingreso = Costosingresos.objects.create(
                    codigo=codigo,
                    tipo=tipo_ingreso,
                    fecha_planeada=fecha_planeada,
                    valor_planeado=valor_aux
                )
                ingreso.save()
            return redirect('main:ingresobutton', proyecto.codigo)



        if tipo_ingreso == 'Recurrente2':
            costos = request.POST.getlist('costo-recurrencia-no-fija')
            fechas_planeadas = request.POST.getlist('fecha-planeada-recurrencia-no-fija')
            for costo, fecha_planeada_str in zip(costos, fechas_planeadas):
                fecha_planeada = datetime.strptime(fecha_planeada_str, '%Y-%m-%d').date()
                ingreso = Costosingresos.objects.create(
                    codigo=codigo,
                    tipo=tipo_ingreso,
                    fecha_planeada=fecha_planeada,
                    valor_planeado=float(costo)
                )
                ingreso.save()
            return redirect('main:ingresobutton', proyecto.codigo)



    return render(request, "./user/nuevoingreso.html",{'proyecto' : proyecto })




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


def costobutton (request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()

    return render(request, "./user/costobutton.html",{'proyecto' : proyecto })

def resumenbutton (request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()

    return render(request, "./user/resumenbutton.html",{'proyecto' : proyecto })


 # documentos
def docu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    docus = Documentos.objects.filter(proyecto=proyecto).first()

    if request.method == 'POST':
        contrato_cliente = is_checkbox_checked(request.POST, 'contrato_cliente')
        acta_inicio = is_checkbox_checked(request.POST, 'acta_inicio')
        constitucion_proyecto = is_checkbox_checked(request.POST, 'constitucion_proyecto')
        kickoff_cliente_interno = is_checkbox_checked(request.POST, 'kickoff_cliente_interno')
        obligaciones_contractuales = is_checkbox_checked(request.POST, 'obligaciones_contractuales')
        oferta_entregada_cliente = is_checkbox_checked(request.POST, 'oferta_entregada_cliente')
        plan_gestion_proyecto = is_checkbox_checked(request.POST, 'plan_gestion_proyecto')
        cronograma = is_checkbox_checked(request.POST, 'cronograma')
        contrato_aliado = is_checkbox_checked(request.POST, 'contrato_aliado')
        acta_inicio_aliado = is_checkbox_checked(request.POST, 'acta_inicio_aliado')
        resumen_oc = is_checkbox_checked(request.POST, 'resumen_oc')
        conciliaciones_proveedor = is_checkbox_checked(request.POST, 'conciliaciones_proveedor')
        backlog_oc = is_checkbox_checked(request.POST, 'backlog_oc')
        matriz_riesgos = is_checkbox_checked(request.POST, 'matriz_riesgos')
        matriz_interesados = is_checkbox_checked(request.POST, 'matriz_interesados')
        correos_clientes_proveedor = is_checkbox_checked(request.POST, 'correos_clientes_proveedor')
        ficha_presentacion_proyecto = is_checkbox_checked(request.POST, 'ficha_presentacion_proyecto')
        solicitud_control_cambio = is_checkbox_checked(request.POST, 'solicitud_control_cambio')
        actas_reuniones_tecnicas = is_checkbox_checked(request.POST, 'actas_reuniones_tecnicas')
        acta_entrega_cliente = is_checkbox_checked(request.POST, 'acta_entrega_cliente')
        acta_recibido_aliado = is_checkbox_checked(request.POST, 'acta_recibido_aliado')
        ficha_cierre = is_checkbox_checked(request.POST, 'ficha_cierre')
        entrega_aseguramiento = is_checkbox_checked(request.POST, 'entrega_aseguramiento')
        entregas_obligaciones_contractura = is_checkbox_checked(request.POST, 'entregas_obligaciones_contractura')



        if docus is not None:
            docus.contrato_cliente = contrato_cliente
            docus.acta_inicio = acta_inicio
            docus.constitucion_proyecto = constitucion_proyecto
            docus.kickoff_cliente_interno = kickoff_cliente_interno
            docus.obligaciones_contractuales = obligaciones_contractuales
            docus.oferta_entregada_cliente = oferta_entregada_cliente
            docus.plan_gestion_proyecto = plan_gestion_proyecto
            docus.cronograma = cronograma
            docus.contrato_aliado = contrato_aliado
            docus.acta_inicio_aliado = acta_inicio_aliado
            docus.resumen_oc = resumen_oc
            docus.conciliaciones_proveedor = conciliaciones_proveedor
            docus.backlog_oc = backlog_oc
            docus.matriz_riesgos = matriz_riesgos
            docus.matriz_interesados = matriz_interesados
            docus.correos_clientes_proveedor = correos_clientes_proveedor
            docus.ficha_presentacion_proyecto = ficha_presentacion_proyecto
            docus.solicitud_control_cambio = solicitud_control_cambio
            docus.actas_reuniones_tecnicas = actas_reuniones_tecnicas
            docus.acta_entrega_cliente = acta_entrega_cliente
            docus.acta_recibido_aliado = acta_recibido_aliado
            docus.ficha_cierre = ficha_cierre
            docus.entrega_aseguramiento = entrega_aseguramiento
            docus.entregas_obligaciones_contractura = entregas_obligaciones_contractura
            docus.save()


        else:
            docus = Documentos.objects.create(
                proyecto=proyecto,
                contrato_cliente=contrato_cliente,
                acta_inicio=acta_inicio,
                constitucion_proyecto=constitucion_proyecto,
                kickoff_cliente_interno=kickoff_cliente_interno,
                obligaciones_contractuales=obligaciones_contractuales,
                oferta_entregada_cliente=oferta_entregada_cliente,
                plan_gestion_proyecto=plan_gestion_proyecto,
                cronograma=cronograma,
                contrato_aliado=contrato_aliado,
                acta_inicio_aliado=acta_inicio_aliado,
                resumen_oc=resumen_oc,
                conciliaciones_proveedor=conciliaciones_proveedor,
                backlog_oc=backlog_oc,
                matriz_riesgos=matriz_riesgos,
                matriz_interesados=matriz_interesados,
                correos_clientes_proveedor=correos_clientes_proveedor,
                ficha_presentacion_proyecto=ficha_presentacion_proyecto,
                solicitud_control_cambio=solicitud_control_cambio,
                actas_reuniones_tecnicas=actas_reuniones_tecnicas,
                acta_entrega_cliente=acta_entrega_cliente,
                acta_recibido_aliado=acta_recibido_aliado,
                ficha_cierre=ficha_cierre,
                entrega_aseguramiento=entrega_aseguramiento,
                entregas_obligaciones_contractura=entregas_obligaciones_contractura
            )
            docus.save()

        return redirect('main:docu', proyecto.codigo )
    return render(request, "./user/docu.html",{'docus':docus ,'proyecto' : proyecto })

def is_checkbox_checked(post_data, checkbox_name):
    return True if checkbox_name in post_data else False

def nuevodocu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    costo = Costos.objects.filter(proyecto=proyecto)
    return render(request, "./user/costos.html",{'costos':costo ,'proyecto' : proyecto })

## comunicaciones
def comu(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    comunis = Comunicacion.objects.filter(codigo=codigo)
    return render(request, "./user/comu.html",{'proyecto' : proyecto, 'comunis':comunis })


def formatocomunica(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()

    if request.method == 'POST':
        rol = request.POST.get('communication-role')
        nombre = request.POST.get('nombre')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')
        aspectos_comunicar = request.POST.get('aspectos_a_comunicar')
        responsable_comunicar = request.POST.get('responsable_de_la_comunicacion')
        cuando_comunica = request.POST.get('cuando_lo_comunica')
        importancia = request.POST.get('importancia')
        estrategias_medios = request.POST.get('estrategias_y_medios')


        comunicaciones = Comunicacion.objects.create(
            codigo = codigo, #
            rol=rol, #
            nombre=nombre,#
            celular=celular,#
            correo=correo,
            aspectos_a_comunicar=aspectos_comunicar,
            responsable_de_la_comunicacion=responsable_comunicar,
            cuando_lo_comunica=cuando_comunica,
            importancia=importancia,
            estrategias_y_medios=estrategias_medios,
            )

        comunicaciones.save()
        return redirect('main:comu', proyecto.codigo )

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
    acti_objects = Acti.objects.all()



    data = {}
    for acti_object in acti_objects:
        fase = acti_object.fasedes
        subfase = acti_object.subfasedes
        tarea = acti_object.tarea

        if fase not in data:
            data[fase] = {"subfases": [], "tareas": []}

        if subfase not in data[fase]["subfases"]:
            data[fase]["subfases"].append(subfase)

        if tarea not in data[fase]["tareas"]:
            data[fase]["tareas"].append(tarea)




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


    return render(request, "./user/nuevaactividad.html",{'proyecto' : proyecto, 'des':des , 'data': data})

def edititems(request,codigo,id_items):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    item = Des.objects.filter(pk=id_items).first()
    if request.method == 'POST':
        procentaje = request.POST.get('porcentaje')
        observaciones = request.POST.get('observaciones')

        item.procentaje = procentaje
        item.observaciones = observaciones
        item.estado = estado_porcentaje(int(procentaje))
        item.save()
        return redirect('main:des', proyecto.codigo )

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
    inicio = Des.objects.filter(codigo=codigo,fase='Inicio')
    planeacion = Des.objects.filter(codigo=codigo,fase='Planeacion')
    ejecucion = Des.objects.filter(codigo=codigo,fase='Ejecucion')
    monitoreo = Des.objects.filter(codigo=codigo,fase='Monitoreo')
    cierre = Des.objects.filter(codigo=codigo,fase='Cierre')

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


## grafica rapida :

def apicarga(request):
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


    return JsonResponse(proyectos_por_gerente, safe=False)



### apis



def apiproyecto(request):
    proyecto = Proyecto.objects.all()
    des = Des.objects.all()
    data1 =[]
    cont = []
    for pro in proyecto:


        record = {
            'id': pro.id,
            'name': pro.name,
            'description': pro.description,
            'alcance': pro.alcance,
            'categoria':pro.categoria,
            'estado' : pro.estado,
            'fecha_creacion' : pro.fecha_creacion,
            'fecha_inicio_planeada' : pro.fecha_creacion,
            'fecha_inicio_real' : pro.fecha_creacion,
            'fecha_finalizacion_planeada' : pro.fecha_creacion,
            'fecha_finalizacion_real' : pro.fecha_creacion,
            'porcentaje_completado': pro.porcentaje_completado ,
            'tipo': pro.tipo,
            'lider': pro.lider,
            'grupo': pro.grupo,
            'programas': pro.programas ,
            'comentarios':pro.comentarios,
            'spi': pro.spi,
            'es':pro.es


        }

        data1.append(record)

    return JsonResponse(data1, safe=False)


def apitareas(request):
    des = Des.objects.all()
    data1 =[]
    for pro in des:
        record = {
            'id': pro.id,
            'titulo': pro.titulo ,
            'descripcion' : pro.descripcion,
            'fecha_inicio' : pro.fecha_inicio,
            'fecha_fin' : pro.fecha_inicio,
            'fase' : pro.fase,
            'subfase' : pro.subfase,
            'procentaje' :int( pro.procentaje),
            'dependencias' : pro.dependencias,
            'observaciones' : pro.observaciones,
            'tiempo_estimado' : pro.tiempo_estimado,
            'tiempo_real' : pro.tiempo_real,
            'estado' : pro.estado,
            'completada' : pro.completada,
            'peso' : pro.peso,
        }
        data1.append(record)
    return JsonResponse(data1, safe=False)



def apiriesgo(request):
    matriz = MatrizRiesgo.objects.all()
    data1 =[]
    for pro in matriz:

        record = {
            'id': pro.id,
            'name': pro.nombre,
            'description': pro.descripcion,
            'causas': pro.causas,
            'plan' : pro.plan,
            'consecuencias': pro.consecuencias ,
            'descripcion_tiempo': pro.descripcion_tiempo,
            'descripcion_alcance': pro.descripcion_alcance,
            'descripcion_costo': pro.descripcion_costo,
            'probavilidad': pro.probavilidad ,
            'gravedad':pro.gravedad,
            'riesgo': pro.riesgo,
            'materializo':pro.materializo,
            'proyecto': pro.proyecto.name,
            'acciones_mitigacion':pro.acciones_mitigacion
        }

        data1.append(record)

    return JsonResponse(data1, safe=False)


def apicostos(request):
    proyecto = Proyecto.objects.all()
    des = Des.objects.all()
    data1 =[]
    for pro in proyecto:

        record = {
            'id': pro.id,
            'name': pro.name,
            'description': pro.description,
            'alcance': pro.alcance,
            'estado' : pro.estado,
            'porcentaje_completado': pro.porcentaje_completado ,
            'tipo': pro.tipo,
            'lider': pro.lider,
            'grupo': pro.grupo,
            'programas': pro.programas ,
            'comentarios':pro.comentarios,
            'spi': pro.spi,
            'es':pro.es
        }

        data1.append(record)

    return JsonResponse(data1, safe=False)


def word(request):
    return render(request, "./WORKFLOW/index.html")


def informe(request,codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    return render(request, "./user/informe.html",{ 'proyecto' : proyecto })



##*  {% url 'main:nuevoproyecto' codigo=proyecto.codigo %}
##*  {% url 'main:project' codigo=proyecto.codigo %}
##*  {% url 'main:riesgos' codigo=proyecto.codigo %}
##* {% url 'main:nuevomatriz' codigo=proyecto.codigo %}