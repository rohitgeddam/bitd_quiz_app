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
        return redirect(reverse_lazy('profile_update'))

# class ProfileCreateView(FormView):
#     form_class = ProfileForm
#     template_name = "profile_create.html"
#     success_url = reverse_lazy('home_page')

#     def form_valid(self, form):
#         form.user = self.request.user
#         user_profile = Profile.objects.filter(user=self.request.user).first()
#         user_profile.completed_profile = True
#         user_profile.save()
#         form.save()
#         return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)

    #     if form.is_valid():
            
    #         user_profile = Profile.objects.filter(user=self.request.user).first()
    #         user_profile.completed_profile = True
    #         user_profile.save()
    #         form.save(kwargs.get('pk'))
    #     else:
    #         return self.form_invalid(form)
def profile_update_view(request):
    instance = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.completed_profile = True
        instance.save()
        return render(request, 'quiz_start.html')
    context = {
        "form": form,
    }
    return render(request, 'profile_update.html', context)
    
    