from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *


class NewsList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            query = News.objects.filter(teacher=user)
            return query
        if user.is_student:
            teachers = list()
            for obj in Lesson.objects.all():
                if user in obj.students.all():
                    teachers.append(obj.teacher)
            if len(teachers) != 0:
                query = News.objects.filter(teacher__in=teachers)
                return query

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class ExerciseList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            query = Exercise.objects.filter(teacher=user)
            return query
        if user.is_student:
            teachers = list()
            for obj in Lesson.objects.all():
                if user in obj.students.all():
                    teachers.append(obj.teacher)
            if len(teachers) != 0:
                query = Exercise.objects.filter(teacher__in=teachers)
                return query

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class AnswerExerciseView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnswerExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            query = AnswerExercise.objects.filter(exercise__teacher=user)
            return query
        if user.is_student:
            query = AnswerExercise.objects.filter(author=user)
            return query


class ExercisesDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class AnswerExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = AnswerExercise.objects.all()
    serializer_class = AnswerExerciseSerializer


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
