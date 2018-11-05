from django.urls import path, include
from . import views

app_name = 'payments'

urlpatterns = [
    path('detail/<int:contract_id>/', views.payment_detail, name="payment_detail"),
    path('edit/<int:contract_id>/<int:payment_id>/', views.payment_edit, name='payment_edit'),
]
