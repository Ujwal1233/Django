from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    Place = models.CharField(max_length=80)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    