from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomLoginForm, InsuranceCompanyFrom, ProceduresFrom, ClientsForm, SupplierForm, \
    AddSupplierToInsuranceFrom, InsuranceCompanyProcedureFrom, InsurancePlanForm
from .models import InsuranceCompany, Procedure, Client, Supplier, InsurancePlan
from django.contrib.auth.decorators import login_required

def custom_login(request):
    form = CustomLoginForm(request.POST)

    context = {
        'title': 'Criar novo Clientes',
        'client': Client.objects.all()
    }

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/client/list', context)
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid credentials.'})

    return render(request, 'auth/login.html', {'form': form})

@login_required
def dashboard(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    context = {
        'title': 'Dashboard',
        'nome_empresa': insuranceCompany.id,
    }

    return render(request, 'dashboard.html',context)

def custom_login2(request):
    form = CustomLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form = CustomLoginForm(request.POST)  # Instantiate the form with POST data

        if form.is_valid():  # Ensure form is valid before accessing cleaned_data
            # Access cleaned data (only available if the form is valid)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in and redirect
                login(request, user)
                return redirect('home')  # Replace with your target URL
            else:
                # Authentication failed
                form.add_error(None, 'Invalid username or password')
        else:
            # If the form is invalid, you can display errors
            form.add_error(None, 'Please correct the errors below')
    else:
        form = CustomLoginForm()  # Instantiate an empty form for GET requests

    return render(request, 'auth/login.html', {'form': form})

def insurance_plan_list(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    # insurancePlan = InsurancePlan.objects.get()
    context = {
        'title': 'Plano',
        'plans' : InsurancePlan.objects.all()
    }

    return render(request, "insuranceCompany/plan_list.html",context)

@login_required
def insurance_plan_create3(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    try:
        company = InsuranceCompany.objects.get(id=insuranceCompany.id, user=request.user)
    except InsuranceCompany.DoesNotExist:
        return redirect('/dashboard/insurance/plan/list')  # Redirect if no such company exists for the user

    if request.method == 'POST':
        form = InsurancePlan(request.POST)
        if form.is_valid():
            # plan = form.cleaned_data['insurancePlan']
            # plan = request.POST['insurancePlan']
            # company.insurancePlan.add(plan)

            context = {
                'title': 'Criar novo Clientes',
                'form': form
            }
            form.save()
            messages.success(request, 'Plano com sucesso!')
            return redirect('/dashboard/insurance/list', context)
    else:
        form = InsurancePlanForm()

    return render(request, 'insuranceCompany/add_existing_plan.html', {'form': form, 'company': company})
def insurance_plan_create(request, id=0):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    if request.method == "GET":
        if id == 0 :
            form = InsurancePlanForm()
        else:
            insurancePlan = InsurancePlan.objects.get(pk=id)
            form = InsurancePlanForm(instance = insurancePlan)

        context = {
            'title': 'Criar novo plano',
            'form': form
        }

        return render(request, "insuranceCompany/add_existing_plan.html",context)
    else:
        form = InsurancePlanForm(request.POST, request.FILES)
        context = {
            'title': 'Criar novo Plano',
            'insuranceCompany': InsurancePlan.objects.all()
        }

        # form.insuranceCompany_id  = insuranceCompany.id

        if form.is_valid():
            form.save()
            messages.success(request, 'Plano criado com sucesso!')
            return render(request, "/dashboard/insurance/supplier/list/", context)
        else:
            return render(request, 'insuranceCompany/add_existing_plan.html', {'form': form})

def insurance_supplier_list(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    company = InsuranceCompany.objects.get(id=insuranceCompany.id)
    suppliers = company.supplier.all()

    context = {
        'title': 'Meus Provedores',
        'suppliers' : suppliers
    }

    return render(request, "insuranceCompany/supplier_list.html",context)
@login_required
def add_insurance_supplier(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    try:
        company = InsuranceCompany.objects.get(id=insuranceCompany.id, user=request.user)
    except InsuranceCompany.DoesNotExist:
        return redirect('/dashboard/insurance/supplier/list/')

    if request.method == 'POST':
        form = AddSupplierToInsuranceFrom(request.POST)
        if form.is_valid():
            plan = request.POST['supplier']
            company.supplier.add(plan)
            context = {
                'title': 'Criar novo Clientes',
                'form': form
            }
            messages.success(request, 'Plano com sucesso!')
            return redirect('/dashboard/insurance/list', context)
    else:
        form = AddSupplierToInsuranceFrom()

    return render(request, 'insuranceCompany/add_existing_supplier.html', {'form': form, 'company': company})
@login_required
def add_insurance_supplier_procedure(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    try:
        company = InsuranceCompany.objects.get(id=insuranceCompany.id, user=request.user)
    except InsuranceCompany.DoesNotExist:
        return redirect('/dashboard/insurance/supplier/list/')

    if request.method == 'POST':
        form = InsuranceCompanyProcedureFrom(request.POST)
        if form.is_valid():
            # plan = request.POST['supplier']
            # company.supplier.add(plan)
            context = {
                'title': 'Criar novo Clientes',
                'form': form
            }
            messages.success(request, 'Plano com sucesso!')
            return redirect('/dashboard/insurance/list', context)
    else:
        form = InsuranceCompanyProcedureFrom()

    return render(request, 'insuranceCompany/add_existing_supplier_procedure.html', {'form': form, 'company': company})

def insurance_list(request):
    context = {
        'title': 'Clientes',
        'insuranceCompany' : InsuranceCompany.objects.all()
    }
    return render(request, "insuranceCompany/list.html",context)

def insurance_form(request, id=0):
    if request.method == "GET":
        if id == 0 :
            form = InsuranceCompanyFrom()
        else:
            insuranceCompany = InsuranceCompany.objects.get(pk=id)
            form = InsuranceCompanyFrom(instance = insuranceCompany)

        context = {
            'title': 'Criar novo Clientes',
            'form': form
        }
        return render(request, "insuranceCompany/create.html",context)
    else:
        form = InsuranceCompanyFrom(request.POST, request.FILES)
        context = {
            'title': 'Criar novo Clientes',
            'insuranceCompany': InsuranceCompany.objects.all()
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente criado com sucesso!')
            return render(request, "/dashboard/insurance/list/", context)
        else:
            return render(request, 'insuranceCompany/create.html', {'form': form})

def procedures_list(request):
    context = {
        'title': 'Procedimentos',
        'procedure' : Procedure.objects.all()
    }
    return render(request, "procedures/list.html",context)

def procedures_form(request, id=0):
    if request.method == "GET":
        if id == 0 :
            form = ProceduresFrom()
        else:
            procedure = Procedure.objects.get(pk=id)
            form = ProceduresFrom(instance = procedure)

        context = {
            'title': 'Procedimentos',
            'form': form,
            'procedure': Procedure.objects.all()
        }
        return render(request, "procedures/create.html",context)
    else:

        form = ProceduresFrom(request.POST, request.FILES)

        context = {
            'title': 'Procedimentos',
            'procedure': Procedure.objects.all()
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Procedimento criado com sucesso!')
            form = ProceduresFrom()
            context = {
                'title': 'Procedimentos',
                'insuranceCompany': Procedure.objects.all(),
                'form':form,
                'procedure': Procedure.objects.all()
            }
            return render(request, "/dashboard/procedure/list/", context)

        else:
            return render(request, 'procedures/create.html', {'form': form})

def client_list(request):
    context = {
        'title': 'Clientes',
        'clients' : Client.objects.all()
    }
    return render(request, "clients/list.html",context)

def client_form(request, id=0):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    if request.method == "GET":
        if id == 0 :
            form = ClientsForm()
        else:
            client = Client.objects.get(pk=id)
            form = ClientsForm(instance = client)

        context = {
            'title': 'Criar novo Clientes',
            'form': form
        }
        return render(request, "clients/create.html",context)

    else:

        form = ClientsForm(request.POST, request.FILES)

        context = {
            'title': 'Criar novo Clientes',
            'client': Client.objects.all()
        }

        if form.is_valid():
            client_saved = form.save(commit=False)
            client_saved.insuranceCompany = insuranceCompany
            client_saved.save()
            messages.success(request, 'Cliente criado com sucesso!')
            return redirect('/dashboard/client/list/', context)
        else:
            return render(request, 'clients/create.html', {'form': form})

def supplier_list(request):
    context = {
        'title': 'Provedor',
        'suppliers' : Supplier.objects.all()
    }
    return render(request, "supplier/list.html",context)

def supplier_form(request, id=0):
    if request.method == "GET":
        if id == 0 :
            form = SupplierForm()
        else:
            supplier = Supplier.objects.get(pk=id)
            form = SupplierForm(instance = client)

        context = {
            'title': 'Provedor',
            'form': form
        }
        return render(request, "supplier/create.html",context)

    else:

        form = SupplierForm(request.POST, request.FILES)

        context = {
            'title': 'Criar novo Provedor',
            'supplier': Supplier.objects.all()
        }

        if form.is_valid():
            supplier = form.save()
            messages.success(request, 'Provedor criado com sucesso!')
            return render(request, '/dashboard/supplier/list.html',context)

        else:
            return render(request, 'supplier/create.html', {'form': form})