import json
from email.message import EmailMessage

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.html import strip_tags
from django.contrib.auth.models import Group

from .forms import CustomLoginForm, InsuranceCompanyFrom, ProceduresFrom, ClientsForm, SupplierForm, \
    AddSupplierToInsuranceFrom, InsurancePlanForm, InsuranceCompanyProcedureForm, \
     AddInsurancePlanClientFrom, BeneficiariesForm, IndividualsForm, CategoryFrom, \
    SubCategoryFrom, CreateUserForm, ProfileForm, LevelForm
from .models import InsuranceCompany, Procedure, Client, Supplier, InsurancePlan, InsuranceCompanyProcedure, \
    Beneficiaries, BeneficiarieTreatment, Category, SubCategory, Individuals, User, Profile, Level, BeneficiaryPlan, \
    BeneficiaryLevel, BeneficiaryICProcedure
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
import re

def create_user(firstUserName,role):

    user = User.objects.create_user(
        username=firstUserName.strip().replace(" ", "").lower(),
        password="password"
    )

    Profile.objects.create(user=user)

    group = Group.objects.get(name=role)
    user.groups.add(group)

    return user

def send_email(request,address,subject,html_content):
    context = {}
    address = address
    subject = subject
    html_content = html_content
    # text_content = strip_tags(html_content)
    text_content = html_content
    message=text_content
    if address and subject and message:
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
            context['result'] = 'Email sent successfully'
        except Exception as e:
            context['result'] = f'Error sending email: {e}'
    # return render(request, "index.html", context)
    return HttpResponse("HTML email sent successfully!")

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


def dashboard(request):

    if request.user.is_authenticated:
        all_insurance = 0;all_insurance_company = 0;all_supplier = 0;insurance_suppliers = 0;insurance_clients_all = 0
        supplier_insuranceCompanys = 0
        insuranceCompany = [];insurance_clients = [];insuranceCompanys = []

        # clients = Client.objects.filter(insuranceCompany__id=insuranceCompany.id)

        if request.user.groups.filter(name='Admin').exists():

            all_insurance = InsuranceCompany.objects.filter(insuranceCompanyType=1).count()
            all_insurance_company = InsuranceCompany.objects.filter(insuranceCompanyType=2).count()
            all_supplier = Supplier.objects.count()
            insuranceCompany = InsuranceCompany.objects.all()[:5]

        elif request.user.groups.filter(name='InsuranceCompany').exists():

            # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
            user = request.user
            insuranceCompany = user.insuranceCompany.all().first()

            insurance_clients = Client.objects.filter(insuranceCompany__id=insuranceCompany.id)[:5]
            insurance_clients_all = Client.objects.filter(insuranceCompany__id=insuranceCompany.id).count()

            company = InsuranceCompany.objects.get(id=insuranceCompany.id)
            insurance_suppliers = company.supplier.all().count()

        elif request.user.groups.filter(name='Supplier').exists():

            user = request.user
            supplier = user.supplier.all().first()
            # supplier = getattr(request.user, 'supplier', None)
            insuranceCompanys = supplier.insuranceCompany.all()
            supplier_insuranceCompanys = supplier.insuranceCompany.count()

        elif request.user.groups.filter(name='client').exists():
            print('You are an admin!')
        else:
            return HttpResponseForbidden('Access denied.')

        context = {
            'title': 'Dashboard',
            'all_insurance': all_insurance,
            'all_insurance_company': all_insurance_company,
            'all_supplier': all_supplier,
            'insuranceCompany': insuranceCompany,
            'insurance_clients': insurance_clients,
            'insurance_suppliers': insurance_suppliers,
            'insurance_clients_all': insurance_clients_all,
            'insuranceCompanys': insuranceCompanys,
            'supplier_insuranceCompanys': supplier_insuranceCompanys,
        }

        return render(request, 'dashboard.html', context)
    else:
        return redirect('custom_login')

def insurance_plan_list(request):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()
    insurancePlan = InsurancePlan.objects.filter(insuranceCompany=insuranceCompany).order_by('-id')

    context = {
        'title': 'Plano',
        'plans' : insurancePlan,
        'insuranceCompany' : insuranceCompany
    }

    return render(request, "insuranceCompany/plan/list.html",context)

def insurance_plan_create(request, id=0):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()

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

        return render(request, "insuranceCompany/plan/create.html",context)
    else:
        form = InsurancePlanForm(request.POST, request.FILES)
        context = {
            'title': 'Planos',
            'plans': InsurancePlan.objects.all()
        }
        if form.is_valid():
            plan = form.save()
            messages.success(request, 'Plano criado com sucesso!')
            return redirect('/dashboard/insurance/plan/add_plan_steap-2/' + str(plan.id), context)
        else:
            messages.error("ERRO ao criar plano")
            return render(request, 'insuranceCompany/plan/create.html', {'form': form})

