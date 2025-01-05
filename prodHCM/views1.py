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

    return render(request, "insuranceCompany/list.html",context)

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

        return render(request, "insuranceCompany/create.html",context)
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

            return render(request, 'insuranceCompany/create.html', {'form': form})

def insurance_supplier_list(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

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
                'title': 'Criar novo Clientes',
                'form': form
            }
            messages.success(request, 'Plano com sucesso!')
            return redirect('/dashboard/insurance/supplier/procedure/', context)
    else:
        form = AddSupplierToInsuranceFrom()

        company = InsuranceCompany.objects.get(id=insuranceCompany.id)
        suppliers = company.supplier.all()

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
            return redirect('/dashboard/insurance/supplier/procedure/', context)
    else:
        form = AddSupplierToInsuranceFrom()

    return render(request, 'insuranceCompany/add_existing_supplier.html', {'form': form, 'company': company})

@login_required
def add_insurance_supplier_procedure1(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)

    try:
        company = InsuranceCompany.objects.get(id=insuranceCompany.id, user=request.user)
    except InsuranceCompany.DoesNotExist:
        return redirect('/dashboard/insurance/supplier/list/')

    if request.method == 'POST':
        form = InsuranceCompanyProcedureForm(request.POST)
        if form.is_valid():
            # plan = request.POST['supplier']
            # company.supplier.add(plan)
            context = {
                'title': 'Criar novo Clientes ----',
                'form': form
            }
            messages.success(request, 'Plano com sucesso!')
            return redirect('/dashboard/insurance/list', context)
    else:

        # form = InsuranceCompanyProcedureForm()
        formset = InsuranceCompanyProcedureForm()

        context = {
            'title': 'Criar novo Clientes ----',
            'form': formset
        }

    return render(request, 'insuranceCompany/add_existing_supplier_procedure.html', context)

# def add_insurance_supplier_procedure(request):
#     insuranceCompany = getattr(request.user, 'insuranceCompany', None)
#     procedures = Procedure.objects.all()
#
#     if request.method == "POST":
#         form = ProcedureSelectionForm(request.POST, procedures=procedures)
#         if form.is_valid():
#             for procedure in procedures:
#                 selected = form.cleaned_data.get(f"procedure_{procedure.id}")
#                 price = form.cleaned_data.get(f"price_{procedure.id}")
#
#                 if selected and price is not None:
#                     InsuranceCompanyProcedure.objects.update_or_create(
#                         insurance_company=insuranceCompany,
#                         procedure=procedure,
#                         defaults={'negotiated_price': price}
#                     )
#                 else:
#                     InsuranceCompanyProcedure.objects.filter(
#                         insurance_company=insuranceCompany,
#                         procedure=procedure
#                     ).delete()
#             return redirect('/dashboard/insurance/list')
#     else:
#         form = ProcedureSelectionForm(procedures=procedures)
#
#     return render(request, 'insuranceCompany/add_existing_supplier_procedure.html', {'form': form, 'procedures': procedures})

def add_insurance_supplier_procedure22(request):

    insurance_company = getattr(request.user, 'insuranceCompany', None)

    # Inicializar o formset com procedimentos para a companhia de seguros específica
    if request.method == 'POST':
        formset = InsuranceCompanyProcedureFormSet(request.POST, queryset=InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company))
        if formset.is_valid():
            formset.save()
            return redirect('success_url')  # Redirecione para uma página de sucesso
    else:
        formset = InsuranceCompanyProcedureFormSet(queryset=InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company))
        context = {
            'title': 'Clientes',
            'insuranceCompany': InsuranceCompany.objects.all().order_by('-id'),
            'procedures': Procedure.objects.all()
        }
    return render(request, 'insuranceCompany/add_existing_supplier_procedure.html', context)
