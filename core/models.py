from django.db import models
from django.contrib.auth.models import User
import uuid


class Store(models.Model):
    id = models.AutoField(primary_key=True, editable=False)

    name = models.CharField(max_length=100, blank=False)
    url = models.URLField(max_length=300, blank=False)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)

    name = models.CharField(max_length=100, blank=False)
    url = models.URLField(max_length=300, blank=False)
    urlToBuy = models.TextField(blank=True)

    priceStart = models.FloatField(blank=False)
    priceCurrent = models.FloatField(blank=False)
    priceHighest = models.FloatField(blank=False)
    priceLowest = models.FloatField(blank=False)

    dateAdded = models.DateTimeField(blank=False)
    dateLastChecked = models.DateTimeField(blank=False)
    dateHighest = models.DateTimeField(blank=False)
    dateLowest = models.DateTimeField(blank=False)

    # storeUUID = models.ForeignKey(Store, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class Connector(models.Model):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'User: ' + str(self.user) + ' -> ' + 'Product: ' + str(self.product)
