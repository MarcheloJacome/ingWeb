# Vista basada en funciones
from aplicaciones.principal.models import ReporteDiario, ReporteGeneral, Test,Registro
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.http import HttpResponse, request
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from .forms import CreateUserForm, RegistroForm, FechasForm, AguaForm,EjercicioForm,SleepForm, NotificacionAguaForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .filters import RegFilter
import datetime


# Create your views here.
@login_required(login_url="/login")
def inicio(request):
    return render(request, 'index')


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se creó exitosamente la cuenta')
    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('index')
        else:
            messages.info(request, 'Datos incorrectos')
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url="/login")
def diario(request):
    user = request.user   
    if request.method =="GET":
        try:
            regis = Registro.objects.get(usuario=user, fecha=datetime.date.today())
        except Registro.DoesNotExist:
            Registro.objects.create(agua=0, ejercicio=0, sleep=0, estres=0, usuario=user)
            regis = Registro.objects.get(
                usuario=user, fecha=datetime.date.today())
        form = RegistroForm(instance=regis)
        if datetime.datetime.now().strftime("%H:%M") == '12:47':
            return redirect('notificacionAgua/'+str(regis.pk))
        return render(request, 'diario.html', {'form': form,'object':regis})
    else:
        regis = Registro.objects.get(usuario=user, fecha=datetime.date.today())
        form = RegistroForm(request.POST, instance=regis)
        if form.is_valid():
            form.save()
            #Puntos por el estres
            resultados =[]
            nE = regis.estres #test de estres
            #calculo de la calificacion
            #puntos por agua
            if regis.agua >= 8:
                resultados += [1]
            else:
                resultados += [regis.agua * 0.125]
            #puntos por ejercicio
            if regis.ejercicio >= 40:
                resultados+=[2]
            else:
                resultados += [regis.ejercicio * 0.05]
            #puntos por sleep
            if regis.sleep >= 7 and regis.sleep:
                resultados += [3.5]
            else:
                resultados += [regis.sleep*(7/16)]      
            #puntos por test de estres
            if nE >=0 and nE<=4:
                resultados += [3.5]
            elif nE>4 and nE<=12:
                resultados += [2.5]
            elif nE > 12 and nE <= 24:
                resultados += [1.5]
            elif nE > 24 and nE <= 40:
                resultados += [0]
            #calculo final de calificacion
            caliFinal=sum(resultados)
            try:
                reporte = ReporteDiario.objects.get(
                    usuario=user, fecha=datetime.date.today())
            except ReporteDiario.DoesNotExist:
                reporte = ReporteDiario.objects.create(
                    fecha=regis.fecha,
                    comentarios="",
                    agua=regis.agua,
                    ejercicio=regis.ejercicio,
                    sleep=regis.sleep,
                    estres=regis.estres,
                    calificacion=caliFinal,
                    usuario=user)
            reporte.comentarios = ""
            reporte.agua = regis.agua
            reporte.ejercicio = regis.ejercicio
            reporte.sleep = regis.sleep
            reporte.estres = regis.estres
            reporte.calificacion = caliFinal
            reporte.save()
        return render(request, 'diario.html', {'form': form, 'object': regis})


