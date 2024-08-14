# ===== Importing Libraries ===========
from collections import deque, defaultdict
# ===== Importing data from files ===========
from decorators import log_function_call, handle_errors


class SaveRecipe:
    def __init__(self):
        # Initializes an empty dictionary where the value will be a list of recipe names and the key is the category
        self.saved_recipes = defaultdict(deque)

    @log_function_call
    @handle_errors
    def save_recipes(self, recipe_names, category):
        # Loops through the recipe_names list, starting at index 1 so output does not start at 0
        # and prints the index next to the current title in the loop
        for index, title in enumerate(recipe_names, start=1):
            print(f"[{index}] {title}")

        # Prompts the user to enter which recipes they want to save
        # Removes whitespace and splits the string to a list
        selected_recipes = input(
            "\nEnter the numbers of the recipes you want to save, separated by commas: ").strip().split(',')

        # Converts the strings to integers and strips away whitespace
        selected_recipes = [int(recipe.strip()) for recipe in selected_recipes]

        # Loops through the list of integers, representing the recipes
        # and checks that the current recipe is within valid range
        for recipe in selected_recipes:
            if 1 <= recipe <= len(recipe_names):
                # If valid, the recipe name will be appended to the saved_recipes dictionary under specified category
                # We set the index back one as to adjust to Pythons zero-based index
                self.saved_recipes[category].append(recipe_names[recipe - 1])
        # Prints a success message when recipe is saved
        print("\nRecipes saved successfully!")

    @log_function_call
    @handle_errors
    def get_saved_recipes(self):
        # Returns saved recipes dict
        return dict(self.saved_recipes)
