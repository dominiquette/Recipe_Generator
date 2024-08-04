# ===== Importing Libraries ===========
import requests


# ===== Functions ===========
def get_user_ingredients():
    ingredients = input("\nEnter the ingredients you have, separated by commas: ")
    return [ingredient.strip() for ingredient in ingredients.split(',')]


def fetch_recipes_by_ingredients(ingredients):
    api_key = "2755959e24c244f78ce2db67c59fd067"
    endpoint = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients),
        "number": 10,  # Number of recipes to return
        "apiKey": api_key
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching recipes: {e}")
        return []


def fetch_recipes_by_category(category):
    api_key = "2755959e24c244f78ce2db67c59fd067"
    endpoint = f"https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "type": category,
        "number": 10,  # Number of recipes to return
        "apiKey": api_key
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
    api_key = "2755959e24c244f78ce2db67c59fd067"
    endpoint = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": api_key
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching recipe instructions: {e}")
        return {}


def display_recipes(recipes, by_ingredients=True):
    if not recipes:
        print("No recipes found.")
        return

    for recipe in recipes:
        print(f"\n\33[33m\33[40m\33[1mRECIPE: {recipe['title']} \33[0m\n")

        if by_ingredients:
            used_ingredients = [ingredient['name'] for ingredient in recipe.get('usedIngredients', [])]
            missed_ingredients = [ingredient['name'] for ingredient in recipe.get('missedIngredients', [])]
            print(f"\33[1mUsed ingredients:\33[0m {', '.join(used_ingredients)}")
            print(f"\33[1mMissing ingredients:\33[0m {', '.join(missed_ingredients)}")
        else:
            ingredients = [ingredient['name'] for ingredient in recipe.get('extendedIngredients', [])]
            print(f"Ingredients: {', '.join(ingredients)}")

        recipe_info = fetch_recipe_instructions(recipe['id'])
        instructions = recipe_info.get('analyzedInstructions', [])
        if instructions:
            print("\n\33[4m\33[1mInstructions:\33[0m")
            for step in instructions[0]['steps']:
                print(f"Step {step['number']}: {step['step']}")
        else:
            print("No instructions available.")

        print('-' * 100)


def fetch_random_recipes():
    api_key = "2755959e24c244f78ce2db67c59fd067"
    endpoint = "https://api.spoonacular.com/recipes/random"
    params = {
        "number": 10,  # Number of random recipes to return
        "apiKey": api_key
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


welcome_message = """
·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
    🧄🍲🍎 Welcome to Group 5 Recipe generator 🍉🍰🥕
·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚ ‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
"""

print(welcome_message)

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

while True:
    display_menu(main_menu_items, "Main Menu")
    choice = input("\nPlease enter your choice: ")

    if choice == '1':
        ingredients = get_user_ingredients()
        recipes = fetch_recipes_by_ingredients(ingredients)
        display_recipes(recipes, by_ingredients=True)
    elif choice == '2':
        recipes = fetch_random_recipes()
        display_recipes(recipes, by_ingredients=False)
    elif choice == '3':
        while True:
            display_menu(category_menu_items, "Recipe Categories")
            category_choice = input("\nPlease select a category: ")

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

            if category_choice in category_mapping:
                category = category_mapping[category_choice]
                recipes = fetch_recipes_by_category(category)
                display_recipes(recipes, by_ingredients=False)
            elif category_choice == '9':
                break  # Back to main menu
            else:
                print("Invalid choice. Please try again.")
    elif choice == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")