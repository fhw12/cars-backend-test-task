from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Car, Comment
from .serializers import CarSerializer, UserSerializer, CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


def indexView(request):
    template = loader.get_template('cars/index.html')
    context = { 'cars': Car.objects.all() }
    return HttpResponse(
        template.render(context, request)
    )

def carView(request, car_id):
    try:
        car = Car.objects.get(pk=car_id)
    except:
        pass
    template = loader.get_template('cars/car.html')
    context = { 'car': car }
    return HttpResponse(
        template.render(context, request)
    )