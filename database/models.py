from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist

class Card(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    url = models.URLField()
    last_updated = models.DateField(auto_now=True)
    card_number = models.CharField(max_length=10)
    effect = models.TextField(null=True)
    color_one = models.CharField(max_length=6)
    color_two = models.CharField(max_length=6, null=True)
    subtype = ArrayField(models.CharField(max_length=100), default=list)
    tags = ArrayField(models.CharField(max_length=100), null=True, default=list)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    rarity = models.CharField(max_length=10)
    art = models.CharField(max_length=13)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name

    @classmethod
    def create_card(cls, card_data):
        """
        creates the appropriate card type based on card_type
        """
        print(f'found card: {card_data}')

        card_type = card_data.get("card_type")

        if card_type == "Leader":
            return Leader.create_from_dict(card_data)
        elif card_type == "Character":
            return Character.create_from_dict(card_data)
        elif card_type == "Stage":
            return Stage.create_from_dict(card_data)
        elif card_type == "Event":
            return Event.create_from_dict(card_data)
        elif card_type == "DON!!":
            return Don.create_from_dict(card_data)
        else:
            raise ValueError(f'Unknown card type: {card_type}')

    @classmethod
    def card_exists(cls, card_data):
        try:
            card_type = card_data.get("card_type")
            product_id = card_data.get("product_id")

            if card_type == "Leader":
                return Leader.objects.filter(product_id=product_id).exists()
            elif card_type == "Character":
                return Character.objects.filter(product_id=product_id).exists()
            elif card_type == "Stage":
                return Stage.objects.filter(product_id=product_id).exists()
            elif card_type == "Event":
                return Event.objects.filter(product_id=product_id).exists()
            elif card_type == "DON!!":
                return Don.objects.filter(product_id=product_id).exists()
        except:
            raise ValueError(f'Unknown object: {card_data}')
        
    @classmethod
    def get_card(cls, card_data):
        try:
            card_type = card_data.get("card_type")
            product_id = card_data.get("product_id")

            if card_type == "Leader":
                return Leader.objects.get(product_id=product_id)
            elif card_type == "Character":
                return Character.objects.get(product_id=product_id)
            elif card_type == "Stage":
                return Stage.objects.get(product_id=product_id)
            elif card_type == "Event":
                return Event.objects.get(product_id=product_id)
            elif card_type == "DON!!":
                return Don.objects.get(product_id=product_id)
        except:
            raise ObjectDoesNotExist(f'Object with {product_id} does not exist')

    @classmethod
    def update_price(cls, card_data, new_price):
        try:
            card_type = card_data.get("card_type")
            product_id = card_data.get("product_id")
            
            if card_type == "Leader":
                card = Leader.objects.get(product_id=product_id)
            elif card_type == "Character":
                card = Character.objects.get(product_id=product_id)
            elif card_type == "Stage":
                card = Stage.objects.get(product_id=product_id)
            elif card_type == "Event":
                card = Event.objects.get(product_id=product_id)
            elif card_type == "DON!!":
                card = Event.objects.get(product_id=product_id)
        except:
            return ObjectDoesNotExist(f'Object with {product_id} does not exist')

        card.price = new_price
        card.save()

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

    @classmethod
    def add_price(cls, card_data, price):
        
        card = Card.get_card(card_data)

        card_type = ContentType.objects.get_for_model(card.__class__)

        PriceHistory.objects.create(
            card_type=card_type,
            product_id=card.product_id,
            price=price
        )

class Leader(Card):
    life = models.IntegerField()
    power = models.IntegerField()
    attribute = ArrayField(models.CharField(max_length=20), default=list)
    
    @classmethod
    def create_from_dict(cls, card_data):
        """
        Create a Leader object with leader-specific fields
        """
        return cls.objects.create(
            product_id=card_data["product_id"],
                name=card_data["name"],
                image_url=card_data["image_url"],
                url=card_data["url"],
                rarity=card_data["rarity"],
                card_number=card_data["card_number"],
                effect=card_data["effect"],
                color_one=card_data["color_one"],
                color_two=card_data["color_two"],
                life=card_data["life"],
                power=card_data["power"],
                subtype=card_data["subtypes"],
                attribute=card_data["attribute"],
                tags=card_data["tags"],
                price=card_data["price"],
                art=card_data["art"]
        )

class Character(Card):
    cost = models.IntegerField()
    power = models.IntegerField()
    counter = models.IntegerField()
    attribute = ArrayField(models.CharField(max_length=20), default=list)

    @classmethod
    def create_from_dict(cls, card_data):
        """
        Create a Character object with character-specific fields
        """
        return cls.objects.create(
            product_id=card_data["product_id"],
            name=card_data["name"],
            image_url=card_data["image_url"],
            url=card_data["url"],
            rarity=card_data["rarity"],
            card_number=card_data["card_number"],
            effect=card_data["effect"],
            color_one=card_data["color_one"],
            cost=card_data["cost"],
            power=card_data["power"],
            subtype=card_data["subtypes"],
            counter=card_data["counter"],
            attribute=card_data["attribute"],
            tags=card_data["tags"],
            price=card_data["price"],
            art=card_data["art"]
        )

class Event(Card):
    cost = models.IntegerField()

    @classmethod
    def create_from_dict(cls, card_data):
        """
        Create an event object with event-specific fields
        """
        return cls.objects.create(
            product_id=card_data["product_id"],
            name=card_data["name"],
            image_url=card_data["image_url"],
            url=card_data["url"],
            rarity=card_data["rarity"],
            card_number=card_data["card_number"],
            effect=card_data["effect"],
            color_one=card_data["color_one"],
            cost=card_data["cost"],
            subtype=card_data["subtypes"],
            tags=card_data["tags"],
            price=card_data["price"],
            art=card_data["art"]
        )

class Stage(Card):
    cost = models.IntegerField()

    @classmethod
    def create_from_dict(cls, card_data):
        """
        Create an event object with event-specific fields
        """
        return cls.objects.create(
            product_id=card_data["product_id"],
            name=card_data["name"],
            image_url=card_data["image_url"],
            url=card_data["url"],
            rarity=card_data["rarity"],
            card_number=card_data["card_number"],
            effect=card_data["effect"],
            color_one=card_data["color_one"],
            cost=card_data["cost"],
            subtype=card_data["subtypes"],
            tags=card_data["tags"],
            price=card_data["price"],
            art=card_data["art"]
        )

class Don(Card):

    @classmethod
    def create_from_dict(cls, card_data):
        """
        Create a Don object with don-specific fields
        """
        return cls.objects.create(
            product_id=card_data["product_id"],
            name=card_data["name"],
            image_url=card_data["image_url"],
            url=card_data["url"],
            rarity=card_data["rarity"],
            card_number=card_data["product_id"],
            effect=card_data["effect"],
            color_one="Don",
            subtype=[],
            tags=[],
            price=card_data["price"],
            art="Don"
        )
