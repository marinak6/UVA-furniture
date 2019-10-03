from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
# Create your views here.


@csrf_exempt
def home(request):

    req = urllib.request.Request(
        'http://microservices:8000/api/v1/newest_items')

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)
