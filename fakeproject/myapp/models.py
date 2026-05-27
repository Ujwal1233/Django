from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    dob=models.DateField()
    job=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    email=models.EmailField()

    def __str__(self):
        return self.name
    