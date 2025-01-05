from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class SupplierType(models.Model):
    name = models.CharField("Nome", max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField("Nome", max_length=255)
    supplierType = models.ForeignKey(SupplierType,related_name='subCategory', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField("Nome",max_length=255)
    category = models.ForeignKey(Category, related_name="subCategory", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Procedure(models.Model):
    name = models.CharField("Procedimento",max_length=255)
    subCategory = models.ForeignKey(SubCategory,related_name='procedure', on_delete=models.SET_NULL, null=True)
    base_price = models.DecimalField("Preço Base", max_digits=10, decimal_places=2, default=0, null=True)
    code = models.CharField(max_length=12,null=True, blank=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField("Nome da empresa",max_length=255)
    firstUserName = models.CharField("Nome do utilizador (Primeiro utilizador)", max_length=255,null=True)
    nuitNumber = models.CharField("NUIT",max_length=15)
    phoneNumber = models.CharField("Número de celular",max_length=15)
    email = models.CharField("Email",max_length=100)
    address = models.CharField("Endereço",max_length=100)
    district = models.CharField("Distrito",max_length=100)
    province = models.CharField("Provincia",max_length=100)
    contractFile = models.FileField(upload_to='static/img/supplierContracts/')
    nuitFile = models.FileField(upload_to='static/img/supplierNuits/')
    user = models.ManyToManyField(User, related_name='supplier')
    supplierType = models.ForeignKey(SupplierType,related_name='supplier', on_delete=models.SET_NULL, null=True)
    latitude = models.CharField("Latitude", max_length=100,null=True, blank=True)
    longitude = models.CharField("longitude", max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name

class InsuranceCompanyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class InsuranceCompany(models.Model):
    name = models.CharField("Nome da empresa",max_length=255)
    firstUserName = models.CharField("Nome do utilizador (Primeiro utilizador)",max_length=255,null=True)
    perParticipationCompay = models.CharField("Percentagem de participação da Empresa",max_length=255,null=True)
    perParticipationBeneficiaries = models.CharField("Percentagem de participação Beneficiários",max_length=255,null=True)
    nuitNumber = models.CharField("NUIT",max_length=15)
    phoneNumber = models.CharField("Número de celular",max_length=15)
    date_of_activity_start = models.DateField("Início de actividade")
    email = models.CharField("Email",max_length=100)
    address = models.CharField("Endereço",max_length=100)
    district = models.CharField("Distrito",max_length=100)
    province = models.CharField("Provincia",max_length=100)
    contractFile = models.FileField(upload_to='static/img/insuranceCompanyContracts/')
    nuitFile = models.FileField(upload_to='static/img/insuranceCompanyNuits/')
    insuranceCompanyType = models.ForeignKey(InsuranceCompanyType, on_delete=models.CASCADE,related_name='insuranceCompany')
    user = models.ManyToManyField(User, blank=True, related_name='insuranceCompany')
    supplier = models.ManyToManyField(Supplier, blank=True,related_name='insuranceCompany')

    def __str__(self):
        return self.name

class InsurancePlan(models.Model):
    name = models.CharField("Nome do Plano", max_length=255,unique=True)
    status = models.CharField("Status do Plano", max_length=20, choices=[
        ('activo', 'Activo'),
        ('cancelado', 'Cancelado'),
        ('suspenso', 'Suspenso'),
        ('expirado', 'Expirado'),
    ], default='activo')
    hasPlafon = models.BooleanField(default=False)
    plafonPrice = models.DecimalField("Plafon do plano", max_digits=10, decimal_places=2,default=0)
    insuranceCompany = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Level(models.Model):
    plan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE, related_name="levels", verbose_name="Plano")
    parent_level = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name="sublevels", blank=True, null=True, verbose_name="Nível Pai"
    )
    name = models.CharField(max_length=255, verbose_name="Nome do Nível")
    hasPlafon = models.BooleanField(default=False, blank=True, null=True)
    plafonPrice = models.DecimalField("Plafon do plano", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return self.name

class InsuranceCompanyProcedure(models.Model):
    negotiated_price = models.DecimalField("Preço Negociado", max_digits=10, decimal_places=2)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE,null=True, blank=True,related_name="insuranceCompanyProcedure")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True,related_name="insuranceCompanyProcedure")

class Client(models.Model):
    name = models.CharField("Nome da empresa",max_length=255)
    firstUserName = models.CharField("Nome do utilizador (Primeiro utilizador)", max_length=255,null=True)
    nuitNumber = models.CharField("NUIT",max_length=15)
    phoneNumber = models.CharField("Número de celular",max_length=15)
    date_of_activity_start = models.DateField("Início de actividade")
    email = models.CharField("Email",max_length=100)
    address = models.CharField("Endereço",max_length=100)
    district = models.CharField("Distrito",max_length=100)
    province = models.CharField("Provincia",max_length=100)
    contractFile = models.FileField(upload_to='static/img/clients/')
    nuitFile = models.FileField(upload_to='static/img/clients/')
    insuranceCompany = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE,null=True, blank=True)
    # user = models.ManyToManyField(User, null=True, blank=True, related_name='client')
    # insurancePlan = models.ManyToManyField(InsurancePlan, null=True, blank=True, related_name='insurancePlan')

    def __str__(self):
        return self.name


class Beneficiaries(models.Model):
    name = models.CharField("Nome da Completo",max_length=255,null=True, blank=True)
    nuitNumber = models.CharField("NUIT",max_length=15, null=True, blank=True)
    plafon = models.CharField("Plafon",max_length=15, null=True, blank=True)
    phoneNumber = models.CharField("Número de celular",max_length=15, null=True, blank=True)
    date_of_activity_start = models.DateField("Início de actividade", null=True, blank=True)
    email = models.CharField("Email",max_length=100, null=True, blank=True)
    address = models.CharField("Endereço",max_length=100, null=True, blank=True)
    district = models.CharField("Distrito",max_length=100, null=True, blank=True)
    province = models.CharField("Provincia",max_length=100, null=True, blank=True)
    session_id = models.CharField("session_id",max_length=100,null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name='beneficiaries')
    insuranceCompany = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, null=True, blank=True, related_name='beneficiaries')
    insurancePlan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE, related_name='beneficiaries',null=True, blank=True)

    def __str__(self):
        return self.name

