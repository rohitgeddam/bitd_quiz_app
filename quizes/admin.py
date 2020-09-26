from django.contrib import admin
import nested_admin
from .models import Question, Quiz, Option, QuizTaker, Response
# Register your models here.


class OptionAdmin(nested_admin.NestedTabularInline):
    model = Option
    

class QuestionAdmin(nested_admin.NestedStackedInline):
    model = Question
    inlines = [OptionAdmin]
    

class QuizAdmin(nested_admin.NestedModelAdmin):
    prepopulated_fields = {"slug": ('name',),}
    inlines = [QuestionAdmin]


admin.site.register(Quiz, QuizAdmin)

admin.site.register(QuizTaker)

