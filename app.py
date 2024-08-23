# ===== Importing Libraries ===========
# Used to make HTTP requests to the API
import requests
# Used to create abstract base classes
from abc import abstractmethod

# ===== Importing data from files ===========
from decorators import log_function_call, handle_errors


# ===== Establish API connection ===========

# SpoonacularAPI class handles making requests to the API
class SpoonacularAPI:
    def __init__(self, base_url, api_key):
        # Creates an instance of the base URL
        self.base_url = base_url
        # Creates an instance of the API key
        self.api_key = api_key

    # Method that handles the requests to the API, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def make_request(self, endpoint, params=None):
        # Constructs the complete API endpoint URL
        url = f'{self.base_url}/{endpoint}'
        # Makes a GET request to the API with the provided URL and parameters
        response = requests.get(url, params=params)
        # Raises an exception for HTTP errors
        response.raise_for_status()
        # Return the JSON response
        return response.json()


# RecipeFinder class handles getting recipes from the API
class RecipeFinder:
    def __init__(self, api):
        # Creates an instance of the API class to make requests
        self.api = api

    # Method that handles making a recipe request by ingredients, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def find_recipes_by_ingredients(self, ingredients):
        # Define the API endpoint for searching recipes by ingredients
        endpoint = "recipes/findByIngredients"
        # Define the parameters for the API request
        params = {
            "ingredients": ingredients,
            "number": 5,  # Number of recipes to return
            "ranking": 2,  # Minimises missing ingredients
            "apiKey": self.api.api_key,  # Uses the stored API key for authentication
            "ignorePantry": "true"  # Ignore common pantry items
        }

        # Make the API request and store the response
        response = self.api.make_request(endpoint, params=params)

        # ValueError for empty or invalid responses
        if not response:
            raise ValueError("API response is empty or invalid.")

        # Return the response from the API
        return response

    # Method that handles making a recipe request by category, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def find_recipes_by_category(self, category):
        # Define the API endpoint for searching recipes by category
        endpoint = "recipes/complexSearch"
        # Define common parameters for the API request
        common_params = {
            "number": 5,  # Number of recipes to return
            "apiKey": self.api.api_key,  # Uses the stored API key for authentication
            "sort": "random",  # Shows different results each time
            "ignorePantry": "true"  # Ignore common pantry items
        }

        # Use CategoryMapping to get category-specific options based on user input
        get_categories = CategoryMapping.get_category(category)
        # If category mapping exists, set parameters accordingly
        if get_categories:
            params = get_categories.set_params(common_params)
        else:
            # If no category-specific options, use the common parameters
            params = common_params

        # Make the API request and store the response
        response = self.api.make_request(endpoint, params=params)

        # ValueError for empty or invalid responses
        if not response:
            raise ValueError("API response is empty or invalid.")
        return response.get("results", [])

    # Method that handles making a recipe request by random search, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def find_random_recipes(self):
        # Define the API endpoint for retrieving random recipes
        endpoint = "recipes/random"
        # Define the parameters for the API request
        params = {
            "number": 5,  # Number of recipes to return
            "apiKey": self.api.api_key  # Uses the stored API key for authentication
        }

        # Make the API request and store the response
        response = self.api.make_request(endpoint, params=params)

        # Check if the response contains a "recipes" key and return its value
        if "recipes" in response:
            return response["recipes"]
        else:
            # Print an error message if the response format is unexpected
            print("Unexpected response format:", response)
            return []

    # Method that handles getting all recipe information, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def find_recipe_details(self, recipe_id):
        # Define the API endpoint for retrieving all recipe information
        endpoint = f"recipes/{recipe_id}/information"
        # Define the parameters for the API request
        params = {
            "apiKey": self.api.api_key  # Uses the stored API key for authentication
        }

        # Make the API request and store the response
        response = self.api.make_request(endpoint, params=params)

        # ValueError for empty or invalid responses
        if not response:
            raise ValueError("API response is empty or invalid.")
        return response


