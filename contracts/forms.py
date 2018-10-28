from django import forms
from .models import Contract


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ('name', 'supplier', 'subject', 'sign', 'amount', 'definite', 'active', 'jgc', 'text',)
        widgets = {
            'sign': forms.DateInput()
        }
