from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            messages.success(request, '成功注册')
            return redirect(reverse('login'))
        messages.error(request,'请检查表单是否正确填写')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {"form": form})
