from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Lesson, Exercise


class AddPer(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_teacher or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.teacher or request.user.is_staff)


class CheckPer(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_student:
            return request.user.has_teacher()[1]
        elif request.user.is_teacher or request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user == obj.teacher or request.user.is_staff)


class StudentEditPer(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user == obj.author or request.user == obj.exercise.teacher or request.user.is_staff:
                return True
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            if request.user == obj.author and obj.access():
                return True
            if request.user == obj.exercise.teacher or request.user.is_staff:
                return True



