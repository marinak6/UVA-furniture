from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bid, Furniture, Person, Category, Authenticator
from django.forms.models import model_to_dict
import json
import urllib.request
import urllib.parse

# Authentication
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import os
import hmac


@csrf_exempt
def check_login(request):
    if request.method == 'POST':
        form_data = request.POST

        try:
            email = form_data['email']
            password = form_data['password']
            if Person.objects.filter(email=email).count() == 1:
                person = Person.objects.get(email=email)
                if check_password(password, person.password):
                    authenticator = hmac.new(
                        key=settings.SECRET_KEY.encode('utf-8'),
                        msg=os.urandom(32),
                        digestmod='sha256',
                    ).hexdigest()

                    my_auth = Authenticator.objects.create(
                        person_id=person,
                        authenticator=authenticator,
                    )
                    my_auth.save()

                    return JsonResponse({'authenticator': my_auth.authenticator})
                else:
                    return JsonResponse({'error': 'password is wrong'})
            else:
                return JsonResponse({'error': 'email is wrong'})
        except Exception as error:
            return JsonResponse({"Microservices Login Error Message": str(error)})


@csrf_exempt
def create_person(request):
    if request.method == 'POST':
        try:
            form_data = json.loads(request.body.decode("utf-8"))
        except:
            form_data = request.POST

        try:
            first_name = form_data['first_name']
            last_name = form_data['last_name']
            password = form_data['password']
            email = form_data['email']

            # make sure email isn't already used
            if Person.objects.filter(email=email).count() == 1:
                raise Exception("Email already taken.")

            person = Person.objects.create(
                first_name=first_name,
                last_name=last_name,
                password=make_password(password),  # hashes the password
                email=email,
            )
            person.save()

            # generate authenticator token
            authenticator = hmac.new(
                key=settings.SECRET_KEY.encode('utf-8'),
                msg=os.urandom(32),
                digestmod='sha256',
            ).hexdigest()

            # save token in Authenticator model
            my_auth = Authenticator.objects.create(
                person_id=person,
                authenticator=authenticator,
            )
            my_auth.save()

            # return person object
            person_dict = model_to_dict(person)
            person_dict.pop('password')
            return JsonResponse(person_dict)
        except Exception as error:
            return JsonResponse({"Microservices Register Error Message": str(error)})


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
            try:
                received_json_data = json.loads(request.body.decode("utf-8"))
            except:
                received_json_data = request.POST
            name = received_json_data["name"]
            if "seller" in received_json_data:
                seller_id = received_json_data['seller']
            elif "auth" in received_json_data:
                try:
                    auth_obj = Authenticator.objects.get(
                        authenticator=received_json_data["auth"])
                except:
                    return JsonResponse({"Status": "Invalid Cookie"})
                seller_id = auth_obj.person_id.id
            else:
                raise Exception("Need a seller or auth")
            category_names = received_json_data['category'].split(",")
            description = received_json_data["description"]
            price = received_json_data["price"]

            seller = Person.objects.get(id=seller_id)
            if not seller:
                return JsonResponse({"Status": "Seller is Invalid"})

            if type(category_names) != list:
                category_names = [category_names]
            obj = Furniture.objects.create(
                name=name,
                current_bid_id=None,
                seller=seller,
                is_bought=False,
                buyer=None,
                description=description,
                price=price,
            )
            for category_name in category_names:
                try:
                    category = Category.objects.get(
                        category=category_name.lower())
                    obj.category.add(category)
                except:
                    new_category = Category.objects.create(
                        category=category_name.lower())
                    new_category.save()
                    obj.category.add(new_category)
            obj.save()

            return_dict = {
                "name": name,
                "current_bid_id": "",
                "seller_id": seller_id,
                "is_bought": False,
                "category": category_names,
                "buyer_id": "",
                "price": price,
                "description": description,
                "id": obj.pk
            }

            return JsonResponse(return_dict)
        except Exception as e:
            return JsonResponse({"Status": str(e)})
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
    except Exception as ex:
        return JsonResponse({"Status": str(ex)})


@csrf_exempt
def delete_furniture(request, id):
    try:
        obj = Furniture.objects.get(pk=id)
        obj.delete()
        return JsonResponse({"Status": "Deleted"})
    except:
        return JsonResponse({"Status": "Furniture with that ID does not exist"})


@csrf_exempt
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


@csrf_exempt
def get_items(request):
    furnitures = Furniture.objects
    res = []
    for furniture in furnitures:
        req = urllib.request.Request(
            'http://microservices:8000/api/v1/furniture/'+str(furniture.pk))
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        res.append(resp)

    return JsonResponse({"Res": res})


@csrf_exempt
def logout(request):
    received_json_data = request.POST
    try:
        auth_obj = Authenticator.objects.get(
            authenticator=received_json_data["authenticator"])
        auth_obj.delete()
    except Exception as ex:
        return JsonResponse({"Status": str(ex)})

    return JsonResponse({"Status": "Deleted"})
