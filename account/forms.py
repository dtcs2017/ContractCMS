from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):
    """
    此处User类实际是自行替换的ABC类
    使用自定义验证器验证两个密码是否相同
    """
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='重复密码', widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(r"密码不一致，请重新输入")
        return cd['password2']

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': '用户名',
            'email': '电子邮件',
        }
