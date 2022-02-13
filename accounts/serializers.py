from rest_framework import serializers

from .models import User
from exercise.models import Lesson


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "password", "national_code", "school_name", "lesson_name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_teacher = True
        user.save()
        lesson = Lesson.objects.create(title=user.lesson_name, teacher=user)
        lesson.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username
        )
        instance.password = validated_data.get(
            'password', instance.password
        )
        instance.username = validated_data.get(
            'first_name', instance.first_name
        )
        instance.password = validated_data.get(
            'last_name', instance.last_name
        )

        instance.save()
        return instance


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "password", "national_code")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_teacher = True
        user.save()
        lesson = Lesson.objects.create(title=user.lesson_name, teacher=user)
        lesson.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username
        )
        instance.password = validated_data.get(
            'password', instance.password
        )
        instance.username = validated_data.get(
            'first_name', instance.first_name
        )
        instance.password = validated_data.get(
            'last_name', instance.last_name
        )

        instance.save()
        return instance
