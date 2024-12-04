from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Car, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'email',
            'is_staff',
        )


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'url',
            'id',
            'make',
            'model',
            'year',
            'description',
            'created_at',
            'updated_at',
            'owner',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'url',
            'id',
            'content',
            'created_at',
            'car',
            'author',
        )