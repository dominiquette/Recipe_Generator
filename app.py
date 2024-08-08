# ===== Importing Libraries ===========
import requests

# ===== Importing data from files ===========
from config import api_key

# ===== Establish API connection ===========
# SpoonacularAPI class handles making requests to the API
class SpoonacularAPI:
    def __init__(self, base_url, api_key):
        # Creates an instance of the base url
        self.base_url = base_url
        # Creates an instance of the api key imported from config
        self.api_key = api_key

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def make_request(self, endpoint, params=None):
        url = f'{self.base_url}/{endpoint}'
        headers = self.get_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

# RecipeFinder class handles getting recipes from the API
class RecipeFinder:
    def __init__(self, api):
        # Creates an instance of the API
        self.api = api

    def find_recipes_by_ingredients(self, ingredients):
        endpoint = "recipes/findByIngredients"
        params = {
            "ingredients": ingredients,
            "number": 10,  # Number of recipes to return
            "ranking": 2,  # minimizes missing ingredients
            "apiKey": api_key,
            "ignorePantry": "true"  # ignore typical pantry items
        }
        try:
            response = self.api.make_request(endpoint, params=params)
            return response
        except requests.RequestException as e:
            print(f"Error fetching recipes: {e}")
            return []

    def find_recipes_by_category(self, category):
        endpoint = "recipes/complexSearch"
        params = {
            "type": category,
            "number": 10,
            "apiKey": api_key
        }
        try:
            response = self.api.make_request(endpoint, params=params)
            return response.get("results", [])
        except requests.RequestException as e:
            print(f"Error fetching recipes: {e}")
            return []

    def find_recipe_instructions(self, recipe_id):
        endpoint = f"recipes/{recipe_id}/information"
        params = {
            "apiKey": api_key
        }
        try:
            response = self.api.make_request(endpoint, params=params)
            return response
        except requests.RequestException as e:
            print(f"Error fetching recipe instructions: {e}")
            return {}

    def find_random_recipes(self):
        endpoint = "recipes/random"
        params = {
            "number": 10,
            "apiKey": api_key
        }
        try:
            response = self.api.make_request(endpoint, params=params)
            if "recipes" in response:
                return response["recipes"]
            else:
                print("Unexpected response format:", response)
                return []
        except requests.RequestException as e:
            print(f"Error fetching random recipes: {e}")
            return []