@login_required(login_url="/login")
def reporteDiarioDetail(request):
    user = request.user
    try:
        reporte = ReporteDiario.objects.get(usuario=user, fecha=datetime.date.today())
    except ReporteDiario.DoesNotExist:
        reporte = ReporteDiario.objects.create(
            fecha=datetime.date.today(),
            comentarios='',
            agua=0, 
            ejercicio=0, 
            sleep=0,
            estres=0,
            calificacion=0,
            usuario=user)
    #Mensajes agua
    if reporte.agua == 0:
        messages.add_message(request, messages.ERROR,
                             'Necesitas tomar agua!', extra_tags='agua')
        #messages.error(request,'Necesitas tomar agua!',extra_tags='agua')
    if reporte.agua > 0 and reporte.agua <= 6:
        messages.add_message(request, messages.WARNING,
                             'Deberías tomar mas agua!', extra_tags='agua')
    if reporte.agua > 6 and reporte.agua <= 8:
        messages.add_message(request, messages.SUCCESS,
                             'Tu ingesta de agua está muy bien!', extra_tags='agua')
    #Mensajes ejercicio
    if reporte.ejercicio == 0:
        messages.add_message(
            request, messages.ERROR, 'Necesitas hacer mas ejercicio!', extra_tags='ejercicio')
    if reporte.ejercicio > 0 and reporte.ejercicio <= 20:
        messages.add_message(request, messages.WARNING,
                             'Deberías hacer un poco mas de ejercicio!', extra_tags='ejercicio')
    if reporte.ejercicio > 20:
        messages.add_message(request, messages.SUCCESS,
                             'Haz realizado una buena cantidad de ejercicio', extra_tags='ejercicio')
    #Mensajes sleep
    if reporte.sleep == 0:
        messages.add_message(
            request, messages.ERROR, 'Necesitas dormir!', extra_tags='sleep')
    if reporte.sleep > 0 and reporte.sleep <= 6:
        messages.add_message(request, messages.WARNING,
                             'Deberías dormir un poco mas!', extra_tags='sleep')
    if reporte.sleep > 6:
        messages.add_message(request, messages.SUCCESS,
                             'Haz dormido lo suficiente', extra_tags='sleep')
    #Mensajes estres
    if reporte.estres >= 0 and reporte.estres <= 8:
        messages.add_message(
            request, messages.SUCCESS, 'Excelente! Haz mantenido un nivel bajo de estres', extra_tags='estres')
    if reporte.estres > 8 and reporte.sleep <= 30:
        messages.add_message(request, messages.WARNING,
                             'Deberías manejar un poco más tu estrés!', extra_tags='estres')
    if reporte.estres > 30:
        messages.add_message(request, messages.ERROR,
                             'Te encuentras muy estresado, intenta relajarte un poco.', extra_tags='estres')
    #Mensajes calificacion
    if reporte.calificacion >= 0 and reporte.calificacion <= 4:
        messages.add_message(
            request, messages.ERROR, 'Necesitas mejorar tus hábitos', extra_tags='calif')
    if reporte.calificacion > 4 and reporte.calificacion <= 8:
        messages.add_message(request, messages.WARNING,
                             'Calificación regular. Podrías mejorar un poco más!', extra_tags='calif')
    if reporte.calificacion > 8:
        messages.add_message(request, messages.SUCCESS,
                             'Excelente! Continúa manteniendo estos hábitos.', extra_tags='calif')
    context ={"object":reporte}
    return render(request,'reporteDiario.html',context)
        #regis = Registro.objects.get(usuario=user, fecha=datetime.date.today())


@login_required(login_url="/login")
def reporteFechas(request):
    user = request.user
    form = FechasForm()
    if request.method == "GET":
        return render(request, 'reporteFechas.html', {'form': form})
    if request.method == 'POST':
        form = FechasForm(request.POST)
        if form.is_valid():
            fechaI = form.cleaned_data.get("fechaInicio")
            fechaF = form.cleaned_data.get("fechaFin")
            if fechaI >= fechaF:
                messages.warning(
                    request, 'La fecha inicial no puede ser igual o posterior a la final')
                #messages.info(request, 'La fecha inicial no puede ser igual o mayor a la final')
                return render(request, 'reporteFechas.html', {'form': form})

            try:
                reportes = ReporteDiario.objects.filter(fecha__range=[fechaI, fechaF],usuario=user)
            except ReporteDiario.DoesNotExist:
                messages.info(
                    request, 'No existen reportes en las fechas introducidas')
                return render(request, 'reporteFechas.html', {'form': form})
            nRep =reportes.count()
            if nRep < 2:
                messages.info(
                    request, 'Deben haber 2 o mas reportes entre las fechas introducidas')
                return render(request, 'reporteFechas.html', {'form': form})
            #request.session['fecha_inicio']=fechaI
            #request.session['fecha_fin'] = fechaF
            global fechaInicio
            def fechaInicio():
                return fechaI
            global fechaFin
            def fechaFin():
                return fechaF
            promAgua=[]
            promEje = []
            promSle=[]
            promEstr=[]
            promCalif = []
            for rep in reportes:
                promAgua += [rep.agua]
                promEje += [rep.ejercicio]
                promSle += [rep.sleep]
                promEstr += [rep.estres]
                promCalif += [rep.calificacion]
            promAgua = sum(promAgua)/nRep
            promEje = sum(promEje)/nRep
            promSle = sum(promSle)/nRep
            promEstr = sum(promEstr)/nRep
            promCalif = sum(promCalif)/nRep
            try:
                ReporteGeneral.objects.get(
                    usuario=user, fechaIn=fechaI, fechaFin=fechaF)
            except ReporteGeneral.DoesNotExist:
                ReporteGeneral.objects.create(
                    fechaIn=fechaI,
                    fechaFin=fechaF,
                    comentarios="",
                    agua=promAgua,
                    ejercicio=promEje,
                    sleep=promSle,
                    estres=promEstr,
                    calificacion=promCalif,
                    usuario=user
                )
            return redirect('reporteGeneral')


