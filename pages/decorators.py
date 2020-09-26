from django.shortcuts import redirect
from user_profile.models import Profile
from django.urls import reverse_lazy

def profile_completion_required():
    def decorator(func):
        def wrap(request, *args, **kwargs):
            profile = Profile.objects.get(user=request.user)
            if (profile.completed_profile):
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse_lazy("profile_list"))
        return wrap
    return decorator
    
            