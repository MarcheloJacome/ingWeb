from django import forms
from django.forms import fields, widgets
from .models import Producto, Registro
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


"""class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()
        }"""


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class RegistroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(RegistroForm, self).__init__(*args, **kwargs)
       self.fields['estres'].widget.attrs['readonly'] = True
       self.fields['agua'].widget.attrs['readonly'] = True
       self.fields['ejercicio'].widget.attrs['readonly'] = True
       self.fields['sleep'].widget.attrs['readonly'] = True
    class Meta:
        model = Registro
        fields=['agua','ejercicio','sleep','estres','usuario']
        labels = {
            'agua':'Vasos de Agua',
            'ejercicio':'Minutos de Ejercicio',
            'sleep':'Horas de Sueño',
            'estres':'Puntuación Test de Estrés'
        }
        widgets = {
            'usuario': forms.HiddenInput(),
            'agua':forms.TextInput(),
            'ejercicio': forms.TextInput(),
            'sleep': forms.TextInput(),
            }


class DateInput(forms.DateInput):
    input_type = 'date'

class FechasForm(forms.Form):
    fechaInicio = forms.DateField(
        required=True, label='Fecha Inicial', widget=DateInput)
    fechaFin = forms.DateField(
        required=True, label='Fecha Final', widget=DateInput)


class AguaForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['agua', 'ejercicio', 'sleep', 'estres', 'usuario']
        labels = {
            'agua': 'Cantidad de Agua',
        }
        widgets = {
            'usuario': forms.HiddenInput(),
            'ejercicio': forms.HiddenInput(),
            'sleep': forms.HiddenInput(),
            'estres': forms.HiddenInput()
        }

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['agua', 'ejercicio', 'sleep', 'estres', 'usuario']
        labels = {
            'ejercicio': 'Tiempo de ejercicio',
        }
        widgets = {
            'usuario': forms.HiddenInput(),
            'agua': forms.HiddenInput(),
            'sleep': forms.HiddenInput(),
            'estres': forms.HiddenInput()
        }


class SleepForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['agua', 'ejercicio', 'sleep', 'estres', 'usuario']
        labels = {
            'sleep': 'Horas de sueño',
        }
        widgets = {
            'usuario': forms.HiddenInput(),
            'agua': forms.HiddenInput(),
            'ejercicio': forms.HiddenInput(),
            'estres': forms.HiddenInput()
        }


class NotificacionAguaForm(forms.Form):
    cantidadAgua = forms.IntegerField(min_value=0)