@login_required(login_url="/login")
def reporteGeneral(request):
    user = request.user
    fechaI=fechaInicio()
    fechaF=fechaFin()
    #fechaI=request.session['fecha_inicio']  
    #fechaF=request.session['fecha_fin']
    try:
        reporte = ReporteGeneral.objects.get(
            usuario=user, fechaIn=fechaI, fechaFin=fechaF)
    except ReporteGeneral.DoesNotExist:
        messages.info(request,'Error')
        return render(request, 'reporteGeneral.html')
    #Mensajes agua
    if reporte.agua == 0:
        messages.add_message(request, messages.ERROR,
                             'Necesitas tomar agua!', extra_tags='agua')
        #messages.error(request,'Necesitas tomar agua!',extra_tags='agua')
    if reporte.agua > 0 and reporte.agua <= 6:
        messages.add_message(request, messages.WARNING,
                             'Deberías tomar mas agua!', extra_tags='agua')
    if reporte.agua > 6 and reporte.agua <= 8:
        messages.add_message(request, messages.SUCCESS,
                             'Tu ingesta de agua está muy bien!', extra_tags='agua')
    #Mensajes ejercicio
    if reporte.ejercicio == 0:
        messages.add_message(
            request, messages.ERROR, 'Necesitas hacer mas ejercicio!', extra_tags='ejercicio')
    if reporte.ejercicio > 0 and reporte.ejercicio <= 20:
        messages.add_message(request, messages.WARNING,
                             'Deberías hacer un poco mas de ejercicio!', extra_tags='ejercicio')
    if reporte.ejercicio > 20:
        messages.add_message(request, messages.SUCCESS,
                             'Haz realizado una buena cantidad de ejercicio', extra_tags='ejercicio')
    #Mensajes sleep
    if reporte.sleep == 0:
        messages.add_message(
            request, messages.ERROR, 'Necesitas dormir!', extra_tags='sleep')
    if reporte.sleep > 0 and reporte.sleep <= 6:
        messages.add_message(request, messages.WARNING,
                             'Deberías dormir un poco mas!', extra_tags='sleep')
    if reporte.sleep > 6:
        messages.add_message(request, messages.SUCCESS,
                             'Haz dormido lo suficiente', extra_tags='sleep')
    #Mensajes estres
    if reporte.estres >= 0 and reporte.estres <= 8:
        messages.add_message(
            request, messages.SUCCESS, 'Excelente! Haz mantenido un nivel bajo de estres', extra_tags='estres')
    if reporte.estres > 8 and reporte.sleep <= 30:
        messages.add_message(request, messages.WARNING,
                             'Deberías manejar un poco más tu estrés!', extra_tags='estres')
    if reporte.estres > 30:
        messages.add_message(request, messages.ERROR,
                             'Te encuentras muy estresado, intenta relajarte un poco.', extra_tags='estres')
    #Mensajes calificacion
    if reporte.calificacion >= 0 and reporte.calificacion <= 4:
        messages.add_message(
            request, messages.ERROR, 'Necesitas mejorar tus hábitos', extra_tags='calif')
    if reporte.calificacion > 4 and reporte.calificacion <= 8:
        messages.add_message(request, messages.WARNING,
                             'Calificación regular. Podrías mejorar un poco más!', extra_tags='calif')
    if reporte.calificacion > 8:
        messages.add_message(request, messages.SUCCESS,
                             'Excelente! Continúa manteniendo estos hábitos.', extra_tags='calif')
    context = {"object": reporte}
    return render(request, 'reporteGeneral.html', context)


@login_required(login_url="/login")
def reportesList(request):
    user = request.user
    reportes = ReporteDiario.objects.filter(usuario=user)
    filter = RegFilter(request.GET,queryset = reportes)
    reportes = filter.qs
    #reportes = get_list_or_404(ReporteDiario, usuario=user)
    context = {'rep_list': reportes,'filter':filter}
    return render(request, "listarReportes.html", context)


