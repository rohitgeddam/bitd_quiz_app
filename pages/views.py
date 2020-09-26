from django.shortcuts import render
from django.views.generic import ListView
from quizes.models import Quiz, QuizTaker, Response

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

# Create your views here.

class HomePageView(ListView):
    model = Quiz
    context_object_name = 'quiz_list'
    
    template_name = 'home.html'

    queryset = Quiz.objects.filter(roll_out=True)

@login_required
def QuizStartPage(request, slug):
    quiz = Quiz.objects.filter(slug=slug).first()
    questions = quiz.questions.all()
    attempted = QuizTaker.objects.filter(user=request.user.id,quiz=quiz.id).count() > 0
    return render(request, 'quiz_start.html', {"quiz": quiz, "questions":questions, "attempted":  attempted})
    

@login_required
def QuizSubmit(request, slug):
    user = request.user
    quiz = Quiz.objects.filter(slug=slug).first()
    questions = quiz.questions.all()

    attempted = QuizTaker.objects.filter(user=request.user.id,quiz=quiz.id).count() > 0

    quiz_taker_score = 0

    if (attempted):
        return HttpResponse("This is not allowed.")
    else:

        for question in questions:
            q_id = question.id
            correct_option = question.options.filter(is_answer=True).first()
            correct_option_id = correct_option.id
            user_response = request.POST.get(str(q_id))

            if(user_response == str(correct_option_id)):
                quiz_taker_score += 1
        
            
        quiz_take = QuizTaker.objects.create(
            user = user,
            quiz = quiz,
            score = quiz_taker_score
        )
       
        return HttpResponse("done" + str(quiz_taker_score))