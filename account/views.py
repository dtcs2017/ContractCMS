from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm
from django.contrib import messages
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='cmslog.log',
                    filemode='a+')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            logging.info("{} | register | id={}".format(new_user.username, new_user.id))
            messages.success(request, '注册成功，请联系管理员激活账号')
            return redirect(reverse('login'))
        messages.error(request, '请检查表单是否正确填写')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {"form": form})
