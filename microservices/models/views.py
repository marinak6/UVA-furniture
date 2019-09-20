from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bid, Furniture
from django.forms.models import model_to_dict
import json


@csrf_exempt
def createBid(request):
    return JsonResponse({'Hello': 'World'})


@csrf_exempt
def createFurniture(request):
    # if request.method == "POST":

    name = request.POST.get('name')
    current_bid_id = request.POST.get('current_bid_id')
    seller = request.POST.get('seller')
    is_bought = request.POST.get('is_bought')
    category = request.POST.get('category')
    buyer = request.POST.get("buyer")
    timestamp = request.POST.get("timestamp")
    description = request.POST.get("description")

    obj = Furniture.objects.create(
        name=name,
        current_bid_id=current_bid_id,
        seller=seller,
        is_bought=is_bought,
        buyer=buyer,
        timestamp=timestamp,
        description=description,
    )
    obj.category.add(category)
    obj.save()
    obj_dict = model_to_dict(obj)
    return JsonResponse(obj_dict)
