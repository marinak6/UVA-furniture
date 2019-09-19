from django.shortcuts import render
from django.http import JsonResponse

def createBid(request):
    return JsonResponse({'Hello': 'World'})