@login_required(login_url="/login")
def reportesDiariosDetail(request,pk):
    reporte = get_object_or_404(ReporteDiario, pk=pk, usuario=request.user)
    #Mensajes agua
    if reporte.agua == 0: 
        messages.add_message(request, messages.ERROR,'Necesitas tomar agua!', extra_tags='agua')
        #messages.error(request,'Necesitas tomar agua!',extra_tags='agua')
    if reporte.agua >0 and reporte.agua <=6:
        messages.add_message(request,messages.WARNING, 'Deberías tomar mas agua!', extra_tags='agua')
    if reporte.agua >6 and reporte.agua <=8:
        messages.add_message(request,messages.SUCCESS, 'Tu ingesta de agua está muy bien!', extra_tags='agua')
    #Mensajes ejercicio
    if reporte.ejercicio == 0:
        messages.add_message(request,messages.ERROR, 'Necesitas hacer mas ejercicio!', extra_tags='ejercicio')
    if reporte.ejercicio > 0 and reporte.ejercicio <= 20:
        messages.add_message(request,messages.WARNING, 'Deberías hacer un poco mas de ejercicio!',extra_tags='ejercicio')
    if reporte.ejercicio > 20:
        messages.add_message(request,messages.SUCCESS, 'Haz realizado una buena cantidad de ejercicio', extra_tags='ejercicio')
    #Mensajes sleep
    if reporte.sleep == 0:
        messages.add_message(
            request, messages.ERROR, 'Necesitas dormir!', extra_tags='sleep')
    if reporte.sleep > 0 and reporte.sleep <= 6:
        messages.add_message(request, messages.WARNING,
                             'Deberías dormir un poco mas!', extra_tags='sleep')
    if reporte.sleep > 6:
        messages.add_message(request, messages.SUCCESS,
                             'Haz dormido lo suficiente', extra_tags='sleep')
    #Mensajes estres
    if reporte.estres >= 0 and reporte.estres <=8:
        messages.add_message(
            request, messages.SUCCESS, 'Excelente! Haz mantenido un nivel bajo de estres', extra_tags='estres')
    if reporte.estres > 8 and reporte.sleep <= 30:
        messages.add_message(request, messages.WARNING,
                             'Deberías manejar un poco más tu estrés!', extra_tags='estres')
    if reporte.estres > 30:
        messages.add_message(request, messages.ERROR,
                             'Te encuentras muy estresado, intenta relajarte un poco.', extra_tags='estres')
    #Mensajes calificacion
    if reporte.calificacion >= 0 and reporte.calificacion <= 4:
        messages.add_message(
            request, messages.ERROR, 'Necesitas mejorar tus hábitos', extra_tags='calif')
    if reporte.calificacion > 4 and reporte.calificacion <= 8:
        messages.add_message(request, messages.WARNING,
                             'Calificación regular. Podrías mejorar un poco más!', extra_tags='calif')
    if reporte.calificacion > 8:
        messages.add_message(request, messages.SUCCESS,
                             'Excelente! Continúa manteniendo estos hábitos.', extra_tags='calif')
    context = {"object": reporte}
    return render(request, 'reporteDetalles.html', context)


@login_required(login_url="/login")
def reporteDiarioDelete(request, pk):
    reporte = get_object_or_404(ReporteDiario, pk=pk, usuario=request.user)
    reporte.delete()
    return redirect('listarReportes')


@login_required(login_url="/login")
def reportesGenList(request):
    user = request.user
    reportes = ReporteGeneral.objects.filter(usuario=user)
    #reportes = ReporteGeneral.objects.get(usuario=user)
    #reportes = get_list_or_404 (ReporteGeneral,usuario=user)
    context = {'rep_list': reportes}
    return render(request, "listarReportesGen.html", context)


