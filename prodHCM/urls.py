from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard,name='dashboard'),

    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),

    # insurance
    path('insurance/create/', views.insurance_form, name='insurance_form'),
    path('insurance/list/', views.insurance_list, name='insurance_list'),
    path('insurance/plan/list/', views.insurance_plan_list, name='insurance_plan_list'),
    path('insurance/plan/add_plan/', views.insurance_plan_create, name='insurance_plan_create'),
    path('insurance/plan/add_plan_steap-2/<int:id>/', views.insurance_plan_create_step2, name='insurance_plan_create_step2'),
    path('insurance/plan/add_plan_procedure/<int:id>/', views.insurance_plan_create_procedure, name='insurance_plan_create_procedure'),
    path('insurance/plan/insurance_plan_create_sublevel', views.insurance_plan_create_sublevel, name='insurance_plan_create_sublevel'),
    path('insurance/plan/save_procedures/', views.save_procedures, name='save_procedures'),
    path('insurance/plan/show_plan/<int:id>/', views.insurance_plan_show, name='insurance_plan_show'),
    path('insurance/supplier/list/', views.insurance_supplier_list, name='insurance_supplier_list'),
    path('insurance/supplier/create/', views.add_insurance_supplier, name='add_insurance_supplier'),
    path('insurance/supplier/procedure/<int:id>/', views.add_insurance_supplier_procedure, name='add_insurance_supplier_procedure'),

    # procedures
    path('procedure/create/', views.procedures_form, name='procedures_form'),
    path('procedure/list/', views.procedures_list, name='procedures_list'),
    path('get_subcategorias/', views.get_subcategorias, name='get_subcategorias'),
    path('get_procedures/', views.get_procedures, name='get_procedures'),

    #category
    path('category/list/', views.category_list, name='category_list'),
    path('category/show/<int:id>/', views.category_show, name='category_show'),

    #subCategory
    path('subCategory/list/', views.subCategory_list, name='subCategory_list'),

    # individuals
    path('individuals/create/', views.individual_form, name='individual_form'),
    path('individuals/list/', views.individual_list, name='individual_list'),

    path('client/create/', views.client_form, name='client_form'),
    path('client/list/', views.client_list, name='client_list'),
    path('client/<int:id>/', views.client_show, name='client_show'),
    path('client/show_link/<int:id>/', views.client_show_link, name='client_show_link'),
    path('client/beneficiarie/<str:session>/<int:client>/', views.client_beneficiaries_store, name='client_beneficiaries_store'),
    path('client/beneficiaries/create/<int:client_id>/', views.beneficiarie_client_create, name='beneficiarie_client_create'),
    path('client/beneficiary/plan/show/<int:id>/', views.beneficiary_plan_show, name='beneficiary_plan_show'),
    path('client/plan/store/', views.client_plan_store, name='client_plan_store'),

    #supplier
    path('supplier/create/', views.supplier_form, name='supplier_form'),
    path('supplier/list/', views.supplier_list, name='supplier_list'),
    path('supplier/list/show/<int:id>/', views.supplier_show, name='supplier_show'),
    path('supplier/client/list/', views.supplier_client_list, name='supplier_client_list'),
    path('supplier/client/show/<int:id>/', views.supplier_client_show, name='supplier_client_show'),
    path('supplier/procedures/', views.supplier_procedures, name='supplier_procedures'),


    path('search-suppliers/', views.search_suppliers, name='search_suppliers'),

    # user
    path('users/list', views.user_list, name="user_list"),

    #profile
    path('manage_profile', views.manage_profile, name="manage_profile"),

    # treatment
    path('supplier/treatment/create/', views.treatment_create, name='treatment_create'),
    path('supplier/treatment/list/', views.treatment_list, name='treatment_list'),
    path('supplier/treatment/show/', views.treatment_show, name='treatment_show'),
    # path('supplier/treatment/show/<int:id>/', views.treatment_show, name='treatment_show'),
    path('supplier/treatment/plan/save_treatment_procedures/', views.save_treatment_procedures, name='save_treatment_procedures'),

    path("get-session-data/", views.get_session_data, name="get_session_data"),



    # path("send-html-email/", views.send_html_email, name="send_html_email"),

]