def add_insurance_supplier_procedure(request):
    insurance_company = getattr(request.user, 'insuranceCompany', None)

    # Inicializar o formset com procedimentos para a companhia de seguros específica
    if request.method == 'POST':
        formset = InsuranceCompanyProcedureFormSet(request.POST, queryset=InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company))
        if formset.is_valid():
            formset.save()
            return redirect('success_url')  # Redirecione para uma página de sucesso
    else:
        formset = InsuranceCompanyProcedureFormSet(queryset=InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company))

        # Obtém todos os procedimentos
        procedures = Procedure.objects.all()

        # Obtém todos os procedimentos já salvos para a companhia de seguros
        saved_procedures = InsuranceCompanyProcedure.objects.filter(insuranceCompany=insurance_company)
        saved_procedures_ids = saved_procedures.values_list('procedure_id',flat=True)  # Lista de IDs dos procedimentos salvos

        # Passa as informações para o template
        context = {
            'title': 'Clientes',
            'insuranceCompany': InsuranceCompany.objects.all().order_by('-id'),
            'procedures': procedures,
            'saved_procedures': saved_procedures,  # Procedimentos já salvos
            'saved_procedures_ids': saved_procedures_ids,  # Procedimentos já salvos
            'formset': formset
        }

    return render(request, 'insuranceCompany/add_existing_supplier_procedure.html', context)


@csrf_exempt
def save_procedures(request):
    if request.method == "POST":
        try:
            # Carregar os dados enviados no corpo da requisição
            data = json.loads(request.body)
            procedures_data = data.get("procedures", [])
            remove_procedures = data.get("remove_procedures", [])
            insurance_company = getattr(request.user, 'insuranceCompany', None)
            insurance_company_id =insurance_company.id
            if not procedures_data and not remove_procedures:
                return JsonResponse({"success": False, "error": "Nenhum procedimento selecionado ou desmarcado."})

            # Remover procedimentos desmarcados
            for procedure_id in remove_procedures:
                try:
                    # Verifica e remove os procedimentos desmarcados
                    insurance_procedure = InsuranceCompanyProcedure.objects.get(
                        insuranceCompany_id=insurance_company_id,
                        procedure_id=procedure_id
                    )
                    insurance_procedure.delete()  # Remove da base de dados
                except InsuranceCompanyProcedure.DoesNotExist:
                    continue  # Se o procedimento não for encontrado, continuar

            # Adicionar ou atualizar os procedimentos selecionados
            for procedure_data in procedures_data:
                procedure_id = procedure_data.get("procedure_id")
                negotiated_price = procedure_data.get("negotiated_price")

                try:
                    procedure = Procedure.objects.get(id=procedure_id)

                    # Verifica se o procedimento já existe na base de dados
                    insurance_procedure, created = InsuranceCompanyProcedure.objects.update_or_create(
                        insuranceCompany_id=insurance_company_id,
                        procedure=procedure,
                        defaults={'negotiated_price': negotiated_price}  # Atualiza o preço negociado
                    )

                    # A variável 'created' indica se o registro foi criado ou atualizado
                    if created:
                        print(f"Procedimento {procedure_id} criado.")
                    else:
                        print(f"Procedimento {procedure_id} atualizado.")

                except Procedure.DoesNotExist:
                    continue  # Se o procedimento não for encontrado, continuar

            return JsonResponse({"success": True, "message": "Procedimentos salvos ou removidos com sucesso!"})

        except json.JSONDecodeError as e:
            return JsonResponse({"success": False, "error": "Erro ao processar os dados."})

    return JsonResponse({"success": False, "error": "Método não permitido."})


# @csrf_exempt
# def save_procedures(request):
#     if request.method == "POST":
#
#         procedures_data = request.POST.getlist('procedure_ids')
#         insurance_company_id = getattr(request.user, 'insuranceCompany', None)
#         # insurance_company = getattr(request.user, 'insuranceCompany', None)
#         for procedure_id in procedures_data:
#             procedure = Procedure.objects.get(id=procedure_id)
#             InsuranceCompanyProcedure.objects.create(
#                 insuranceCompany_id=insurance_company_id,
#                 procedure=procedure,
#                 negotiated_price=4000  # ou calcule conforme necessário
#             )
#         return JsonResponse({"success": True})
#     return JsonResponse({"success": False, "error": "Método não permitido"})

# def save_procedures(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         procedures = data.get('procedures', [])
#
#         for item in procedures:
#             procedure_id = item['procedure_id']
#             price = item['price']
#
#             # Substitua `None` por valores reais para `insuranceCompany` e `supplier` se necessário
#             InsuranceCompanyProcedure.objects.create(
#                 insuranceCompany=None,  # Exemplo
#                 supplier=None,  # Exemplo
#                 negotiated_price=price,
#                 procedure_id=procedure_id
#             )
#
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})


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