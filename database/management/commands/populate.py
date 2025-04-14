from django.core.management.base import BaseCommand
from database.utils.tcg_api import get_all_groups, get_cards_per_tcgcsv_group, get_prices_for_group
from database.utils.database_helpers import product_to_dictionary, get_card_price
from database.models import Card, PriceHistory

class Command(BaseCommand):
    help = "populates card info from tcgcsv"

    def handle(self, *args, **options):
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
            
        self.stdout.write(self.style.SUCCESS("Command executed successfully"))




