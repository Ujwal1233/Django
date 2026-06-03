from django.contrib import admin
from .models import *
# Register your models here.


# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'marks', 'age', 'email', 'place')

admin.site.register(Student)