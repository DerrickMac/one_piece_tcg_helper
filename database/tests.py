import datetime
import re
from django.test import TestCase
from django.utils import timezone

from .models import Leader, Character, Stage, Event
from database.test_data import leader_card, product_response, price_response, test_sp_product

def extract_art_type_regex(name):
    """
    Extracts the art type from a card name using regex for more precise matching.
    
    This approach uses regular expressions to specifically look for patterns
    like "(Manga)", "(Parallel)", or "(SP)" as standalone elements in parentheses.
    
    Args:
        name: The card name string to analyze
        
    Returns:
        String representing the art type: "Manga", "Parallel", "SP", or "Base"
    """
    # Look for Manga first (highest priority)
    if re.search(r'\(Manga\)', name):
        return "Manga"
    
    # Look for Parallel
    if re.search(r'\(Parallel\)', name):
        return "Parallel"
    
    # Look for SP
    if re.search(r'\(SP\)', name):
        return "SP"
    
    # Default case
    return "Base"

def get_card_price(product_id):
    for product in price_response["results"]:
        if product["productId"] == product_id:
            return product["marketPrice"]

def product_to_dictionary(product):
    """
    Converts a product object into a standardized dictionary containing all required fields.
    This function ensures all necessary card data is extracted correctly from the input object.
    
    Args:
        product: The source product object containing card information
        
    Returns:
        A dictionary with standardized keys for database storage
    """
    # Initialize the result dictionary
    result = {}
    
    # Basic card information
    result["product_id"] = product.get("productId")  # Note the camelCase to snake_case conversion
    result["name"] = product.get("name")
    result["image_url"] = product.get("imageUrl")
    result["url"] = product.get("url")
    
    # Handle extended data fields
    extended_data = product.get("extendedData", [])
    
    # Extract card number from extended data
    number_item = next((item for item in extended_data if item.get("name") == "Number"), None)
    result["card_number"] = number_item.get("value") if number_item else None
    
    # Extract effect/description from extended data
    description_item = next((item for item in extended_data if item.get("name") == "Description"), None)
    result["effect"] = description_item.get("value") if description_item else None
    
    # Extract and process colors
    color_item = next((item for item in extended_data if item.get("name") == "Color"), None)
    color_value = color_item.get("value") if color_item else None
    
    # Split colors if they exist
    if color_value:
        colors = color_value.split(";")
        result["color_one"] = colors[0].strip() if colors else None
        result["color_two"] = colors[1].strip() if len(colors) > 1 else None
    else:
        result["color_one"] = None
        result["color_two"] = None
    
    # Extract subtype information
    subtype_item = next((item for item in extended_data if item.get("name") == "Subtypes"), None)
    result["subtype"] = subtype_item.get("value") if subtype_item else None
    
    # Extract attribute information
    attribute_item = next((item for item in extended_data if item.get("name") == "Attribute"), None)
    result["attribute"] = attribute_item.get("value") if attribute_item else None
    
    # Extract and process tags from the effect/description
    if result["effect"]:
        import re
        tags = re.findall(r'\[(.*?)\]', result["effect"])
        result["tags"] = tags
    else:
        result["tags"] = []
    
    # Extract rarity information
    rarity_item = next((item for item in extended_data if item.get("name") == "Rarity"), None)
    result["rarity"] = rarity_item.get("value") if rarity_item else None
    
    # Extract card stats
    power_item = next((item for item in extended_data if item.get("name") == "Power"), None)
    result["power"] = power_item.get("value") if power_item else None
    
    life_item = next((item for item in extended_data if item.get("name") == "Life"), None)
    result["life"] = life_item.get("value") if life_item else None
    
    result["price"] = get_card_price(result["product_id"])
    result["art"] = extract_art_type_regex(result["name"])

    
    return result

class ParseJSONTests(TestCase):
    def test_skip_all_non_card_products(self):
        """
        ensure products such as booster boxes, booster packs, non-cards do not get added to DB
        """
        parsed_response = []
        for product in product_response["results"]:
            if not product["extendedData"]:
                continue
            parsed_response.append(product)
        
        self.assertNotEqual(len(product_response), len(parsed_response))

    def test_SP_art(self):
        """
        checks if SP is being parsed from name correctly and assigned as the art value
        """
        for product in test_sp_product["results"]:
            result = product_to_dictionary(product)
            break
        self.assertEqual(result["art"], "SP")

    
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
