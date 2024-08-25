# ===== Importing Libraries ===========
# Importing deque for queue operations and defaultdict for dictionaries with default values
from collections import deque, defaultdict

# ===== Importing methods from files ===========
from .decorators import log_function_call, handle_errors


class SaveRecipe:
    def __init__(self):
        """
        Initialize the SaveRecipe instance with an empty dictionary.
        The dictionary's keys are categories, and the values are deques
        of recipe names under each category.
        """
        self.saved_recipes = defaultdict(deque)

    @log_function_call
    @handle_errors
    def save_recipes(self, recipe_names, category):
        """
        Save selected recipes to a specified category.

        Args:
            recipe_names (list): A list of recipe names.
            category (str): The category under which the recipes will be saved.

        This method displays the list of recipes with index numbers,
        prompts the user to select recipes by entering their indices,
        and then saves the selected recipes under the specified category.
        """
        # Display recipe names with indices
        for index, title in enumerate(recipe_names, start=1):
            print(f"[{index}] {title}")

        # Prompt user for recipe selection
        selected_recipes = input(
            "\nEnter the numbers of the recipes you want to save, separated by commas: ").strip().split(',')

        # Convert user input to a list of integers, stripping any extra whitespace
        selected_recipes = [int(recipe.strip()) for recipe in selected_recipes]

        # Validate and save selected recipes
        for recipe in selected_recipes:
            if 1 <= recipe <= len(recipe_names):
                # Append selected recipe to the appropriate category
                self.saved_recipes[category].append(recipe_names[recipe - 1])

        print("\nRecipes saved successfully!")

    @log_function_call
    @handle_errors
    def get_saved_recipes(self):
        """
        Retrieve the dictionary of saved recipes.

        Returns:
            dict: A dictionary where keys are recipe categories and values
                  are lists of saved recipe names under each category.
        """
        return dict(self.saved_recipes)