@login_required(login_url="/login")
def reportesGenDetail(request, pk):
    reporte = get_object_or_404(ReporteGeneral, pk=pk, usuario=request.user)
    #Mensajes agua
    if reporte.agua == 0:
        messages.add_message(request, messages.ERROR,
                             'Necesitas tomar agua!', extra_tags='agua')
        #messages.error(request,'Necesitas tomar agua!',extra_tags='agua')
    if reporte.agua > 0 and reporte.agua <= 6:
        messages.add_message(request, messages.WARNING,
                             'Deberías tomar mas agua!', extra_tags='agua')
    if reporte.agua > 6 and reporte.agua <= 8:
        messages.add_message(request, messages.SUCCESS,
                             'Tu ingesta de agua está muy bien!', extra_tags='agua')
    #Mensajes ejercicio
    if reporte.ejercicio == 0:
        messages.add_message(
            request, messages.ERROR, 'Necesitas hacer mas ejercicio!', extra_tags='ejercicio')
    if reporte.ejercicio > 0 and reporte.ejercicio <= 20:
        messages.add_message(request, messages.WARNING,
                             'Deberías hacer un poco mas de ejercicio!', extra_tags='ejercicio')
    if reporte.ejercicio > 20:
        messages.add_message(request, messages.SUCCESS,
                             'Haz realizado una buena cantidad de ejercicio', extra_tags='ejercicio')
    #Mensajes sleep
    if reporte.sleep == 0:
        messages.add_message(
            request, messages.ERROR, 'Necesitas dormir!', extra_tags='sleep')
    if reporte.sleep > 0 and reporte.sleep <= 6:
        messages.add_message(request, messages.WARNING,
                             'Deberías dormir un poco mas!', extra_tags='sleep')
    if reporte.sleep > 6:
        messages.add_message(request, messages.SUCCESS,
                             'Haz dormido lo suficiente', extra_tags='sleep')
    #Mensajes estres
    if reporte.estres >= 0 and reporte.estres <= 8:
        messages.add_message(
            request, messages.SUCCESS, 'Excelente! Haz mantenido un nivel bajo de estres', extra_tags='estres')
    if reporte.estres > 8 and reporte.sleep <= 30:
        messages.add_message(request, messages.WARNING,
                             'Deberías manejar un poco más tu estrés!', extra_tags='estres')
    if reporte.estres > 30:
        messages.add_message(request, messages.ERROR,
                             'Te encuentras muy estresado, intenta relajarte un poco.', extra_tags='estres')
    #Mensajes calificacion
    if reporte.calificacion >= 0 and reporte.calificacion <= 4:
        messages.add_message(
            request, messages.ERROR, 'Necesitas mejorar tus hábitos', extra_tags='calif')
    if reporte.calificacion > 4 and reporte.calificacion <= 8:
        messages.add_message(request, messages.WARNING,
                             'Calificación regular. Podrías mejorar un poco más!', extra_tags='calif')
    if reporte.calificacion > 8:
        messages.add_message(request, messages.SUCCESS,
                             'Excelente! Continúa manteniendo estos hábitos.', extra_tags='calif')
    context = {"object": reporte}
    return render(request, 'reporteGenDetalles.html', context)


@login_required(login_url="/login")
def reporteGenDelete(request, pk):
    reporte = get_object_or_404(ReporteGeneral, pk=pk, usuario=request.user)
    reporte.delete()
    return redirect('listarReportesGen')


@login_required(login_url="/login")
def updateAgua(request,pk):
    regis = get_object_or_404(
        Registro, usuario=request.user, pk=pk)
    form = AguaForm(instance=regis)
    if request.method == 'GET':  
        return render(request, 'updateAgua.html', {'form': form, 'object': regis})


@login_required(login_url="/login")
def updateEjercicio(request,pk):
    regis = get_object_or_404(
        Registro, usuario=request.user, pk=pk)
    form = EjercicioForm(instance=regis)
    if request.method == 'GET':
        return render(request, 'updateEjercicio.html', {'form': form})


@login_required(login_url="/login")
def updateSleep(request,pk):
    regis = get_object_or_404(
        Registro, usuario=request.user, pk=pk)
    form = SleepForm(instance=regis)
    if request.method == 'GET':
        return render(request, 'updateSleep.html', {'form': form})


@login_required(login_url="/login")
def notificacionAgua(request, pk):
    regis = get_object_or_404(
        Registro, usuario=request.user, pk=pk)
    if request.method == 'GET':
        form = NotificacionAguaForm()
        return render(request, 'notificacionAgua.html', {'form': form})
    else:
        form = NotificacionAguaForm(request.POST)
        if form.is_valid():
            cAgua = form.cleaned_data.get("cantidadAgua")
            regis.agua += cAgua
            regis.save()
        return redirect('index')
