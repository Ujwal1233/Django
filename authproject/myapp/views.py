from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.
def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        User.objects.create_user(username=username,email=email,password=password)
        return HttpResponse("Registered Successfully")
    return render(request,'register.html')