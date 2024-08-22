# ===== Importing data from files ===========
from user_input import UserInput
from display import MenuDisplay, RecipeDisplay
from recipe_saver import SaveRecipe
from app import RecipeFinder, SpoonacularAPI
from config import api_key
from decorators import log_function_call, handle_errors  # Import the decorators


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

    # Method that runs the application
    @log_function_call  # Log when the run method starts and ends
    @handle_errors  # Handle any exceptions uniformly
    def run(self):
        print(self.welcome_message)
        while True:
            try:
                self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
                choice = self.user.get_choice("\nWhat would you like to do? ").strip()

                if choice == '1':
                    ingredients = self.user.get_user_ingredients()
                    recipes = self.get_recipe.find_recipes_by_ingredients(ingredients)
                    # if there is no API key in config.py, will return to main menu
                    if recipes is None:
                        print("\nReturning to main menu...")
                        continue
                    self.show_recipe.display_recipes(recipes, by_ingredients=True)
                    ingredients_titles = [recipe['title'] for recipe in recipes]

                    if self.user.get_save_recipe_choice():
                        self.saved_recipes.save_recipes(ingredients_titles, 'Ingredients')

                elif choice == '2':
                    recipes = self.get_recipe.find_random_recipes()
                    if recipes is None:
                        print("\nReturning to main menu...")
                        continue
                    self.show_recipe.display_recipes(recipes, by_ingredients=False)
                    random_titles = [recipe['title'] for recipe in recipes]

                    if self.user.get_save_recipe_choice():
                        self.saved_recipes.save_recipes(random_titles, 'Random')

                elif choice == '3':
                    while True:
                        self.menu.display_menu(self.menu.category_menu_items, "Recipe Categories")
                        category_choice = self.user.get_choice("\nPlease select a category: ").strip()

                        if category_choice in self.menu.category_mapping:
                            category = self.menu.category_mapping[category_choice]
                            recipes = self.get_recipe.find_recipes_by_category(category)
                            if recipes is None:
                                print("\nReturning to main menu...")
                                break
                            self.show_recipe.display_recipes(recipes, by_ingredients=False)
                            category_titles = [recipe['title'] for recipe in recipes]

                            if self.user.get_save_recipe_choice():
                                self.saved_recipes.save_recipes(category_titles, category)

                        elif category_choice == '9':
                            break  # Back to main menu
                        else:
                            print("Invalid choice. Please try again.")

                elif choice == '4':
                    # Calls the display_saved_recipes function and passing the get_saved_recipes function as an argument
                    self.show_recipe.display_saved_recipes(self.saved_recipes.get_saved_recipes())

                elif choice == '5':
                    print("Thank you for using our recipe app, goodbye!")
                    exit()  # Terminates the program execution

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
    app = App().run()
