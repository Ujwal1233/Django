from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def view2(result):
    b="this is response from second app"
    return HttpResponse(b)