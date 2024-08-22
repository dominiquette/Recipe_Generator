# ===== Importing methods and classes from files ===========
from user_input import UserInput
from display import MenuDisplay, RecipeDisplay
from recipe_saver import SaveRecipe
from app import RecipeFinder, SpoonacularAPI, RecipeDetails
from config import api_key
from decorators import log_function_call, handle_errors
from output import RecipeExporter


# App class is the main application class, handles running the application
class App:
    def __init__(self):
        # Creates an instance of the user class
        # The get_name method is called here as it is instantiated and called in the user class init method
        self.user = UserInput()
        # Initialise a welcome message as a string
        self.welcome_message = f"""
        ·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
        🧄🍲🍎 Welcome {self.user.name}, to Group 5 Recipe Generator 🍉🍰🥕 
        ·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚ ‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
        """
        # Creates an instance of the Menu class
        self.menu = MenuDisplay()
        # Creates a local instance of the SpoonacularAPI class
        api = SpoonacularAPI("https://api.spoonacular.com", api_key)
        # Creates an instance of the RecipeFinder class, passing the api instance
        self.get_recipe = RecipeFinder(api)
        # Creates an instance of the Recipe class, passing the get_recipe instance
        self.show_recipe = RecipeDisplay(self.get_recipe)
        # Creates an instance of the SaveRecipe class
        self.saved_recipes = SaveRecipe()
        # Creates an instance of RecipeDetails class, passing the api instance and recipe_finder
        self.recipe_details = RecipeDetails(api, self.get_recipe)
        # Creates an instance of RecipeExporter class, passing recipe_details and saved_recipes instances
        self.recipe_exporter = RecipeExporter(self.recipe_details, self.saved_recipes)

    # Method that runs the application
    @log_function_call  # Log when the run method starts and ends
    @handle_errors  # Handle any exceptions uniformly
    def run(self):
        print(self.welcome_message)
        # Starts an infinite loop for the main menu that will run until you explicitly exit the programme
        while True:
            try:
                # Displays the main menu options to the user
                self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
                # Prompts the user for their menu choice and removes any whitespace
                choice = self.user.get_choice("\nWhat would you like to do? ").strip()

                # Option 1: Find recipes by ingredients
                if choice == '1':
                    # Gets a list of ingredients from the user
                    ingredients = self.user.get_user_ingredients()
                    # Find recipes using the provided ingredients by calling API connected methods
                    recipes = self.get_recipe.find_recipes_by_ingredients(ingredients)

                    # If the API call fails, return to main menu
                    if recipes is None:
                        print("\nReturning to main menu...")
                        continue

                    # Display the recipes found using the ingredients
                    self.show_recipe.display_recipes(recipes, by_ingredients=True)
                    # Get the recipe titles from the list of recipes
                    ingredients_titles = [recipe['title'] for recipe in recipes]

                    # Asks the user if they want to save the recipes
                    if self.user.get_save_recipe_choice():
                        # Saves the recipe name under the category 'Ingredients'
                        self.saved_recipes.save_recipes(ingredients_titles, 'Ingredients')

                # Option 2: Find random recipes
                elif choice == '2':
                    # Finds random recipes using the API
                    recipes = self.get_recipe.find_random_recipes()

                    # If the API call fails, return to main menu
                    if recipes is None:
                        print("\nReturning to main menu...")
                        continue

                    # Display the randomly found recipes
                    self.show_recipe.display_recipes(recipes, by_ingredients=False)
                    # Get the recipe titles from the random recipes
                    random_titles = [recipe['title'] for recipe in recipes]

                    # Asks the user if they want to save the recipes
                    if self.user.get_save_recipe_choice():
                        # Saves the random recipe name under the category 'Random'
                        self.saved_recipes.save_recipes(random_titles, 'Random')

                # Option 3: Find recipes by category
                elif choice == '3':
                    # Starts a loop for category selection
                    while True:
                        # Display the category menu options to the user
                        self.menu.display_menu(self.menu.category_menu_items, "Recipe Categories")
                        # Prompts the user for their category choice and removes any whitespace
                        category_choice = self.user.get_choice("\nPlease select a category: ").strip()

                        # Checks if the user's choice is a valid category
                        if category_choice in self.menu.category_mapping:
                            # Maps the user's choice to a recipe category
                            category = self.menu.category_mapping[category_choice]
                            # Finds recipes based on the chosen category
                            recipes = self.get_recipe.find_recipes_by_category(category)

                            # If the API call fails, return to main menu
                            if recipes is None:
                                print("\nReturning to main menu...")
                                # Exits the category selection loop and goes back to main menu
                                break

                            # Display the recipes found for the selected category
                            self.show_recipe.display_recipes(recipes, by_ingredients=False)
                            # Gets the recipe name from the list of category recipes
                            category_titles = [recipe['title'] for recipe in recipes]

                            # Asks the user if they want to save the recipes
                            if self.user.get_save_recipe_choice():
                                # Save the category recipe name under the category name
                                self.saved_recipes.save_recipes(category_titles, category)

                        # Option to go back to the main menu from category selection
                        elif category_choice == '9':
                            break

                        # Handles invalid category choices
                        else:
                            print("Invalid choice. Please try again.")

                # Option 4: Display saved recipes
                elif choice == '4':
                    # Displays saved recipes
                    self.show_recipe.display_saved_recipes(self.saved_recipes.get_saved_recipes())

                # Option 5: Exports saved recipes to an Excel file
                elif choice == '5':
                    self.recipe_exporter.export_to_excel('saved_recipes.xlsx')

                # Option 6: Exit the programme
                elif choice == '6':
                    print("Thank you for using our recipe app, goodbye!")
                    # Terminates the program execution
                    exit()

                # Handles invalid menu choices
                else:
                    print("Invalid choice. Please try again.")

            except ValueError as ve:
                print(f"Value error occurred: {ve}")  # Resolves specific ValueError
            except KeyError as ke:
                print(f"Invalid key used: {ke}")  # Resolves specific KeyError
            except Exception as e:
                print(f"An unexpected error occurred: {e}")  # Accounts for any other unexpected errors


# ===== Main ===========
if __name__ == "__main__":
    # Initialises an instance of the App class and calls the run() method to start the application
    app = App().run()
