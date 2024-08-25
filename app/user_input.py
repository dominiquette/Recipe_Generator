# ===== Importing methods from files ===========
from .decorators import log_function_call, handle_errors


# UserInput class handles getting the user's input
class UserInput:
    def __init__(self):
        """
        Initialize the UserInput object and prompt for the user's name upon creation.
        """
        self.name = self.get_name()

    @log_function_call
    @handle_errors
    def get_name(self):
        """
        Prompt the user for their name and validate the input.

        Returns:
            str: The user's name.

        Raises:
            ValueError: If the input is empty.
        """
        name = input("What's your name? ").strip()

        if not name:
            raise ValueError("Name cannot be empty. Please enter your name again.")

        return name

    @log_function_call
    @handle_errors
    def get_user_ingredients(self):
        """
        Prompt the user for a list of ingredients, separated by commas.

        Returns:
            list: A list of ingredients with leading and trailing whitespace removed.
        """
        ingredients = input("\nPlease enter the ingredients you have, separated by commas: ").strip()
        return [ingredient.strip() for ingredient in ingredients.split(',')]

    @log_function_call
    @handle_errors
    def get_save_recipe_choice(self):
        """
        Prompt the user whether they want to save a recipe.

        Returns:
            bool: True if the user chooses 'Y', False if 'N'.

        Notes:
            If the input is invalid, the user will be prompted again.
        """
        save_choice = input("\nWould you like to save any of these recipes (Y/N)? ").strip().upper()

        if save_choice == 'Y':
            return True
        elif save_choice == 'N':
            return False
        else:
            print("Invalid choice. Please enter 'Y' or 'N'.")
            return self.get_save_recipe_choice()

    @log_function_call
    @handle_errors
    def get_choice(self, prompt):
        """
        Prompt the user for a choice with a custom prompt message.

        Args:
            prompt (str): The prompt message to display to the user.

        Returns:
            str: The user's choice.

        Notes:
            Continuously prompts until a non-empty input is provided.
        """
        while True:
            choice = input(prompt).strip()

            if not choice:
                print("Input cannot be empty. Please try again.")
                continue

            return choice