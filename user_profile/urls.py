from django.urls import path

from user_profile.views import profile_list_view, ProfileCreateView
urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name="profile_create"),
    path('', profile_list_view, name="profile_list")
]