import re     

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
    
    # Look for Alternate Art
    if re.search(r'\(Alternate Art\)', name):
        return "Alternate Art"

    # Look for Alternate Art
    if re.search(r'\(Full Art\)', name):
        return "Full Art"
    
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

def get_card_price(product_id, prices):
    """
    This function finds the market price of a card given its product ID.

    Args:
        product_id: product_id integer
    
    Returns:
        The price of the card as a deciminal value 
    """ 
    for product in prices:
        if product["productId"] == product_id:
            if product["marketPrice"]:
                return product["marketPrice"]
            else:
                return 0
    return 0

def product_to_dictionary(product, prices):
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
            result["attribute"] = split_tag_string(item.get("value"))
    
    ## OUTLIERS START ##
    # if card does not have a counter value, create a default value of 0
    if "counter" not in result:
        result["counter"] = 0
    # if card does not have an effect, it must be a vanilla card so create a default value of blank string
    if "effect" not in result:
        result["effect"] = ""
    # if card does not have an effect, it would not have any tags either
    if "tags" not in result:
        result["tags"] = []
    # some leaders in JSON do not have life values so create default values based on general knowledge for mono color (5 life) / dual color (4 life)
    if result["card_type"] == "Leader" and "life" not in result:
        # dual color
        if result["color_two"]:
            result["life"] = int(4)
        else:
            result["life"] = int(5)
    # if card does not have a Power value, its power must be 0 and left out of the JSON data completely (such as Kin'emon OP10-027)
    if "power" not in result:
        result["power"] = 0
    # if card does not have a Subtype value, create a default value of []. (Demo leader Uta doesn't have subtype data)
    if "subtypes" not in result:
        result["subtypes"] = []
    ## OUTLIERS END ##

    ## CARD SPECIFIC FIXES ##

    # Card: "I Want to Live!!" EB01-050 was erroneously marked as a Character when its an event"
    if result["product_id"] == 544587:
        result["card_type"] = "Event"

    # Card: "The Ark Maxim" OP06-117 was erroneously marked as a Character when its a stage"
    if result["product_id"] == 541658:
        result["card_type"] = "Stage"

    # Card: "The Ark Maxim" (Pre-Release) OP06-117 was erroneously marked as a Character when its a stage"
    if result["product_id"] == 541720:
        result["card_type"] = "Stage"

    # Card: "Kuro (Alternate Art)" OP03-021 is missing color in the JSON data"
    if result["product_id"] == 498039:
        result["color_one"] = "Green"
        result["color_two"] = None

    # Card: "Arlong (Alternate Art)" OP03-022 is missing colors in the JSON data"
    if result["product_id"] == 498064:
        result["color_one"] = "Green"
        result["color_two"] = "Yellow"

    ## CARD SPECIFIC FIXES END ##

    result["price"] = get_card_price(result["product_id"], prices)
    result["art"] = extract_art_type_regex(result["name"])

    return result

