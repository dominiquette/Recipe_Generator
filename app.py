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
        response.raise_for_status()  # Raises an exception for HTTP errors
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

    @log_function_call
    @handle_errors
    def find_recipe_details(self, recipe_id):
        endpoint = f"recipes/{recipe_id}/information"
        params = {
            "apiKey": self.api.api_key  # Uses the API key from the API instance
        }
        response = self.api.make_request(endpoint, params=params)
        if not response:
            raise ValueError("API response is empty or invalid.")  # # ValueError for empty or invalid responses
        return response


class RecipeDetails:
    def __init__(self, api, get_recipe):
        # Creates an instance of the API
        self.api = api
        self.get_recipe = get_recipe

    # Function that searches a recipe by title and return the ID
    @log_function_call
    @handle_errors
    def find_recipe_id(self, recipe_title):
        endpoint = "recipes/complexSearch"
        params = {
            "query": recipe_title,
            "apiKey": self.api.api_key
        }
        response = self.api.make_request(endpoint, params=params)
        if not response:
            print(f"No recipes found for title '{recipe_title}'")
            return None

        return response['results'][0]['id']

    @log_function_call
    @handle_errors
    def find_instructions_ingredients(self, recipe_title):
        # Find the recipe ID
        recipe_id = self.find_recipe_id(recipe_title)
        if not recipe_id:
            raise ValueError(f'No ID found for {recipe_title}')

        # Get information of the recipe from find_recipe_details method
        api_response = self.get_recipe.find_recipe_details(recipe_id)
        if not api_response:
            raise ValueError(f'No response from API for recipe ID: {recipe_id}')

        # Extract and format ingredients
        if 'extendedIngredients' in api_response:
            ingredients_list = []
            for ingredient in api_response['extendedIngredients']:
                name = ingredient.get('name', 'Unknown')
                amount = ingredient.get('amount', '')
                unit = ingredient.get('measures', {}).get('us', {}).get('unitShort', '')
                ingredients_list.append(f"{amount} {unit} {name}")
            ingredients = ", ".join(ingredients_list)
        else:
            ingredients = None
            print("No ingredients found in the API response.")

        # Extract and format instructions
        if 'analyzedInstructions' in api_response and api_response['analyzedInstructions']:
            instructions_steps = api_response['analyzedInstructions'][0]['steps']
            instructions = "\n".join([f"Step {step['number']}: {step['step']}" for step in instructions_steps])
        else:
            instructions = None
            print("No instructions found in the API response.")

        return ingredients, instructions


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
