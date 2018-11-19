from django.shortcuts import render
from django.contrib import messages


def dashboard(request):
    """
    首页，无需权限即可访问
    :param request:
    :return:
    """
    return render(request, 'dashboard/dashboard.html')


def about(request):
    """
    关于页面
    :param request:
    :return:
    """

    return render(request, 'dashboard/about.html')
