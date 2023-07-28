from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    dietary_tags = models.CharField(max_length=100)
    item_id = models.AutoField(primary_key=True, default=1)

    def __str__(self):
        return self.name
