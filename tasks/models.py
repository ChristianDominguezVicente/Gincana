from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Usuario(BaseUserManager):
    def create_user(self, email, nombre, apellidos, fecha_nacimiento, genero, pais, ciudad, organizacion, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        
        usuario = self.model(
            email = self.normalize_email(email),
            nombre = nombre, 
            apellidos = apellidos,
            fecha_nacimiento = fecha_nacimiento,
            genero = genero,
            pais = pais,
            ciudad = ciudad,
            organizacion = organizacion
        )

        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self, email, nombre, apellidos, fecha_nacimiento, genero, pais, ciudad, organizacion,  password):
        usuario = self.create_user(
            email, 
            nombre = nombre, 
            apellidos = apellidos,
            fecha_nacimiento = fecha_nacimiento,
            genero = genero,
            pais = pais,
            ciudad = ciudad,
            organizacion = organizacion,
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

class Profesor(AbstractBaseUser):
    email = models.EmailField("Correo Electrónico", unique = True, max_length=254, primary_key=True)
    nombre = models.CharField("Nombre" ,max_length=200, null=True, blank=False)
    apellidos = models.CharField("Apellidos", max_length=200, null=True, blank=False)
    imagen = models.ImageField("Imagen de Perfil", upload_to='perfil/', max_length=200, blank = True, null = True)
    usuario_activo = models.BooleanField(default = True)
    usuario_administrador = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=False)
    genero = models.CharField("Género", max_length=200, null=True, blank=True)
    pais = models.CharField("País", max_length=200, null=True, blank=True)
    ciudad = models.CharField("Ciudad", max_length=200, null=True, blank=True)
    organizacion = models.CharField("Organizacion", max_length=200, null=True, blank=False)
    objects = Usuario()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'fecha_nacimiento', 'genero', 'pais', 'ciudad', 'organizacion']

    def __str__(self):
        return f'{self.nombre},{self.apellidos}'
    
    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador
    
class Gincana(models.Model):
    titulo = models.CharField('Nombre de la gincana', max_length=100)
    descripcion = models.TextField('Descirpción de la gincana', blank=True)
    fecha = models.DateTimeField('Fecha de creación', auto_now_add=True)
    edicion = models.DateTimeField('Edición de la gincana', null=True, blank=True)
    duracion = models.TimeField('Duración', null=True, blank=True)
    visibilidad = models.BooleanField('Visibilidad de la gincana', default=False)
    activa = models.BooleanField('Actividad de la gincana', default=False)
    imagen = models.ImageField("Imagen de la gincana", upload_to='gincana/', max_length=200, blank = True, null = True)
    email_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - ' + self.email_profesor.email
    
class GincanaJugada(models.Model):
    duracion = models.TimeField('Duración', null=True, blank=True)
    total_puntos = models.IntegerField('Puntuación', null=True, blank=True)
    edición = models.DateTimeField('Edición', auto_now_add=True, primary_key=True)
    gincana = models.ForeignKey(Gincana, on_delete=models.CASCADE)

    def __str__(self):
        return self.gincana.titulo + ' - ' + self.edición