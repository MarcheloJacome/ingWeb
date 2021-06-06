from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from aplicaciones.tests.models import Test
# Create your models here.


class Pregunta(models.Model):
    id = models.AutoField(primary_key=True)
    texto = models.CharField(max_length=300)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.texto)

    def get_respuestas(self):
        return self.respuesta_set.all()


class Respuesta(models.Model):
    id = models.AutoField(primary_key=True)
    texto = models.CharField(max_length=300)
    valor = models.IntegerField()
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"pregunta: {self.pregunta.texto}, respuesta: {self.texto}, valor: {self.valor}"
