from django import forms
from .models import DirectPayment, DirectCost, DirectRequisition


class DirectCostForm(forms.ModelForm):
    class Meta:
        model = DirectCost
        fields = ('name', 'amount', 'supplier', 'subject', 'text')


class DirectRequisitionForm(forms.ModelForm):
    class Meta:
        model = DirectRequisition
        fields = ('amount', 'invoice', 'payday', 'text')


class DirectPaymentForm(forms.ModelForm):
    class Meta:
        model = DirectPayment
        fields = ('amount', 'record', 'payday', 'rate', 'text')
