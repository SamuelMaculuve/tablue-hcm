from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField("Nome", max_length=255)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField("Nome",max_length=255)
    category = models.ForeignKey(Category, related_name="subCategory", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Procedure(models.Model):
    name = models.CharField("Procedimento",max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subCategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    base_price = models.DecimalField("Preço Base", max_digits=10, decimal_places=2, default=0, null=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField("Nome da empresa",max_length=255)
    nuitNumber = models.CharField("NUIT",max_length=15)
    phoneNumber = models.CharField("Número de celular",max_length=15)
    date_of_activity_start = models.DateField("Início de actividade")
    email = models.CharField("Email",max_length=100)
    address = models.CharField("Endereço",max_length=100)
    district = models.CharField("Distrito",max_length=100)
    province = models.CharField("Provincia",max_length=100)
    contractFile = models.FileField(upload_to='SupplierContracts/')
    nuitFile = models.FileField(upload_to='SupplierNuits/')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='supplier')
    # procedure = models.ManyToManyField(Procedure, blank=True)

    def save(self, *args, **kwargs):
        if not self.user:
            new_user = User.objects.create_user(
                username=self.name.lower().replace(" ", "_"),
                password="password"
            )
            self.user = new_user

            # group_name = 'Supplier'
            # group = Group.objects.get(name=group_name)
            # new_user.groups.add(group)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class InsuranceCompanyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class InsuranceCompany(models.Model):
    name = models.CharField("Nome da empresa",max_length=255)
    nuitNumber = models.CharField("NUIT",max_length=15)
    phoneNumber = models.CharField("Número de celular",max_length=15)
    date_of_activity_start = models.DateField("Início de actividade")
    email = models.CharField("Email",max_length=100)
    address = models.CharField("Endereço",max_length=100)
    district = models.CharField("Distrito",max_length=100)
    province = models.CharField("Provincia",max_length=100)
    contractFile = models.FileField(upload_to='InsuranceCompanyContracts/')
    nuitFile = models.FileField(upload_to='InsuranceCompanyNuits/')
    insuranceCompanyType = models.ForeignKey(InsuranceCompanyType, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='insuranceCompany')
    supplier = models.ManyToManyField(Supplier, blank=True)

    def save(self, *args, **kwargs):
        if not self.user:
            new_user = User.objects.create_user(
                username=self.name.lower().replace(" ", "_"),
                password="password"
            )
            self.user = new_user

            # group_name = 'InsuranceCompany'
            # group = Group.objects.get(name=group_name)
            # new_user.groups.add(group)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class InsuranceCompanyProcedure(models.Model):
    insuranceCompany = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    procedure = models.ManyToManyField(Procedure, blank=True)
    negotiated_price = models.DecimalField("Preço Negociado", max_digits=10, decimal_places=2)


class Client(models.Model):
    name = models.CharField("Nome da empresa",max_length=255)
    nuitNumber = models.CharField("NUIT",max_length=15)
    phoneNumber = models.CharField("Número de celular",max_length=15)
    date_of_activity_start = models.DateField("Início de actividade")
    email = models.CharField("Email",max_length=100)
    address = models.CharField("Endereço",max_length=100)
    district = models.CharField("Distrito",max_length=100)
    province = models.CharField("Provincia",max_length=100)
    contractFile = models.FileField(upload_to='clients/')
    nuitFile = models.FileField(upload_to='clients/')
    insuranceCompany = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE,null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='client')

    def save(self, *args, **kwargs):
        if not self.user:
            new_user = User.objects.create_user(
                username=self.name.lower().replace(" ", "_"),
                password="password"
            )
            self.user = new_user

            # group_name = 'client'
            # group = Group.objects.get(name=group_name)
            # new_user.groups.add(group)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class InsurancePlan(models.Model):
    name = models.CharField("Nome do Plano", max_length=255)
    status = models.CharField("Status do Plano", max_length=20, choices=[
        ('ativo', 'Ativo'),
        ('cancelado', 'Cancelado'),
        ('suspenso', 'Suspenso'),
        ('expirado', 'Expirado'),
    ], default='ativo')
    insuranceCompany = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, null=True, blank=True)
    procedure = models.ManyToManyField(Procedure, blank=True)

    def __str__(self):
        return self.name

class Beneficiaries(models.Model):
    name = models.CharField("Nome da empresa",max_length=255)
    nuitNumber = models.CharField("NUIT",max_length=15)
    phoneNumber = models.CharField("Número de celular",max_length=15)
    date_of_activity_start = models.DateField("Início de actividade")
    email = models.CharField("Email",max_length=100)
    address = models.CharField("Endereço",max_length=100)
    district = models.CharField("Distrito",max_length=100)
    province = models.CharField("Provincia",max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    insuranceCompany = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, null=True, blank=True)
    insurancePlan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE)

    