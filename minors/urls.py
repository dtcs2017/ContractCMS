from django.urls import path
from . import views

app_name = 'minors'

urlpatterns = [
    path('list/', views.minor_list, name='minor_list'),
    path('list/<int:subject_id>/', views.minor_list, name='minor_list_by_subject'),
    path('add/', views.minor_add, name='minor_add'),
    path('edit/<int:directcost_id>/', views.minor_edit, name='minor_edit'),
    path('req/list/<int:directcost_id>/', views.req_list, name='req_list'),
    path('req/edit/<int:directcost_id>/<int:req_id>/', views.req_edit, name='req_edit'),
    path('pay/list/<int:directcost_id>/', views.directpayment_list, name='pay_list'),
    path('pay/edit/<int:directcost_id>/<int:pay_id>/', views.pay_edit, name='pay_edit'),
]
