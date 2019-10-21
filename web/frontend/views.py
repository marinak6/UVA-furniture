from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

from django.shortcuts import (
    get_object_or_404, redirect, render, render_to_response)

from .forms import (CreateListingForm, CreateRegisterForm)


def logged_in():
    try:
        auth_user = request.COOKIES.get('authenticator')
    except:
        auth_user = ""

    if auth_user:
        return True
    else:
        return False


def home(request):
    req = urllib.request.Request('http://exp:8000/api/v1/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if logged_in:
        resp["logged_in"] = True
    else:
        resp["logged_in"] = False
    return render(request, 'home.html', {'resp': resp["Res"]})


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
        try:
            exp_service_url = 'http://exp:8000/api/v1/login'
            encoded_login_data = urllib.parse.urlencode(
                received_login_data).encode('utf-8')
            request2 = urllib.request.Request(
                exp_service_url, data=encoded_login_data, method='POST')
            json_respsonse = urllib.request.urlopen(
                request2).read().decode('utf-8')
            response = json.loads(json_respsonse)

            # we can now log them in
            authenticator = response['authenticator']
            if request.GET.get('next'):
                response = redirect(request.GET.get('next'))
            else:
                response = HttpResponseRedirect(reverse('frontend:index'))
            response.set_cookie('authenticator', authenticator)
            return response
        except Exception as error:
            args = {'error': str(error)}
            return render(request, "login.html", args)
    else:
        if request.GET.get('next'):
            next_link = request.GET.get('next')
        else:
            next_link = reverse(home)
        return render(request, 'login.html', {"next_link": next_link})


def logout(request):
    response = HttpResponseRedirect(reverse('frontend:index'))
    response.delete_cookie('authenticator')
    return response


def create_listing(request):
    auth_user = request.COOKIES.get('authenticator')
    if not auth_user:
        return HttpResponseRedirect(reverse("frontend:login") + "?next=" + reverse("frontend:create_listing"))
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if not form.is_valid():
            form_args = {'form': form}
            return render(request, "post_item.html", form_args)
        form_data = form.cleaned_data
        # Need to change this later to auth user
        form_data["auth"] = auth_user

        url = 'http://exp:8000/api/v1/furniture/create'
        encode_form = urllib.parse.urlencode(form_data).encode('utf-8')
        new_request = urllib.request.Request(
            url, data=encode_form, method='POST')
        resp_json = urllib.request.urlopen(new_request).read().decode('utf-8')
        resp = json.loads(resp_json)
        new_furniture_id = resp["id"]

        return redirect('/item/'+str(new_furniture_id))
    else:
        form = CreateListingForm()
        form_args = {'form': form}
        # need to change to auth_render
        return render(request, "create_listing.html", form_args)


def register(request):
    if request.method == 'POST':
        register_data = request.POST
        try:
            exp_service_url = 'http://exp:8000/api/v1/register'
            encoded_register_data = urllib.parse.urlencode(
                register_data).encode('utf-8')
            request2 = urllib.request.Request(
                exp_service_url, data=encoded_register_data, method='POST')
            json_respsonse = urllib.request.urlopen(
                request2).read().decode('utf-8')
            response = json.loads(json_respsonse)
            return HttpResponseRedirect('login')
        except Exception as error:
            form = CreateRegisterForm()
            args = {'form': form, 'error': str(error)}
            return render(request, "register.html", args)
    else:
        form = CreateRegisterForm()
        args = {'form': form}
        return render(request, "register.html", args)
