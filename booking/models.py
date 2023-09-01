from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings 




class DietaryPreference(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')
    dietary_preference = models.ForeignKey(
        DietaryPreference, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings', null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.menu_item.name} - {self.rating} stars"






