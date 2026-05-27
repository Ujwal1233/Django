from django.shortcuts import render
from myapp.models import Employee
# Create your views here.
def fakeview(request):
    e=Employee.objects.all()
    d={ 'employees':e }
    return render(request,'fake.html', d)