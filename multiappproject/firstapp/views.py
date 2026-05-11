from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def view1(request):
    a="this is response from 1st app"
    return HttpResponse(a)