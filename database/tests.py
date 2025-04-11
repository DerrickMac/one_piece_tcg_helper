import re
from django.test import TestCase

from .models import Leader, Character, Stage, Event
from database.test_data import price_response, non_card_product, sp_character, base_leader, parallel_leader, character_with_counter, event_card, stage_card, manga

def extract_art_type_regex(name):
    """
    This function uses regex to extract art types: Manga, Parallel, or SP from card name. 
    If none are present, card is "Base" rarity.

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

def extract_action_tags(effect_text):
    """
    This function looks for tags like [Activate:Main] that appear at the start of 
    the description, but ignores type references like [Animal] that appear in the 
    middle of the text.
    
    Args:
        effect_text: The card effect/description text
        
    Returns:
        List of action tags found at the beginning of the description
    """
    if not effect_text:
        return []
    
    tags = []
    # Match the beginning sequence of tags (handles both space and slash separators)
    # This pattern looks for a sequence of bracketed content at the start,
    # allowing for slashes or spaces between bracketed items
    start_pattern = r'^\s*((?:\s*\[.*?\](?:\s*(?:\/|\s)\s*\[.*?\])*)+)'
    start_match = re.match(start_pattern, effect_text)
    
    if start_match:
        # Get the full sequence of opening tags
        opening_sequence = start_match.group(1)
        
        # Extract individual tags from this sequence
        start_tags = re.findall(r'\[(.*?)\]', opening_sequence)
        tags.extend(start_tags)
    
    # Look for [Trigger] tag anywhere in the text
    trigger_match = re.search(r'\[Trigger\]', effect_text)
    if trigger_match and "Trigger" not in tags:
        tags.append("Trigger")
    
    return tags

def split_color_string(color_string):
    """
    This function splits a semicolon-separated string into two color values

    Args:
        color_string: card color text
    
    Returns:
        A tuple containing two elements (color_one, color_two)
    """ 
    if color_string:
        colors = color_string.split(";")
        color_one = colors[0].strip() if colors else None
        color_two = colors[1].strip() if len(colors) > 1 else None
    else:    
        color_one, color_two = None, None
    return color_one, color_two

def split_tag_string(tag_string):
    """
    This function splits a semicolon-separated string into a list of tags

    Args:
        tag_string: tag text
    
    Returns:
        A list containing individual tags
    """ 
    if tag_string:
        values = [value.strip() for value in tag_string.split(";")]
        return values
    else:    
        return []

def get_card_price(product_id):
    """
    This function finds the market price of a card given its product ID.

    Args:
        product_id: product_id integer
    
    Returns:
        The price of the card as a deciminal value 
    """ 

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
    result["product_id"] = int(product.get("productId"))
    result["name"] = product.get("name")
    result["image_url"] = product.get("imageUrl")
    result["url"] = product.get("url")
    
    # Handle extended data fields
    extended_data = product.get("extendedData", [])
    
    # Extract card data from extended data
    for item in extended_data:
        if item.get("name") == "Rarity":
            result["rarity"] = item.get("value")
        elif item.get("name") == "Number":
            result["card_number"] = item.get("value")
        elif item.get("name") == "Description":
            result["effect"] = item.get("value")
            result["tags"] = extract_action_tags(result["effect"])
        elif item.get("name") == "Color":
            result["color_one"], result["color_two"] = split_color_string(item.get("value"))
        elif item.get("name") == "CardType":
            result["card_type"] = item.get("value")
        elif item.get("name") == "Cost":
            result["cost"] = int(item.get("value"))
        elif item.get("name") == "Life":
            result["life"] = int(item.get("value"))
        elif item.get("name") == "Power":
            result["power"] = int(item.get("value"))
        elif item.get("name") == "Subtypes":
            result["subtypes"] = split_tag_string(item.get("value"))
        elif item.get("name") == "Counterplus":
            result["counter"] = int(item.get("value"), 0)
        elif item.get("name") == "Attribute":
            result["attribute"] = item.get("value")
    
    # if card does not have a counter value, create a default value of 0
    if "counter" not in result:
        result["counter"] = 0

    result["price"] = get_card_price(result["product_id"])
    result["art"] = extract_art_type_regex(result["name"])

    return result

class ParseJSONTests(TestCase):
    def test_skip_all_non_card_products(self):
        """
        ensure products such as booster boxes, booster packs, non-cards do not get added to DB
        """
        parsed_response = []
        for product in non_card_product["results"]:
            if not product["extendedData"]:
                continue
            parsed_response.append(product)
        
        self.assertNotEqual(len(non_card_product["results"]), len(parsed_response))

    # Test Product ID
    def test_product_id(self):
        """
        verifies product_to_dictionary() extracts productID correctly
        """
        result = product_to_dictionary(sp_character)
        self.assertEqual(result["product_id"], 558019)

    # Test Name
    def test_name(self):
        """
        verifies product_to_dictionary() extracts name correctly
        """
        result = product_to_dictionary(sp_character)
        self.assertEqual(result["name"], "Portgas.D.Ace (SP)")

    # Color Tests
    def test_two_colors(self):
        """
        verifies that two color leaders are assigned values for color_one and color_two
        """
        result = product_to_dictionary(base_leader)
        self.assertEqual(result["color_one"], "Green")
        self.assertEqual(result["color_two"], "Red")

    def test_one_color(self):
        """
        verifies that one color cards are assigned values for color_one and not color_two
        """
        result = product_to_dictionary(sp_character)
        self.assertEqual(result["color_one"], "Red")
        self.assertEqual(result["color_two"], None)

    # Subtype Tests
    def test_subtypes(self):
        """
        checks if card subtypes are properly extracted
        """
        result = product_to_dictionary(base_leader)
        self.assertEqual(result["subtypes"], ["Animal", "Straw Hat Crew", "Drum Kingdom"])

    # Test Price
    def test_price(self):
        """
        checks if card price is properly assigned
        """
        result = product_to_dictionary(base_leader)
        self.assertEqual(result["price"], 0.07)

    # Art Tests
    def test_SP_art(self):
        """
        checks if SP is being parsed from name correctly and assigned as the art value
        """
        result = product_to_dictionary(sp_character)
        self.assertEqual(result["art"], "SP")
    
    def test_base_art(self):
        """
        checks if Base will be assigned as art value in the absence of SP, Parallel, Manga in name.
        """
        result = product_to_dictionary(base_leader)
        self.assertEqual(result["art"], "Base")
    
    def test_parallel_art(self):
        """
        checks if Parallel is being parsed from name correctly and assigned as the art value.
        """
        result = product_to_dictionary(parallel_leader)
        self.assertEqual(result["art"], "Parallel")
    
    def test_manga_art(self):
        """
        checks if Manga is being parsed from name correctly and assigned as the art value.
        """
        result = product_to_dictionary(manga)
        self.assertEqual(result["art"], "Manga")
    
    # Counter Tests
    def test_card_with_counter(self):
        """
        checks if counter has been assigned correctly for a card that has a counter
        """
        result = product_to_dictionary(character_with_counter)
        self.assertEqual(result["counter"], 1000)

    def test_card_with_no_counter(self):
        """
        checks if counter has been assigned correctly as 0 for a card that has no counter value
        """
        result = product_to_dictionary(manga)
        self.assertEqual(result["counter"], 0)

    # Tag Tests
    def test_multiple_tags(self):
        """
        checks if tags are properly extracted from card effects
        """
        result = product_to_dictionary(base_leader)
        self.assertEqual(result["tags"], ["Activate:Main", "Once Per Turn"])

class LeaderModelTests(TestCase):
    def test_leader_card_entered_into_database(self):
        """
        Ensuring Leader card is entered into the Leader table
        """

        card = product_to_dictionary(base_leader)

        if card["card_type"] == "Leader":

            leader = Leader.objects.create(
                product_id=card["product_id"],
                name=card["name"],
                image_url=card["image_url"],
                url=card["url"],
                rarity=card["rarity"],
                card_number=card["card_number"],
                effect=card["effect"],
                color_one=card["color_one"],
                color_two=card["color_two"],
                life=card["life"],
                power=card["power"],
                subtype=card["subtypes"],
                attribute=card["attribute"],
                tags=card["tags"],
                price=card["price"],
                art=card["art"],
        )

        # Verify the leader card was created with the correct attributes
        self.assertEqual(leader.product_id, 558021)
        self.assertEqual(leader.name, "Tony Tony.Chopper (001)")
        self.assertEqual(leader.image_url, "https://tcgplayer-cdn.tcgplayer.com/product/558021_200w.jpg")
        self.assertEqual(leader.url, "https://www.tcgplayer.com/product/558021/one-piece-card-game-two-legends-tony-tonychopper-001")
        self.assertEqual(leader.rarity, "L")
        self.assertEqual(leader.card_number, "OP08-001")
        self.assertEqual(leader.effect, "[Activate:Main] [Once Per Turn] Give up to 3 of your [Animal] or [Drum Kingdom] type Characters up to 1 rested DON!! card each.")
        self.assertEqual(leader.color_one, "Green")
        self.assertEqual(leader.color_two, "Red")
        self.assertEqual(leader.life, 4)
        self.assertEqual(leader.power, 5000)
        self.assertEqual(leader.subtype, ["Animal", "Straw Hat Crew", "Drum Kingdom"])
        self.assertEqual(leader.attribute, "Strike")
        self.assertEqual(leader.tags, ["Activate:Main", "Once Per Turn"])
        self.assertEqual(leader.price, 0.07)
        self.assertEqual(leader.art, "Base")
        
        # Retrieve it from the database again to ensure it was saved correctly
        saved_leader = Leader.objects.get(product_id=card["product_id"])
        self.assertEqual(saved_leader.name, card["name"])
        self.assertEqual(saved_leader.power, card["power"])

class CharacterModelTests(TestCase):
    def test_character_card_entered_into_database(self):
        """
        Ensuring Character card is entered into the Character table
        """

        card = product_to_dictionary(sp_character)

        if card["card_type"] == "Character":

            character = Character.objects.create(
                product_id=card["product_id"],
                name=card["name"],
                image_url=card["image_url"],
                url=card["url"],
                rarity=card["rarity"],
                card_number=card["card_number"],
                effect=card["effect"],
                color_one=card["color_one"],
                color_two=card["color_two"],
                cost=card["cost"],
                power=card["power"],
                subtype=card["subtypes"],
                counter=card["counter"],
                attribute=card["attribute"],
                tags=card["tags"],
                price=card["price"],
                art=card["art"],
        )

        # Verify the leader card was created with the correct attributes
        self.assertEqual(character.product_id, 558019)
        self.assertEqual(character.name, "Portgas.D.Ace (SP)")
        self.assertEqual(character.image_url, "https://tcgplayer-cdn.tcgplayer.com/product/558019_200w.jpg")
        self.assertEqual(character.url, "https://www.tcgplayer.com/product/558019/one-piece-card-game-two-legends-portgasdace-sp")
        self.assertEqual(character.rarity, "SR")
        self.assertEqual(character.card_number, "OP02-013")
        self.assertEqual(character.effect, "[On Play] Give up to 2 of your opponent's Characters 3000 power during this turn. Then, if your Leader's type includes \"Whitebeard Piratess\", this Character gains [Rush] during this turn.\u003Cbr\u003E\r\n(This card can attack on the turn in which it is played.)")
        self.assertEqual(character.color_one, "Red")
        self.assertEqual(character.color_two, None)
        self.assertEqual(character.cost, 7)
        self.assertEqual(character.power, 7000)
        self.assertEqual(character.subtype, ["Whitebeard Pirates"])
        self.assertEqual(character.attribute, "Special")
        self.assertEqual(character.tags, ["On Play"])
        self.assertEqual(character.price, 77.14)
        self.assertEqual(character.art, "SP")
        
        # Retrieve it from the database again to ensure it was saved correctly
        saved_character = Character.objects.get(product_id=card["product_id"])
        self.assertEqual(saved_character.name, card["name"])
        self.assertEqual(saved_character.power, card["power"])

class StageModelTests(TestCase):
    def test_stage_card_entered_into_database(self):
        """
        Ensuring Stage card is entered into the Stage table
        """

        card = product_to_dictionary(stage_card)
        print(card["product_id"])

        if card["card_type"] == "Stage":

            stage = Stage.objects.create(
                product_id=card["product_id"],
                name=card["name"],
                image_url=card["image_url"],
                url=card["url"],
                rarity=card["rarity"],
                card_number=card["card_number"],
                effect=card["effect"],
                color_one=card["color_one"],
                color_two=card["color_two"],
                cost=card["cost"],
                subtype=card["subtypes"],
                tags=card["tags"],
                price=card["price"],
                art=card["art"],
        )

        # Verify the leader card was created with the correct attributes
        self.assertEqual(stage.product_id, 558044)
        self.assertEqual(stage.name, "Drum Kingdom")
        self.assertEqual(stage.image_url, "https://tcgplayer-cdn.tcgplayer.com/product/558044_200w.jpg")
        self.assertEqual(stage.url, "https://www.tcgplayer.com/product/558044/one-piece-card-game-two-legends-drum-kingdom")
        self.assertEqual(stage.rarity, "C")
        self.assertEqual(stage.card_number, "OP08-020")
        self.assertEqual(stage.effect, "[Opponent's Turn] All of your [Drum Kingdom] type Characters gain +1000 power.")
        self.assertEqual(stage.color_one, "Red")
        self.assertEqual(stage.color_two, None)
        self.assertEqual(stage.cost, 1)
        self.assertEqual(stage.subtype, ["Drum Kingdom"])
        self.assertEqual(stage.tags, ["Opponent's Turn"])
        self.assertEqual(stage.price, 0.03)
        self.assertEqual(stage.art, "Base")
        
        # Retrieve it from the database again to ensure it was saved correctly
        saved_stage = Stage.objects.get(product_id=card["product_id"])
        self.assertEqual(saved_stage.name, card["name"])
        
class EventModelTests(TestCase):
    def test_event_card_entered_into_database(self):
        """
        Ensuring Event card is entered into the Event table
        """

        card = product_to_dictionary(event_card)

        if card["card_type"] == "Event":

            event = Event.objects.create(
                product_id=card["product_id"],
                name=card["name"],
                image_url=card["image_url"],
                url=card["url"],
                rarity=card["rarity"],
                card_number=card["card_number"],
                effect=card["effect"],
                color_one=card["color_one"],
                color_two=card["color_two"],
                cost=card["cost"],
                subtype=card["subtypes"],
                tags=card["tags"],
                price=card["price"],
                art=card["art"],
        )

        # Verify the leader card was created with the correct attributes
        self.assertEqual(event.product_id, 558063)
        self.assertEqual(event.name, "Electrical Luna")
        self.assertEqual(event.image_url, "https://tcgplayer-cdn.tcgplayer.com/product/558063_200w.jpg")
        self.assertEqual(event.url, "https://www.tcgplayer.com/product/558063/one-piece-card-game-two-legends-electrical-luna")
        self.assertEqual(event.rarity, "R")
        self.assertEqual(event.card_number, "OP08-036")
        self.assertEqual(event.effect, "[Main] All of your opponent's rested Characters with a cost of 7 or less will not become active in your opponent's next Refresh Phase.\u003Cbr\u003E\r\n[Trigger] Rest up to 1 of your opponent's Characters.")
        self.assertEqual(event.color_one, "Green")
        self.assertEqual(event.color_two, None)
        self.assertEqual(event.cost, 3)
        self.assertEqual(event.subtype, ["Minks"])
        self.assertEqual(event.tags, ["Main", "Trigger"])
        self.assertEqual(event.price, 0.41)
        self.assertEqual(event.art, "Base")
        
        # Retrieve it from the database again to ensure it was saved correctly
        saved_event = Event.objects.get(product_id=card["product_id"])
        self.assertEqual(saved_event.name, card["name"])