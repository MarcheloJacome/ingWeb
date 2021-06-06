from django.contrib import admin
from .models import Producto, Registro, ReporteDiario, ReporteGeneral
# Register your models here.
# admin.site.register(Usuario)


admin.site.register(Producto)
admin.site.register(Registro)
admin.site.register(ReporteDiario)
admin.site.register(ReporteGeneral)
##admin.site.register(Pregunta,PreguntaAdmin)
##admin.site.register(Test)
##admin.site.register(Respuesta)
#admin.site.register(Resultado)
