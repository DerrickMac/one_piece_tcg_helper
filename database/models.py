from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField


class Card(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    url = models.URLField()
    last_updated = models.DateField(auto_now=True)
    card_number = models.CharField(max_length=8)
    effect = models.TextField()
    color_one = models.CharField(max_length=6)
    color_two = models.CharField(max_length=6, null=True)
    subtype = ArrayField(models.CharField(max_length=100), default=list)
    tags = ArrayField(models.CharField(max_length=100), null=True, default=list)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    rarity = models.CharField(max_length=3)
    art = models.CharField(max_length=8)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name

class PriceHistory(models.Model):
    card_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("card_type", "product_id")
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.date} at {self.price}'

    class Meta:
        indexes = [
            models.Index(fields=["card_type", "product_id"])
        ]

class Leader(Card):
    life = models.IntegerField()
    power = models.IntegerField()
    attribute = models.CharField(max_length=10)

class Character(Card):
    cost = models.IntegerField()
    power = models.IntegerField()
    counter = models.IntegerField()
    attribute = models.CharField(max_length=10)

class Event(Card):
    cost = models.IntegerField()

class Stage(Card):
    cost = models.IntegerField()


