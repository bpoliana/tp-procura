import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class HealthCenter(models.Model):
    name = models.CharField(max_length=60)
    center_type = models.CharField(max_length=15)
    cnpj = models.CharField(max_length=15)

    def __str__(self):
        return self.nome


class n_UserManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            name__icontains=query, email__icontains=query
        )


class n_User(models.Model):
    user_id = models.AutoField(primary_key=True)
    dj_user = models.OneToOneField(User, on_delete=models.CASCADE)
    utype = models.CharField(max_length=3, blank=True, null=True)

    objects = n_UserManager()

    def get_type(self):
        return self.utype
# def __str__(self):
#	return self.dj_user.name


class Doctor(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Patient(models.Model):
    patient_cpf = models.CharField(max_length=11)
    patient_birthday = models.DateField()
    user = models.ForeignKey(n_User, on_delete=models.CASCADE)

class Fornecedor(models.Model):
    fornecedor_cnpj=models.CharField(max_length=14)

class Medicine(models.Model):
    medicamento_id = models.AutoField(primary_key = True) 
    medicamento_data = models.DateField()
    medicamento_nome = models.CharField(max_length= 45)
    medicamento_dosagem = models.CharField(max_length= 45)
    medicamento_fabricante = models.CharField(max_length= 45)
    medicamento_quantidade = models.DecimalField(max_digits =5,decimal_places=0)
    medicamento_preco = models.DecimalField(max_digits= 2, decimal_places=2 )
    medicamento_endereco = models.CharField(max_length= 45)

# def __str__(self):
# return self.medicamento_nome
