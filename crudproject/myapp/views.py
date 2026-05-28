from django.shortcuts import get_object_or_404, redirect, render

from myapp.forms import EmployeeForm
from myapp.models import Employee


def display(request):
    employees = Employee.objects.order_by('-id')
    return render(request, 'display.html', {'employees': employees})


def insert_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()

    return render(request, 'insert.html', {'form': form, 'title': 'Add Employee', 'submit_text': 'Save Employee'})


def update_view(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'insert.html', {'form': form, 'title': 'Update Employee', 'submit_text': 'Update Employee', 'employee': employee})


def delete_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('home')