# RecipeDetails class retrieves and formats recipe ingredients and instructions for output
class RecipeDetails:
    def __init__(self, api, get_recipe):
        # Store instances of the API and RecipeFinder classes
        self.api = api
        self.get_recipe = get_recipe

    # Method that searches a recipe by title and return the ID, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def find_recipe_id(self, recipe_title):
        # Define the API endpoint for searching recipes by name
        endpoint = "recipes/complexSearch"
        # Define the parameters for the API request
        params = {
            "query": recipe_title,  # Search query is the recipe name
            "apiKey": self.api.api_key  # Use the stored API key for authentication
        }

        # Make the API request and store the response
        response = self.api.make_request(endpoint, params=params)

        # If no recipes were found, print error message
        if not response:
            print(f"No recipes found for title '{recipe_title}'")
            return None

        # Return the ID of the first recipe in the search results
        return response['results'][0]['id']

    # Method that uses the recipe ID to get the instructions and ingredients
    # decorated with logging and error handling
    @log_function_call
    @handle_errors
    def find_instructions_ingredients(self, recipe_title):
        # Find the recipe ID
        recipe_id = self.find_recipe_id(recipe_title)

        # If no recipe ID is found, raise an error
        if not recipe_id:
            raise ValueError(f'No ID found for {recipe_title}')

        # Get information of the recipe from find_recipe_details method
        api_response = self.get_recipe.find_recipe_details(recipe_id)

        # If the API response is empty, raise an error
        if not api_response:
            raise ValueError(f'No response from API for recipe ID: {recipe_id}')

        # Extract and format ingredients from the API response
        if 'extendedIngredients' in api_response:
            ingredients_list = []

            for ingredient in api_response['extendedIngredients']:
                # Get the name, amount, and unit of each ingredient
                name = ingredient.get('name', 'Unknown')
                amount = ingredient.get('amount', '')
                unit = ingredient.get('measures', {}).get('us', {}).get('unitShort', '')

                # Append the formatted ingredient to the list
                ingredients_list.append(f"{amount} {unit} {name}")
            # Join the list of ingredients into a single string
            ingredients = ", ".join(ingredients_list)
        else:
            ingredients = None
            # If no ingredients found, print message
            print("No ingredients found in the API response.")

        # Extract and format instructions from the API response
        if 'analyzedInstructions' in api_response and api_response['analyzedInstructions']:
            # Get step-by-step instructions
            instructions_steps = api_response['analyzedInstructions'][0]['steps']
            # Format instructions as numbered steps
            instructions = "\n".join([f"Step {step['number']}: {step['step']}" for step in instructions_steps])
        else:
            instructions = None
            # If no instructions found, print message
            print("No instructions found in the API response.")

        # Return the formatted ingredients and instructions
        return ingredients, instructions


# CategoryParams class handles the categories search, making it easy to add or remove categories
class CategoryParams:
    @abstractmethod
    # Abstract method that must be implemented by subclasses
    def set_params(self, common_params):
        pass


# Specific category classes that define parameters for different recipe types
class SnacksOption(CategoryParams):
    def set_params(self, common_params):
        # Filter for snack recipes
        common_params["type"] = "snack"
        # Filter for quick recipes (15 minutes or less)
        common_params["maxReadyTime"] = 15
        return common_params


class VegOption(CategoryParams):
    def set_params(self, common_params):
        # Filter for vegan or vegetarian recipes
        common_params["diet"] = "vegan|vegetarian"
        return common_params


class FishOption(CategoryParams):
    def set_params(self, common_params):
        # Filter for recipes that include fish as an ingredient
        common_params["includeIngredients"] = "fish"
        return common_params


class ChickenOption(CategoryParams):
    def set_params(self, common_params):
        # Filter for recipes that include chicken as an ingredient
        common_params["includeIngredients"] = "chicken"
        return common_params


class BeefOption(CategoryParams):
    def set_params(self, common_params):
        # Filter for recipes that include beef as an ingredient
        common_params["includeIngredients"] = "beef"
        return common_params


class LambOption(CategoryParams):
    def set_params(self, common_params):
        # Filter for recipes that include lamb as an ingredient
        common_params["includeIngredients"] = "lamb"
        return common_params


class PorkOption(CategoryParams):
    def set_params(self, common_params):
        # Filter for recipes that include pork as an ingredient
        common_params["includeIngredients"] = "pork"
        return common_params


class DessertOption(CategoryParams):
    def set_params(self, common_params):
        # Filter for dessert recipes
        common_params["type"] = "dessert"
        return common_params


# CategoryMapping class maps category names to specific category classes
class CategoryMapping:
    def get_category(category):
        # Dictionary mapping category names to corresponding category classes
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
        # Return the corresponding category class or None if the category is not found
        return categories.get(category, None)
