from django.shortcuts import render, redirect
from django.views.generic import ListView
from quizes.models import Quiz, QuizTaker, Response, Option
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .decorators import profile_completion_required
# Create your views here.

class HomePageView(ListView):
    model = Quiz
    context_object_name = 'quiz_list'
    
    template_name = 'home.html'

    queryset = Quiz.objects.filter(roll_out=True)

@login_required
@profile_completion_required()
def QuizStartPage(request, slug):
    quiz = Quiz.objects.filter(slug=slug).first()
    questions = quiz.questions.all()
    attempted = QuizTaker.objects.filter(user=request.user.id,quiz=quiz.id).count() > 0
    user = request.user
  
    
    if(attempted):
        score = QuizTaker.objects.filter(user=user, quiz=quiz).first().score
        
        user_response = []
        for question in questions:
          
            # try:
            response = Response.objects.filter(user=user,quiz=quiz,question=question).first()
            data = {
                "question":question,
                "is_correct": response.is_correct,
                "user_option": response.option,
                "correct_option": response.correct_option
            }
            # except:

            #     data = {
            #         "is_correct": False,
            #         "user_option": None,
            #         "correct_option": response.correct_option
            #     }
            
            user_response.append(data)

        return render(request, 'quiz_start.html', {"quiz": quiz, "questions":questions, "attempted":  attempted,"responses": user_response, "score":score})
          

    return render(request, 'quiz_start.html', {"quiz": quiz, "questions":questions, "attempted":  attempted,})
    

@login_required
@profile_completion_required()
def QuizSubmit(request, slug):
    user = request.user
    quiz = Quiz.objects.filter(slug=slug).first()
    questions = quiz.questions.all()

    attempted = QuizTaker.objects.filter(user=request.user.id,quiz=quiz.id).count() > 0

    quiz_taker_score = 0

    if (attempted):
        return redirect(reverse_lazy("quiz_start", args=(quiz.slug,)))
    else:
        responses = []
        for question in questions:

            try:
                q_id = question.id
                correct_option = question.options.filter(is_answer=True).first()
                # correct_option_id = correct_option.id
                user_response = request.POST.get(str(q_id))
                user_option = question.options.filter(id = int(user_response)).first()
            
                
                if(correct_option.id == user_option.id):
                    quiz_taker_score += 1
                    is_correct = True
                else:
                    is_correct = False
                    
                
                responses.append(
                    Response(
                        user = user,
                        quiz = quiz,
                        question = question,
                        option = user_option,
                        correct_option = correct_option,
                        is_correct = is_correct
                    )
                )
            except:
                # user not attempted this question.
                responses.append(
                    Response(
                        user = user,
                        quiz = quiz,
                        question = question,
                        option = None,
                        correct_option = correct_option,
                        is_correct = False
                    )
                )
            
        quiz_take = QuizTaker.objects.create(
            user = user,
            quiz = quiz,
            score = quiz_taker_score
        )

        Response.objects.bulk_create(responses)
       
        return redirect(reverse_lazy("quiz_start",args=(quiz.slug,)))