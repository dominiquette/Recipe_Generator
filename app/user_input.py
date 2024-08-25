# ===== Importing methods from files ===========
from .decorators import log_function_call, handle_errors


# UserInput class handles getting the user's input
class UserInput:
    def __init__(self):
        # Automatically calls the get_name method to initialise the user's name upon object creation
        self.name = self.get_name()

    # Method that handles getting the user's name, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def get_name(self):
        # Prompts the user to input their name, and removes any whitespace
        name = input("What's your name? ").strip()

        # If name is empty, raises ValueError with a message
        if not name:
            raise ValueError("Name cannot be empty. Please enter your name again.")

        # Returns the user's name after validation
        return name

    # Method that handles getting the ingredients from the user, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def get_user_ingredients(self):
        # Prompts the user to input a list of ingredients, separated by commas
        ingredients = input("\nPlease enter the ingredients you have, separated by commas: ").strip()
        # Returns the string as a list with removed whitespaces, so it can be passed correctly to the Spoonacular API
        return [ingredient.strip() for ingredient in ingredients.split(',')]

    # Method that prompts the user to decide whether they want to save a recipe
    # decorated with logging and error handling
    @log_function_call
    @handle_errors
    def get_save_recipe_choice(self):
        # Prompts the user for a choice. Removes whitespaces and turns the string uppercase
        save_choice = input("\nWould you like to save any of these recipes (Y/N)? ").strip().upper()

        # Returns True if the user chooses 'Y' (yes), False if 'N' (no)
        if save_choice == 'Y':
            return True
        elif save_choice == 'N':
            return False
        else:
            # If an invalid input is given, prints error message
            print("Invalid choice. Please enter 'Y' or 'N'.")

            # Recursively call the method until user has given valid input
            # Returns the boolean value
            return self.get_save_recipe_choice()

    # Method that prompts the user for a generic choice, used in menu selection
    # decorated with logging and error handling
    @log_function_call
    @handle_errors
    def get_choice(self, prompt):
        # Continuously prompts the user for input until a valid value is provided
        while True:
            # Gets user input and removes whitespace
            choice = input(prompt).strip()

            # Checks if the input is empty, prints a message and re-prompts
            if not choice:
                print("Input cannot be empty. Please try again.")
                # Re-prompt the user
                continue

            # Return the inout
            return choice
