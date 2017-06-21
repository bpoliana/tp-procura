import datetime

from django import forms
from django.core.exceptions import ValidationError
from datetime import *
from django.contrib.auth.models import User
from django.forms import ModelForm

from proc.models import Patient
from .models import n_User
from .models import Medicine


class RegistrationForm(forms.Form):
    # cpf_regex = '^[0-9{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$'
    cpf_regex = '^[0-9]{11}$'
    cpf_error_msg = 'Esse cpf é inválido.'

    name = forms.CharField(label='Nome', max_length=100, required=True)
    cpf = forms.RegexField(label='CPF:', regex=cpf_regex, max_length=14, min_length=11, required=True)
    #	user_type = forms.CharField(label='Você é Paciente, Médico, Gerente de Centros de Saúde ou Fornecedor?', max_length=20, required=True)

    email = forms.EmailField(label='Email:', required=True)
    password = forms.CharField(label='Senha:', widget=forms.PasswordInput(), required=True)
    conf_password = forms.CharField(label='Confirme sua senha:', widget=forms.PasswordInput(), required=True)

    date_cadastro = date.today()


class RegistrationFormMedicine(forms.Form):
    # class Meta:
    # model = Medicine
    # fields = ['medicamento_id','medicamento_nome','medicamento_data','medicamento_dosagem','medicamento_fabricante','medicamento_quantidade']
    medicamento_nome = forms.CharField(label='Nome', max_length=45, required=True)
    medicamento_data = forms.DateField(label='Vencimento', required=True)
    medicamento_dosagem = forms.CharField(label='Dosagem', max_length=45, required=True)
    medicamento_fabricante = forms.CharField(label='Fabricante', max_length=45, required=True)
    medicamento_quantidade = forms.DecimalField(label='Quantidade', max_digits=5, decimal_places=0, required=True)
    medicamento_preco = forms.DecimalField(label = 'Preço',max_digits= 5,decimal_places=2, required=True)
    medicamento_endereco =  forms.CharField(max_length= 45)


class RegistrationFormPatient(forms.Form):
    this_year = date.today().year
    patient_cpf = forms.CharField(label='CPF', max_length=30, required=True)
    patient_birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, this_year + 1)),
                                       label='Data de Nascimento')

    def clean_patient_cpf(self):  # Valida CPF ja existe
        cpf = self.cleaned_data['patient_cpf']
        exist_cpf = Patient.objects.filter(patient_cpf=cpf)

        if len(exist_cpf) > 0:
            raise ValidationError('CPF ja existe')
        return self.cleaned_data['patient_cpf']

    def clean_patient_birthday(self):  # Valida data
        birthday = self.cleaned_data['patient_birthday']

        if birthday > date.today():
            raise ValidationError('Nao chegamos a essa data ainda')
        return self.cleaned_data['patient_birthday']


class RegistrationFormFornecedor(forms.Form):
    patient_cnpj = forms.CharField(label='CNPJ', max_length=30, required=True)
    
    def clean_fornecedor_cnpj(self):  # Valida CNPJ ja existe
        cnpj= self.cleaned_data['fornecedor_cnpj']
        exist_cnpj = Fornecedor.objects.filter(fornecedor_cnpj=cnpj)

        if len( exist_cnpj) > 0:
            raise ValidationError('CNPJ ja existe')
        return self.cleaned_data['fornecedor_cnpj']

class UpdateFormFornecedor(forms.Form):
    nome = forms.CharField(label='Nome', max_length=15)
    email = forms.EmailField(label='Email')
    fornecedor_cnpj = forms.CharField(label='CNPJ', max_length=30, required=True)


class UpdateFormPatient(forms.Form):
    this_year = date.today().year
    nome = forms.CharField(label='Nome', max_length=15)
    email = forms.EmailField(label='Email')
    patient_cpf = forms.CharField(label='CPF', max_length=30, required=True)
    patient_birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, this_year + 1)),
                                       label='Data de Nascimento')

    def clean_patient_birthday(self):  # Valida data
        birthday = self.cleaned_data['patient_birthday']

        if birthday > date.today():
            raise ValidationError('Nao chegamos a essa data ainda')
        return self.cleaned_data['patient_birthday']


class RegistrationFormGlobal(forms.Form):
    tipo = (
        ("Med", "Médico"),
        ("Pac", "Paciente"),
        ("For", "Fornecedor"),
        ("Cen", "Centro de Saúde")
    )

    tipoform = forms.ChoiceField(choices=tipo, label='Tipo')
    name = forms.CharField(max_length=100, label='Nome')
    email = forms.EmailField(max_length=100, label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), max_length=20, label='Senha')
