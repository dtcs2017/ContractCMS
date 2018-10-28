from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('list/<int:subject_id>/', views.contract_list, name='contract_list_subject'),
    path('list/', views.contract_list, name='contract_list'),
    path('detail/<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('add/', views.contract_add, name='contract_add'),
    path('add/<int:master_id>/', views.contract_add, name='contract_add_supple'),
    path('edit/<int:contract_id>/', views.contract_edit, name='contract_edit'),
]
