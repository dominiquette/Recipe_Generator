# ===== Importing methods and classes from files ===========
# Import necessary classes and functions from various modules for the application
from app.user_input import UserInput
from app.display import MenuDisplay, RecipeDisplay
from app.recipe_saver import SaveRecipe
from app.app import RecipeFinder, SpoonacularAPI, RecipeDetails
from app.config import api_key
from app.decorators import log_function_call, handle_errors
from app.output import RecipeExporter


# The App class serves as the entry point for the Recipe Generator application.
# It manages the application's flow, user interaction, and integrates with the API for recipe retrieval.
class App:
    def __init__(self):
        """Initializes the main components of the application."""
        # Instantiate the UserInput class to handle user interactions
        self.user = UserInput()

        # Welcome message customised for the user, displayed at the start of the application
        self.welcome_message = f"""
        ·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
        🧄🍲🍎 Welcome {self.user.name}, to Group 5 Recipe Generator 🍉🍰🥕 
        ·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚ ‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
        """

        # Instantiate the MenuDisplay class to manage menu-related displays
        self.menu = MenuDisplay()

        # Create an instance of SpoonacularAPI with the provided base URL and API key
        api = SpoonacularAPI("https://api.spoonacular.com", api_key)

        # Instantiate RecipeFinder to handle recipe search functionality
        self.get_recipe = RecipeFinder(api)

        # Instantiate RecipeDisplay to manage the display of found recipes
        self.show_recipe = RecipeDisplay(self.get_recipe)

        # Instantiate SaveRecipe to manage the saving of selected recipes
        self.saved_recipes = SaveRecipe()

        # Instantiate RecipeDetails to manage detailed recipe information retrieval
        self.recipe_details = RecipeDetails(api, self.get_recipe)

        # Instantiate RecipeExporter to handle exporting of saved recipes to an Excel file
        self.recipe_exporter = RecipeExporter(self.recipe_details, self.saved_recipes)

    # The run method is the core loop of the application.
    # It presents the user with options, processes their choices, and interacts with the various components of the app.
    @log_function_call
    @handle_errors
    def run(self):
        """Runs the main application loop."""
        print(self.welcome_message)

        # Infinite loop to keep the application running until the user decides to exit
        while True:
            # Display the main menu and prompt the user for their choice
            self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
            choice = self.user.get_choice("\nWhat would you like to do? ").strip()

            # Option 1: Find recipes by ingredients
            if choice == '1':
                # Get a list of ingredients from the user and find matching recipes
                ingredients = self.user.get_user_ingredients()
                recipes = self.get_recipe.find_recipes_by_ingredients(ingredients)

                # If no recipes are found, return to the main menu
                if recipes is None:
                    print("\nReturning to main menu...")
                    continue

                # Display found recipes and ask if the user wants to save them
                self.show_recipe.display_recipes(recipes, by_ingredients=True)
                ingredients_titles = [recipe['title'] for recipe in recipes]

                if self.user.get_save_recipe_choice():
                    # Save the selected recipes under the 'Ingredients' category
                    self.saved_recipes.save_recipes(ingredients_titles, 'Ingredients')

            # Option 2: Find random recipes
            elif choice == '2':
                # Finds random recipes using the API
                recipes = self.get_recipe.find_random_recipes()

                # If no recipes are found, return to the main menu
                if recipes is None:
                    print("\nReturning to main menu...")
                    continue

                # Display the random recipes and ask if the user wants to save them
                self.show_recipe.display_recipes(recipes, by_ingredients=False)
                random_titles = [recipe['title'] for recipe in recipes]

                if self.user.get_save_recipe_choice():
                    # Save the random recipes under the 'Random' category
                    self.saved_recipes.save_recipes(random_titles, 'Random')

            # Option 3: Find recipes by category
            elif choice == '3':
                # Loop to allow the user to select a category and find recipes accordingly
                while True:
                    self.menu.display_menu(self.menu.category_menu_items, "Recipe Categories")
                    category_choice = self.user.get_choice("\nPlease select a category: ").strip()

                    # If a valid category is selected, fetch recipes from that category
                    if category_choice in self.menu.category_mapping:
                        category = self.menu.category_mapping[category_choice]
                        recipes = self.get_recipe.find_recipes_by_category(category)

                        # If no recipes are found, return to the main menu
                        if recipes is None:
                            print("\nReturning to main menu...")
                            break

                        # Display the recipes found for the selected category and ask if the user wants to save them
                        self.show_recipe.display_recipes(recipes, by_ingredients=False)
                        # Gets the recipe name from the list of category recipes
                        category_titles = [recipe['title'] for recipe in recipes]

                        # Asks the user if they want to save the recipes
                        if self.user.get_save_recipe_choice():
                            # Save the category recipe name under the category name
                            self.saved_recipes.save_recipes(category_titles, category)

                    # Option to go back to the main menu
                    elif category_choice == '9':
                        break

                    # Handles invalid category choices
                    else:
                        print("Invalid choice. Please try again.")

            # Option 4: Display saved recipes
            elif choice == '4':
                # Display recipes that the user has previously saved
                self.show_recipe.display_saved_recipes(self.saved_recipes.get_saved_recipes())

            # Option 5: Exports saved recipes to an Excel file
            elif choice == '5':
                # Export the saved recipes to 'saved_recipes.xlsx'
                self.recipe_exporter.export_to_excel('saved_recipes.xlsx')

            # Option 6: Exit the program
            elif choice == '6':
                # Thanks the user and exit the program
                print("Thank you for using our recipe app, goodbye!")
                exit()

            # Handles invalid menu choices
            else:
                print("Invalid choice. Please try again.")


# ===== Main ===========
# This block ensures the application runs when executed as a script
if __name__ == "__main__":
    # Initialize the App class and start the application
    app = App().run()
