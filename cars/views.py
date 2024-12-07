from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Car, Comment
from .serializers import CarSerializer, UserSerializer, CommentSerializer
from re import match
import datetime

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView


"""
Permissions helpers
"""
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class Disable(BasePermission):
    def has_object_permission(self, request, view, obj):
        return False


"""
ViewSets
"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [Disable()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        car_id = self.kwargs.get('car_id')
        car = Car.objects.get(pk=car_id)
        serializer.save(car=car, author=self.request.user)

    def get_queryset(self):
        car_id = self.kwargs.get('car_id')
        return self.queryset.filter(car=car_id)


"""
Views
"""
# Index page (List of cars)
def index_view(request):
    template = loader.get_template('cars/index.html')
    context = { 'cars': Car.objects.all() }
    return HttpResponse(template.render(context, request))


# NewCar view (form)
@login_required
def new_car(request):
    template = loader.get_template('cars/new_car.html')
    context = {}
    return HttpResponse(template.render(context, request))


# SignIn view (form)
def signin_view(request):
    template = loader.get_template('cars/signin.html')
    context = {}
    return HttpResponse(template.render(context, request))


# SignUp view (form)
def signup_view(request):
    template = loader.get_template('cars/signup.html')
    context = {}
    return HttpResponse(template.render(context, request))


# Car viewer (Card of the car)
def car_view(request, car_id):
    car = Car.objects.get(pk=car_id)
    comments = Comment.objects.filter(car=car.id)
    template = loader.get_template('cars/car.html')
    context = { 'car': car, 'comments': comments }
    return HttpResponse(template.render(context, request))


"""
Handlers
"""
# Login handler
def login_handler(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request=request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Log in: error')


# Registration handler
def reg_handler(request):
    username = request.POST['username']
    password = request.POST['password']
    repeated_password = request.POST['repeated_password']

    if not match(r'[a-zA-Z0-9]{4,16}', username):
        return HttpResponse('Логин не соответствует шаблону! Допустимые символы: Латиница, Цифры. Длина от 4 до 16 символов.')
    elif password != repeated_password:
        return HttpResponse("Пароль и повторный пароль не совпадают!")
    elif not match(r'.{8,}', password):
        return HttpResponse('Пароль не соответствует шаблону! Длина пароля должна быть от 8 символов.')

    try:
        User.objects.get(username=username)
        return HttpResponse('Пользователь уже существует!')
    except User.DoesNotExist:
        User.objects.create_user(username, '', password)
        user = authenticate(request=request, username=username, password=password)
        login(request, user)
        return redirect('/')


# AddComment handler
@login_required
def add_comment_handler(request, car_id):
    content = request.POST['content']
    car = Car.objects.get(pk=car_id)
    comment = Comment.objects.create(car=car, created_at=datetime.datetime.now(), content=content, author=request.user)
    return redirect(f'/car/{car_id}')


# AddCar handler
@login_required
def add_car_handler(request):
    make = request.POST['make']
    model = request.POST['model']
    year = request.POST['year']
    description = request.POST['description']
    car = Car.objects.create(make=make, model=model, year=year, description=description, created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(), owner=request.user,
    )
    return redirect('/')


# DeleteCar handler
@login_required
def delete_car_handler(request, car_id):
    car = Car.objects.get(pk=car_id)
    if car is None:
        return HttpResponse('Ошибка: Данной публикации об автомобиле не существует')
    if car.owner != request.user:
        return HttpResponse('Ошибка: Вы не можете удалить публикацию, т.к не являетесь её автором.')
    car.delete()
    return redirect(f'/')


# UpdateCar handler
@login_required
def update_car_handler(request, car_id):
    make = request.POST['make']
    model = request.POST['model']
    year = request.POST['year']
    description = request.POST['description']
    car = Car.objects.get(pk=car_id)
    if car is None:
            return HttpResponse('Ошибка: Данной публикации об автомобиле не существует')
    if car.owner != request.user:
        return HttpResponse('Ошибка: Вы не можете удалить публикацию, т.к не являетесь её автором.')
    car.make = make
    car.model = model
    car.year = year
    car.description = description
    car.save()
    return redirect(f'/car/{car_id}')


# Logout handler
@login_required
def logout_handler(request):
    logout(request)
    return redirect('/')