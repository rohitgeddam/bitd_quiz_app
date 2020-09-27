from django.urls import path, include


from .views import HomePageView, QuizStartPage, QuizSubmit, leaderboard

urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    
    path('quiz/<slug:slug>/', QuizStartPage, name="quiz_start"),
    path('quiz/<slug:slug>/submit/', QuizSubmit, name="quiz_submit"),
    path('leaderboard/', leaderboard, name="leaderboard")
]