from django.db import models
from django.db.models.deletion import CASCADE
from aplicaciones.tests.models import Test
from aplicaciones.principal.models import Registro
from django.contrib.auth.models import User
# Create your models here.


class Resultado(models.Model):
    id = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE,null=True)
    puntuacion = models.FloatField()
    user = models.ForeignKey(User,on_delete=CASCADE,null=True)

    def __str__(self):
        return str(self.id)
