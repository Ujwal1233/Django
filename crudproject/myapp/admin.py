from django.contrib import admin

from myapp.models import Employee

    
# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['id','name','age','email','place','job','salary']
admin.site.register(Employee, EmployeeAdmin)
