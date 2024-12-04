from django.db import models
from django.contrib.auth.models import Group, User


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(default=2024)
    description = models.CharField(max_length=1000)
    created_at = models.DateField()
    updated_at = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.PROTECT)


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    created_at = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)