from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

def custom_permission_required(permission):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.has_perm(permission):
                return render(request, 'no_permission.html')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@custom_permission_required('frontend.lgd_bd_access')
def my_view(request):
    # your view code here
    return render(request, 'no_permission.html')