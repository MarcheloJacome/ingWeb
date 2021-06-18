from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.views.generic.detail import DetailView
# Create your models here.

cantidad_agua = [
    (0, '0 vasos'),
    (1, '1 vaso'),
    (2, '2 vasos'),
    (3, '3 vasos'),
    (4, '4 vasos'),
    (5, '5 vasos'),
    (6, '6 vasos'),
    (7, '7 vasos'),
    (8, '8+ vasos'),
]
minutos_ejercicio = [
    (0, '0 minutos'),
    (10, '10 minutos'),
    (20, '20 minutos'),
    (30, '30 minutos'),
    (40, '40+ minutos'),
]
horas_suenio = [
    (0, '0 horas'),
    (1, '1 hora'),
    (2, '2 horas'),
    (3, '3 horas'),
    (4, '4 horas'),
    (5, '5 horas'),
    (6, '6 horas'),
    (7, '7 horas'),
    (8, '8+ horas'),
]
"""class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre"""


class Producto(models.Model):
    #id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre


class Test(models.Model):
    #id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    numero_preguntas = models.IntegerField()

    def __str__(self):
        return f"{self.nombre}"

    def get_preguntas(self):
        return self.pregunta_set.all()[:self.numero_preguntas]

class Registro(models.Model):
    #id = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    agua = models.IntegerField(choices=cantidad_agua)
    ejercicio = models.IntegerField(choices=minutos_ejercicio)
    sleep = models.IntegerField(choices=horas_suenio)
    estres = models.DecimalField(max_digits=5, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pk)


class ReporteDiario(models.Model):
    #id = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True)
    #comentarios = models.CharField(max_length=300)
    agua = models.IntegerField()
    ejercicio = models.IntegerField()
    sleep = models.IntegerField()
    estres = models.DecimalField(max_digits=5, decimal_places=2)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #registro = models.OneToOneField(Registro,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pk)


class ReporteGeneral(models.Model):
    #id = models.AutoField(primary_key=True)
    fechaIn = models.DateField(null=True)
    fechaFin = models.DateField(null=True)
    #comentarios = models.CharField(max_length=300)
    agua = models.DecimalField(max_digits=5, decimal_places=2)
    ejercicio = models.DecimalField(max_digits=5, decimal_places=2)
    sleep = models.DecimalField(max_digits=5, decimal_places=2)
    estres = models.DecimalField(max_digits=5, decimal_places=2)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pk)








