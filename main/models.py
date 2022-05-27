from typing import Callable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import BooleanField, DateTimeField, DecimalField, FloatField, TextField
from django.db.models.fields.related import ForeignKey

# Create your models here.


class User(AbstractUser):
    country = TextField()
    date = DateTimeField()
    pass


class Quote(models.Model):
    user = ForeignKey(User, on_delete=CASCADE)
    date = DateTimeField()
    best_time = FloatField()
    quote = TextField()
    auther = TextField(max_length=64)
    title = TextField(max_length=64)

class Like(models.Model):
    user = ForeignKey(User, on_delete=CASCADE)
    quote = ForeignKey(Quote, on_delete=CASCADE)
    type = BooleanField() ## True = like False = dislike

class Records(models.Model):
    user = ForeignKey(User, on_delete=CASCADE)
    quote = ForeignKey(Quote,on_delete=CASCADE)
    country = TextField()
    best_time = DecimalField(max_digits=5, decimal_places=2)
    date = DateTimeField()
