# ===== Importing data from files ===========
from decorators import log_function_call, handle_errors


# ===== Menu class handles displaying menu options ===========

# Menu class that handles displaying and managing the menu options
class MenuDisplay:
    def __init__(self):
        # Displaying options
        # Creates an instance of main menu items
        self.main_menu_items = [
            "[1] Get recipes based on ingredients",
            "[2] Get random recipes",
            "[3] View recipe categories",
            "[4] View your saved recipes",
            "[5] Export saved recipes to Excel",
            "[6] Exit"
        ]
        # Creates an instance of category menu items
        self.category_menu_items = [
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
        # Creates an instance of category mapping
        self.category_mapping = {
            '1': 'vegan',
            '2': 'vegetarian',
            '3': 'gluten free',
            '4': 'fish',
            '5': 'meat',
            '6': 'dessert',
            '7': 'healthy',
            '8': 'raw'
        }

    @log_function_call
    @handle_errors
    def display_menu(self, menu_items, title):
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


# Recipe class handles getting the list of ingredients and displaying it
# Interacts with the RecipeFinder to get the recipes from the API
class RecipeDisplay:
    def __init__(self, get_recipe):
        self.get_recipe = get_recipe

    @log_function_call
    @handle_errors
    def display_recipes(self, recipes, by_ingredients=True):
        # Check if the recipes list is empty
        if not recipes:
            print("No recipes found.")
            return

        # Loop through each recipe in the list, printing their index before the name
        # Using index in displaying the recipes makes the option to save recipes by index user-friendly
        for index, recipe in enumerate(recipes, start=1):
            # Print the recipe title with styling for emphasis
            print(f"\n\33[33m\33[40m\33[1mRECIPE {index}: {recipe['title']} \33[0m\n")  # Black background, yellow font.

            if by_ingredients:
                # Extract and print used ingredients
                used_ingredients = [ingredient['name'] for ingredient in recipe.get('usedIngredients', [])]
                missed_ingredients = [ingredient['name'] for ingredient in recipe.get('missedIngredients', [])]
                print(f"\33[1mUsed ingredients:\33[0m")
                for ingredient in used_ingredients:
                    print(f" - {ingredient}")  # Prints inline points. Example: - Chicken
                print(f"\n\33[1mMissing ingredients:\33[0m")
                for ingredient in missed_ingredients:
                    print(f" - {ingredient}")

            # Fetch and display recipe instructions and ingredients
            recipe_info = self.get_recipe.find_recipe_details(recipe['id'])
            extended_ingredients = recipe_info.get('extendedIngredients', [])
            if extended_ingredients:
                # Print the list of all ingredients needed for the recipe
                print(f"\n\33[1mIngredients:\33[0m")
                for ingredient in extended_ingredients:
                    print(f" - {ingredient['original']}")
            else:
                print("No ingredients available.")

            # Extract and print step-by-step cooking instructions
            instructions = recipe_info.get('analyzedInstructions', [])
            if instructions:
                print("\n\33[4m\33[1mInstructions:\33[0m")
                for step in instructions[0]['steps']:
                    print(f"Step {step['number']}: {step['step']}")
            else:
                print("No instructions available.")

                # Print a separator line for readability
                print('-' * 100)

    # Function that handles displaying the saved recipes
    @log_function_call
    @handle_errors
    def display_saved_recipes(self, saved_recipes):
        # Check if dictionary is empty
        if not saved_recipes:
            print("No saved recipes.")
            return

        # Prints header
        print("\n\33[33m\33[40m\33[1mHere are your saved recipes:\33[0m")
        # Iterates over the categories connected to each recipe title in the dict
        # Items() is used to iterate over key-value pairs
        for category, title in saved_recipes.items():
            # Joins the recipe titles to one string separated by commas
            print(f"\33[1m - Saved Recipes by {category}:\33[0m {', '.join(title)}")

        # Print a separator line for readability
        print('-' * 100)
