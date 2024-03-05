from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout
from .decorador import * 
from .pruebas import * 
from .models import * 
from collections import defaultdict
from django.http import HttpResponse
## funciones propias 
from .mail import *
import random
import json



def Login(request):
    # if request.user.is_authenticated:
    #     return redirect('inicio_administrator')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            usuario = Usuario.objects.get(usuario=user)
            
            if usuario.rol == 'administrador':
                return redirect('inicio_administrator')
            
            elif usuario.rol == 'gerente':
                
                return redirect('inicio_manager', usuario.id )
            
            elif usuario.rol == 'miembro':
                return redirect('pagina_miembro')
            else:
                return render(request, 'error.html', {'mensaje': 'Rol no reconocido'})
            
            
            
        else:
            return render(request, './user/login.html', {'error_message': 'Credenciales inválidas. Por favor, inténtalo de nuevo.'})
    else:
        return render(request, "./user/login.html")

def Logout(request):
    logout(request)
    return redirect('main:login')



# def inicio_administrador(request):
#     #usurios = 
#     usuarios = Usuario.objects.select_related('usuario').all()
    
#     # user = request.user()
#     # context = {
#     #     'email': user.email,
#     #     'first_name': user.first_name,
#     # }
#     # context = {
#     #     'email': 'user.email',
#     #     'first_name': 'user.first_name',
#     # }
#     print(usuarios)
#     return render(request, "./user/inicio_administrador.html", usuarios)


def inicio_administrador(request):
    usuarios = Usuario.objects.select_related('usuario').filter(rol='gerente')
    tipos_proyecto = ['Tipo I', 'Tipo II', 'Tipo III', 'Tipo IV']  # Lista de tipos de proyecto

    # Simular datos aleatorios para cada usuario y tipo de proyecto
    proyectos_por_usuario = {}
    for usuario in usuarios:
        proyectos_por_usuario[usuario] = {
            'tipo1': random.randint(0, 10),
            'tipo2': random.randint(0, 10),
            'tipo3': random.randint(0, 10),
            'tipo4': random.randint(0, 10),
        }

    context = {
        'proyectos_por_usuario': proyectos_por_usuario,
        'tipos_proyecto': tipos_proyecto,
    }
    return render(request, './user/inicio_administrador.html', context)


def inicio_gerente(request, id_gerente):
    usuario = Usuario.objects.get(id=id_gerente)
    proyectos = Proyecto.objects.filter(user=usuario)
    
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',
        'proyectos': proyectos,
    }
    return render(request, "./user/inicio_gerente.html", context)



def nuevoproyecto(request , codigo):
    proyecto = Proyecto.objects.filter(codigo=codigo).first()
    proyecto 
    
    context = {
        'codigo': proyecto.codigo,
        'name': proyecto.name ,
        'descr': proyecto.description,
    }
    print(context)
    if request.method == 'POST':
        if proyecto:
            # Actualizar los campos del proyecto que no se asignaron en asignar
            proyecto.fecha_inicio_real = request.POST.get('project-start-date-real')
            proyecto.fecha_finalizacion_real = request.POST.get('project-end-date-real')
            proyecto.alcance_proyecto = request.POST.get('project-scope')
            proyecto.estado_proyecto = request.POST.get('project-status')
            proyecto.porcentaje_completado = request.POST.get('project-completion-percentage')
            proyecto.tipo_proyecto = request.POST.get('project-type')
            proyecto.lider_proyecto = request.POST.get('project-leader')
            proyecto.grupo_proyecto = request.POST.get('project-group')
            proyecto.categoria_proyecto = request.POST.get('project-category')
            proyecto.antecedentes_proyecto = request.POST.get('project-background')
            proyecto.fase_proyecto = request.POST.get('project-phase')
            proyecto.comentarios_proyecto = request.POST.get('project-comments')
            proyecto.porcentaje_completado = 0 
            proyecto.save()
            
        
        # Crea un tablero asociado al proyecto
        tablero = Tablero(titulo= proyecto.codigo , proyect=proyecto)
        tablero.save()
        
        # Crea las columnas por defecto
        nombres_columnas = ['Por hacer', 'En progreso', 'En revisión', 'Hecho']
        for nombre in nombres_columnas:
            Columna.objects.create(tablero=tablero, titulo=nombre)
        
        return redirect('inicio_manager', proyecto.user.id )
    
        
    
    return render(request, "./user/nuevoproyecto.html" , {'context':context , 'gerente': proyecto.user} ) 


