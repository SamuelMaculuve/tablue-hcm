from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory

from prodHCM.models import InsuranceCompany, Procedure, Category, Client, Supplier, InsurancePlan, \
    InsuranceCompanyProcedure


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
            'date_of_activity_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        # labels = {
        #             'clientType':'Tipo de cliente',
        #             'fullname':'Nome da empresa',
        #             'nuitNumber':'NUIT',
        #             'phoneNumber':'Telemóvel',
        #             'date_of_activity_start':'Início de atividade',
        #             'email':'Email',
        #             'address':'Endereço da empresa',
        #             'district':'Distrito',
        #             'province':'Provincia',
        #             'contractFile':'',
        #             'nuitFile':'',
        #         }

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

# Crie o formset para gerenciar múltiplas instâncias
InsuranceCompanyProcedureFormSet = modelformset_factory(
    InsuranceCompanyProcedure,
    form=InsuranceCompanyProcedureForm,
    extra=0  # Ajuste conforme necessário para campos adicionais em branco
)
# class InsuranceCompanyProcedureForm(forms.ModelForm):
#     class Meta:
#         model = InsuranceCompanyProcedure
#         fields = ('insuranceCompany','supplier','negotiated_price','procedure')
#         # widgets = {
#         #             'insuranceCompany': forms.HiddenInput(),
#         #             'supplier': forms.HiddenInput(),
#         #             'procedure': forms.CheckboxInput(),
#         #         }
#
# class ProcedureSelectionForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         procedures = kwargs.pop('procedures', [])
#         super().__init__(*args, **kwargs)
#
#         for procedure in procedures:
#             # Checkbox para selecionar o procedimento
#             self.fields[f"procedure_{procedure.id}"] = forms.BooleanField(
#                 required=False,
#                 label="",
#                 widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'})
#             )
#             # Campo de preço associado ao procedimento
#             self.fields[f"price_{procedure.id}"] = forms.DecimalField(
#                 required=False,
#                 max_digits=10,
#                 decimal_places=2,
#                 label="",
#                 widget=forms.NumberInput(attrs={'class': 'price-input-class', 'placeholder': 'Preço'})
#             )

class AddSupplierToInsuranceFrom(forms.Form):
    supplier = forms.ModelMultipleChoiceField(
        queryset = Supplier.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        label=''
    )

class ProceduresFrom(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = '__all__'
        # fields = ('clientType','fullname','nuitNumber','date_of_activity_start')

    # def __init__(self, *args, **kwargs):
    #     super(Category,self).__init__(*args, **kwargs)
    #     self.fields['category'].empty_label = "Select"
    #
    # def __init__(self, *args, **kwargs):
    #     super(SubCategory,self).__init__(*args, **kwargs)
    #     self.fields['category'].empty_label = "Select"

class ClientsForm(forms.ModelForm):
        class Meta:
            model = Client
            fields = ('insuranceCompany','name','nuitNumber','phoneNumber','date_of_activity_start','email','address','district','province','contractFile','nuitFile')
            # fields = '__all__'
            widgets = {
                'insuranceCompany': forms.HiddenInput(),
                'date_of_activity_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            }

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
    # def __init__(self, *args, **kwargs):
    #     super(ProviderForm, self).__init__(*args, **kwargs)
    #     self.fields['insuranceCompany'].empty_label = "Select"