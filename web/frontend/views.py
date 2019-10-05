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
