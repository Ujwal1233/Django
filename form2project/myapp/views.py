from django.shortcuts import render
from .forms import *
# Create your views here.
def formview(request):
    f=StudentForm()
    if request.method=="POST":
        f=StudentForm(request.POST)
        if f.is_valid():
            name=f.cleaned_data['name']
            age=f.cleaned_data['age']
            place=f.cleaned_data['place']
            email=f.cleaned_data['email']
        d={'name':name,'age':age,'place':place,'email':email}
        return render(request,'output.html',d)
    d={'form':f}
    return render(request,'form.html',d)