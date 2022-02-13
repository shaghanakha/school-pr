from django.contrib import admin
from .models import News, Exercise, Lesson, AnswerExercise

admin.site.register(Lesson)
admin.site.register(News)
admin.site.register(Exercise)
admin.site.register(AnswerExercise)
