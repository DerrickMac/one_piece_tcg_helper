import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Leader, Character, Stage, Event

leader_card = {
    "product_id": 453505,
    "name": "Trafalgar Law (002)",
    "image_url": "https://tcgplayer-cdn.tcgplayer.com/product/453505_200w.jpg", 
    "url": "https://www.tcgplayer.com/product/453505/one-piece-card-game-romance-dawn-trafalgar-law-002",
    "card_number": "OP01-002",
    "effect": "[Activate:Main] [Once Per Turn] (2) \u003Cem\u003E(You may rest the specified number of DON!! cards in your cost area.)\u003C/em\u003E: If you have 5 Characters, return 1 of your Characters to your hand. Then, play up to 1 Character with a cost of 5 or less from your hand that is a different color than the returned Character.",
    "color_one": "Green",
    "color_two": "Red",
    "subtype": ["Heart Pirates", "Supernovas"],
    "attribute": "Slash",
    "tags": ["Activate:Main", "Once Per Turn"],
    "price": 0.29,
    "rarity": "L",
    "art": "Base",
    "life": 4,
    "power": 5000
}

class LeaderModelTests(TestCase):
    def test_leader_card_entered_into_database(self):
        """
        Using dummy data to enter a Leader card into the Leader table
        """
        leader = Leader.objects.create(
            product_id=leader_card["product_id"],
            name=leader_card["name"],
            image_url=leader_card["image_url"],
            url=leader_card["url"],
            card_number=leader_card["card_number"],
            effect=leader_card["effect"],
            color_one=leader_card["color_one"],
            color_two=leader_card["color_two"],
            subtype=leader_card["subtype"],
            attribute=leader_card["attribute"],
            tags=leader_card["tags"],
            price=leader_card["price"],
            rarity=leader_card["rarity"],
            art=leader_card["art"],
            life=leader_card["life"],
            power=leader_card["power"]
        )

        # Verify the leader card was created with the correct attributes
        self.assertEqual(leader.product_id, 453505)
        self.assertEqual(leader.name, "Trafalgar Law (002)")
        self.assertEqual(leader.card_number, "OP01-002")
        self.assertEqual(leader.color_one, "Green")
        self.assertEqual(leader.color_two, "Red")
        self.assertEqual(leader.life, 4)
        self.assertEqual(leader.power, 5000)
        
        # Verify that it actually exists in the database
        self.assertEqual(Leader.objects.count(), 1)
        
        # Retrieve it from the database again to ensure it was saved correctly
        saved_leader = Leader.objects.get(product_id=leader_card["product_id"])
        self.assertEqual(saved_leader.name, leader_card["name"])
        self.assertEqual(saved_leader.power, leader_card["power"])
