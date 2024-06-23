from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Publicacion(models.Model):

    autor = models.ForeignKey(User, on_delete=models.RESTRICT)
    contenido = models.TextField()

    def __str__(self):
        return self.autor