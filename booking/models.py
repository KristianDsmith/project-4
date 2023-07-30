from django.db import models, connection


class DietaryPreference(models.Model):
    name = models.CharField(max_length=100)


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')
    dietary_preference = models.ForeignKey(
        DietaryPreference, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


table_name = "booking_dietarypreference"
table_names = connection.introspection.table_names()

if table_name in table_names:
    print(f"Table '{table_name}' exists in the database.")
else:
    print(f"Table '{table_name}' does not exist in the database.")
