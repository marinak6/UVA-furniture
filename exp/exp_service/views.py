from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse
import json
import re
from elasticsearch import Elasticsearch
from kafka import KafkaProducer

# Create your views here.
producer = KafkaProducer(bootstrap_servers='kafka:9092')
producer2 = KafkaProducer(bootstrap_servers='kafka:9092')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form_data = request.POST
        try:
            microservices_url = 'http://microservices:8000/api/v1/login'
            encoded_form_data = urllib.parse.urlencode(
                form_data).encode('utf-8')
            request2 = urllib.request.Request(
                microservices_url, data=encoded_form_data, method='POST')
            json_respsonse = urllib.request.urlopen(
                request2).read().decode('utf-8')
            response = json.loads(json_respsonse)  # redundant?
            return JsonResponse(response)

        except Exception as error:
            return JsonResponse({'error': str(error)})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form_data = request.POST
        try:
            microservices_url = 'http://microservices:8000/api/v1/person/create'
            encoded_form_data = urllib.parse.urlencode(form_data).encode('utf-8')
            request2 = urllib.request.Request(microservices_url, data=encoded_form_data, method='POST')
            json_respsonse = urllib.request.urlopen(request2).read().decode('utf-8')
            response = json.loads(json_respsonse)
            return JsonResponse(response)

        except Exception as error:
            return JsonResponse({'ERROR': str(error)})
    else:
        return JsonResponse({'ERROR': 'GET request sent to POST API'})


@csrf_exempt
def home(request):

    req = urllib.request.Request(
        'http://microservices:8000/api/v1/newest_items')

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)
    

@csrf_exempt
def search(request):
    if request.method == 'POST':
        sort = request.POST.get('sort')
        query = request.POST.get('query')
        query_cleaned = re.sub('[^A-Za-z0-9]+', ' ', query) # removes any Elasticsearch reserved keywords
        try:
            es = Elasticsearch(['es'])
            if sort == 'true':
                response = es.search(index='listing_index', body={"query": {"function_score": {"query": {"query_string": {"query": query_cleaned}},"field_value_factor": {"field": "visits","modifier": "log1p","missing": 0.1}}}})
            else:
                response = es.search(index='listing_index', body={'query': {'simple_query_string': {'query': query_cleaned}}, 'size': 10})
            return JsonResponse({'listings': response['hits']['hits']}) # ['hits']['hits'] is where matches are
        except Exception as error:
            return JsonResponse({'ERROR': str(error)})
    else:
        return JsonResponse({'ERROR': 'Sent GET request to POST api'})


@csrf_exempt
def item(request, item_id):
    try:
        received_json_data = json.loads(request.body.decode("utf-8"))
    except:
        received_json_data = request.POST

    auth = received_json_data["auth"]
    if auth == -1:
        user_id = -1
    else:
        url = 'http://microservices:8000/api/v1/auth_to_id'
        encode_form = urllib.parse.urlencode(
            received_json_data).encode('utf-8')
        new_request = urllib.request.Request(
            url, data=encode_form, method='POST')
        resp_json = urllib.request.urlopen(
            new_request).read().decode('utf-8')
        resp = json.loads(resp_json)
        user_id = resp["user_id"]

    data_for_producer = {"user_id": user_id, "item_id": item_id}
    producer2.send('page-view',
                   json.dumps(data_for_producer).encode('utf-8'))

    req = urllib.request.Request(
        'http://microservices:8000/api/v1/furniture/'+str(item_id))

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return JsonResponse(resp)
    

@csrf_exempt
def item_recommendations(request, item_id):
    if request.method == 'GET':
        try:
            req = urllib.request.Request(
                'http://microservices:8000/api/v1/recommendation/'+str(item_id))
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            
            recommendations = []
            for recomm_id in resp['recommendations']:
                req2 = urllib.request.Request(
                    'http://microservices:8000/api/v1/furniture/'+str(recomm_id))
                resp2_json = urllib.request.urlopen(req2).read().decode('utf-8')
                resp2 = json.loads(resp2_json)
                
                # make sure item actually exists
                if 'Status' not in resp2:
                    recommendations.append(resp2)
                    
            return JsonResponse({'data': recommendations})
        except Exception as error:
            return JsonResponse({'ERROR': str(error)})
    else:
        return JsonResponse({'ERROR': 'POST request sent to a GET API'})
        


@csrf_exempt
def createFurniture(request):
    post_data = request.POST

    url = 'http://microservices:8000/api/v1/furniture/create'
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    producer.send('new-listings-topic', json.dumps(resp).encode('utf-8'))
    return JsonResponse(resp)


@csrf_exempt
def logout(request):
    post_data = request.POST

    url = 'http://microservices:8000/api/v1/logout'
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return JsonResponse(resp)
