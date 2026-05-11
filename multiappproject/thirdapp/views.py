from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def view3(result):
    c="this is response from thirdapp"
    return HttpResponse(c)