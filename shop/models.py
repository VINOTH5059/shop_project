from django.db import models
from django.contrib.auth.models import User
import datetime
import os
from django.utils import timezone

def getfilename(instance, filename):
    now_time = timezone.now().strftime("%y%m%d%H%M%S")
    new_filename = f"{now_time}_{filename}"
    return os.path.join('uploads/', new_filename)

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=getfilename, null=True, blank=True)
    description = models.TextField(max_length=500, default="No description")
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    Product_image = models.ImageField(upload_to=getfilename, null=True, blank=True)
    quantity = models.IntegerField()
    description = models.TextField(max_length=500, default="No description")
    original_price = models.FloatField(null=True, blank=True)
    selling_price = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
