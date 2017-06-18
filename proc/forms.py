import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import n_User
from .models import Medicine


class RegistrationForm(forms.Form):

	#cpf_regex = '^[0-9{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$'
	cpf_regex = '^[0-9]{11}$'
	cpf_error_msg = 'Esse cpf é inválido.'

	name = forms.CharField(label='Nome', max_length=100, required=True)
	cpf = forms.RegexField(label = 'CPF:', regex=cpf_regex, max_length=14, min_length=11, required = True)
#	user_type = forms.CharField(label='Você é Paciente, Médico, Gerente de Centros de Saúde ou Fornecedor?', max_length=20, required=True)

	email = forms.EmailField(label='Email:', required=True)
	password = forms.CharField(label= 'Senha:', widget=forms.PasswordInput(), required=True)
	conf_password = forms.CharField(label= 'Confirme sua senha:', widget=forms.PasswordInput(), required=True)
	
	date_cadastro = datetime.date.today()


class RegistrationFormMedicine(forms.Form):
	#class Meta:
		#model = Medicine
		#fields = ['medicamento_id','medicamento_nome','medicamento_data','medicamento_dosagem','medicamento_fabricante','medicamento_quantidade']
	medicamento_nome = forms.CharField(label='Nome', max_length=45, required=True)
	medicamento_data = forms.DateField(label = 'Vencimento', required = True)
	medicamento_dosagem = forms.CharField(label='Dosagem',max_length=45, required=True)
	medicamento_fabricante = forms.CharField(label='Fabricante',max_length=45,required=True)
	medicamento_quantidade = forms.DecimalField(label='Quantidade', max_digits=5,decimal_places=0,required=True)
    	
class RegistrationFormPatient(forms.Form):
	patient_cpf = forms.CharField(label='CPF', max_length=30, required=True)
	patient_birthday = forms.CharField(label='Data de Nascimento', max_length=30, required=True)
	
class RegistrationFormGlobal(forms.Form):
	tipo = (
		("Med","Médico"),
		("Pac","Paciente"),
		("For","Fornecedor"),
		("Cen","Centro de Saúde")
	)

	tipoform = forms.ChoiceField(choices = tipo, label = 'Tipo')
	name = forms.CharField(max_length=100, label = 'Nome')
	email = forms.EmailField(max_length=100, label='Email')
	password = forms.CharField(widget=forms.PasswordInput(),max_length=20, label = 'Senha')


