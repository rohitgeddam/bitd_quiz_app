from django.contrib import admin
import nested_admin

from .models import Question, Quiz, Option, QuizTaker, Response
# Register your models here.


class OptionAdmin(nested_admin.NestedTabularInline):
    model = Option
    extra = 0
    class Media:
       js = ('ckeditor/ckeditor/ckeditor.js')

class QuestionAdmin(nested_admin.NestedStackedInline):
    model = Question
    inlines = [OptionAdmin]
    extra = 0
    class Media:
        js = ('ckeditor/ckeditor/ckeditor.js')

class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ['name', 'start_time', 'end_time', 'roll_out']
    prepopulated_fields = {"slug": ('name',),}
    exclude = ['created_by',]
    inlines = [QuestionAdmin]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super(QuizAdmin, self).save_model(request, obj, form, change)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Response)
admin.site.register(QuizTaker)

