import json
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def _to_float(value):
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return 0.0


def _get_calories(nutriments):
    return _to_float(
        nutriments.get("energy-kcal_100g")
        or nutriments.get("energy-kcal")
        or 0
    )


def search_foods(search_term):
    if not search_term:
        return []

    max_tries = 5

    for tries in range(max_tries):
        try:
            params = {
                "search_terms": search_term,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 10,
                "fields": "product_name,nutriments",
            }

            url = f"{BASE_URL}?{urlencode(params)}"

            request = Request(
                url,
                headers={"User-Agent": "NutriEPS/1.0 (Python/3.13; Project-NutriEPS-UdL)"}
            )

            with urlopen(request, timeout=3) as response:
                data = json.loads(response.read().decode("utf-8"))

            products = data.get("products", [])
            results = []

            for product in products:
                nutriments = product.get("nutriments", {}) or {}

                results.append({
                    "name": product.get("product_name") or "Producto sin nombre",
                    "calories": _get_calories(nutriments),
                    "protein": _to_float(nutriments.get("proteins_100g")),
                    "carbs": _to_float(nutriments.get("carbohydrates_100g")),
                    "fat": _to_float(nutriments.get("fat_100g")),
                })

            return results

        except Exception as e:
            # If in all tries didn't get an api response throw an error
            if tries == max_tries - 1:
                raise e

            # Wait a bit until throw another req to the api
            time.sleep(0.5)

    return None