class Individuals(models.Model):
    name = models.CharField("Nome da Completo",max_length=255,null=True, blank=True)
    nuitNumber = models.CharField("NUIT",max_length=15, null=True, blank=True)
    percentageParticipation = models.CharField("Percentagem de participação",max_length=15, null=True, blank=True)
    phoneNumber = models.CharField("Número de celular",max_length=15, null=True, blank=True)
    date_of_activity_start = models.DateField("Início de actividade", null=True, blank=True)
    email = models.CharField("Email",max_length=100, null=True, blank=True)
    address = models.CharField("Endereço",max_length=100, null=True, blank=True)
    district = models.CharField("Distrito",max_length=100, null=True, blank=True)
    province = models.CharField("Provincia",max_length=100, null=True, blank=True)
    session_id = models.CharField("session_id",max_length=100,null=True, blank=True)
    insuranceCompany = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, null=True, blank=True, related_name='individuals')
    insurancePlan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE, related_name='individuals',null=True, blank=True)


    def __str__(self):
        return self.name

class BeneficiarieTreatment(models.Model):
    beneficiarie = models.ForeignKey(Beneficiaries, on_delete=models.CASCADE, related_name='beneficiarieTreatment')
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, null=True, blank=True, related_name='beneficiarieTreatment')


    def __str__(self):
        return f"Treatment for {self.beneficiarie} - {self.procedure}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_color = models.CharField(max_length=20, blank=True, null=True, default="#000")
    logo = models.ImageField(upload_to='static/img/profile_logo/', blank=True, null=True)
    photo = models.ImageField(upload_to='static/img/profile_photos/', blank=True, null=True)

