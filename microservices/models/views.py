from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bid, Furniture, Person, Category
from django.forms.models import model_to_dict
import json
from django.contrib.auth.models import User


@csrf_exempt
def createBid(request):
    received_json_data = json.loads(request.body.decode("utf-8"))


@csrf_exempt
def createFurniture(request):

    # if request.method == "POST":
    received_json_data = json.loads(request.body.decode("utf-8"))

    name = received_json_data["name"]
    # bid_id = received_json_data['current_bid_id']
    seller_id = received_json_data['seller']
    is_bought = received_json_data['is_bought']
    category_name = received_json_data['category']
    # buyer = received_json_data["buyer"]
    description = received_json_data["description"]
    price = received_json_data["price"]

    # current_bid_id = Bid.objects.get(id=bid_id)
    seller = Person.objects.get(id=seller_id)
    category = Category.objects.get(category=category_name)

    obj = Furniture.objects.create(
        name=name,
        current_bid_id=None,
        seller=seller,
        is_bought=is_bought,
        buyer=None,
        description=description,
        price=price,
    )
    obj.category.add(category)
    obj.save()
    obj_dict = model_to_dict(obj)
    return JsonResponse({"Status": "Sucess"})
