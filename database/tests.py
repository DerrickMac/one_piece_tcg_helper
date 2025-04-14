from datetime import date
from decimal import Decimal
from django.test import TestCase
from .models import Card, Leader, Character, Stage, Event, PriceHistory
from database.test_data import non_card_product, sp_character, base_leader, parallel_leader, character_with_counter, event_card, stage_card, manga
from database.utils.database_helpers import product_to_dictionary, get_card_price
from database.utils.tcg_api import get_all_groups, get_cards_per_tcgcsv_group, get_prices_for_group
from django.db import connection

# prices = get_prices_for_group("68", "23462")

# class ParseJSONTests(TestCase):
#     def test_skip_all_non_card_products(self):
#         """
#         ensure products such as booster boxes, booster packs, non-cards do not get added to DB
#         """
#         parsed_response = []
#         for product in non_card_product["results"]:
#             if not product["extendedData"]:
#                 continue
#             parsed_response.append(product)
        
#         self.assertNotEqual(len(non_card_product["results"]), len(parsed_response))

#     # Test Product ID
#     def test_product_id(self):
#         """
#         verifies product_to_dictionary() extracts productID correctly
#         """
#         result = product_to_dictionary(sp_character, prices)
#         self.assertEqual(result["product_id"], 558019)

#     # Test Name
#     def test_name(self):
#         """
#         verifies product_to_dictionary() extracts name correctly
#         """
#         result = product_to_dictionary(sp_character, prices)
#         self.assertEqual(result["name"], "Portgas.D.Ace (SP)")

#     # Color Tests
#     def test_two_colors(self):
#         """
#         verifies that two color leaders are assigned values for color_one and color_two
#         """
#         result = product_to_dictionary(base_leader, prices)
#         self.assertEqual(result["color_one"], "Green")
#         self.assertEqual(result["color_two"], "Red")

#     def test_one_color(self):
#         """
#         verifies that one color cards are assigned values for color_one and not color_two
#         """
#         result = product_to_dictionary(sp_character, prices)
#         self.assertEqual(result["color_one"], "Red")
#         self.assertEqual(result["color_two"], None)

#     # Subtype Tests
#     def test_subtypes(self):
#         """
#         checks if card subtypes are properly extracted
#         """
#         result = product_to_dictionary(base_leader, prices)
#         self.assertEqual(result["subtypes"], ["Animal", "Straw Hat Crew", "Drum Kingdom"])

#     # Test Price
#     def test_price(self):
#         """
#         checks if card price is properly assigned
#         """
#         result = product_to_dictionary(base_leader, prices)
#         self.assertTrue(result["price"])

#     # Art Tests
#     def test_SP_art(self):
#         """
#         checks if SP is being parsed from name correctly and assigned as the art value
#         """
#         result = product_to_dictionary(sp_character, prices)
#         self.assertEqual(result["art"], "SP")
    
#     def test_base_art(self):
#         """
#         checks if Base will be assigned as art value in the absence of SP, Parallel, Manga in name.
#         """
#         result = product_to_dictionary(base_leader, prices)
#         self.assertEqual(result["art"], "Base")
    
#     def test_parallel_art(self):
#         """
#         checks if Parallel is being parsed from name correctly and assigned as the art value.
#         """
#         result = product_to_dictionary(parallel_leader, prices)
#         self.assertEqual(result["art"], "Parallel")
    
#     def test_manga_art(self):
#         """
#         checks if Manga is being parsed from name correctly and assigned as the art value.
#         """
#         result = product_to_dictionary(manga, prices)
#         self.assertEqual(result["art"], "Manga")
    
#     # Counter Tests
#     def test_card_with_counter(self):
#         """
#         checks if counter has been assigned correctly for a card that has a counter
#         """
#         result = product_to_dictionary(character_with_counter, prices)
#         self.assertEqual(result["counter"], 1000)

#     def test_card_with_no_counter(self):
#         """
#         checks if counter has been assigned correctly as 0 for a card that has no counter value
#         """
#         result = product_to_dictionary(manga, prices)
#         self.assertEqual(result["counter"], 0)

#     # Tag Tests
#     def test_multiple_tags(self):
#         """
#         checks if tags are properly extracted from card effects
#         """
#         result = product_to_dictionary(base_leader, prices)
#         self.assertEqual(result["tags"], ["Activate:Main", "Once Per Turn"])

# class LeaderModelTests(TestCase):
#     def test_leader_card_entered_into_database(self):
#         """
#         Ensuring Leader card is entered into the Leader table
#         """

#         card = product_to_dictionary(base_leader, prices)
#         leader = Card.create_card(card)

