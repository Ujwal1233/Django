from myapp.models import Employee
from django import forms

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'age', 'email', 'place', 'job', 'salary']