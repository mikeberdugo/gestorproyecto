from django.db import models
from django.contrib.auth.models import User
from markupfield.fields import MarkupField
from django.contrib.auth import models as authmodels
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator



class Usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ROLES = (
        ('administrador', 'Administrador'),
        ('gerente', 'Gerente'),
        ('miembro', 'Miembro'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    equipos = models.ManyToManyField('Equipo', related_name='miembros')



class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()



class Proyecto(models.Model):

    STATES = (
        ('abierto', 'Abierto'),
        ('suspendido', 'Suspendido'),
        ('cerrado', 'Cerrado'),
    )

    # Definir las opciones para los campos
    CATEGORIA = (
        ('I', 'Tipo I'),
        ('II', 'Tipo II'),
        ('III', 'Tipo III'),
        ('IV', 'Tipo IV'),
    )

    FASES = (
        ('inicio', 'Inicio'),
        ('planeacion', 'Planeación'),
        ('ejecucion', 'Ejecución'),
        ('monitoreo_control', 'Monitoreo y Control'),
        ('cierre', 'Cierre'),
    )
    # abierto , suspendido  , cerrado
    TYPE =(
        ('Proyectos Integración', 'Proyectos Integración'),
        ('Necesidades entrega operación', 'Necesidades entrega operación'),
        ('Proyectos Producto Propio', 'Necesidades entrega operación'),
        ('Necesidades', 'Necesidades'),
    )

    name = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100) ## auto increment - automatico
    description = models.TextField()

    fecha_creacion = models.DateField(null=True, blank=True)
    fecha_inicio_planeada = models.DateField(null=True, blank=True) #
    fecha_inicio_real = models.DateField(null=True, blank=True) ##  automatica
    fecha_finalizacion_planeada = models.DateField(null=True, blank=True)
    fecha_finalizacion_real = models.DateField(null=True, blank=True) # automatica

    alcance = models.TextField()
    estado = models.CharField(max_length=50 , choices=STATES) ## generar tipos

    porcentaje_completado = models.IntegerField(default=0) ## automatico
    tipo = models.CharField(max_length=50 , choices = TYPE ) ##  proyecto o necesidad
    user = models.ManyToManyField(Usuario)
    lider = models.CharField(max_length=100) ## automatico
    grupo = models.CharField(max_length=200,null=True, blank=True) ## grupo asociado lista desplegable - brayan
    categoria = models.CharField(max_length=100 , choices = CATEGORIA) # desplegable  lista desplegable - brayan
    antecedentes = models.TextField() ###
    fase = models.CharField(max_length=100 ,choices = FASES) ### lista , brayan los tiene
    programas =  models.CharField(max_length=100) # lista falta llegar
    comentarios = models.TextField(null=True, blank=True) ##
    spi = models.FloatField(default=0) ## indicador
    es = models.FloatField(default=0) ## formualdo

    ## informacion extra

    contrato = models.CharField(max_length=100,null=True, blank=True)
    objeto = models.TextField(null=True, blank=True)
    cliente = models.CharField(max_length=100,null=True,blank=True)
    valor = models.FloatField(default=0.0,validators=[MinValueValidator(0.0)])
    name_contractor =  models.CharField(max_length=100,null=True,blank=True )


    ##
    columna = models.BooleanField(default=False) ##  asignado



class Grupo(models.Model):
    grupo = models.CharField(max_length=100)
    cluster = models.CharField(max_length=100)

    @classmethod
    def generate_initial_data(cls):
        data = [
            {'grupo': 'Software y TXH', 'cluster': 'Julio Cesar Caicedo Caicedo'},
            {'grupo': 'Cloud Computing e Infraestructura', 'cluster': 'Javier Alejandro Sanchez Sanabria'},
            {'grupo': 'Computing e Infraestructura', 'cluster': 'Jhon Fredy Arroyave Martínez'},
            {'grupo': 'Infraestructura', 'cluster': 'José Manuel Cáceres García'},
            {'grupo': 'Ciberseguridad y SD-WAN', 'cluster': 'Milton Andres Pineda Ochoa'},
            {'grupo': 'BPO', 'cluster': 'Yorfan Mauricio Colmenares Padilla'},
        ]
        for item in data:
            Grupo.objects.get_or_create(grupo=item['grupo'], cluster=item['cluster'])


# Este receptor de señal se ejecutará después de que se guarde un objeto Grupo
@receiver(post_save, sender=Grupo)
def create_initial_data(sender, instance, created, **kwargs):
    if created:
        Grupo.generate_initial_data()


class Hito(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    asignado = models.ForeignKey(Usuario,on_delete=models.CASCADE , null=True, blank=True ) ## general una relacion de uno a muchos
    porcentaje = models.FloatField(null=True, blank=True ,default = 0.0)

#* leciones aprendidas
class ComentarioTarea(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    identificando_problema = models.TextField(blank=True , null=True )
    causa = models.TextField(blank=True , null=True)
    solucion = models.TextField(blank=True , null=True )
    planes_mejora_aplicados = models.TextField(blank=True , null=True)
    resultados_planes_mejora = models.TextField(blank=True , null=True)
    fecha_creacion = models.DateField()

    def str(self):
        return f"Comentario para {self.tarea.nombre}"

class MatrizRiesgo(models.Model):
    # Definir opciones para RIESGOS y GAVEDAD
    RIESGOS = (
        ('grave', 'Muy grave'),
        ('importante', 'Importante'),
        ('apreciable', 'Apreciable'),
        ('marginal', 'Marginal'),
    )

    GAVEDAD = (
        (1, 'Muy Bajo'),
        (2, 'Bajo'),
        (3, 'Medio'),
        (4, 'Alto'),
        (5, 'Muy Alto'),
    )

    # Definir campos del modelo
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()## falta
    causas = models.TextField() ## falta
    plan = models.TextField() # falta
    consecuencias = models.TextField() ## edit
    descripcion_tiempo = models.TextField() ## falta
    descripcion_alcance = models.TextField() ## falta
    descripcion_costo = models.TextField() ## falta
    probavilidad = models.IntegerField(choices=GAVEDAD)
    gravedad = models.IntegerField(choices=GAVEDAD)  # Cambiado a IntegerField
    riesgo = models.CharField(max_length=20)
    materializo = models.TextField() ## edit
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    acciones_mitigacion = models.TextField() ## edit

class Documentos(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    contrato_cliente = models.BooleanField(default=False)
    acta_inicio = models.BooleanField(default=False)
    constitucion_proyecto = models.BooleanField(default=False)
    kickoff_cliente_interno = models.BooleanField(default=False)
    obligaciones_contractuales = models.BooleanField(default=False)
    oferta_entregada_cliente = models.BooleanField(default=False)
    plan_gestion_proyecto = models.BooleanField(default=False)
    cronograma = models.BooleanField(default=False)
    contrato_aliado = models.BooleanField(default=False)
    acta_inicio_aliado = models.BooleanField(default=False)
    resumen_oc = models.BooleanField(default=False)
    conciliaciones_proveedor = models.BooleanField(default=False)
    backlog_oc = models.BooleanField(default=False)
    matriz_riesgos = models.BooleanField(default=False)
    matriz_interesados = models.BooleanField(default=False)
    correos_clientes_proveedor = models.BooleanField(default=False)
    ficha_presentacion_proyecto = models.BooleanField(default=False)
    solicitud_control_cambio = models.BooleanField(default=False)
    actas_reuniones_tecnicas = models.BooleanField(default=False)
    acta_entrega_cliente = models.BooleanField(default=False)
    acta_recibido_aliado = models.BooleanField(default=False)
    ficha_cierre = models.BooleanField(default=False)
    entrega_aseguramiento = models.BooleanField(default=False)
    entregas_obligaciones_contractura = models.BooleanField(default=False)




class Tablero(models.Model):
    titulo = models.CharField(max_length=200)
    proyect =  models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tablero')

    def __str__(self):
        return self.titulo

    def nueva_columna(self, titulo):
        c = Columna(titulo=titulo, tablero=self)
        c.save()
        return c

class Columna(models.Model):
    titulo = models.CharField(max_length=200)
    tablero = models.ForeignKey(Tablero, related_name='columnas', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.titulo, self.tablero)

    def nueva_tarjeta(self, titulo, descripcion):
        t = Tarjeta(titulo=titulo, descripcion=descripcion, columna=self)
        t.save()
        return t

class Tarjeta(models.Model):
    titulo = models.CharField(max_length=200 , blank=True)
    descripcion = models.TextField(blank=True)
    columna = models.ForeignKey(Columna, related_name='tarjetas', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100 , blank=True)
    fecha_inicio = models.DateField(blank=True)
    fecha_fin = models.DateField(blank=True)
    porcentaje = models.FloatField(null=True, blank=True ,default = 0.0)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE , blank=True)


class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    hito = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    asignado = models.ForeignKey(Usuario , on_delete=models.CASCADE)
    estado = models.CharField(max_length=100)  # Lista desplegable: SIN iniciar, En Proceso, Finalizada
    procentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dependencias = models.ManyToManyField('self', symmetrical=False, blank=True)

    def get_dependencies_titles(self):
        return self.dependencies.values_list('title', flat=True)

class Recurso(models.Model):
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='recursos')
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)


## neuvo modelo :
class Des(models.Model):
    codigo = models.CharField(max_length=200,blank=True)
    titulo = models.CharField(max_length=200,blank=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fase = models.CharField(max_length=100,blank=True)
    subfase = models.CharField(max_length=100,blank=True)
    procentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dependencias = models.CharField(max_length=200,blank=True, null=True)
    observaciones = models.TextField()
    tiempo_estimado = models.IntegerField(default=0, verbose_name='Tiempo Estimado (horas)',blank=True)
    tiempo_real = models.IntegerField(default=0, verbose_name='Tiempo real (horas)',blank=True)
    estado = models.CharField(max_length=200,blank=True)
    completada = models.BooleanField(default=False,blank=True)
    peso = models.IntegerField(default=1, verbose_name='Peso de actividad',blank=True)


class Comunicacion(models.Model):
    codigo = models.CharField(max_length=100)
    rol = models.CharField(max_length=100) ## falta validar roles
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=20)
    correo = models.EmailField()
    aspectos_a_comunicar = models.TextField()
    responsable_de_la_comunicacion =  models.TextField()
    cuando_lo_comunica =  models.TextField()
    importancia = models.TextField()
    estrategias_y_medios = models.TextField()


class Acti(models.Model):
    fasedes = models.CharField(max_length=200)
    subfasedes = models.CharField(max_length=200)
    tarea = models.CharField(max_length=200)
    horas = models.IntegerField(default=0, verbose_name='Tiempo Estimado (horas)',blank=True)


class Costos(models.Model):
    codigo = models.CharField(max_length=100)
    contrato = models.CharField(max_length=100)
    cliente = models.CharField(max_length=200)
    valor_total_ingreso = models.FloatField(default=0.0,validators=[MinValueValidator(0.0)])
    costo_presupuestado = models.FloatField(default=0.0,validators=[MinValueValidator(0.0)])
    utilidad = models.FloatField(default=0.0,validators=[MinValueValidator(0.0)])
    margen  = models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    bloqueo = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # Calcula la utilidad como la resta entre el valor total de ingreso y el costo presupuestado
        self.utilidad = self.valor_total_ingreso - self.costo_presupuestado
        self.margen = round(self.utilidad / self.valor_total_ingreso, 3)
        super().save(*args, **kwargs)



class Costosingresos(models.Model):
    codigo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    fecha_planeada = models.DateField(blank=True, null=True)
    valor_planeado = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)
    fechapago = models.DateField(blank=True, null=True)
    valorpagado = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)
    saldo = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)
    observaciones = models.CharField(max_length=100, blank=True, null=True)



class Costoscostos(models.Model):
    codigo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    aliado = models.CharField(max_length=100)
    fecha_planeada = models.DateField()
    costos_p = models.FloatField(default=0.0,validators=[MinValueValidator(0.0)])
    fecha_pago = models.DateField()
    valor_pagado = models.FloatField(default=0.0,validators=[MinValueValidator(0.0)])
    saldo = models.FloatField(default=0.0,validators=[MinValueValidator(0.0)])
    obsevaciones = models.CharField(max_length=100)










