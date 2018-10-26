from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(r"密码不一致，请重新输入")
        return cd['password2']

    class Meta:
        model = User
        fields = ('username', 'email')
