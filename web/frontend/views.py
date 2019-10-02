from django.shortcuts import render

# Create your views here.

from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)


def home(request):
    return render(request, 'home.html')
