from cloudinary.models import CloudinaryField
from django.db import models


class DietaryPreference(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=5, default="€")
    dietary_tags = models.CharField(max_length=100)
    image = CloudinaryField('image', default='static/images/dish-1.jpg')
    item_id = models.AutoField(primary_key=True)
    dietary_preferences = models.ManyToManyField(DietaryPreference, blank=True)

    def __str__(self):
        return self.name
