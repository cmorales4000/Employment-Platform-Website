from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.conf import settings

# Create your models here
#apply=models.ManyToManyField(Usuario, blank=True, related_name="apply") intentado


class UsuarioManager(BaseUserManager):
    def create_user(self,username,nombre,dni,password=None):
        if not dni:
            raise ValueError('Falta Documento de Identificación')

        usuario = self.model(
            username = username,
            nombre = nombre, 
            dni = dni,
            password = password

            
        )

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self,username,nombre,dni,password):
        usuario = self.create_user(
            
            username = username,
            nombre = nombre, 
            dni = dni,
            password=password
            
        )
        
        usuario.usuario_administrador = True
        usuario.save()
        return usuario
        

class Usuario(AbstractBaseUser):
    
    username = models.CharField('Nombre de Usuario', max_length=20, unique=True)
    password = models.CharField('Password', max_length=128)
    email = models.EmailField('Correo Electrónico', blank=True, null=True)
    dni = models.PositiveIntegerField('Cédula/NIT', unique=True)
    nombre = nombre=models.CharField('Nombre/Razón Legal', max_length=30)
    contacto = models.PositiveIntegerField('Teléfono',blank=True, null=True)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', max_length=200, blank=True, null=True)
    hdv = models.FileField('Curriculum (Aplicantes)', upload_to='hdv/', max_length=200, blank=True, null=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    is_empresa = models.BooleanField('Es Empleador? (Empresa)',default=False)
    objects = UsuarioManager()
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre','dni','password']



    def __str__(self):
        return self.nombre

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador




class area(models.Model):
    nombre=models.CharField(max_length=30)

    def __str__(self):
        return self.nombre



class ciudad(models.Model):
    nombre=models.CharField(max_length=20)

    def __str__(self):
        return self.nombre



class oferta(models.Model):
    titulo=models.CharField(max_length=50)
    area=models.ForeignKey(area, on_delete=models.CASCADE)
    ciudad=models.ForeignKey(ciudad, on_delete=models.CASCADE)
    contenido=models.TextField()
    salario=models.PositiveIntegerField()
    horario=models.CharField(max_length=80)
    empresa=models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='oferta'
        verbose_name_plural='ofertas'

    def __str__(self):
        return self.titulo

    def nombreempresa(self):
        return self.empresa.nombre

    def logoempresa(self):
        return self.empresa.imagen.url

    def nombrearea(self):
        return self.area.nombre

    def nombreciudad(self):
        return self.ciudad.nombre

    
class aplicantes(models.Model):
    ofertaaplicada = models.ForeignKey(oferta, on_delete=models.CASCADE)
    aplicante = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['ofertaaplicada', 'aplicante'], name='unoporoferta')]

    def titulooferta(self):
        return self.ofertaaplicada.titulo

    def nombreaplicante(self):
        return self.aplicante.nombre

