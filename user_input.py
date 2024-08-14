# User class handles getting the user's info and calls the method to initialise the name attribute
# This way the prompt will always happen and the object (User) will have a name attribute set at the start
class UserInput:
    def __init__(self):
        self.name = self.get_name()

    def get_name(self):
        name = input("What's your name? ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")  # Uses ValueError for empty names
        return name


    def get_user_ingredients(self):
        try:
            ingredients = input("\nPlease enter the ingredients you have, separated by commas: ").strip()
            # Returns the string as a list, so it can be passed correctly to the Spoonacular API
            return [ingredient.strip() for ingredient in ingredients.split(',')]
        except ValueError as ve:
            print(f"Error retrieving user's ingredients: {ve}")  # Resolves specific ValueError
            return []
        except Exception as e:
            print(f"Error retrieving user's ingredients: {e}")  # Accounts for other unexpected errors
            return []


    # Function that handles prompting the user to select if they want to save a recipe
    def get_save_recipe_choice(self):
        # Prompts the user for an input. strip() removes whitespaces and upper() turns the string to uppercase
        save_choice = input("\nWould you like to save any of these recipes (Y/N)? ").strip().upper()

        # If user input is Y then return True, if input is N then return False
        if save_choice == 'Y':
            return True
        elif save_choice == 'N':
            return False
        else:
            # If neither, print error message
            print("Invalid choice. Please enter 'Y' or 'N'.")
            # Recursively call the method until user has given valid input
            # Returns the boolean value
            return self.get_save_recipe_choice()


    # Prompts the user to input their choice
    def get_choice(self, prompt):
        while True:
            try:
                choice = input(prompt).strip()
                if not choice:
                    raise ValueError("Input cannot be empty.")  # ValueError for empty input
                return choice
            except ValueError as ve:
                print(f"Error getting the user's choice: {ve}")  # Resolves specific ValueError
            except Exception as e:
                print(f"Unexpected error occurred: {e}")  # Accounts for other unexpected errors

