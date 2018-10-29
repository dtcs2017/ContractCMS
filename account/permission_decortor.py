from django.core.exceptions import PermissionDenied


def contractor_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_contractor:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper


def accountant_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_accountant:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
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
