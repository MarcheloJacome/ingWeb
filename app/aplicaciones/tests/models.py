from django.db import models

# Create your models here.


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    numero_preguntas = models.IntegerField()

    def __str__(self):
        return f"{self.nombre}"

    def get_preguntas(self):
        return self.pregunta_set.all()[:self.numero_preguntas]