#         # Verify the leader card was created with the correct attributes
#         self.assertEqual(leader.product_id, 558021)
#         self.assertEqual(leader.name, "Tony Tony.Chopper (001)")
#         self.assertEqual(leader.image_url, "https://tcgplayer-cdn.tcgplayer.com/product/558021_200w.jpg")
#         self.assertEqual(leader.url, "https://www.tcgplayer.com/product/558021/one-piece-card-game-two-legends-tony-tonychopper-001")
#         self.assertEqual(leader.rarity, "L")
#         self.assertEqual(leader.card_number, "OP08-001")
#         self.assertEqual(leader.effect, "[Activate:Main] [Once Per Turn] Give up to 3 of your [Animal] or [Drum Kingdom] type Characters up to 1 rested DON!! card each.")
#         self.assertEqual(leader.color_one, "Green")
#         self.assertEqual(leader.color_two, "Red")
#         self.assertEqual(leader.life, 4)
#         self.assertEqual(leader.power, 5000)
#         self.assertEqual(leader.subtype, ["Animal", "Straw Hat Crew", "Drum Kingdom"])
#         self.assertEqual(leader.attribute, ["Strike"])
#         self.assertEqual(leader.tags, ["Activate:Main", "Once Per Turn"])
#         self.assertEqual(leader.price, card["price"])
#         self.assertEqual(leader.art, "Base")
        
#         # Retrieve it from the database again to ensure it was saved correctly
#         self.assertTrue(Leader.card_exists(card))
#         saved_leader = Leader.get_card(card)
#         self.assertEqual(saved_leader.name, card["name"])
#         self.assertEqual(saved_leader.power, card["power"])

# class CharacterModelTests(TestCase):
#     def test_character_card_entered_into_database(self):
#         """
#         Ensuring Character card is entered into the Character table
#         """

#         card = product_to_dictionary(sp_character, prices)
#         character = Card.create_card(card)

#         # Verify the character card was created with the correct attributes
#         self.assertEqual(character.product_id, 558019)
#         self.assertEqual(character.name, "Portgas.D.Ace (SP)")
#         self.assertEqual(character.image_url, "https://tcgplayer-cdn.tcgplayer.com/product/558019_200w.jpg")
#         self.assertEqual(character.url, "https://www.tcgplayer.com/product/558019/one-piece-card-game-two-legends-portgasdace-sp")
#         self.assertEqual(character.rarity, "SR")
#         self.assertEqual(character.card_number, "OP02-013")
#         self.assertEqual(character.effect, "[On Play] Give up to 2 of your opponent's Characters 3000 power during this turn. Then, if your Leader's type includes \"Whitebeard Piratess\", this Character gains [Rush] during this turn.\u003Cbr\u003E\r\n(This card can attack on the turn in which it is played.)")
#         self.assertEqual(character.color_one, "Red")
#         self.assertEqual(character.color_two, None)
#         self.assertEqual(character.cost, 7)
#         self.assertEqual(character.power, 7000)
#         self.assertEqual(character.subtype, ["Whitebeard Pirates"])
#         self.assertEqual(character.attribute, ["Special"])
#         self.assertEqual(character.tags, ["On Play"])
#         self.assertEqual(character.price, card["price"])
#         self.assertEqual(character.art, "SP")
        
#         # Retrieve it from the database again to ensure it was saved correctly
#         self.assertTrue(Character.card_exists(card))
#         saved_character = Character.get_card(card)
#         self.assertEqual(saved_character.name, card["name"])
#         self.assertEqual(saved_character.power, card["power"])

# class StageModelTests(TestCase):
#     def test_stage_card_entered_into_database(self):
#         """
#         Ensuring Stage card is entered into the Stage table
#         """

#         card = product_to_dictionary(stage_card, prices)
#         stage = Card.create_card(card)
    
#         # Verify the stage card was created with the correct attributes
#         self.assertEqual(stage.product_id, 558044)
#         self.assertEqual(stage.name, "Drum Kingdom")
#         self.assertEqual(stage.image_url, "https://tcgplayer-cdn.tcgplayer.com/product/558044_200w.jpg")
#         self.assertEqual(stage.url, "https://www.tcgplayer.com/product/558044/one-piece-card-game-two-legends-drum-kingdom")
#         self.assertEqual(stage.rarity, "C")
#         self.assertEqual(stage.card_number, "OP08-020")
#         self.assertEqual(stage.effect, "[Opponent's Turn] All of your [Drum Kingdom] type Characters gain +1000 power.")
#         self.assertEqual(stage.color_one, "Red")
#         self.assertEqual(stage.color_two, None)
#         self.assertEqual(stage.cost, 1)
#         self.assertEqual(stage.subtype, ["Drum Kingdom"])
#         self.assertEqual(stage.tags, ["Opponent's Turn"])
#         self.assertEqual(stage.price, card["price"])
#         self.assertEqual(stage.art, "Base")
        
#         # Retrieve it from the database again to ensure it was saved correctly
#         self.assertTrue(Stage.card_exists(card))
#         saved_stage = Stage.get_card(card)
#         self.assertEqual(saved_stage.name, card["name"])
        
# class EventModelTests(TestCase):
#     def test_event_card_entered_into_database(self):
#         """
#         Ensuring Event card is entered into the Event table
#         """

#         card = product_to_dictionary(event_card, prices)
#         event = Card.create_card(card)
    
