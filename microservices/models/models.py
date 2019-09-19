from django.db.models import CharField, Model
from enum import Enum
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Furniture(models.Model):
    name = models.CharField(max_length=128)
    current_bid_id = models.OneToOneField(Bid)
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    is_bought = models.BooleanField(default=False)
    category = models.ManyToManyField(Category)

    buyer = models.ForeignKey(
        User
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField()

    def __str__(self):
        return self.name


# Create your models here.


class Bid(models.Model):
    # a bidder can have many bids but a bid has only one bidder
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    # Will create timestamp when the object is created
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_id = models.OneToOneField(Furniture)
    status = models.CharField(max_lendth=20, choices=StatusChoices.choices())


class StatusChoices(Enum):
    Accepted = "ACCEPTED"
    Pending = "PENDING"
    Rejected = "REJECTED"
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
