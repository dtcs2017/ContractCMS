from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponse


def contractor_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_contractor:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse('不具备添加和修改合同权限，请退回上一页')
    return wrapper


def accountant_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_accountant:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse('不具备添加和修改付款权限，请返回上一页')
    return wrapper


def engineer_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_engineer:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper


def frontier_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_frontier:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper


def designer_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_designer:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper
