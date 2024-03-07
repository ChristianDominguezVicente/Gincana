from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Usuario(BaseUserManager):
    def create_user(self, email, username, nombre, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        
        usuario = self.model(
            username = username, 
            email = self.normalize_email(email), 
            nombre = nombre
        )

        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self, email, username, nombre, password):
        usuario = self.create_user(
            email, 
            username = username, 
            nombre = nombre, 
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

class Profesor(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique = True, max_length=100)
    email = models.EmailField("Correo Electrónico", unique = True, max_length=254)
    nombre = models.CharField("Nombre" ,max_length=200, null=True, blank=True)
    apellidos = models.CharField("Apellidos", max_length=200, null=True, blank=True)
    imagen = models.ImageField("Imagen de Perfil", upload_to='perfil/', max_length=200, blank = True, null = True)
    usuario_activo = models.BooleanField(default = True)
    usuario_administrador = models.BooleanField(default=False)
    fecha_nacimiento = models.DateTimeField(auto_now_add=True)
    genero = models.CharField("Género", max_length=200, blank=False)
    telefono = models.IntegerField(null=True, blank=True)
    organizacion = models.CharField("Organizacion", max_length=200, null=True, blank=True)
    objects = Usuario()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre']

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
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    edicion = models.DateTimeField(null=True, blank=True)
    visibilidad = models.BooleanField(default=False)
    email_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - ' + self.email_profesor.username