#         # Verify the event card was created with the correct attributes
#         self.assertEqual(event.product_id, 558063)
#         self.assertEqual(event.name, "Electrical Luna")
#         self.assertEqual(event.image_url, "https://tcgplayer-cdn.tcgplayer.com/product/558063_200w.jpg")
#         self.assertEqual(event.url, "https://www.tcgplayer.com/product/558063/one-piece-card-game-two-legends-electrical-luna")
#         self.assertEqual(event.rarity, "R")
#         self.assertEqual(event.card_number, "OP08-036")
#         self.assertEqual(event.effect, "[Main] All of your opponent's rested Characters with a cost of 7 or less will not become active in your opponent's next Refresh Phase.\u003Cbr\u003E\r\n[Trigger] Rest up to 1 of your opponent's Characters.")
#         self.assertEqual(event.color_one, "Green")
#         self.assertEqual(event.color_two, None)
#         self.assertEqual(event.cost, 3)
#         self.assertEqual(event.subtype, ["Minks"])
#         self.assertEqual(event.tags, ["Main", "Trigger"])
#         self.assertEqual(event.price, card["price"])
#         self.assertEqual(event.art, "Base")
        
#         # Retrieve it from the database again to ensure it was saved correctly
#         self.assertTrue(Event.card_exists(card))
#         saved_event = Event.get_card(card)
#         self.assertEqual(saved_event.name, card["name"])

# class PriceHistoryTests(TestCase):
#     def test_add_price_to_price_history(self):
#         """
#         checking that a price can be successfully entered into the PriceHistory table
#         """

#         card = product_to_dictionary(base_leader, prices)
#         card_instance = Card.create_card(card)
#         PriceHistory.add_price(card_instance, 0.07)
#         # price_history = PriceHistory.objects.filter(product_id=card_instance["product_id"])
        
#         price_history = PriceHistory.objects.all()
#         self.assertEqual(price_history.count(), 1)

#         price_record = price_history.first()
#         self.assertEqual(price_record.price, Decimal('0.07'))
#         self.assertEqual(price_record.date, date.today())
#         self.assertEqual(price_record.content_object, card_instance)

# class PriceTests(TestCase):
#     def test_update_price(self):
#         """
#         Checks if price gets changed successfully for an existing card 
#         """
#         card = product_to_dictionary(base_leader, prices)
#         leader = Card.create_card(card)
#         self.assertEqual(leader.price, card["price"])

#         #change price
#         Leader.update_price(card, 0.01)
#         update_leader = Leader.get_card(card)
#         self.assertEqual(update_leader.price, Decimal("0.01"))

class HttpRequestTests(TestCase):

    # def test_http_request_for_specific_group(self):
    #     category_id = '68'
    #     group_id = "17675"
            
    #     products = get_cards_per_tcgcsv_group(category_id, group_id)
    #     prices = get_prices_for_group(category_id, group_id)

    #     cards_entered = 0
    #     cards_updated = 0
    #     for product in products:
    #         # Skip if the product isn't a card
    #         if not product['extendedData']:
    #             continue

    #         # Check if card exists in DB
    #         card = product_to_dictionary(product, prices)
    #         if Card.card_exists(card):
    #             # update the price
    #             new_price = get_card_price(card["product_id"], prices)
    #             if not new_price:
    #                 print("new_price is returning None")
    #                 return None
    #             elif new_price == card["price"]:
    #                 print("new price is not new")

    #             Card.update_price(card, new_price)
    #             # add to Price History
    #             PriceHistory.add_price(card, new_price)
    #             cards_updated += 1

    #         # If card doesn't exist
    #         else:
    #             # add card to DB
    #             new_card = Card.create_card(card)
    #             # add to Price History
    #             PriceHistory.add_price(card, new_card.price)
    #             cards_entered += 1
        
    #     print(cards_entered)
    #     print(cards_updated)

    def test_http_request_to_card_exists(self):
        category_id = '68'
        all_groups = get_all_groups(category_id)
        
        for group in all_groups:
            # Skip demo card group or promo card group 
            if group["groupId"] == 23907 or group["groupId"] == 17675:
                continue

            products = get_cards_per_tcgcsv_group(category_id, group["groupId"])
            prices = get_prices_for_group(category_id, group["groupId"])

            for product in products:
                # Skip if the product isn't a card
                if not product['extendedData']:
                    continue

                # Check if card exists in DB
                card = product_to_dictionary(product, prices)
                if Card.card_exists(card):
                    # update the price
                    new_price = get_card_price(card["product_id"], prices)
                    if not new_price:
                        print("new_price is returning None")
                        return None
                    elif new_price == card["price"]:
                        print("new price is not new")

                    Card.update_price(card, new_price)
                    # add to Price History
                    PriceHistory.add_price(card, new_price)

                # If card doesn't exist
                else:
                    # add card to DB
                    new_card = Card.create_card(card)
                    # add to Price History
                    PriceHistory.add_price(card, new_card.price)

