from django.urls import path
from . import views
from .views import procedures_form

urlpatterns = [

    path('', views.dashboard,name='dashboard'),

    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),

    # insurance
    path('insurance/create/', views.insurance_form, name='insurance_form'),
    path('insurance/list/', views.insurance_list, name='insurance_list'),
    path('insurance/plan/list/', views.insurance_plan_list, name='insurance_plan_list'),
    path('insurance/plan/add_plan/', views.insurance_plan_create, name='insurance_plan_create'),
    path('insurance/supplier/list/', views.insurance_supplier_list, name='insurance_supplier_list'),
    path('insurance/supplier/create/', views.add_insurance_supplier, name='add_insurance_supplier'),
    path('insurance/supplier/procedure/<int:id>/', views.add_insurance_supplier_procedure, name='add_insurance_supplier_procedure'),

    # procedures
    path('procedure/create/', views.procedures_form, name='procedures_form'),
    path('procedure/list/', views.procedures_list, name='procedures_list'),

    #clients
    path('client/create/', views.client_form, name='client_form'),
    path('client/list/', views.client_list, name='client_list'),
    path('client/<int:id>/', views.client_detail, name='client_detail'),

    #supplier
    path('supplier/create/', views.supplier_form, name='supplier_form'),
    path('supplier/list/', views.supplier_list, name='supplier_list'),
    path('supplier/client/list/', views.supplier_client_list, name='supplier_client_list'),
    path('supplier/client/show/<int:id>/', views.supplier_client_show, name='supplier_client_show'),
    path('save-procedures/', views.save_procedures, name='save_procedures'),

]
