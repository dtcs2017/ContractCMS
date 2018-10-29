from django.urls import path
from . import views

app_name = 'requisitions'

urlpatterns = [
    path('detail/<int:contract_id>/', views.requisition_detail, name='req_detail'),
    path('edit/<int:contract_id>/<int:req_id>/', views.requisition_edit, name='req_edit'),
]
