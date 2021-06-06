from django.db.models import fields
from django import forms
from django.forms import widgets
from django.forms.fields import DateField
import django_filters
from django_filters import DateFilter
from aplicaciones.principal.models import ReporteDiario


class DateInput(forms.DateInput):
    input_type = 'date'

class RegFilter(django_filters.FilterSet):
    fechaFil = DateFilter(
        field_name="fecha",
        lookup_expr="iexact",
        widget=DateInput,
        label="Fecha"
    )

    startDate = DateFilter(
        field_name="fecha", 
        lookup_expr="gte",
        widget=DateInput,
        label="Fecha Inicial"
        )
    endDate = DateFilter(
        field_name="fecha",
         lookup_expr="lte",
         widget=DateInput,
         label="Fecha Final"
         )
    class Meta:
        model = ReporteDiario
        fields= ['fecha']
        widgets = {
            'fecha' : DateInput()
        }





