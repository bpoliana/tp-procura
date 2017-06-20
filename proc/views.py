from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import *
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from .models import HealthCenter, n_User, Medicine
from .forms import *
from .tables import *
from datetime import *
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
import pdb


def register(request):
    form = RegistrationFormGlobal()

    if request.POST:
        form = RegistrationFormGlobal(request.POST)
        if form.is_valid():
            tipoUser = form.cleaned_data["tipoform"]
            nomeUser = form.cleaned_data["name"]
            senhaUser = form.cleaned_data["password"]
            emailUser = form.cleaned_data["email"]

            dUser = User.objects.create_user(username=emailUser, first_name=nomeUser, email=emailUser,
                                             password=senhaUser)
            nUser = n_User.objects.create(dj_user=dUser, utype=tipoUser)

            if tipoUser == 'Pac':
                return HttpResponseRedirect('/proc/patientregister/' + str(nUser.pk))
            if tipoUser == 'Med':
                return redirect('login')  # cadastro especifico (nameurl)
            if tipoUser == 'Cen':
                return redirect('login')  # cadastro especifico (nameurl)
            if tipoUser == 'For':
                return redirect('login')  # cadastro especifico (nameurl)

    return render(request, 'proc/register.html', {'form': form})


def health_centers(request):
    h = HealthCenter.objects.filter(type='Saude mental')
    # return render(request, 'proc/health_centers.html', {'list1': list1})
    return render(request, 'proc/health_centers.html', {'h': h})


def doctors(request):
    return render(request)


def registersasa(request):
    print(request.method)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['name'], password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])
            return render(request, 'proc/success.html', {'form': form})

    else:
        form = RegistrationForm()
        # variables = RequestContext(request, {'form': form})

    return render(request, 'proc/register.html', {'form': form})


def register_sucessed(request):
    return render_to_response('proc/success.html', )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')  # logout redireciona para pagina inicial


@login_required(login_url='/accounts/login')
def home(request):
    return render_to_response('proc/index.html', {})


def login_user(request):
    return render_to_response('registration/login.html', {})


def medicine_manager(request):
    return render_to_response('proc/main_medicine.html', {})


def medicine_register(request):
    print(request.method)
    if request.method == 'POST':
        form = RegistrationFormMedicine(request.POST)
        if form.is_valid():
            med = Medicine()
            med.medicamento_nome = form.cleaned_data['medicamento_nome']
            med.medicamento_data = form.cleaned_data['medicamento_data']
            med.medicamento_dosagem = form.cleaned_data['medicamento_dosagem']
            med.medicamento_fabricante = form.cleaned_data['medicamento_fabricante']
            med.medicamento_quantidade = form.cleaned_data['medicamento_quantidade']

            med.save()
            # return render(request,'proc/success.html',{'form':form})
            return HttpResponseRedirect('')
    else:
        form = RegistrationFormMedicine()

    return render(request, 'proc/medicineregister.html', {'form': form})


def medicine_show(request):
    queryset = Medicine.objects.all()
    # table = MedicineTable(queryset)
    return render(request, "proc/medicine_registered.html", {'queryset': queryset})


def medicine_delete(request, id):
    med = Medicine.objects.get(pk=id)
    med.delete()
    # Medicine.objects.filter(medicamento_id=id).delete()
    return HttpResponseRedirect('/proc/medicine_registered')


def medicine_update(request, id):
    # pdb.set_trace()
    med = Medicine.objects.get(pk=id)

    if request.method == 'POST':
        form = RegistrationFormMedicine(request.POST)
        if form.is_valid():  # request.POST.get('medicamento_nome')
            # pdb.set_trace()
            med.medicamento_nome = form.cleaned_data['medicamento_nome']
            med.medicamento_data = form.cleaned_data['medicamento_data']
            med.medicamento_dosagem = form.cleaned_data['medicamento_dosagem']
            med.medicamento_fabricante = form.cleaned_data['medicamento_fabricante']
            med.medicamento_quantidade = form.cleaned_data['medicamento_quantidade']
            med.save()
            return HttpResponseRedirect('/proc/medicine_registered')

    else:
        form = RegistrationFormMedicine()
        # form.medicamento_nome = med.medicamento_nome
        # form.medicamento_data = med.medicamento_data
        # form.medicamento_dosagem= med.medicamento_dosagem
        # form.medicamento_fabricante = med.medicamento_fabricante
        # form.medicamento_quantidade = med.medicamento_quantidade
    return render(request, 'proc/medicineupdate.html', {'form': form, 'id': id, 'med': med})


def patient_register(request, id):
    print(request.method)
    form = RegistrationFormPatient()
    if request.method == 'POST':
        form = RegistrationFormPatient(request.POST)
        if form.is_valid():
            user = n_User.objects.get(pk=id)
            cpf = form.cleaned_data['patient_cpf']
            birthday = form.cleaned_data['patient_birthday']
            Patient.objects.create(user=user, patient_cpf=cpf, patient_birthday=birthday)
            return redirect('login')

    return render(request, 'proc/patientregister.html', {'form': form, 'id': id})


def patient_show(request):
    queryset = Patient.objects.get(pk=id)
    return render(request, "proc/patient_registered.html", {'queryset': queryset})


def patient_delete(request, id):
    pat = Patient.objects.get(pk=id)
    pat.delete()
    return HttpResponseRedirect('/proc/patient_registered')


def patient_update(request, id):
    pat = Patient.objects.get(pk=id)

    if request.method == 'POST':
        form = RegistrationFormPatient(request.POST)
        if form.is_valid():
            pat.patient_name = form.cleaned_data['patient_name']
            pat.patient_cpf = form.cleaned_data['patient_cpf']
            pat.patient_telefone = form.cleaned_data['patient_telefone']
            pat.patient_brithday = form.cleaned_data['patient_birthday']
            pat.patient_password = form.cleaned_data['patient_password']

            pat.save()
            return HttpResponseRedirect('/proc/patient_registered')

    else:
        form = RegistrationFormPatient()

    return render(request, 'proc/patientupdate.html', {'form': form, 'id': id, 'pat': pat})
