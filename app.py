# ===== Importing Libraries ===========
import requests

# ===== Importing data from files ===========
from config import api_key


# ===== Establish API connection ===========
# SpoonacularAPI class handles making requests to the API
class SpoonacularAPI:
    def __init__(self, base_url, api_key):
        # Creates an instance of the base URL
        self.base_url = base_url
        # Creates an instance of the API key imported from config
        self.api_key = api_key

    def make_request(self, endpoint, params=None):
        url = f'{self.base_url}/{endpoint}'
        try:  # Try-Except Block for any HTTP and network errors
            response = requests.get(url, params=params)
            response.raise_for_status()  # # Raises an exception for HTTP errors
            return response.json()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Resolves specific HTTP errors
        except requests.RequestException as request_error:
            print(f"Request error occurred: {request_error}")  # Resolves general request errors
        except Exception as e:
            print(f"An issue occurred while connecting to the Spoonacular API:: {e}")
        return {}


# RecipeFinder class handles getting recipes from the API
class RecipeFinder:
    def __init__(self, api):
        # Creates an instance of the API
        self.api = api

    def find_recipes_by_ingredients(self, ingredients):
        endpoint = "recipes/findByIngredients"
        params = {
            "ingredients": ingredients,
            "number": 2,  # Number of recipes to return
            "ranking": 2,  # Minimises missing ingredients
            "apiKey": self.api.api_key,  # Uses the API key from the API instance
            "ignorePantry": "true"  # Ignore typical pantry items
        }
        try:  # Try-Except Block for API request errors
            response = self.api.make_request(endpoint, params=params)
            if not response:
                raise ValueError("API response is empty or invalid.")  # ValueError for empty or invalid responses
            return response
        except ValueError as value_error:
            print(f"Validation error: {value_error}")  # Resolves specific ValueError
        except requests.RequestException as request_error:
            print(f"Request error occurred: {request_error}")  # Resolves general request errors
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return []

    def find_recipes_by_category(self, category):
        endpoint = "recipes/complexSearch"
        params = {
            "type": category,
            "number": 2,
            "apiKey": api_key
        }
        try:
            response = self.api.make_request(endpoint, params=params)
            if not response:
                raise ValueError("API response is empty or invalid.")  # ValueError for empty or invalid responses
            return response.get("results", [])
        except ValueError as value_error:
            print(f"Validation error: {value_error}")  # Resolves specific ValueError
        except requests.RequestException as request_error:
            print(f"Request error occurred: {request_error}")  # Resolves general request errors
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return []

    def find_recipe_instructions(self, recipe_id):
        endpoint = f"recipes/{recipe_id}/information"
        params = {
            "apiKey": self.api.api_key  # Uses the API key from the API instance
        }
        try:  # Try-Except Block
            response = self.api.make_request(endpoint, params=params)
            if not response:
                raise ValueError("API response is empty or invalid.")  # # ValueError for empty or invalid responses
            return response
        except ValueError as value_error:
            print(f"Validation error: {value_error}")  # Resolves specific ValueError
        except requests.RequestException as request_error:
            print(f"Request error occurred: {request_error}")  # Resolves general request errors
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return {}

    def find_random_recipes(self):
        endpoint = "recipes/random"
        params = {
            "number": 2,
            "apiKey": self.api.api_key  # Uses the API key from the API instance
        }
        try:
            response = self.api.make_request(endpoint, params=params)
            if "recipes" in response:
                return response["recipes"]
            else:
                print("Unexpected response format:", response)  # Resolves unexpected response formats
                return []
        except requests.RequestException as request_error:
            print(f"Request error occurred: {request_error}")  # Resolves any errors that occur during HTTP requests
        except Exception as e:
            print(f"Error fetching random recipes: {e}")
        return []
