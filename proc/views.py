from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import *
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from .models import HealthCenterOk, n_User, Medicine
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
    return redirect('proc:home')  # logout redireciona para pagina inicial


@login_required(login_url='/accounts/login')
def home(request):
    return render(request,'proc/index.html', {})


def login_user(request):
    return render(request, 'registration/login.html', {})


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
    form = RegistrationFormPatient()
    if request.method == 'POST':
        form = RegistrationFormPatient(request.POST)
        if form.is_valid():
            user = n_User.objects.get(pk=id)
            cpf = form.cleaned_data['patient_cpf']
            birthday = form.cleaned_data['patient_birthday']
            Patient.objects.create(user=user, patient_cpf=cpf, patient_birthday=birthday)
            messages.info(request, 'Paciente criado com sucesso')
            return redirect('login')

    return render(request, 'proc/patientregister.html', {'form': form, 'id': id})

def show_perfil(request):
    tipo = n_User.objects.get(dj_user=request.user).utype

    if tipo == 'Pac': # adicionar os links de cada perfil
        return redirect('proc:patient_registered')
    else:
        return redirect('proc:home')

def patient_show(request):
    dj_user = request.user
    user = n_User.objects.get(dj_user=dj_user)
    pat = Patient.objects.get(user=user)
    return render(request, "proc/showpatient.html", {'pat': pat})


def patient_delete(request):
    dj_user = request.user
    user = n_User.objects.get(dj_user=dj_user)
    pat = Patient.objects.get(user=user)
    if request.method == 'POST':
        messages.info(request, 'Paciente deletado com sucesso')
        pat.delete()
        user.delete()
        dj_user.delete()
        return redirect('proc:home')


    return render(request,'proc/patientdelete.html', {})


@login_required(login_url='/accounts/login')
def patient_update(request):
    dj_user = request.user
    user = n_User.objects.get(dj_user=dj_user)
    pat = Patient.objects.get(user=user)
    form = UpdateFormPatient()
    nome_field = form.fields['nome']
    email_field = form.fields['email']
    cpf_field = form.fields['patient_cpf']
    birth_field = form.fields['patient_birthday']

    # Set inital values
    nome_field.initial = dj_user.first_name
    email_field.initial = dj_user.username
    cpf_field.initial = pat.patient_cpf
    birth_field.initial = pat.patient_birthday

    if request.method == 'POST':
        form = UpdateFormPatient(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            cpf = form.cleaned_data['patient_cpf']
            birth = form.cleaned_data['patient_birthday']
            flag_error = False
            if email != dj_user.username and len(User.objects.filter(username=email)) > 0:
                flag_error = True
                form.add_error('email', 'Email ja existe')
            if cpf != pat.patient_cpf and len(Patient.objects.filter(patient_cpf=cpf)) > 0:
                flag_error = True
                form.add_error('patient_cpf', 'CPF ja existe')

            if not flag_error:
                pat.patient_cpf = cpf
                pat.patient_birthday = birth
                pat.save()
                dj_user.first_name = nome
                dj_user.username = email
                dj_user.save()
                messages.info(request, 'Paciente editado com sucesso')
                return redirect('patient_registered')


    return render(request, 'proc/patientupdate.html', {'form': form, 'id': pat.pk, 'pat': pat})

#Centro de Saude

def healthcenter_register(request, id):
    form = RegistrationFormHealthCenter()
    if request.method == 'POST':
        form = RegistrationFormHealthCenter(request.POST)
        if form.is_valid():
            user = n_User.objects.get(pk=id)
            nome = form.cleaned_data['centro_nome']
            tipo = form.cleaned_data['centro_tipo']
            endereco = form.cleaned_data['centro_endereco']
            HealthCenterOk.objects.create(user=user, healthcenter_nome=nome, healthcenter_tipo=tipo)
            messages.info(request, 'Centro de Saude criado com sucesso')
            return redirect('login')

    return render(request, 'proc/patientregister.html', {'form': form, 'id': id})

def show_perfil(request):
    tipo = n_User.objects.get(dj_user=request.user).utype

    if tipo == 'Cen': # adicionar os links de cada perfil
        return redirect('proc:healthcenter_registered')
    else:
        return redirect('proc:home')

def healthcenter_show(request):
    dj_user = request.user
    user = n_User.objects.get(dj_user=dj_user)
    cen = HealthCenterOk.objects.get(user=user)
    return render(request, "proc/healthcenter_show.html", {'cen': cen})


def healthcenter_delete(request):
    dj_user = request.user
    user = n_User.objects.get(dj_user=dj_user)
    cen = HealthCenterOk.objects.get(user=user)
    if request.method == 'POST':
        messages.info(request, 'Centro de Saude deletado com sucesso')
        cen.delete()
        user.delete()
        dj_user.delete()
        return redirect('proc:home')


    return render(request,'proc/healthcenter_delete.html', {})


@login_required(login_url='/accounts/login')
def healthcenter_update(request):
    dj_user = request.user
    user = n_User.objects.get(dj_user=dj_user)
    cen = HealthCenterOk.objects.get(user=user)
    form = UpdateFormPatient()
    nome_field = form.fields['nome']
    email_field = form.fields['email']
    nome_centro_field = form.fields['cen.centro_nome']
    tipo_centro_field = form.fields['cen.centro_tipo']

    end_field = form.fields['centro_endereco']

    # Set inital values
    nome_field.initial = dj_user.first_name
    email_field.initial = dj_user.username
    nome_centro_field.initial = cen.centro_nome
    end_field.initial = cen.centro_endereco

    if request.method == 'POST':
        form = UpdateFormPatient(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            cen_nome = form.cleaned_data['centro_nome']
            cen_tipo = form.cleaned_data['centro_tipo']
            cen_end = form.cleaned_data['centro_endereco']
            
            flag_error = False
            if email != dj_user.username and len(User.objects.filter(username=email)) > 0:
                flag_error = True
                form.add_error('email', 'Email ja existe')
            if cen_nome != cen.centro_nome and len(HealthCenterOk.objects.filter(centro_nome=cen_nome)) > 0:
                flag_error = True
                form.add_error('centro_nome', 'Ja existe um Centro com esse nome.')

            if not flag_error:
                cen.cen_nome = nome
                cen.centro_tipo = cen_tipo
                cen.centro_endereco = cen_end
                cen.save()
                dj_user.first_name = nome
                dj_user.username = email
                dj_user.save()
                messages.info(request, 'Centro de saude editado com sucesso')
                return redirect('healthcenter_registered')


    return render(request, 'proc/healthcenter_update.html', {'form': form, 'id': cen.pk, 'cen': cen})
