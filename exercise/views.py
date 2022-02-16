from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from accounts.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .permissions import *


class NewsListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, AddPer)
    serializer_class = NewsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return News.objects.all()
        elif user.is_teacher:
            query = News.objects.filter(teacher=user)
            return query

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class NewsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, CheckPer)
    serializer_class = NewsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            a = user.has_teacher()
            if a[1]:
                query = News.objects.filter(teacher__in=a[0])
                return query


class ExerciseListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, AddPer)
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Exercise.objects.all()
        elif user.is_teacher:
            query = Exercise.objects.filter(teacher=user)
            return query

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class ExerciseList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, CheckPer)
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            a = user.has_teacher()
            if a[1]:
                query = Exercise.objects.filter(teacher__in=a[0])
                return query


class Answers(generics.ListAPIView):
    permission_classes = (IsAuthenticated, CheckPer)
    serializer_class = AnswerExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AnswerExercise.objects.all()
        if user.is_student:
            return AnswerExercise.objects.filter(author=user)
        if user.is_teacher:
            return AnswerExercise.objects.filter(exercise__teacher=user)


class AnswerToExercise(APIView):
    permission_classes = (IsAuthenticated, CheckPer)
    serializer_class = AnswerExerciseSerializer

    def get(self, request, e_id):
        if AnswerExercise.objects.filter(exercise__id=e_id, author=request.user).exists():
            return HttpResponseRedirect(reverse('answers_list'))
        else:
            exe = get_object_or_404(Exercise, id=e_id)
            return Response({"answer to": str(exe)})

    def post(self, request, e_id):
        answer_serializer = AnswerSerializer(data=request.data)
        if answer_serializer.is_valid():
            exe = get_object_or_404(Exercise, id=e_id)
            if AnswerExercise.objects.filter(exercise=exe, author=request.user):
                return Response({'message': 'you already answered'})
            if timezone.now() > exe.deadline:
                return Response({'message': 'Deadline is expired!'})
            if exe.teacher not in request.user.has_teacher()[0]:
                return Response({'message': 'you are not in teacher list!'})
            Answer = AnswerExercise.objects.create(exercise=exe, author=request.user)
            Answer.body = answer_serializer.data['body']
            Answer.file = answer_serializer.data['file']
            Answer.save()
            return Response({'message': 'Done!'})
        return Response({'message': answer_serializer.errors})


class ExercisesDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CheckPer)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class AnswerExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, StudentEditPer)
    queryset = AnswerExercise.objects.all()
    serializer_class = AnswerExerciseSerializer


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CheckPer)
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AddPer)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
