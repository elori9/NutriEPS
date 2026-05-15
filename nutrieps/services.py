import json
import urllib.parse
from urllib.request import Request, urlopen


def safe_float(val):
    try:
        return round(float(val), 2)
    except (ValueError, TypeError):
        return 0.0


def search_foods(search_term):
    # Search parsed
    safe_term = urllib.parse.quote(search_term)

    api_url = f'https://world.openfoodfacts.org/cgi/search.pl?search_terms={safe_term}&search_simple=1&action=process&json=1&page_size=10'

    results = []

    try:
        # Change header for not getting blocked
        req = Request(api_url, headers={'User-Agent': 'NutriEPS-StudentProject/1.0'})

        with urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))

                products = data.get('products', [])

                for item in products:
                    name = item.get('product_name_en') or item.get('product_name')

                    if not name:
                        continue

                    nutriments = item.get('nutriments', {})

                    # Add it, if it has the kcal
                    calories = safe_float(nutriments.get('energy-kcal_100g') or nutriments.get('energy-kcal'))

                    if calories > 0:
                        results.append({
                            'name': name.capitalize(),
                            'calories': calories,
                            'protein': safe_float(nutriments.get('proteins_100g')),
                            'carbs': safe_float(nutriments.get('carbohydrates_100g')),
                            'fat': safe_float(nutriments.get('fat_100g'))
                        })
    except Exception as e:
        print(f"Error on search_foods: {e}")

    return results
