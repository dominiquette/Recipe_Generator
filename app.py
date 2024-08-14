# ===== Importing Libraries ===========
import requests

# ===== Importing data from files ===========
from config import api_key
from decorators import log_function_call, handle_errors  # Import decorators


# ===== Establish API connection ===========
# SpoonacularAPI class handles making requests to the API
class SpoonacularAPI:
    def __init__(self, base_url, api_key):
        # Creates an instance of the base URL
        self.base_url = base_url
        # Creates an instance of the API key imported from config
        self.api_key = api_key

    @log_function_call
    @handle_errors
    def make_request(self, endpoint, params=None):
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url, params=params)
        response.raise_for_status()  # # Raises an exception for HTTP errors
        return response.json()


# RecipeFinder class handles getting recipes from the API
class RecipeFinder:
    def __init__(self, api):
        # Creates an instance of the API
        self.api = api

    @log_function_call
    @handle_errors
    def find_recipes_by_ingredients(self, ingredients):
        endpoint = "recipes/findByIngredients"
        params = {
            "ingredients": ingredients,
            "number": 10,  # Number of recipes to return
            "ranking": 2,  # Minimises missing ingredients
            "apiKey": self.api.api_key,  # Uses the API key from the API instance
            "ignorePantry": "true"  # Ignore typical pantry items
        }
        response = self.api.make_request(endpoint, params=params)
        if not response:
            raise ValueError("API response is empty or invalid.")  # ValueError for empty or invalid responses
        return response

    @log_function_call
    @handle_errors
    def find_recipes_by_category(self, category):
        endpoint = "recipes/complexSearch"
        params = {
            "type": category,
            "number": 10,
            "apiKey": self.api.api_key
        }
        if category in ["vegan", "vegetarian", "gluten free", "ketogenic"]:
            params["diet"] = category  # Set diet parameter for specific diets
        elif category == "fish":
            params["includeIngredients"] = "fish"
        elif category == "chicken":
            params["includeIngredients"] = "chicken"
        elif category == "beef":
            params["includeIngredients"] = "beef"
        elif category == "lamb":
            params["includeIngredients"] = "lamb"
        elif category == "pork":
            params["includeIngredients"] = "pork"
        elif category == "duck":
            params["includeIngredients"] = "duck"
        elif category == "dessert":
            params["type"] = "dessert"
        elif category == "salad":
            params["type"] = "salad"

        response = self.api.make_request(endpoint, params=params)
        if not response:
            raise ValueError("API response is empty or invalid.")  # ValueError for empty or invalid responses
        return response.get("results", [])

    @log_function_call
    @handle_errors
    def find_recipe_instructions(self, recipe_id):
        endpoint = f"recipes/{recipe_id}/information"
        params = {
            "apiKey": self.api.api_key  # Uses the API key from the API instance
        }
        response = self.api.make_request(endpoint, params=params)
        if not response:
            raise ValueError("API response is empty or invalid.")  # # ValueError for empty or invalid responses
        return response

    @log_function_call
    @handle_errors
    def find_random_recipes(self):
        endpoint = "recipes/random"
        params = {
            "number": 10,
            "apiKey": self.api.api_key  # Uses the API key from the API instance
        }
        response = self.api.make_request(endpoint, params=params)
        if "recipes" in response:
            return response["recipes"]
        else:
            print("Unexpected response format:", response)  # Resolves unexpected response formats
            return []
