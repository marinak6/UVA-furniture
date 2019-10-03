from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bid, Furniture, Person, Category
from django.forms.models import model_to_dict
import json
from django.contrib.auth.models import User
import urllib.request
import urllib.parse
import json


@csrf_exempt
def createBid(request):

    if request.method == 'POST':
        form_data = request.POST  # Postman: request.body -> "form-data"
        try:
            new_bid = Bid(
                bidder=None,
                price=0.0,
                item_id=None,
                status='PENDING'
            )
            if form_data and form_data['price']:
                # TODO: doesn't convert to float in Postman tests
                new_bid.price = float(form_data['price'])

            if form_data and form_data['bidder']:
                # Person exists
                if Person.objects.filter(pk=form_data['bidder']).count() == 1:
                    new_bid.bidder = Person.objects.get(
                        pk=int(form_data['bidder']))

            if form_data and form_data['item_id']:
                # Furniture exists
                if Furniture.objects.filter(pk=form_data['item_id']).count() == 1:
                    new_bid.item_id = Furniture.objects.get(
                        pk=int(form_data['item_id']))

            new_bid.save()  # you must save() before getting
            database_object = get_object_or_404(Bid, pk=new_bid.pk)
            return JsonResponse(model_to_dict(database_object))

        except Exception as error:
            return JsonResponse({"Worked": False, "Error": str(error), "request.POST": str(form_data)})
    else:
        return JsonResponse({"Worked": False, "Error": "GET request sent to a POST API"})


@csrf_exempt
def bid(request, id):

    if request.method == "POST":  # UPDATES Bid data
        form_data = request.POST  # Postman: request.body -> "form-data"
        try:
            bid = get_object_or_404(Bid, pk=id)
            if form_data and form_data['price']:  # user can only set price
                bid.price = form_data['price']

            bid.save()  # you must save() before getting
            database_object = get_object_or_404(Bid, pk=bid.pk)
            return JsonResponse(model_to_dict(database_object))

        except Exception as error:
            return JsonResponse({"Worked": False, "Error": str(error), "request.POST": str(form_data)})
    else:  # GETS Bid data
        try:
            bid = get_object_or_404(Bid, pk=id)
            return JsonResponse(model_to_dict(bid))
        except Exception as error:
            return JsonResponse({"Worked": False, "Error": str(error)})


@csrf_exempt
def deleteBid(request, id):

    if request.method == "POST":
        try:
            Bid.objects.get(pk=id).delete()  # deletes immedietely
            return JsonResponse({"Status": "Bid: " + str(id) + "Deleted"})

        except Exception as error:
            return JsonResponse({"Worked": False, "Error": str(error)})
    else:
        return JsonResponse({"Worked": False, "Error": "GET request sent to a POST API"})


@csrf_exempt
def updateBid(request, id):

    if request.method == "POST":  # UPDATES Bid data
        form_data = request.POST  # Postman: request.body -> "form-data"
        try:
            bid = get_object_or_404(Bid, pk=id)
            if form_data and form_data['price']:  # user can only set price
                bid.price = form_data['price']

            bid.save()  # you must save() before getting
            database_object = get_object_or_404(Bid, pk=bid.pk)
            return JsonResponse(model_to_dict(database_object))

        except Exception as error:
            return JsonResponse({"Worked": False, "Error": str(error), "request.POST": str(form_data)})
    else:
        return JsonResponse({"Worked": False, "Error": "GET request sent to a POST API"})


@csrf_exempt
def createFurniture(request):

    if request.method == "POST":
        try:
            received_json_data = json.loads(request.body.decode("utf-8"))
            name = received_json_data["name"]
            seller_id = received_json_data['seller']
            is_bought = received_json_data['is_bought']
            category_names = received_json_data['category']
            description = received_json_data["description"]
            price = received_json_data["price"]

            seller = Person.objects.get(id=seller_id)
            if not seller:
                return JsonResponse({"Status": "Seller is Invalid"})
            if not (is_bought == "True" or is_bought == "False"):
                return JsonResponse({"Status": "is_bought is Invalid"})

            if type(category_names) != list:
                return JsonResponse({"Status": "Category needs to be in a list"})
            obj = Furniture.objects.create(
                name=name,
                current_bid_id=None,
                seller=seller,
                is_bought=is_bought,
                buyer=None,
                description=description,
                price=price,
            )
            for category_name in category_names:
                category = Category.objects.get(category=category_name)
                obj.category.add(category)

            obj.save()

            return_dict = {
                "name": name,
                "current_bid_id": "",
                "seller_id": seller_id,
                "is_bought": False,
                "category": category_names,
                "buyer_id": "",
                "price": price,
                "description": description
            }
            return JsonResponse(return_dict)
        except:
            return JsonResponse({"Status": "Invalid ID"})
    else:
        return JsonResponse({"Status": "Something went wrong"})


@csrf_exempt
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
                "id": id,
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
            return JsonResponse({"Status": "Invalid furniture ID"})


@csrf_exempt
def update_furniture(request, id):
    try:
        obj = Furniture.objects.get(pk=id)
        received_json_data = json.loads(request.body.decode("utf-8"))
        for key in received_json_data:
            if key == "current_bid_id":
                value = Bid.objects.get(id=received_json_data[key])
                setattr(obj, key, value)

            elif key == "seller":
                value = Person.objects.get(id=received_json_data[key])
                setattr(obj, key, value)

            elif key == "category":
                if type(received_json_data["category"]) != list:
                    return JsonResponse({"Status": "Category needs to be in a list"})
                value = []
                obj.category.clear()
                for item in received_json_data["category"]:
                    category = Category.objects.get(category=item)
                    obj.category.add(category)
            elif key == "buyer":
                value = Person.objects.get(id=received_json_data[key])
                setattr(obj, key, value)
            else:
                value = received_json_data[key]
                setattr(obj, key, value)
        obj.save()
        return JsonResponse({"Status": "Furniture has been updated"})
    except:
        return JsonResponse({"Status": "Invalid ID"})


@csrf_exempt
def delete_furniture(request, id):
    try:
        obj = Furniture.objects.get(pk=id)
        obj.delete()
        return JsonResponse({"Status": "Deleted"})
    except:
        return JsonResponse({"Status": "Furniture with that ID does not exist"})


def newest_items(request):

    furnitures = Furniture.objects.order_by('-timestamp')[:3]
    res = []
    for furniture in furnitures:

        req = urllib.request.Request(
            'http://microservices:8000/api/v1/furniture/'+str(furniture.pk))

        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        res.append(resp)

    return JsonResponse({"Res": res})
