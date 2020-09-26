from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.views.generic import FormView
from .models import Profile
from django.urls import reverse_lazy

# Create your views here.

def profile_list_view(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    if (user_profile.completed_profile):
        # list view
        return render(request, "user_profile.html", {"user_profile": user_profile})
    else:
        return redirect(reverse_lazy('profile_create'))
class ProfileCreateView(FormView):
    form_class = ProfileForm
    template_name = "profile_create.html"
    success_url = reverse_lazy('profile_list')

    def is_valid(self, form):
        print("valid")
        super(ProfileCreateView, self).is_valid(form)
        