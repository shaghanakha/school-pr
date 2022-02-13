from django.shortcuts import render
from .serializers import TeacherSerializer

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.username}!'},
            status=status.HTTP_204_NO_CONTENT
        )


class TeacherRegistration(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TeacherSerializer

    def perform_create(self, serializer):
        serializer.save()
