from django.db.models import Model
from enum import Enum
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.

class Authenticator(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    authenticator = models.CharField(max_length=64, primary_key=True)
    date_created = models.DateField(auto_now=True)
    

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.TextField(null=True) # default value, but still form required


class StatusChoices(Enum):
    Accepted = "ACCEPTED"
    Pending = "PENDING"
    Rejected = "REJECTED"
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Bid(models.Model):
    # a bidder can have many bids but a bid has only one bidder
    bidder = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True)
    # Will create timestamp when the object is created
    timestamp = models.DateTimeField(default=datetime.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_id = models.OneToOneField(
        'Furniture', on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices())


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Furniture(models.Model):
    name = models.CharField(max_length=128)
    current_bid_id = models.OneToOneField(
        Bid, on_delete=models.CASCADE, null=True, blank=True,)
    seller = models.ForeignKey(
        Person,
        related_name='seller',
        on_delete=models.CASCADE,
    )
    is_bought = models.BooleanField(default=False)
    category = models.ManyToManyField(Category)

    buyer = models.ForeignKey(
        Person, related_name='buyer', on_delete=models.PROTECT, null=True, blank=True,)
    timestamp = models.DateTimeField(default=datetime.now)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField()

    def __str__(self):
        return self.name
