from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    )
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=9, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO)

    def __str__(self):
        return f'[{self.username}] - {self.last_name}, {self.first_name} {self.email}'

class Region(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Inmueble(models.Model):
    TIPO_INMUEBLE = (
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela'),
    )
    ESTADO_INMUEBLE = (
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('arrendado', 'Arrendado'),
    )
    id_publicacion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    m2_construidos = models.IntegerField()
    m2_totales = models.IntegerField(null=True, blank=True)
    estacionamientos = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    direccion = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_inmueble = models.CharField(max_length=20, choices=TIPO_INMUEBLE, default='casa')
    estado_inmueble = models.CharField(max_length=20, choices=ESTADO_INMUEBLE, default='disponible')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    arrendador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion= models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='inmuebles/', null=True, blank=True)
    visitas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class SolicitudArriendo(models.Model):
    TIPO_SOLICITUD = (
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
    )
    id_solicitud = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    arrendatario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=TIPO_SOLICITUD)

    def __str__(self):
        return f"{self.arrendatario} - {self.inmueble}"
    

class Mensajes(models.Model):
    ESTADO_MENSAJE = (
        ('pendiente', 'Pendiente'),
        ('leido', 'Leido'),
        ('respondido', 'Respondido'),
    )
    id_mensaje = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    mensaje = models.TextField(null=False, blank=False)
    estado = models.CharField(max_length=20, choices=ESTADO_MENSAJE, default='pendiente')

    def __str__(self):
        return f"{self.inmueble} - {self.usuario}"
    
class Respuestas(models.Model):
    id_respuesta = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mensaje_padre = models.ForeignKey(Mensajes, on_delete=models.CASCADE)
    respuesta = models.TextField(null=False, blank=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self): 
        return f"{self.id_mensaje} - {self.respuesta}"
    

class RegionComuna(models.Model):
    region = models.CharField(max_length=50, null=False, blank=False)
    comunas = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.region} - {self.comuna}"