# ===== Importing Libraries ===========
from app import RecipeFinder, SpoonacularAPI

# ===== Importing data from files ===========
from config import api_key
from display import Menu, Recipe


# User class handles getting the user's info and calls the method to initialise the name attribute
# This way the prompt will always happen and the object (User) will have a name attribute set at the start
class User:
    def __init__(self):
        self.name = self.get_name()

    def get_name(self):
        name = input("What's your name? ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")  # Uses ValueError for empty names
        print(f"Welcome to our console app, {name}! What do you need help with?")
        return name


# App class is the main application class, handles running the application
class App:
    def __init__(self):
        # Initialise a welcome message as a string
        self.welcome_message = """
        ·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
            🧄🍲🍎 Welcome to Group 5 Recipe Generator 🍉🍰🥕 
        ·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚ ‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
        """
        # Creates an instance of the User class
        # The get_name method is called here as it is instantiated and called in the User class __init__ method
        self.user = User()
        # Creates an instance of the Menu class
        self.menu = Menu()
        # Creates a local instance of the SpoonacularAPI class
        api = SpoonacularAPI("https://api.spoonacular.com", api_key)
        # Creates an instance of the RecipeFinder class, passing the api instance
        self.get_recipe = RecipeFinder(api)
        # Creates an instance of the Recipe class, passing the get_recipe instance
        self.recipe = Recipe(self.get_recipe)

    # Method that runs the application
    def run(self):
        print(self.welcome_message)

        while True:
            try:
                self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
                choice = self.menu.get_choice("\nPlease enter your choice: ").strip()

                if choice == '1':
                    ingredients = self.recipe.get_user_ingredients()
                    recipes = self.get_recipe.find_recipes_by_ingredients(ingredients)
                    self.recipe.display_recipes(recipes, by_ingredients=True)

                elif choice == '2':
                    recipes = self.get_recipe.find_random_recipes()
                    self.recipe.display_recipes(recipes, by_ingredients=False)

                elif choice == '3':
                    while True:
                        self.menu.display_menu(self.menu.category_menu_items, "Recipe Categories")
                        category_choice = self.menu.get_choice("\nPlease select a category: ").strip()

                        if category_choice in self.menu.category_mapping:
                            category = self.menu.category_mapping[category_choice]
                            recipes = self.get_recipe.find_recipes_by_category(category)
                            self.recipe.display_recipes(recipes, by_ingredients=False)

                        elif category_choice == '9':
                            break  # Back to main menu
                        else:
                            print("Invalid choice. Please try again.")
                elif choice == '4':
                    print("Thank you for using our recipe app, Goodbye!")
                    break
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
    # Creates an instance of the App class
    app = App()
    # Calls the run method of the App instance
    app.run()
