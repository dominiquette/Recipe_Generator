# ===== Importing Libraries ===========
# Importing the requests library to handle HTTP requests
import requests


# ===== Importing data from files ===========
# Importing the Spoonacular API key from a separate config file
from config import api_key


# ===== Establish API connection ===========
# Define a class to handle API interactions
class APIClient:
    # Initialize the APIClient with a base URL and API key
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    # Methods to get headers for the API request
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    # Method to make a GET request to the API
    def make_request(self, endpoint, params=None):
        url = f'{self.base_url}/{endpoint}'   # Construct the full URL
        headers = self.get_headers()   # Get the headers for the request
        response = requests.get(url, headers=headers, params=params)   # Make the GET request
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()   # Return the response as JSON


# ===== API Functions ===========


def fetch_recipes_by_ingredients(ingredients):
    endpoint = "https://api.spoonacular.com/recipes/findByIngredients"   # API endpoint
    params = {
        "ingredients": ",".join(ingredients),   # Join ingredients into a comma-separated string
        "number": 10,  # Number of recipes to return
        "ranking": 2,  # Rank by minimizing missing ingredients
        "ignorePantry": True,  # Ignore common pantry ingredients
        "apiKey": api_key   # API key for authentication
    }
    try:
        response = requests.get(endpoint, params=params)   # Make the GET request with parameters
        response.raise_for_status()   # Raise an exception for HTTP errors
        return response.json()   # Return the response as JSON
    except requests.RequestException as e:  # Handle request exceptions
        print(f"Error fetching recipes: {e}")
        return []


# Function to fetch recipes based on category
def fetch_recipes_by_category(category):
    endpoint = "https://api.spoonacular.com/recipes/complexSearch"   # API endpoint
    params = {
        "number": 10,  # Number of recipes to return
        "apiKey": api_key
    }

    # Adjust the parameters based on the selected category
    if category in ["vegan", "vegetarian", "gluten free", "ketogenic"]:
        params["diet"] = category   # Set diet parameter for specific diets
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

    try:
        response = requests.get(endpoint, params=params)   # Make the GET request with parameters
        response.raise_for_status()   # Raise an exception for HTTP errors
        data = response.json()    # Return the response as JSON
        return data.get("results", [])
    except requests.RequestException as e:   # Handle request exceptions
        print(f"Error fetching recipes: {e}")
        return []


# Function to fetch detailed step-by-step recipe instructions
def fetch_recipe_instructions(recipe_id):
    endpoint = f"https://api.spoonacular.com/recipes/{recipe_id}/information" # API endpoint
    params = {
        "apiKey": api_key
    }
    try:
        response = requests.get(endpoint, params=params)    # Make the GET request with parameters
        response.raise_for_status()   # Raise an exception for HTTP errors
        return response.json()   # Return the response as JSON
    except requests.RequestException as e:   # Handle request exceptions
        print(f"Error fetching recipe instructions: {e}")
        return {}


# Function to fetch random recipes
def fetch_random_recipes():
    endpoint = "https://api.spoonacular.com/recipes/random"   # API endpoint
    params = {
        "number": 10,  # Number of random recipes to return
        "apiKey": appid
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if "recipes" in data:
            return data["recipes"]   # Return the list of recipes
        else:
            print("Unexpected response format:", data)
            return []
    except requests.RequestException as e:   # Handle request exceptions
        print(f"Error fetching random recipes: {e}")
        return []


# ===== Displaying functions ===========
# Function to display a menu with a title and items
def display_menu(menu_items, title):
    # Define the width of the box, including borders
    width = 44

    # Create the top border
    print("\n\t╔" + "═" * (width - 2) + "╗")
    print(f"\t║ {title.ljust(width - 4)} ║")
    print("\t╠" + "═" * (width - 2) + "╣")

    # Print each menu item, padded to fit the box width
    for item in menu_items:
        print(f"\t║ {item.ljust(width - 4)} ║")

    # Create the bottom border
    print("\t╚" + "═" * (width - 2) + "╝")


# ===== Displaying options ===========
# Main menu items to display
main_menu_items = [
    "[1] Get recipes based on ingredients",
    "[2] Get random recipes",
    "[3] View Recipe Categories",
    "[4] Exit"
]

# Category menu items to display
category_menu_items = [
    "[1] Vegan Recipes",
    "[2] Vegetarian Recipes",
    "[3] Gluten-Free Recipes",
    "[4] Fish Recipes",
    "[5] Chicken Recipes",
    "[6] Beef Recipes",
    "[7] Lamb Recipes",
    "[8] Pork Recipes",
    "[9] Duck Recipes",
    "[10] Desserts",
    "[11] Salad Recipes",
    "[12] Keto Recipes",
    "[13] Back to Main Menu"
]

# Mapping category menu selections to API parameters
category_mapping = {
    '1': 'vegan',
    '2': 'vegetarian',
    '3': 'gluten free',
    '4': 'fish',
    '5': 'chicken',
    '6': 'beef',
    '7': 'lamb',
    '8': 'pork',
    '9': 'duck',
    '10': 'dessert',
    '11': 'salad',
    '12': 'ketogenic'
}