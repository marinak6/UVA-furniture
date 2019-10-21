from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse

# Create your views here.

from django.shortcuts import (
    get_object_or_404, redirect, render, render_to_response)

from .forms import (CreateListingForm, CreateRegisterForm)


def home(request):
    req = urllib.request.Request('http://exp:8000/api/v1/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    # return JsonResponse(resp)
    return render(request, 'home.html', {'resp': resp["Res"]})
    # return render(request, 'home.html')


def item_details(request, item_id):
    # get item
    req = urllib.request.Request('http://exp:8000/api/v1/item/'+str(item_id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    item = json.loads(resp_json)
    context = {
        'item': item
    }
    # logic of status probably needs to change. We should update status for any existing items also
    if("Status" in context['item']):
        return render(request, 'invalid_access.html')
    return render(request, 'item_details.html', context)


def login(request):
    if(request.method == "POST"):
        received_login_data = request.POST
        login_info = {
            "email": received_login_data['email'],
            "password": received_login_data['password']
        }
    # call login experience service that would check username/password
        return JsonResponse(login_info)
    else:
        return render(request, 'login.html')


def create_listing(request):
    if request.method == "POST":
        received_json_data = request.POST
        listing = {
            "name": received_json_data["name"],
            "category_names": received_json_data['categories'].split(","),
            "description": received_json_data["description"],
            "price": received_json_data["price"]
        }
        return JsonResponse(listing)
    else:
        form = CreateListingForm()
        args = {'form': form}
        # need to change to auth_render
        return render(request, "create_listing.html", args)


def register(request):
    if request.method == 'POST':
        register_data = request.POST
        register_info = {
            "first_name": register_data["first_name"],
            "last_name": register_data["last_name"],
            "email": register_data["email"],
            "password": register_data["password"],
        }
        # authenticate user

        return JsonResponse(register_info)  # need to remove later
    else:
        form = CreateRegisterForm()
        args = {'form': form}
        return render(request, "register.html", args)
