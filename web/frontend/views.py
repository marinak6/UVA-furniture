from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse

# Create your views here.

from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)

from .forms import CreateListingForm


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


def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if not form.is_valid():
            form_args = {'form': form}
            return render(request, "post_item.html", form_args)
        form_data = form.cleaned_data
        # Need to change this later to auth user
        form_data["seller"] = "1"

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
