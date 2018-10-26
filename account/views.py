from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            return redirect(reverse('login'))

    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {"form": form})


