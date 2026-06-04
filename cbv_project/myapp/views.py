from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from django.views.generic import CreateView
# Create your views here.
class Doctorlist(ListView):
    model = Doctor
    # default context: doctor_list
    # default templates: doctor_list.html

class Doctordetails(DetailView):
    model = Doctor
    # template_name = 'myapp/doctor_details.html'
    # context_object_name = 'doctor_details_list'

class DoctorUpdate(UpdateView):
    model = Doctor
    # provide fields for the ModelForm
    fields = ['name', 'age', 'email', 'Place', 'specialization']
    template_name = 'myapp/doctor_form.html'
    success_url = reverse_lazy('doctors')

class DoctorDelete(DeleteView):
    model = Doctor
    template_name = 'myapp/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctors')

class DoctorCreate(CreateView):
    model = Doctor
    fields = ['name', 'age', 'email', 'Place', 'specialization']
    template_name = 'myapp/doctor_form.html'
    success_url = reverse_lazy('doctors')

