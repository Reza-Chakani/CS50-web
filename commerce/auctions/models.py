from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name
    
class List(models.Model):
    name = models.CharField(max_length= 100)
    category = models.ForeignKey(Category, related_name="list", on_delete=models.CASCADE) 
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name = "list", on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watch")

    def __str__(self):
        return self.name
    
    
class Bid(models.Model):
    user = models.ForeignKey(User, related_name = "bid", on_delete=models.CASCADE)
    item = models.ForeignKey(List, related_name = "bid", on_delete=models.CASCADE, null=True)
    bid = models.FloatField(blank=True, null=True)

class Comment(models.Model):
    name = models.ForeignKey(User, related_name = "comment", on_delete=models.CASCADE)
    item = models.ForeignKey(List, related_name = "comment", on_delete=models.CASCADE, null=True)
    comment = models.TextField(blank=True, null=True)