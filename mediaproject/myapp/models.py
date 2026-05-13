from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="products/")

    def __str__(self) -> str:
        return self.name