def crearprojecto(request , codigo):        
    return render(request, './user/createproject.html')



def asignar(request):
    gerentes = Usuario.objects.filter(rol='gerente')
    
    if request.method == 'POST':
        project_name = request.POST.get('project-name')
        project_descrip = request.POST.get('project-descrip')
        project_managers = request.POST.get('project-managers')
        usuario = get_object_or_404(Usuario, id=project_managers)
        
        # Generar un código aleatorio único para el proyecto
        while True:
            # Generar un código aleatorio
            codigo = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            # Verificar si el código generado ya existe en la base de datos
            if not Proyecto.objects.filter(codigo=codigo).exists():
                break
        
        proyecto1 = Proyecto.objects.create(
            name=project_name, 
            codigo=codigo, 
            description=project_descrip, 
            user=usuario, 
            estado='abierto'  # Añadido el estado del proyecto
        )
        proyecto1.save()
        
        # Llamar a la función para enviar el correo electrónico
        enviar_correo_post(usuario.id, proyecto1.codigo, 'tipo1')
        return redirect('inicio_administrator')
    
    return render(request, './user/asignar.html', {'gerentes': gerentes})


## pruebas 
def diagrama(request):
    todas_las_tareas = Tarea.objects.all()

    # Estructurar las tareas en el formato adecuado para el diagrama de Gantt
    actividades = []
    for tarea in todas_las_tareas:
        dependencias = [dep.id for dep in tarea.dependencias.all()]
        actividad = {
            "id": tarea.id,
            "name": tarea.nombre,
            "start": tarea.fecha_inicio.strftime('%Y-%m-%d'),
            "end": tarea.fecha_fin.strftime('%Y-%m-%d'),
            "progress": calcular_progreso(tarea),  # Calcular el progreso de la tarea
            "dependencies": dependencias, 
        }
        
        actividades.append(actividad)
    
    # Convertir las actividades a formato JSON
    actividades_json = json.dumps(actividades)
    return render(request, './datos.html',{'actividades': actividades_json})

def calcular_progreso(tarea):
    return 70


def corre(request):
    enviar_correo_post('pueba','valor')
    return 0 

def gestion(request):
    return render(request, './user/barra_lateral.html')


def proyecto(request , id_proyect):
    proyecto = Proyecto.objects.filter(id=id_proyect).first()
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',
        'proyecto_name': proyecto.name ,
        'proyecto_id' : proyecto.id ,
        
    }
    
    return render(request , './user/proyecto.html' ,{'context': context , 'proyecto' : proyecto })


### proceso kanban : 
def kanban(request , id_project):
    
    proyecto = Proyecto.objects.filter(id=id_project).first()
    if proyecto:
        tablero = proyecto.tablero
    
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


def nuevaactividad(request , id_project , id_columna):
    columna = id_columna and get_object_or_404(Columna, id=id_columna) or None
    
    proyecto = Proyecto.objects.filter(id=id_project).first()
    if proyecto:
        tablero = proyecto.tablero
    
    context = {
        'email': 'user.email',
        'first_name': 'user.first_name',
    }    
    
    if request.method == 'POST':
        nombre_actividad = request.POST.get('actividad-nombre')
        descripcion_actividad = request.POST.get('actividad-descripcion')
        fecha_inicio = request.POST.get('actividad-fecha-inicio')
        fecha_fin = request.POST.get('actividad-fecha-fin')
        
        actividad = Hito.objects.create(
            nombre=nombre_actividad,
            descripcion=descripcion_actividad,
            proyecto=proyecto,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )
        
        actividad.save()
        
        tarjeta = Tarjeta.objects.create(
            actividad=actividad,
            columna = columna,
            titulo = nombre_actividad , 
            descripcion = descripcion_actividad, 
        )
        
        tarjeta.columna = columna
        
        tarjeta.save()
        print(tarjeta)
        return redirect('kanban', id_project=proyecto.id)
    
    return render(request , '././user/nuevaactividad.html', {'context':context , 'tablero':tablero , 'proyecto' : proyecto })