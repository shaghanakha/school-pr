from django.urls import path
from exercise.views import *

urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('exercises/', ExerciseList.as_view(), name='exercise_list'),
    path('exercises/<int:pk>', ExercisesDetail.as_view(), name='exercises_detail'),
    path('exercises/answer/', AnswerExerciseView.as_view(), name='answer_list'),
    # path('exercises/answer/<int:e_id>', AnswerToExercise.as_view(), name='answer_add'),
    path('lessons/<int:pk>', LessonDetail.as_view(), name='lessons_detail'),
    path('answer/<int:pk>', AnswerExerciseDetail.as_view(), name='answer_detail'),

]
