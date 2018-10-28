from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    messages.success(request, '测试消息')
    return render(request, 'dashboard/dashboard.html')
