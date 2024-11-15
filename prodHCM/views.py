import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomLoginForm, InsuranceCompanyFrom, ProceduresFrom, ClientsForm, SupplierForm, \
    AddSupplierToInsuranceFrom, InsurancePlanForm, InsuranceCompanyProcedureForm, \
    InsuranceCompanyProcedureFormSet
from .models import InsuranceCompany, Procedure, Client, Supplier, InsurancePlan, InsuranceCompanyProcedure
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def custom_login(request):
    form = CustomLoginForm(request.POST or None)
    context = {
        'title': 'Criar novo Clientes',
        'form': form,
    }

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            # Update context with an error message
            context['error'] = 'Credenciais inválidas.'  # 'Invalid credentials.'

    return render(request, 'auth/login.html', context)

def custom_logout(request):
    logout(request)
    return redirect('custom_login')

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        insuranceCompany = getattr(request.user, 'insuranceCompany', None)

        context = {
            'title': 'Dashboard',
            'nome_empresa': insuranceCompany,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('custom_login')

def insurance_plan_list(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    insurancePlan = InsurancePlan.objects.all().order_by('-id')
    # insurancePlan = InsurancePlan.objects.filter(insuranceCompany__id=4)
    # plans = InsurancePlan.objects.filter(insuranceCompany__name="Company Name")

    context = {
        'title': 'Plano',
        'plans' : insurancePlan,
        'insuranceCompany' : insuranceCompany
    }

    return render(request, "insuranceCompany/plan_list.html",context)

@login_required
def insurance_plan_create(request, id=0):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    if request.method == "GET":
        if id == 0 :
            form = InsurancePlanForm()
        else:
            insurancePlan = InsurancePlan.objects.get(pk=id)
            form = InsurancePlanForm(instance = insurancePlan)

        context = {
            'title': 'Criar Plano',
            'form': form,
            'insuranceCompany': insuranceCompany,
        }

        return render(request, "insuranceCompany/add_existing_plan.html",context)
    else:
        form = InsurancePlanForm(request.POST, request.FILES)
        context = {
            'title': 'Planos',
            'plans': InsurancePlan.objects.all()
        }
        if form.is_valid():
            form.save()
            return redirect('/dashboard/insurance/plan/list/',context)
        else:

            return render(request, 'insuranceCompany/add_existing_plan.html', {'form': form})

def insurance_supplier_list(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    company = InsuranceCompany.objects.get(id=insuranceCompany.id)
    suppliers = company.supplier.all()
    try:
        company = InsuranceCompany.objects.get(id=insuranceCompany.id, user=request.user)
    except InsuranceCompany.DoesNotExist:
        return redirect('/dashboard')

    if request.method == 'POST':
        form = AddSupplierToInsuranceFrom(request.POST)
        if form.is_valid():
            plan = request.POST['supplier']
            company.supplier.add(plan)
            context = {
                'title': 'Meus Provedores',
                'suppliers': suppliers,
                'form': form
            }
            messages.success(request, 'Plano com sucesso!')
            return redirect('/dashboard/insurance/supplier/list/', context)
    else:
        form = AddSupplierToInsuranceFrom()

        context = {
            'title': 'Meus Provedores',
            'suppliers': suppliers,
            'form': form
        }

        return render(request, 'insuranceCompany/supplier_list.html', context)

@login_required
def add_insurance_supplier(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    try:
        company = InsuranceCompany.objects.get(id=insuranceCompany.id, user=request.user)
    except InsuranceCompany.DoesNotExist:
        return redirect('/dashboard/insurance/supplier/list/')

    print(request.method)

    if request.method == 'POST':
        form = AddSupplierToInsuranceFrom(request.POST)
        print(form.is_valid())
        plan = request.POST['supplier']
        print(plan)
        company.supplier.add(plan)
        context = {
            'title': 'Adicionar provedores',
            'form': form
        }
        messages.success(request, 'Plano com sucesso!')
        return redirect('/dashboard/insurance/supplier/procedure/', context)
        # if form.is_valid():

    else:

        form = AddSupplierToInsuranceFrom()

    return render(request, 'insuranceCompany/add_existing_supplier.html', {'form': form, 'company': company})

@login_required
def add_insurance_supplier_procedure(request,id):

    insurance_company = getattr(request.user, 'insuranceCompany', None)
    supplier = Supplier.objects.get(id=id)

    if request.method == 'POST':
        formset = InsuranceCompanyProcedureFormSet(request.POST, queryset=InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company,supplier=supplier))
        if formset.is_valid():
            formset.save()
            return redirect('/dashboard/insurance/supplier/list/')
    else:
        formset = InsuranceCompanyProcedureFormSet(queryset=InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company,supplier=supplier))

        saved_procedures = InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company,supplier=supplier)
        saved_procedures_ids = saved_procedures.values_list('procedure_id',flat=True)  # Lista de IDs dos procedimentos salvos

        context = {
            'title': 'Procedimentos',
            'supplier': supplier,
            'insuranceCompany': InsuranceCompany.objects.all().order_by('-id'),
            'procedures': Procedure.objects.all(),
            'saved_procedures': saved_procedures,  # Procedimentos já salvos
            'saved_procedures_ids': saved_procedures_ids,  # Procedimentos já salvos
        }

    return render(request, 'insuranceCompany/add_existing_supplier_procedure.html', context)

@csrf_exempt  # Desativar o CSRF apenas se necessário para AJAX; idealmente, configure o CSRF no frontend
def save_procedures(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            procedures_data = data.get("procedures", [])
            supplier_id = data.get("supplier_id")

            insurance_company_id = getattr(request.user, 'insuranceCompany', None)

            if not procedures_data:
                return JsonResponse({"success": False, "error": "Nenhum procedimento selecionado."})

            # Loop para salvar cada procedimento selecionado com o preço negociado
            for procedure_data in procedures_data:
                procedure_id = procedure_data.get("procedure_id")
                negotiated_price = procedure_data.get("negotiated_price")

                try:
                    procedure = Procedure.objects.get(id=procedure_id)
                    # Cria o registro de InsuranceCompanyProcedure
                    InsuranceCompanyProcedure.objects.create(
                        insuranceCompany_id=insurance_company_id.id,
                        procedure=procedure,
                        supplier_id=supplier_id,
                        negotiated_price=negotiated_price
                    )
                except Procedure.DoesNotExist:
                    return JsonResponse({"success": False, "error": f"Procedimento {procedure_id} não encontrado."})

            return JsonResponse({"success": True, "message": "Procedimentos salvos com sucesso!"})

        except json.JSONDecodeError as e:
            return JsonResponse({"success": False, "error": "Erro ao processar os dados."})

    return JsonResponse({"success": False, "error": "Método não permitido."})

def insurance_list(request):
    context = {
        'title': 'Clientes',
        'insuranceCompany' : InsuranceCompany.objects.all().order_by('-id')
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
            'insuranceCompany': InsuranceCompany.objects.all().order_by('-id')
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente criado com sucesso!')
            return redirect('/dashboard/insurance/list/', context)
        else:
            return render(request, 'insuranceCompany/create.html', {'form': form})

def procedures_list(request):
    context = {
        'title': 'Procedimentos',
        'procedures' : Procedure.objects.all()
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

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    context = {
        'title': 'Clientes',
        'clients' : Client.objects.filter(insuranceCompany__id=insuranceCompany.id)
    }

    return render(request, "clients/list.html",context)

def client_form(request, id=0):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    if request.method == "GET":
        if id == 0 :
            form = ClientsForm(initial={'insuranceCompany': insuranceCompany})
        else:
            client = Client.objects.get(pk=id)
            form = ClientsForm(instance = client)

        context = {
            'title': 'Criar novo Clientes',
            'form': form,
            'insuranceCompany': insuranceCompany,
        }
        return render(request, "clients/create.html",context)

    else:

        form = ClientsForm(request.POST, request.FILES)

        context = {
            'title': 'Criar novo Clientes',
            'client': Client.objects.filter(insuranceCompany__id=insuranceCompany.id)
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente criado com sucesso!')
            return redirect('/dashboard/client/list/', context)
        else:
            return render(request, 'clients/create.html', {'form': form})

@login_required
def client_detail(request, id):

    client = get_object_or_404(Client, id=id)

    context = {
        'title': client.name,
        'client' : client
    }

    return render(request, 'clients/show.html', context)

def supplier_list(request):

    context = {
        'title': 'Provedor',
        'suppliers' : Supplier.objects.all()
    }
    return render(request, "supplier/list.html",context)

def supplier_client_list(request):

    supplier = getattr(request.user, 'supplier', None)

    insuranceCompanys = supplier.insuranceCompany.all()

    context = {
        'title': 'Clientes',
        'insuranceCompanys' : insuranceCompanys
    }

    return render(request, "supplier/client_list.html",context)

def supplier_form(request, id=0):
    if request.method == "GET":
        if id == 0 :
            form = SupplierForm()
        else:
            supplier = Supplier.objects.get(pk=id)
            form = SupplierForm(instance = supplier)

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
def supplier_client_show(request,id):

    supplier = getattr(request.user, 'supplier', None)

    insurance_company = InsuranceCompany.objects.get(pk=id)

    saved_procedures = InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company,supplier=supplier)
    saved_procedures_ids = saved_procedures.values_list('procedure_id',flat=True)  # Lista de IDs dos procedimentos salvos

    context = {
            'title': insurance_company.name,
            'supplier': supplier,
            'insuranceCompany': InsuranceCompany.objects.all().order_by('-id'),
            'procedures': Procedure.objects.all(),
            'saved_procedures': saved_procedures,
            'insurance_company': insurance_company,
     }

    return render(request, 'supplier/client_show.html', context)


