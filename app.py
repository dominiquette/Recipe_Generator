# ===== Importing Libraries ===========
import requests

# ===== Importing data from files ===========
from config import appid


# ===== Establish API connection ===========
class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
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


def fetch_recipes_by_ingredients(ingredients):
    endpoint = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients),
        "number": 10,  # Number of recipes to return
        "apiKey": appid
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching recipes: {e}")
        return []


def fetch_recipes_by_category(category):
    endpoint = f"https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "type": category,
        "number": 10,  # Number of recipes to return
        "apiKey": appid
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        print(f"Error fetching recipes: {e}")
        return []


def fetch_recipe_instructions(recipe_id):

    endpoint = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": appid
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching recipe instructions: {e}")
        return {}


def fetch_random_recipes():
    endpoint = "https://api.spoonacular.com/recipes/random"
    params = {
        "number": 10,  # Number of random recipes to return
        "apiKey": appid
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if "recipes" in data:
            return data["recipes"]
        else:
            print("Unexpected response format:", data)
            return []
    except requests.RequestException as e:
        print(f"Error fetching random recipes: {e}")
        return []


# ===== Displaying functions ===========
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
main_menu_items = [
    "[1] Get recipes based on ingredients",
    "[2] Get random recipes",
    "[3] View Recipe Categories",
    "[4] Exit"
]

category_menu_items = [
    "[1] Vegan Recipes",
    "[2] Vegetarian Recipes",
    "[3] Gluten-Free Recipes",
    "[4] Fish Recipes",
    "[5] Meat Recipes",
    "[6] Desserts",
    "[7] Healthy Snacks",
    "[8] Raw Fruit and Veg Recipes",
    "[9] Back to Main Menu"
]

category_mapping = {
    '1': 'vegan',
    '2': 'vegetarian',
    '3': 'gluten free',
    '4': 'fish',
    '5': 'meat',
    '6': 'dessert',
    '7': 'healthy',
    '8': 'raw'
}

