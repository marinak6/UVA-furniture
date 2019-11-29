from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.urls import reverse
import urllib.request
import urllib.parse
import json

from .forms import (CreateListingForm, CreateRegisterForm)
from datetime import timedelta
import redis


def logged_in_render(request, template, args):
    try:
        auth_user = request.COOKIES.get('authenticator')
    except:
        auth_user = ""

    if auth_user:
        args["logged_in"] = True
    else:
        args["logged_in"] = False

    return render(request, template, args)


def home(request):
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        redis_connected = True
        r.exists("home.html")
    except:
        redis_connected = False

    if redis_connected:
        if r.exists("home.html") == 1:
            return logged_in_render(request, 'home.html', json.loads(r.get("home.html").decode('utf-8')))
        else:
            req = urllib.request.Request('http://exp:8000/api/v1/')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            response_obj = logged_in_render(
                request, 'home.html', {'resp': resp["Res"]})
            dump = json.dumps({'resp': resp["Res"]})
            r.set('home.html', dump)
            r.expire("home.html", timedelta(minutes=5))
            return response_obj
    else:
        req = urllib.request.Request('http://exp:8000/api/v1/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        response_obj = logged_in_render(
            request, 'home.html', {'resp': resp["Res"]})
        return response_obj


def search(request):
    sort = request.GET.get('sort')
    query = request.GET.get('query')
    query_encoded = urllib.parse.urlencode(
        {'query': query, 'sort': sort}).encode('utf-8')
    api_url = 'http://exp:8000/api/v1/search/'
    api_request = urllib.request.Request(
        api_url, data=query_encoded, method='POST')
    response = urllib.request.urlopen(api_request).read()
    response_decoded = json.loads(response.decode('utf-8'))
    results = []
    if 'listings' in response_decoded:
        for listing in response_decoded['listings']:
            # _source is where model fields are stored
            results.append(listing['_source'])
    context = {'query': query, 'results': results}
    if 'ERROR' in response_decoded:
        context['ERROR'] = response_decoded['ERROR']
    if sort == 'true':
        context['sort'] = True
    return logged_in_render(request, 'search.html', context)


def item_details(request, item_id):
    # get item

    auth_user = request.COOKIES.get('authenticator')

    if not auth_user:
        form_data = {"auth": -1}
    else:
        form_data = {"auth": auth_user}

    url = 'http://exp:8000/api/v1/item/'+str(item_id)
    encode_form = urllib.parse.urlencode(form_data).encode('utf-8')
    new_request = urllib.request.Request(
        url, data=encode_form, method='POST')
    resp_json = urllib.request.urlopen(new_request).read().decode('utf-8')
    item = json.loads(resp_json)
    context = {
        'item': item
    }

    # logic of status probably needs to change. We should update status for any existing items also
    if("Status" in context['item']):
        return render(request, 'invalid_access.html')

    return logged_in_render(request, 'item_details.html', context)


def login(request):
    auth_user = request.COOKIES.get('authenticator')
    if auth_user:
        return HttpResponseRedirect(reverse('frontend:index'))
        
    # User submitted the Login form
    if request.method == "POST":
        received_login_data = request.POST
        login_info = {
            "email": received_login_data['email'],
            "password": received_login_data['password']
        }
        try:
            exp_service_url = 'http://exp:8000/api/v1/login'
            encoded_login_data = urllib.parse.urlencode(received_login_data).encode('utf-8')
            request2 = urllib.request.Request(exp_service_url, data=encoded_login_data, method='POST')
            json_respsonse = urllib.request.urlopen(request2).read().decode('utf-8')
            response = json.loads(json_respsonse)
            
            # Something went wrong on the experience service level
            if 'error' in response:
                args = {'error': response['error']}
                return render(request, "login.html", args)
                
            # We can now login the User
            authenticator = response['authenticator']
            
            # Send the User to the page they attempted to access
            if request.GET.get('next'):
                response = redirect(request.GET.get('next'))
            else:
                response = HttpResponseRedirect(reverse('frontend:index'))
                
            # A User's cookie is how we authenticate them
            response.set_cookie('authenticator', authenticator)
            return response
        except Exception as error:
            args = {'error': str(error)}
            return render(request, "login.html", args)
    
    # User clicked link to Login page
    else:
        next_link = reverse("frontend:index")
        if request.GET.get('next'):
            next_link = request.GET.get('next')
        return render(request, 'login.html', {"next_link": next_link})


def logout(request):
    response = HttpResponseRedirect(reverse('frontend:index'))
    authenticator = request.COOKIES.get('authenticator')
    if authenticator:
        try:
            url = 'http://exp:8000/api/v1/logout/'
            form_data = {"authenticator": authenticator}
            encode_form = urllib.parse.urlencode(form_data).encode('utf-8')
            new_request = urllib.request.Request(
                url, data=encode_form, method='POST')
            resp_json = urllib.request.urlopen(
                new_request).read().decode('utf-8')
        except Exception as ex:
            return JsonResponse({"Status": str(ex)})
        # resp = json.loads(resp_json)

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
            return render(request, "create_listing.html", form_args)
        form_data = form.cleaned_data
        # Need to change this later to auth user
        form_data["auth"] = auth_user

        url = 'http://exp:8000/api/v1/furniture/create'
        encode_form = urllib.parse.urlencode(form_data).encode('utf-8')
        new_request = urllib.request.Request(
            url, data=encode_form, method='POST')
        resp_json = urllib.request.urlopen(new_request).read().decode('utf-8')
        resp = json.loads(resp_json)
        if "Status" in resp:
            return HttpResponseRedirect(reverse("frontend:login") + "?next=" + reverse("frontend:create_listing"))
        new_furniture_id = resp["id"]

        return redirect('/item/'+str(new_furniture_id))
    else:
        form = CreateListingForm()
        form_args = {'form': form}
        # need to change to auth_render
        return logged_in_render(request, "create_listing.html", form_args)


def register(request):
    if request.method == 'POST':
        form = CreateRegisterForm(request.POST)
        if form.is_valid():
            valid_data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password']
            }
            try:
                exp_service_url = 'http://exp:8000/api/v1/register'
                encoded_valid_data = urllib.parse.urlencode(valid_data).encode('utf-8')
                request2 = urllib.request.Request(exp_service_url, data=encoded_valid_data, method='POST')
                json_respsonse = urllib.request.urlopen(request2).read().decode('utf-8')
                response = json.loads(json_respsonse)
                if 'ERROR' in response:
                    args = {'form': form, 'ERROR': response['ERROR']}
                    return render(request, 'register.html', args)
                    
                # Register was successful
                return HttpResponseRedirect('login')
            except Exception as error:
                args = {'form': form, 'ERROR': str(error)}
                return render(request, 'register.html', args)
    else:
        form = CreateRegisterForm()
        
    # Catches invalid forms and GET requests
    return render(request, 'register.html', {'form': form})
