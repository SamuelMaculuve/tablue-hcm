from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from prodHCM.models import InsuranceCompany, Procedure, Category, Client, Supplier, InsurancePlan, \
    InsuranceCompanyProcedure, BeneficiarieTreatment, Beneficiaries, SubCategory, Individuals, Profile


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class InsuranceCompanyFrom(forms.ModelForm):
    class Meta:
        model = InsuranceCompany
        fields = ('name','nuitNumber','phoneNumber','date_of_activity_start','email','address','district','province','contractFile','nuitFile','insuranceCompanyType','firstUserName','perParticipationCompay','perParticipationBeneficiaries')
        widgets = {
            'date_of_activity_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        labels = {
            'insuranceCompanyType': 'Tipo',
        }

    def __init__(self, *args, **kwargs):
        super(InsuranceCompanyFrom,self).__init__(*args, **kwargs)
        self.fields['insuranceCompanyType'].empty_label = "Select"

class InsurancePlanForm(forms.ModelForm):
    class Meta:
        model = InsurancePlan
        fields =  '__all__'
        # fields = ('name','status')
        # labels = {
        #     'name' : 'Nome',
        #     'status' : 'Estado',
        #     'insuranceCompany' : 'insuranceCompany',
        #     'procedure' : 'procedure',
        # }
    procedure = forms.ModelMultipleChoiceField(
        queryset = Procedure.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        label='Lista de procedimento'
    )

class InsuranceCompanyProcedureForm(forms.ModelForm):
    class Meta:
        model = InsuranceCompanyProcedure
        fields = ['procedure', 'negotiated_price']
        widgets = {
            'negotiated_price': forms.NumberInput(attrs={'placeholder': 'Preço Negociado'}),
            'procedure': forms.CheckboxInput(),
        }

InsuranceCompanyProcedureFormSet = modelformset_factory(
    InsuranceCompanyProcedure,
    form=InsuranceCompanyProcedureForm,
    extra=0
)

class AddSupplierToInsuranceFrom(forms.Form):
    supplier = forms.ModelMultipleChoiceField(
        queryset = Supplier.objects.all(),
        widget = forms.RadioSelect(attrs={'class': 'single-supplier'}),
        label=''
    )

class ProceduresFrom(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = ('name','subCategory','base_price','code')
        subCategory = forms.ModelChoiceField(queryset=SubCategory.objects.none(), empty_label="Selecione a categoria primeiro")

class CategoryFrom(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.DateInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'supplierType': 'Tipo de provedor',
        }

class SubCategoryFrom(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'
        labels = {
            'category': 'Categoria',
        }

class ClientsForm(forms.ModelForm):
        class Meta:
            model = Client
            fields = ('insuranceCompany','name','nuitNumber','phoneNumber','date_of_activity_start','email','address','district','province','contractFile','nuitFile','firstUserName')
            # fields = '__all__'
            widgets = {
                'insuranceCompany': forms.HiddenInput(),
                'date_of_activity_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            }


class AddInsurancePlanClientFrom(forms.Form):
    insurancePlan = forms.ModelMultipleChoiceField(
        queryset=InsurancePlan.objects.all(),  # Inicialmente vazio
        # queryset=InsurancePlan.objects.none(),  # Inicialmente vazio
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'single-InsurancePlan'}),
        label=''
    )

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'nuitNumber', 'phoneNumber', 'email', 'address',
                  'district', 'province', 'contractFile', 'nuitFile','supplierType','firstUserName','latitude','longitude')

        widgets = {
            'date_of_activity_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'procedures': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'supplierType': 'Tipo de provedor',
        }


class BeneficiarieTreatmentForm(forms.ModelForm):
    class Meta:
        model = BeneficiarieTreatment
        fields = '__all__'
        widgets = {
            'beneficiarie': forms.HiddenInput(),
            'procedures': forms.CheckboxSelectMultiple(),
        }

class BeneficiariesForm(forms.ModelForm):
    class Meta:
        model = Beneficiaries
        fields = ('insuranceCompany','client','name','email','insurancePlan','phoneNumber')
        widgets = {
            'client': forms.HiddenInput(),
            'insuranceCompany': forms.HiddenInput(),
        }
        labels = {
            'insurancePlan': 'Plano',
        }

class IndividualsForm(forms.ModelForm):
    class Meta:
        model = Individuals
        fields = ('insuranceCompany','name','email','insurancePlan','phoneNumber')
        widgets = {
            'insuranceCompany': forms.HiddenInput(),
        }
        labels = {
            'insurancePlan': 'Plano',
        }


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Digite o email'
    }))
    first_name = forms.CharField(required=True, label="Primeiro Nome", widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Digite o primeiro nome'
    }))
    last_name = forms.CharField(required=True, label="Último Nome", widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Digite o último nome'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome de usuário'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'preferred_color','logo']
        widgets = {
            'preferred_color': forms.TextInput(attrs={'type': 'color'}),
        }