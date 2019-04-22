from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
# Create your views here.

def index(request):
    return render(request, "food/home.html")
