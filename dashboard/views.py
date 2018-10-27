from django.shortcuts import render
from django.contrib import messages


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
