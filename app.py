# ===== Importing Libraries ===========
import requests
from abc import abstractmethod

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
            "number": 3,  # Number of recipes to return
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
        common_params = {
            "number": 3,
            "apiKey": self.api.api_key,
            "sort": "random",  # to show different results each time
            "ignorePantry": "true"  # Ignore typical pantry items
        }
        # interface segregation of categories in different classes
        get_categories = CategoryMapping.get_category(category)
        if get_categories:
            params = get_categories.set_params(common_params)
        else:
            params = common_params

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
            "number": 3,
            "apiKey": self.api.api_key  # Uses the API key from the API instance
        }
        response = self.api.make_request(endpoint, params=params)
        if "recipes" in response:
            return response["recipes"]
        else:
            print("Unexpected response format:", response)  # Resolves unexpected response formats
            return []


# a class to handle the categories search, we could easily add or remove categories
class CategoryParams:
    @abstractmethod
    def set_params(self, common_params):
        pass


class SnacksOption(CategoryParams):
    def set_params(self, common_params):
        common_params["type"] = "snack"
        common_params["maxReadyTime"] = 15
        return common_params


class VegOption(CategoryParams):
    def set_params(self, common_params):
        # the pipe means recipes that are vegan OR vegetarian
        common_params["diet"] = "vegan|vegetarian"
        return common_params


class FishOption(CategoryParams):
    def set_params(self, common_params):
        common_params["includeIngredients"] = "fish"
        return common_params


class ChickenOption(CategoryParams):
    def set_params(self, common_params):
        common_params["includeIngredients"] = "chicken"
        return common_params


class BeefOption(CategoryParams):
    def set_params(self, common_params):
        common_params["includeIngredients"] = "beef"
        return common_params


class LambOption(CategoryParams):
    def set_params(self, common_params):
        common_params["includeIngredients"] = "lamb"
        return common_params


class PorkOption(CategoryParams):
    def set_params(self, common_params):
        common_params["includeIngredients"] = "pork"
        return common_params


class DessertOption(CategoryParams):
    def set_params(self, common_params):
        common_params["type"] = "dessert"
        return common_params


class CategoryMapping:
    def get_category(category):
        categories = {
            "snacks": SnacksOption(),
            "veg": VegOption(),
            "fish": FishOption(),
            "chicken": ChickenOption(),
            "beef": BeefOption(),
            "lamb": LambOption(),
            "pork": PorkOption(),
            "dessert": DessertOption(),
        }
        return categories.get(category, None)
