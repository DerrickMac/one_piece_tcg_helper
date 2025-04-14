import requests

def get_all_groups(category_id):
    url = f"https://tcgcsv.com/tcgplayer/{category_id}/groups"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    return []

def get_cards_per_tcgcsv_group(category_id, group_id):
    response = requests.get(f"https://tcgcsv.com/tcgplayer/{category_id}/{group_id}/products")
    if response.status_code == 200:
        return response.json()['results']
    return []

def get_prices_for_group(category_id, group_id):
    url = f"https://tcgcsv.com/tcgplayer/{category_id}/{group_id}/prices"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    return []