def construir_hierarquia(niveis, parent=None, visitados=None):
    if visitados is None:
        visitados = set()

    hierarquia = []
    for nivel in niveis:
        if nivel.id in visitados:
            continue  # Ignorar ciclos ou níveis já processados
        if nivel.parent_level == parent:
            visitados.add(nivel.id)
            subniveis = construir_hierarquia(niveis, parent=nivel, visitados=visitados)
            hierarquia.append({
                'id': nivel.id,
                'name': nivel.name,
                'plafonPrice': nivel.plafonPrice,
                'insurancecompanyprocedures': list(nivel.insuranceCompanyProcedure.all()),
                'sublevels': subniveis,
            })
    return hierarquia

def insurance_plan_create_step2(request, id=0):

    user = request.user

    if request.method == "GET":
        if id == 0 :
            form = LevelForm()
        else:
            insurancePlan = get_object_or_404(InsurancePlan, id=id)
            plan = InsurancePlan.objects.prefetch_related(
                'levels__sublevels__insuranceCompanyProcedure'
            ).get(id=id)

            plan = InsurancePlan.objects.prefetch_related('levels__insuranceCompanyProcedure').get(id=id)
            levels = Level.objects.filter(plan=plan).select_related('parent_level').prefetch_related('insuranceCompanyProcedure')
            hierarquia = construir_hierarquia(levels)

            form = LevelForm()
            context = {
                'title': insurancePlan.name,
                'insurancePlan': insurancePlan,
                'plan': plan,
                'form': form,
                'levels': levels,
                'hierarquia': hierarquia,
            }

            return render(request, 'insuranceCompany/plan/create-step-2.html', context)
    else:
        plan = request.POST.get('plan')

        form = LevelForm(request.POST, request.FILES)

        context = {
            'title': 'Planos',
            'plans': InsurancePlan.objects.all()
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Plano adicionado com sucesso!')
            return redirect('/dashboard/insurance/plan/add_plan_steap-2/' + str(plan), context)
        else:
            return redirect('/dashboard/insurance/plan/add_plan_steap-2/' + str(plan), context)

def insurance_plan_create_sublevel(request):

    if request.method == "POST":
        form = LevelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Adicionado com sucesso!')
            return redirect(request.META.get('HTTP_REFERER', '/fallback-url'))

        else:
            messages.error(request, 'Adicionado sem sucesso!')
            return redirect(request.META.get('HTTP_REFERER', '/fallback-url'))

    else:
        messages.error(request, 'Adicionado sem sucesso 2!')
        return redirect(request.META.get('HTTP_REFERER', '/fallback-url'))

def insurance_plan_create_procedure(request, id=0):

    if request.method == "GET":
        if id == 0 :
            form = LevelForm()
        else:
            level = get_object_or_404(Level, id=id)
            procedures = Procedure.objects.all()

            context = {
                'title': 'Nivel - '+level.name,
                'level': level,
                'procedures': procedures,
            }

            return render(request, 'insuranceCompany/plan/procedure/create_on_plan.html', context)
    else:
        plan = request.POST.get('plan')

        form = LevelForm(request.POST, request.FILES)

        context = {
            'title': 'Planos',
            'plans': InsurancePlan.objects.all()
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Adicionado com sucesso!')
            return redirect('/dashboard/insurance/plan/add_plan_steap-2/' + str(plan), context)
        else:

            return render(request, 'insuranceCompany/plan/create.html', {'form': form})

def insurance_plan_show(request, id):

    insurancePlan = get_object_or_404(InsurancePlan, id=id)
    # procedures = insurancePlan.procedure.all()

    context = {
        'title': insurancePlan.name,
        'insurancePlan': insurancePlan,
        # 'procedures': procedures,
    }

    return render(request, 'insuranceCompany/show_existing_plan.html', context)

def insurance_supplier_list(request):

    insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()

    # print(insuranceCompany.id)

    company = InsuranceCompany.objects.get(id=insuranceCompany.id)
    suppliers = company.supplier.all()

    try:
        company = InsuranceCompany.objects.get(id=insuranceCompany.id, user=request.user)
        # insuranceCompanyProcedure = InsuranceCompanyProcedure.objects.filter(insuranceCompany=insuranceCompany)
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
            'form': form,
            # 'insuranceCompanyProcedures': insuranceCompanyProcedure,
        }

        return render(request, 'insuranceCompany/supplier_list.html', context)

def add_insurance_supplier(request):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()
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

def get_subcategorias(request):

    category_id = request.GET.get('category_id')
    subCategorys = SubCategory.objects.filter(category_id=category_id)

    data = {
        'subCategorys': [{'id': sub.id, 'nome': sub.name} for sub in subCategorys]
    }

    return JsonResponse(data)

def get_procedures(request):

    subCategory_id = request.GET.get('subCategory_id')
    procedures = Procedure.objects.filter(subCategory_id=subCategory_id)

    data = {
        'procedures': [{'id': sub.id, 'name': sub.name} for sub in procedures]
    }

    return JsonResponse(data)

def add_insurance_supplier_procedure(request,id):
    # insurance_company = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insurance_company = user.insuranceCompany.all().first()
    supplier = Supplier.objects.get(id=id)

    context = {
        'title': 'Procedimentos',
        'supplier': supplier,
        'insuranceCompany': InsuranceCompany.objects.all().order_by('-id'),
        'procedures': Procedure.objects.all(),
        # 'saved_procedures': saved_procedures,
        # 'saved_procedures_ids': saved_procedures_ids,
    }

    return render(request, 'insuranceCompany/add_existing_supplier_procedure.html', context)

def save_procedures(request):

    level = get_object_or_404(Level, id=request.POST.get('level'))

    try:
        if request.method == "POST":
            data = json.loads(request.POST.get("procedures", "[]"))

            for item in data:
                procedure = Procedure.objects.get(id=item['id'])
                InsuranceCompanyProcedure.objects.create(
                    procedure=procedure,
                    negotiated_price=item['negotiated_price'],
                    level=level
                )
            messages.success(request, 'Procedimentos salvos com sucesso!')
            return redirect(reverse('insurance_plan_create_step2', args=[level.plan.id]))

    except requests.RequestException as e:
        messages.error(request, 'Procedimentos salvos com sucesso!')
        return redirect(reverse('insurance_plan_create_step2', args=[9]))

def search_suppliers(request):

    query = request.GET.get('q', '')

    if query:
        suppliers = Supplier.objects.filter(name__icontains=query)
    else:
        suppliers = Supplier.objects.all()[:10]

    results = [{'id': p.id, 'name': p.name} for p in suppliers]
    return JsonResponse(results, safe=False)

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
            insuranceCompany = form.save()
            firstUserName = request.POST.get('firstUserName')
            user = create_user(firstUserName,"InsuranceCompany")
            insuranceCompany.user.add(user)
            messages.success(request, 'Cliente criado com sucesso!')
            return redirect('/dashboard/insurance/list/', context)
        else:
            return render(request, 'insuranceCompany/create.html', {'form': form})

def procedures_list(request):

    categories = Category.objects.all()  # Obtém todas as categorias
    category_data = []

    # Para cada categoria, buscamos suas subcategorias e somamos os procedimentos
    for category in categories:
        subcategories = category.subCategory.all()  # Obtém todas as subcategorias da categoria
        total_procedures = 0
        subcategory_names = []

        for subcategory in subcategories:
            procedure_count = subcategory.procedure.count()  # Conta o número de procedimentos na subcategoria
            total_procedures += procedure_count
            subcategory_names.append(subcategory.name)

        category_data.append({
            'category_name': category.name,
            'subcategories': ', '.join(subcategory_names),  # Lista as subcategorias separadas por vírgulas
            'total_procedures': total_procedures
        })
        context = {
            'title': 'Procedimentos',
            'procedures': Procedure.objects.all().order_by('-id'),
            'category_data': category_data
        }

        return render(request, "procedures/list.html",context)

def procedures_form(request, id=0):
    if request.method == "GET":
        if id == 0 :
            form = ProceduresFrom()

        else:
            procedure = Procedure.objects.get(pk=id)
            form = ProceduresFrom(instance = procedure)

        category_id = request.GET.get('category_id')
        subCategory_id = request.GET.get('subCategory_id')

        if category_id and subCategory_id:
            procedures = Procedure.objects.filter(subCategory_id=subCategory_id)
        else:
            procedures = Procedure.objects.none()

        categorys = Category.objects.all()

        context = {
            'title': 'Procedimentos',
            'form': form,
            'procedure': Procedure.objects.all(),
            'categorys': categorys,
        }
        return render(request, "procedures/create.html",context)
    else:

        form = ProceduresFrom(request.POST, request.FILES)

        procedures_data = request.POST.get('procedures_data')

        if procedures_data:
            import json
            procedures = json.loads(procedures_data)

            procedure_objects = [
                Procedure(
                    name=procedure['name'],
                    code=procedure['id_prodCode'],
                    subCategory=SubCategory.objects.get(pk=procedure['subcategory_id']),
                )
                for procedure in procedures
            ]

            Procedure.objects.bulk_create(procedure_objects)

            context = {
                'title': 'Procedimentos',
                'insuranceCompany': Procedure.objects.all(),
                'form':form,
                'procedure': Procedure.objects.all()
            }

            messages.success(request, 'Procedimentos adicionado(s) com sucesso!')

            return redirect("/dashboard/procedure/list/", context)

        else:
            return render(request, 'procedures/create.html', {'form': form})

def category_list(request, id=0):

    if request.method == "GET":
        if id == 0 :
            form = CategoryFrom()
        else:
            form = CategoryFrom()

        context = {
            'title': 'Categorias',
            'form': form,
            'categorys': Category.objects.all().order_by('-id'),
        }
        return render(request, "category/list.html",context)

    else:

        form = CategoryFrom(request.POST)

        context = {
            'title': 'Categorias',
            'categorys': Category.objects.all().order_by('-id'),
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criado com sucesso!')
            return redirect('/dashboard/category/list/', context)
        else:
            context = {
                'title': 'Categorias',
                'form': form,
                'categorys': Category.objects.all().order_by('-id'),
            }
            return render(request, 'category/list.html', context)

def category_show(request, id):

    category = get_object_or_404(Category, pk=id)

    context = {
        'title': category.name,
        'category': category,
    }

    return render(request, "category/show.html", context)

def subCategory_list(request, id=0):

    if request.method == "GET":
        if id == 0 :
            form = SubCategoryFrom()
        else:
            form = SubCategoryFrom()

        context = {
            'title': 'Sub Categorias',
            'form': form,
            'subCategorys': SubCategory.objects.all().order_by('-id'),
        }
        return render(request, "category/subCategory/list.html",context)

    else:

        form = SubCategoryFrom(request.POST)

        context = {
            'title': 'Sub Categorias',
            'subCategorys': SubCategory.objects.all().order_by('-id'),
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Sub Categoria criado com sucesso!')
            return redirect('/dashboard/subCategory/list', context)
        else:
            context = {
                'title': 'Sub Categorias',
                'form': form,
                'subCategorys': SubCategory.objects.all().order_by('-id'),
            }
            return render(request, 'category/subCategory/list.html', context)

def client_list(request):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()
    context = {
        'title': 'Clientes',
        'clients' : Client.objects.filter(insuranceCompany__id=insuranceCompany.id)
    }

    return render(request, "clients/list.html",context)

def client_form(request, id=0):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()

    if request.method == "GET":
        if id == 0 :
            form = ClientsForm(initial={'insuranceCompany': insuranceCompany})
        else:
            client = Client.objects.get(pk=id)
            form = ClientsForm(instance = client)
            firstUserName = request.POST.get('firstUserName')
            user = create_user(firstUserName,"Client")
            client.user.add(user)

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

def client_show(request, id):

    client = get_object_or_404(Client, id=id)

    beneficiaries = client.beneficiaries.all().order_by('-id')

    # insurancePlan = client.insurancePlan.all().order_by('-id')
    insurancePlan = list(client.insurancePlan.all().order_by('-id'))

    form = AddInsurancePlanClientFrom()

    context = {
        'title': client.name,
        'client': client,
        'linkGenerated': '',
        'form': form,
        'insurancePlans': insurancePlan,
        'beneficiaries': beneficiaries,
    }

    return render(request, 'clients/show.html', context)

def client_show_link(request, id):

    client = get_object_or_404(Client, id=id)
    insurancePlan = client.insurancePlan.all()
    linkGenerated = get_session_data(request,client)

    url = "http://3.111.58.154:5000/create_session"
    token = "$2y$10$q6P7XwLxQk2QWlFg.b5Z4OvjGLQ9VjwE3cB8kXsEg6O1Bw6o"
    payload = {'entity_id': 'gfgugsafjasfj'}
    files = []
    headers = {"Authorization": f"Bearer {token}"}
    link = ""
    session_id = ""

    try:
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code == 201:
            response_data = response.json()
            link = response_data.get('data', {}).get('link', '')
            session_id = response_data.get('data', {}).get('session_id', '')
            # url = reverse('client_beneficiaries_store', args=[session_id, client.id])
            url = reverse('client_beneficiaries_store', args=[session_id, client.id])

            print("Link:", link)
            print("Session ID:", session_id)

        else:
            link = ""
            session_id = ""

    except requests.RequestException as e:
        link = ""
        session_id = ""
        print("Erro na requisição:", e)

    context = {
        'title': client.name,
        'client': client,
        'linkGenerated': link,
        'session_id': session_id,
        'url': url,
        'insurancePlans': insurancePlan,
    }

    return render(request, 'clients/show.html', context)

def client_beneficiaries_store(request, session,client):

    client = get_object_or_404(Client, id=client)
    # insurance_company = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insurance_company = user.insuranceCompany.all().first()

    linkGenerated = get_session_data(request,client)


    url = "http://3.111.58.154:5000/feedback_session"
    token = "$2y$10$q6P7XwLxQk2QWlFg.b5Z4OvjGLQ9VjwE3cB8kXsEg6O1Bw6o"
    payload = {'session_id': 'HRxeCeaJArlTYnz8iIvu288'}
    files = []
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    beneficiary = Beneficiaries(
        name="Samuel",
        address="1 de maio",
        session_id=session,
        client=client,
        insuranceCompany=insurance_company,
        insurancePlan=2,
    )

    beneficiary.save()
    # Verificar se o status da resposta é 200
    if response.status_code == 200:
        data = response.json()  # Assumindo que a resposta seja um JSON
        print("200")
        print(data)
        # Extrair os campos necessários
        full_name = data.get('full name')
        address = data.get('address-portuguese')
        date_of_birth = data.get('date of birth')
        print(full_name)
        print(date_of_birth)

        if full_name and address and date_of_birth:
            # Criar e salvar a instância do modelo
            beneficiary = Beneficiaries(
                name=full_name,
                address=address,
                date_of_activity_start=date_of_birth,
                session_id=session,
                client=client,
                insuranceCompany=insurance_company,
                insurancePlan=2,
            )
            beneficiary.save()
            print("Dados do beneficiário salvos com sucesso!")
        else:
            print("Dados incompletos para salvar o beneficiário.")
    else:
        print(f"Erro ao acessar a API: {response.status_code}")

    print("VM7")

    context = {
        'title': client.name,
        'client': client,
        'linkGenerated': "https://fnbsdk.tablu.tech?id="+session,
        'session_id': session,
    }

    return render(request, 'clients/show.html', context)

def client_plan_store(request):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()

    client_id = request.POST['client']

    client = Client.objects.get(id=client_id)
    print(client)

    if request.method == 'POST':

        form = AddInsurancePlanClientFrom(request.POST)
        if form.is_valid():
            plan = request.POST['insurancePlan']

            client.insurancePlan.add(plan)

            context = {
                'title': 'Meus Provedores',
                'form': form
            }
            messages.success(request, 'Plano adicionado com sucesso!')

            return redirect('/dashboard/client/'+ str(client.id), context)
    else:
        form = AddInsurancePlanClientFrom()

        client = get_object_or_404(Client, id=id)

        context = {
            'title': client.name,
            'client': client,
            'linkGenerated': '',
            'form': form,
        }

        return render(request, 'clients/show.html', context)

def supplier_list(request):

    context = {
        'title': 'Provedor',
        'suppliers' : Supplier.objects.all().order_by('-id')
    }

    return render(request, "supplier/list.html",context)

def supplier_show(request,id=0):

    supplier = Supplier.objects.get(id=id)
    insuranceCompanyProcedure = supplier.insuranceCompanyProcedure.all()

    context = {
        'title': 'Provedor',
        'supplier' : supplier,
        'insuranceCompanyProcedure' : insuranceCompanyProcedure,
    }

    return render(request, "supplier/show.html",context)

def supplier_client_list(request):

    # supplier = getattr(request.user, 'supplier', None)
    user = request.user
    supplier = user.supplier.all().first()

    insuranceCompanys = supplier.insuranceCompany.all()

    context = {
        'title': 'Clientes',
        'insuranceCompanys' : insuranceCompanys
    }

    return render(request, "supplier/client_list.html",context)

def supplier_form(request, id=0):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()

    categorys = Category.objects.all()

    if request.method == "GET":
        if id == 0 :
            form = SupplierForm()
        else:
            supplier = Supplier.objects.get(pk=id)
            form = SupplierForm(instance = supplier)


        category_id = request.GET.get('category_id')
        subCategory_id = request.GET.get('subCategory_id')

        if category_id and subCategory_id:
            procedures = Procedure.objects.filter(subCategory_id=subCategory_id)
        else:
            procedures = Procedure.objects.none()

        context = {
            'title': 'Provedor',
            'form': form,
            'categorys': categorys,
        }
        return render(request, "supplier/create.html", context)
    else:

        form = SupplierForm(request.POST, request.FILES)

        data = json.loads(request.POST.get('procedures_data', '[]'))

        context = {
            'title': 'Criar novo Provedor',
            'supplier': Supplier.objects.all()
        }

        if form.is_valid():

            supplier = form.save()

            firstUserName = request.POST.get('firstUserName')
            user = create_user(firstUserName,"Supplier")
            supplier.user.add(user)

            for procedure_data in data:
                name = procedure_data.get('name')
                price = procedure_data.get('price')
                procedure_id = procedure_data.get('id')

                # Verifica se o nome foi fornecido
                if not name:
                    return JsonResponse({'message': 'Nome do procedimento é obrigatório.'}, status=400)

                # Busca ou cria o procedimento pelo nome
                procedure = Procedure.objects.get(id=procedure_id)

                # Cria ou atualiza o InsuranceCompanyProcedure
                InsuranceCompanyProcedure.objects.update_or_create(
                    supplier=supplier,
                    procedure=procedure,
                    defaults={
                        'negotiated_price': price,
                    }
                )
            messages.success(request, 'Provedor criado com sucesso!')

            return redirect( '/dashboard/supplier/list/',context)

        else:
            # Exibe os erros no console
            print("Formulário inválido. Erros:")
            print(form.errors.as_json())
            context = {
                'title': 'Provedor',
                'form': form,
                'categorys': categorys,
            }

            return render(request, 'supplier/create.html', context)

def supplier_client_show(request,id):

    # supplier = getattr(request.user, 'supplier', None)
    user = request.user
    supplier = user.supplier.all().first()
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

def supplier_procedures(request):

    #supplier = getattr(request.user, 'supplier', None)

    user = request.user
    supplier = user.supplier.all().first()

    procedures = InsuranceCompanyProcedure.objects.filter(supplier=supplier)

    context = {
        'title': "Procedimentos",
        'procedures': procedures,
     }

    return render(request, 'supplier/procedures/list.html', context)

def send_beneficiaries_email(request,savedForm):

    url = "http://3.111.58.154:5000/create_session"
    token = "$2y$10$q6P7XwLxQk2QWlFg.b5Z4OvjGLQ9VjwE3cB8kXsEg6O1Bw6o"
    payload = {'entity_id': 'gfgugsafjasfj'}
    files = []
    headers = {"Authorization": f"Bearer {token}"}
    link = ""
    session_id = ""

    try:
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code == 201:
            response_data = response.json()
            link = response_data.get('data', {}).get('link', '')
            session_id = response_data.get('data', {}).get('session_id', '')

            print("EMAIL:", savedForm.email)
            print("Link:", link)
            print("Session ID:", session_id)

            savedForm.session_id = session_id
            savedForm.save()

            address = savedForm.email
            name = savedForm.name
            subject = "Heath Care Management complete the submission of your data"
            html_content = "Olá,    !"+ name+"""
                
            Para completar o processo de submissão dos seus dados, por favor clique no link abaixo e preencha as informações necessárias:
    
            👉Complete sua submissão aqui {link}
    
            Se tiver qualquer dúvida ou dificuldade, estamos à disposição para ajudar! 😊
            """.format(link=link)

            send_email(request, address, subject, html_content)
        else:

            link = ""
            session_id = ""

    except requests.RequestException as e:
        print("Erro na requisição:", e)

def beneficiarie_client_create(request, client_id=0):

    client = get_object_or_404(Client, id=client_id)
    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()
    beneficiaries = client.beneficiaries.all().order_by('-id')
    insurancePlans = client.insurancePlan.all().order_by('-id')

    if request.method == "POST":
        beneficiaries_data = request.POST.get('beneficiaries', '[]')
        beneficiaries = json.loads(beneficiaries_data)

        for beneficiaries in beneficiaries:

            savedForm = Beneficiaries.objects.create(
                client=client,
                name=beneficiaries['name'],
                email=beneficiaries['email'],
                phoneNumber=beneficiaries['phoneNumber'],
                insurancePlan_id=beneficiaries['insurancePlan'],
                insuranceCompany=insuranceCompany
            )

            insurancePlan = InsurancePlan.objects.get(pk=beneficiaries['insurancePlan'])
            savedForm.clone_plan(insurancePlan)

            #send_beneficiaries_email(request, savedForm)

        messages.success(request, 'Beneficiários adicionados com sucesso!')
        return redirect(f'/dashboard/client/{client.id}')

    else:
        form = BeneficiariesForm()
        context = {
            'title': 'Adicionar beneficiário',
            'form': form,
            'insuranceCompany': insuranceCompany,
            'client': client,
            'beneficiaries': beneficiaries,
            'insurancePlans': insurancePlans,
        }
        return render(request, "clients/beneficiaries/create.html", context)

def construir_hierarquia_beneficiary1(niveis, parent=None, visitados=None):
    if visitados is None:
        visitados = set()

    hierarquia = []
    for nivel in niveis:
        if nivel.id in visitados:
            continue  # Ignorar ciclos ou níveis já processados
        if nivel.parent_level == parent:
            visitados.add(nivel.id)
            subniveis = construir_hierarquia_beneficiary(niveis, parent=nivel, visitados=visitados)
            hierarquia.append({
                'id': nivel.id,
                'name': nivel.name,
                'plafonPrice': nivel.plafonPrice,
                'procedures': list(nivel.beneficiaryICProcedure.all()),
                'sublevels': subniveis,
            })
    return hierarquia

def construir_hierarquia_beneficiary(levels):
    # Organizar os níveis por seus pais
    tree = {}
    for level in levels:
        parent_id = level.level_parent_id
        if parent_id not in tree:
            tree[parent_id] = []
        tree[parent_id].append(level)

    # Função recursiva para construir a hierarquia
    def construir_subarvore(parent_id):
        subarvore = []
        for level in tree.get(parent_id, []):
            subarvore.append({
                'level': level,
                'children': construir_subarvore(level.id)
            })
        return subarvore

    return construir_subarvore(None)  # Começa com os níveis sem pai

def construir_hierarquia2(niveis, parent=None, visitados=None):
    if visitados is None:
        visitados = set()

    hierarquia = []
    for nivel in niveis:
        if nivel.id in visitados:
            continue  # Ignorar ciclos ou níveis já processados
        if nivel.parent_level == parent:
            visitados.add(nivel.id)
            subniveis = construir_hierarquia2(niveis, parent=nivel, visitados=visitados)
            hierarquia.append({
                'id': nivel.id,
                'name': nivel.name,
                'plafonPrice': nivel.plafonPrice,
                'beneficiaryICProcedure': list(nivel.beneficiaryICProcedure.all()),
                'sublevels': subniveis,
            })
    return hierarquia

def beneficiary_plan_show(request, id=0):

    user = request.user

    beneficiary = get_object_or_404(Beneficiaries, id=id)

    beneficiaryPlan = BeneficiaryPlan.objects.get(beneficiary=beneficiary)

    plan = BeneficiaryPlan.objects.prefetch_related('beneficiaryLevel__beneficiaryICProcedure').get(id=beneficiaryPlan.id)

    if request.method == "GET":
        if id == 0:
            form = LevelForm()
        else:

            levels = BeneficiaryLevel.objects.filter(insurancePlan=plan).select_related('parent_level').prefetch_related('beneficiaryICProcedure')

            hierarquia = construir_hierarquia2(levels)

            print(hierarquia)
            # Preparar o formulário
            form = LevelForm()
            context = {
                'title': "",
                'beneficiary': beneficiary,
                'beneficiaryPlan': beneficiaryPlan,
                'levels': levels,
                'hierarquia': hierarquia,
                'form': form,
            }

            return render(request, 'clients/beneficiaries/plan/show.html', context)

    else:
        plan = request.POST.get('plan')

        form = LevelForm(request.POST, request.FILES)

        context = {
            'title': 'Planos',
            'plans': BeneficiaryPlan.objects.all()
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Plano adicionado com sucesso!')
            return redirect('/dashboard/beneficiary/plan/add_plan_step-2/' + str(plan), context)
        else:
            return redirect('/dashboard/beneficiary/plan/add_plan_step-2/' + str(plan), context)

def individual_form(request):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()
    if request.method == "POST":
        individuals_data = request.POST.get('individuals', '[]')
        individuals = json.loads(individuals_data)
        print(individuals)

        for individuals in individuals:
            savedForm = Individuals.objects.create(
                name=individuals['name'],
                email=individuals['email'],
                insurancePlan_id=individuals['insurancePlan'],
                phoneNumber=individuals['phoneNumber'],
                insuranceCompany=insuranceCompany
            )
            send_beneficiaries_email(request, savedForm)

        individuals = insuranceCompany.individuals.all()

        context = {
            'title': "Indivíduos",
            'individuals': individuals,
            'insuranceCompany': insuranceCompany,
        }
        messages.success(request, 'Adicionados com sucesso!',context)
        return redirect('/dashboard/individuals/list/',context)

    else:
        form = IndividualsForm()
        context = {
            'title': 'Adicionar Indivíduos',
            'form': form,
            'insuranceCompany': insuranceCompany,
        }
        return render(request, "individuals/create.html", context)

def individual_list(request):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()
    individuals = insuranceCompany.individuals.all()

    context = {
        'title': "Indivíduos",
        'individuals': individuals,
        'insuranceCompany': insuranceCompany,
    }

    return render(request, 'individuals/list.html', context)

def get_session_data(request,client):

    url = "http://3.111.58.154:5000/create_session"
    token = "$2y$10$q6P7XwLxQk2QWlFg.b5Z4OvjGLQ9VjwE3cB8kXsEg6O1Bw6o"
    payload = {'entity_id': 'gfgugsafjasfj'}
    files = []
    headers = {"Authorization": f"Bearer {token}"}
    existing_user = ""
    try:

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code == 201:

            response_data = response.json()
            link = response_data.get('data', {}).get('link', '')
            session_id = response_data.get('data', {}).get('session_id', '')
            linkGenerated = link
            # Exibe os valores no console
            print("Link:", link)
            print("Session ID:", session_id)

            #
            # # Verifica se o cookie "user_name" já existe
            # if not request.COOKIES.get("session_id"):
            #     # response = render(request, "clients/show.html", {"session_id": session_id,"client":client,'linkGenerated': linkGenerated,})
            #     request.set_cookie("user_name", session_id)  # Salva o cookie
            #     # request.set_cookie("session_id", session_id)
            #     return response
            # else:
            #     # Retorna com o user_name já existente no cookie
            #     request.COOKIES.get("session_id")
            context = {
                'link': link,
            }

        else:
            # Caso o status não seja 201, retorna erro
            return JsonResponse({
                'message': 'Erro ao criar a sessão',
                'status': response.status_code
            }, status=response.status_code)

    except requests.RequestException as e:
        # Exibe o erro no console
        print("Erro na requisição:", e)

        # Retorna o erro como JSON para depuração
        return JsonResponse({"error": "Erro na requisição", "details": str(e)}, status=500)

def treatment_list(request):
    user = request.user

    supplier = Supplier.objects.get(user=user)
    beneficiarieTreatments = BeneficiarieTreatment.objects.filter(supplier=supplier)

    print(beneficiarieTreatments)

    context = {
        'title': 'Atendimento',
        'beneficiarieTreatments' : beneficiarieTreatments
    }

    return render(request, "treatment/list.html",context)

def treatment_create2(request, id=0):

    # insuranceCompany = getattr(request.user, 'insuranceCompany', None)
    user = request.user
    insuranceCompany = user.insuranceCompany.all().first()
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
            return render(request, 'treatment/create.html', {'form': form})
def treatment_show(request, id=0):

    beneficiarieTreatment = get_object_or_404(BeneficiarieTreatment, id=id)

    context = {
       'title': "Detalhes do tratamento",
       'beneficiarieTreatment': beneficiarieTreatment,
    }

    return render(request, 'treatment/show.html', context)

def treatment_create(request):

    procedures = Procedure.objects.all()
    beneficiarie = []
    search_query = request.POST.get('id')
    try:
        if search_query.isdigit():

            beneficiary = Beneficiaries.objects.get(pk=int(search_query))

            beneficiaryPlan = BeneficiaryPlan.objects.get(beneficiary=beneficiary)

            beneficiaryLevels = BeneficiaryLevel.objects.filter(insurancePlan=beneficiaryPlan)

            procedures = BeneficiaryICProcedure.objects.filter(level__in=beneficiaryLevels)

        else:
            beneficiary = Beneficiaries.objects.get(phoneNumber=search_query)
        # beneficiarie = Beneficiaries.objects.get(pk=request.POST['id'])
    except Beneficiaries.DoesNotExist:
        messages.error(request, f'Beneficiario não encontrado')
        return redirect(request.META.get('HTTP_REFERER', '/'))


    context = {
        'title': beneficiary.name,
        'beneficiary': beneficiary,
        'procedures': procedures,
    }

    return render(request, 'treatment/create.html', context)

def check_plafon(procedure, limite=10):

    nivel_atual = procedure.level

    while nivel_atual:

        if nivel_atual.plafonPrice > limite:
            nivel_atual.plafonPrice
            # return False
        nivel_atual = nivel_atual.parent_level

    return True

def update_plafon(procedure, limite):

    nivel_atual = procedure.level

    while nivel_atual:

        if nivel_atual.plafonPrice > limite:
            nivel_atual.plafonPrice = nivel_atual.plafonPrice - limite
            nivel_atual.save()
        nivel_atual = nivel_atual.parent_level

    return True

def save_treatment_procedures(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            procedures_data = data.get("procedures", [])

            beneficiary_id = data.get("beneficiary")

            beneficiary = Beneficiaries.objects.get(pk=int(beneficiary_id))

            user = request.user

            supplier = Supplier.objects.get(user=user)

            beneficiaryPlan = BeneficiaryPlan.objects.get(beneficiary=beneficiary)

            if not procedures_data:
                return JsonResponse({"success": False, "error": "Nenhum procedimento selecionado."})

            treatments = []
            treatment = BeneficiarieTreatment.objects.create(
                beneficiarie=beneficiary,
                description="Descrição do tratamento",
                supplier=supplier
            )
            for procedure_data in procedures_data:
                procedure_id = procedure_data.get("procedure_id")

                try:

                    procedure = BeneficiaryICProcedure.objects.get(id=procedure_id)

                    canContinue = check_plafon(procedure, procedure.procedure.base_price)

                    if canContinue:
                        update_plafon(procedure,procedure.procedure.base_price)
                        procedure.negotiated_price = procedure.negotiated_price - procedure.procedure.base_price
                        procedure.save()

                        treatment.procedure.add(procedure.procedure)

                    else:
                        return JsonResponse({"success": False, "error": f"Procedimento {procedure_id} não tem plafon."})

                except Procedure.DoesNotExist:
                    return JsonResponse({"success": False, "error": f"Procedimento {procedure_id} não tem plafon."})

            if treatments:
                BeneficiarieTreatment.objects.bulk_create(treatments)
            return JsonResponse({"success": True, "message": "Procedimentos salvos com sucesso!"})

        except json.JSONDecodeError as e:
            return JsonResponse({"success": False, "error": "Erro ao processar os dados."})

    return JsonResponse({"success": False, "error": "Método não permitido."})


def verificar_plafon_por_procedimento(hierarquia, procedimento, limite=10):
    """
    Verifica se o plafonPrice dos níveis hierárquicos e do procedimento atendem a uma condição.

    Args:
        hierarquia (list): A lista de níveis hierárquicos.
        procedimento (str): O nome do procedimento a ser verificado.
        limite (int): O valor limite para a verificação do plafonPrice.

    Returns:
        bool: True se todas as condições forem atendidas, False caso contrário.
    """
    for nivel in hierarquia:
        # Verifica se o procedimento está neste nível
        if procedimento in nivel['insurancecompanyprocedures']:
            # Se o plafonPrice do nível atual é válido
            return nivel['plafonPrice'] > limite

        # Verifica recursivamente nos subníveis
        if nivel['sublevels']:
            resultado = verificar_plafon_por_procedimento(nivel['sublevels'], procedimento, limite)
            if resultado:
                # Verifica se o nível atual também atende ao limite
                return nivel['plafonPrice'] > limite
    return False

def user_list(request):

    users = User.objects.all()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'title': "Utilizadores",
                'users': users,
            }
            messages.success(request, "Usuário criado com sucesso!")
            return redirect('/dashboard/users/list/', context)
    else:
        form = CreateUserForm()

        context = {
            'title': "Utilizadores",
            'users': users,
            'form': form,
        }

    return render(request, 'user/user_list.html', context)



def manage_profile(request):

    profile = request.user.profile
    if profile:
        profile = profile
    else:
        profile = []

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            context = {
                'title': "Gerir perfil",
                'form': form,
                'profile': profile
            }
            messages.success(request, 'Adicionados com sucesso!', context)
            return redirect('/dashboard/manage_profile',context)
    else:

        form = ProfileForm(instance=profile)

        context = {
            'title': "Gerir perfil",
            'form': form,
            'profile': profile
        }

    return render(request, 'auth/profile/manage_profile.html', context)

