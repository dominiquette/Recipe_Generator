# ===== Importing methods from files ===========
from .decorators import log_function_call, handle_errors


# ===== Menu Display Handling ===========

# Menu class that handles displaying and managing the menu options
class MenuDisplay:
    def __init__(self):
        # Displaying options
        # Creates an instance of main menu items with options for the user to choose
        self.main_menu_items = [
            "[1] Get recipes based on ingredients",
            "[2] Get random recipes",
            "[3] View recipe categories",
            "[4] View your saved recipes",
            "[5] Export saved recipes to Excel",
            "[6] Exit"
        ]
        # Creates an instance of category menu items for recipe categories
        self.category_menu_items = [
            "[1] Quick Snacks Recipes",
            "[2] Vegan or Vegetarian Recipes",
            "[3] Fish Recipes",
            "[4] Chicken Recipes",
            "[5] Beef Recipes",
            "[6] Lamb Recipes",
            "[7] Pork Recipes",
            "[8] Dessert Recipes",
            "[9] Back to Main Menu"
        ]
        # Creates an instance of category mapping
        self.category_mapping = {
            '1': 'snacks',
            '2': 'veg',
            '3': 'fish',
            '4': 'chicken',
            '5': 'beef',
            '6': 'lamb',
            '7': 'pork',
            '8': 'dessert'
        }

    # Method to display a menu with a formatted title and a list of menu items
    # decorated with logging and error handling
    @log_function_call
    @handle_errors
    def display_menu(self, menu_items, title):
        if title is None:
            title = ""
        # Define the width of the box, including borders
        width = 44

        # Create the top border of the menu
        print("\n\t╔" + "═" * (width - 2) + "╗")
        # Print the title inside the box, adjusting it to the width
        print(f"\t║ {title.ljust(width - 4)} ║")
        # Creates a dividing line between the title and the menu items
        print("\t╠" + "═" * (width - 2) + "╣")

        # Loopa through each menu item and prints it within the box, padded to fit the width
        for item in menu_items:
            print(f"\t║ {item.ljust(width - 4)} ║")

        # Create the bottom border
        print("\t╚" + "═" * (width - 2) + "╝")


# Recipe class handles getting the list of ingredients and displaying it
# Interacts with the RecipeFinder to get the recipes from the API
class RecipeDisplay:
    def __init__(self, get_recipe):
        # Creates an instance of the recipe_finder class
        self.get_recipe = get_recipe

    # Method to display the list of recipes with ingredients and instructions
    # decorated with logging and error handling
    @log_function_call
    @handle_errors
    def display_recipes(self, recipes, by_ingredients=True):

        # Checks if the recipes list is empty and prints a message if no recipes are found
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
                # Extract and print missing ingredients
                missed_ingredients = [ingredient['name'] for ingredient in recipe.get('missedIngredients', [])]

                print(f"\33[1mUsed ingredients:\33[0m")
                for ingredient in used_ingredients:
                    # Prints each used ingredient with an inline point
                    print(f" - {ingredient}")

                print(f"\n\33[1mMissing ingredients:\33[0m")
                for ingredient in missed_ingredients:
                    # Prints each missing ingredient with an inline point
                    print(f" - {ingredient}")

            # Extract and display recipe instructions and ingredients
            recipe_info = self.get_recipe.find_recipe_details(recipe['id'])
            extended_ingredients = recipe_info.get('extendedIngredients', [])

            if extended_ingredients:
                # Print the list of all ingredients needed for the recipe
                print(f"\n\33[1mIngredients:\33[0m")

                for ingredient in extended_ingredients:
                    # Display ingredients in their original form
                    print(f" - {ingredient['original']}")
            else:
                # If no ingredients found, prints message
                print("No ingredients available.")

            # Extract and display step-by-step cooking instructions
            instructions = recipe_info.get('analyzedInstructions', [])

            if instructions:
                print("\n\33[4m\33[1mInstructions:\33[0m")

                for step in instructions[0]['steps']:
                    # Print each step with its number
                    print(f"Step {step['number']}: {step['step']}")
            else:
                # If no instructions found, prints message
                print("No instructions available.")

                # Print a separator line for readability
                print('-' * 100)

    # Method that handles displaying the saved recipes, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def display_saved_recipes(self, saved_recipes):

        # Check if dictionary is empty and prints message
        if not saved_recipes:
            print("No saved recipes.")
            return

        # Prints header for the saved recipes section
        print("\n\33[33m\33[40m\33[1mHere are your saved recipes:\33[0m")

        # Loop through saved recipes, grouped by category
        # Items() is used to iterate over key-value pairs
        for category, title in saved_recipes.items():
            # Print each category and the corresponding saved recipe titles, separated by commas
            print(f"\33[1m - Saved Recipes by {category}:\33[0m {', '.join(title)}")

        # Print a separator line for readability
        print('-' * 100)
