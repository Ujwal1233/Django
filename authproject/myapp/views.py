from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate,login

def register(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"]

        # Prevent UNIQUE constraint failure on username
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose another.")

        try:
            User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            return HttpResponse("Username already exists. Please choose another.")

        return redirect('login')

    return render(request, "register.html")

def loginview(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login Successfully.....")

        return HttpResponse("Invalid username or password")

    return render(request, "login.html")
