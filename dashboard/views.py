from django.shortcuts import render
from django.contrib import messages


def dashboard(request):
    messages.success(request, '测试消息')
    return render(request, 'dashboard/dashboard.html')
