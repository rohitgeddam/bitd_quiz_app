from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from django.urls import reverse
# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    allowed_time = models.DurationField()
    roll_out = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'quizes'
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('quiz_start', args=(self.slug,))
        

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    
    text = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.text[:30]
    
class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options',  on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:30]
    
class QuizTaker(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='quiz_takers',  on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='quiz_takers',  on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, default=0.0, max_digits=4)

    def __str__(self):
        return self.user.username
    
    
class Response(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='responses',  on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='responses',  on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}_{self.quiz.name}'
    
    