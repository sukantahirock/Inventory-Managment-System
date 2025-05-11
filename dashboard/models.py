from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True,blank=True)
    password = models.CharField(max_length=255,blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    password = models.CharField(max_length=255,blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
"""
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
"""

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)  # Add this line

    def __str__(self):
        return self.name

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
