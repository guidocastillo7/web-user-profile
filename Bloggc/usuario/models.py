from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True)
    pais = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imgPerfil', default='imgPerfil/img_default.jpg')

    def __str__(self):
        return self.pais
    
