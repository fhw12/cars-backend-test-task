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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class Disable(BasePermission):
    def has_object_permission(self, request, view, obj):
        return False


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


# index view (car list)
def index_view(request):
    template = loader.get_template('cars/index.html')
    context = { 'cars': Car.objects.all() }
    return HttpResponse(template.render(context, request))


# login action
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request=request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Log in: error')


# sign up action
def reg_view(request):
    username = request.POST['username']
    password = request.POST['password']
    repeated_password = request.POST['repeated_password']

    if not match(r'[a-zA-Z0-9]{4,16}', username):
        return HttpResponse('Error username')
    elif not match(r'.{8,}', password) or password != repeated_password:
        return HttpResponse('Error password')
    
    User.objects.create_user(username, '', password)
  
    user = authenticate(request=request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Log in: error')


# adds comment
@login_required
def add_comment(request, car_id):
    content = request.POST['content']
    car = Car.objects.get(pk=car_id)
    comment = Comment.objects.create(car=car, created_at=datetime.datetime.now(), content=content, author=request.user)
    return HttpResponse('done')


# adds a new car to database from the new car form
@login_required
def add_car(request):
    make = request.POST['make']
    model = request.POST['model']
    year = request.POST['year']
    description = request.POST['description']

    car = Car.objects.create(make=make, model=model, year=year, description=description, created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(), owner=request.user,
    )
    return HttpResponse('done')

@login_required
def delete_car(request, car_id):
    car = Car.objects.get(pk=car_id)

    if car is None:
        return HttpResponse('error: car is none')

    if car.owner != request.user:
        return HttpResponse('error: you are not the owner of publication of this car')

    car.delete()

    return redirect(f'/')


# update the car
@login_required
def edit_car(request, car_id):
    make = request.POST['make']
    model = request.POST['model']
    year = request.POST['year']
    description = request.POST['description']
    
    car = Car.objects.get(pk=car_id)

    if car is None:
        return HttpResponse('error: car is none')
    
    if car.owner != request.user:
        return HttpResponse('error: you are not the owner of publication of this car')

    car.make = make
    car.model = model
    car.year = year
    car.description = description
    car.save()

    return redirect(f'/car/{car_id}')


# new car form
@login_required
def new_car(request):
    template = loader.get_template('cars/new_car.html')
    context = {}
    return HttpResponse(template.render(context, request))


# sign in view
def signin_view(request):
    template = loader.get_template('cars/signin.html')
    context = {}
    return HttpResponse(template.render(context, request))


# sign up view
def signup_view(request):
    template = loader.get_template('cars/signup.html')
    context = {}
    return HttpResponse(template.render(context, request))


# logout action
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


# car view
def car_view(request, car_id):
    car = Car.objects.get(pk=car_id)
    comments = Comment.objects.filter(car=car.id)
    template = loader.get_template('cars/car.html')
    context = { 'car': car, 'comments': comments }
    return HttpResponse(template.render(context, request))