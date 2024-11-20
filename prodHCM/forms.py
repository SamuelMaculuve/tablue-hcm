from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory

from prodHCM.models import InsuranceCompany, Procedure, Category, Client, Supplier, InsurancePlan, \
    InsuranceCompanyProcedure, BeneficiarieTreatment, Beneficiaries, SubCategory


class CustomLoginForm(AuthenticationForm):
    # Customizing the AuthenticationForm
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class InsuranceCompanyFrom(forms.ModelForm):
    class Meta:
        model = InsuranceCompany
        # fields = '__all__'
        fields = ('name','nuitNumber','phoneNumber','date_of_activity_start','email','address','district','province','contractFile','nuitFile','insuranceCompanyType')
        widgets = {
            'date_of_activity_start': forms.DateInput(
            format='%Y-%m-%d',  # Specify the date format (e.g., YYYY-MM-DD)
            attrs={
                'type': 'date',  # HTML5 date picker
                'class': 'form-control',  # Add Bootstrap styling (optional)
                'placeholder': 'YYYY-MM-DD',
            }
        ),
        },

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
        fields = '__all__'
        subCategory = forms.ModelChoiceField(queryset=SubCategory.objects.none(), empty_label="Selecione a categoria primeiro")


class ClientsForm(forms.ModelForm):
        class Meta:
            model = Client
            fields = ('insuranceCompany','name','nuitNumber','phoneNumber','date_of_activity_start','email','address','district','province','contractFile','nuitFile')
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
        fields = '__all__'
        widgets = {
            'date_of_activity_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'procedures': forms.CheckboxSelectMultiple(),
        }

        def clean_procedures(self):
            # If no procedures are selected, return an empty list
            procedure = self.cleaned_data.get('procedures', [])
            return procedures

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
        fields = ('insuranceCompany','client','name','email','insurancePlan')
        widgets = {
            'client': forms.HiddenInput(),
            'insuranceCompany': forms.HiddenInput(),
        }
        labels = {
            'insurancePlan': 'Plano',
        }