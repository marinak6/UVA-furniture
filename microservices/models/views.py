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

    if request.method == "POST":
        try:
            received_json_data = json.loads(request.body.decode("utf-8"))
            name = received_json_data["name"]
            seller_id = received_json_data['seller']
            is_bought = received_json_data['is_bought']
            category_name = received_json_data['category']
            description = received_json_data["description"]
            price = received_json_data["price"]

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
        except:
            return JsonResponse({"Status": "Something went wrong"})
    else:
        return JsonResponse({"Status": "Something went wrong"})


def furniture(request, id):

    if request.method == "GET":
        try:
            furniture = Furniture.objects.get(id=id)
            obj_dict = model_to_dict(furniture)
            name = obj_dict["name"]
            if obj_dict["current_bid_id"]:
                current_bid_id = obj_dict["current_bid_id"]
            else:
                current_bid_id = ""

            category = []
            for item in obj_dict["category"]:
                category.append(item.category)
            return_dict = {
                "name": name,
                "current_bid_id": current_bid_id,
                "seller_id": obj_dict["seller"],
                "is_bought": obj_dict["is_bought"],
                "category": category,
                "buyer_id": obj_dict["buyer"],
                "timestamp": obj_dict["timestamp"],
                "price": obj_dict["price"],
                "description": obj_dict["description"],
            }
            return JsonResponse(return_dict)
        except:
            return JsonResponse({"Status": "Something went wrong"})
