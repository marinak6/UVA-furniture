from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse

# Create your views here.

from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)


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
    # add logic for logging in
    return render(request, 'login.html')
