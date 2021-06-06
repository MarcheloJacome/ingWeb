from django.shortcuts import render,redirect
from .models import Test
from django.views.generic import ListView
from django.http import JsonResponse
from aplicaciones.preguntas.models import Pregunta, Respuesta
from aplicaciones.resultados.models import Resultado
from aplicaciones.principal.models import Registro, ReporteDiario
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.



class TestListView(ListView):
    model = Test
    template_name = 'tests/main.html'


@login_required(login_url="/login")
def test_view(request, pk,pk2):
    test = Test.objects.get(pk=pk)
    return render(request, 'tests/test.html',{'obj':test})
#mandar el pk aqui en otra variable aparte de data


@login_required(login_url="/login")
def test_data_view(request,pk,pk2):
    test = Test.objects.get(pk=pk)
    preguntas =[]
    for p in test.get_preguntas():
        respuestas = []
        for r in p.get_respuestas():
            respuestas.append(r.texto)
        preguntas.append({str(p):respuestas})
    return JsonResponse({
        'data': preguntas,
    })


@login_required(login_url="/login")
def save_test_view(request, pk,pk2):
    #print(request.POST)
    if request.is_ajax():
        preguntas = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            print('key: ',k)
            pregunta = Pregunta.objects.get(texto=k)
            preguntas.append(pregunta)
        print(preguntas)
        user = request.user
        test = Test.objects.get(pk=pk)
        score = 0
        results = []
        for p in preguntas:
            r_selected = request.POST.get(p.texto)
            if r_selected != "":
                pregunta_respuestas = Respuesta.objects.filter(pregunta=p)
                for r in pregunta_respuestas:
                    if r_selected == r.texto:
                        score += r.valor
                results.append({str(p):{'respondida':r_selected}})
            else:
                results.append({str(p):'no respondida'})
        regis = Registro.objects.get(usuario=user, fecha=datetime.date.today())
        repor = ReporteDiario.objects.get(
            usuario=user, fecha=datetime.date.today())
        repor.estres = score
        regis.estres = score
        print('Puntuacion:')
        print(regis.estres)
        repor.save()
        regis.save()
        #regis = Registro.objects.filter(usuario=user).filter(
            #fecha=datetime.date.today())
        print(regis.usuario)
        Resultado.objects.create(test=test, user=user, puntuacion=score)
        return JsonResponse({'puntuacion':score,'resultados':results})
