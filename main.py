# ===== Importing Libraries ===========
from app import RecipeFinder, SpoonacularAPI
from collections import deque
# ===== Importing data from files ===========
from config import api_key
from display import Menu, Recipe
from decorators import log_function_call, handle_errors  # Import the decorators


# User class handles getting the user's info and calls the method to initialise the name attribute
# This way the prompt will always happen and the object (User) will have a name attribute set at the start
class User:
    def __init__(self):
        self.name = self.get_name()

    @log_function_call
    @handle_errors
    def get_name(self):
        while True:
            name = input("What's your name?: ").strip()
            if not name:
                print("\nName cannot be empty. Please enter your name again.")
            else:
                print(f"\nWelcome to our console app, {name}! What do you need help with?")
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
        print(self.welcome_message)
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
    @log_function_call  # Log when the run method starts and ends
    @handle_errors  # Handle any exceptions uniformly
    def run(self):
        total_titles = deque()  # I created a list to add the recipe's name results
        while True:

            self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
            choice = self.menu.get_choice("\nPlease enter your choice: ").strip()

            if choice == '1':
                ingredients = self.recipe.get_user_ingredients()
                recipes = self.get_recipe.find_recipes_by_ingredients(ingredients)
                self.recipe.display_recipes(recipes, by_ingredients=True)
                ingredients_titles = [recipe['title'] for recipe in recipes]

                # Below I added it to the left because is our first option
                total_titles.appendleft(
                    f"\n\33[1m - Here are your recipes by ingredient\33[0m: {', '.join(ingredients_titles)}")
                # print(ingredients_titles)
                # print(total_titles)

            elif choice == '2':
                recipes = self.get_recipe.find_random_recipes()
                self.recipe.display_recipes(recipes, by_ingredients=False)
                random_titles = [recipe['title'] for recipe in recipes]
                total_titles.append(f"\n\33[1m - Here are your random recipes:\33[0m {', '.join(random_titles)}")
                # print(random_titles)

            elif choice == '3':
                while True:
                    self.menu.display_menu(self.menu.category_menu_items, "Recipe Categories")
                    category_choice = self.menu.get_choice("\nPlease select a category: ").strip()

                    if category_choice in self.menu.category_mapping:
                        category = self.menu.category_mapping[category_choice]
                        recipes = self.get_recipe.find_recipes_by_category(category)
                        self.recipe.display_recipes(recipes, by_ingredients=False)
                        category_titles = [recipe['title'] for recipe in recipes]
                        total_titles.append(
                            f"\n\33[1m - Here are your recipes by category:\33[0m {', '.join(category_titles)}")
                        print(category_titles)

                    elif category_choice == '9':
                        break  # Back to main menu
                    else:
                        print("Invalid choice. Please try again.")
            elif choice == '4':
                # print(total_titles)
                print(f"\n\33[33m\33[40m\33[1mHere are your Recipes names so far: \33[0m")
                for titles in total_titles:
                    # self.recipe.display_deque()
                    print(titles)
                print('-' * 100)

            elif choice == '5':
                print("Thank you for using our recipe app, Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


# ===== Main ===========
if __name__ == "__main__":
    # Creates an instance of the App class
    app = App()
    # Calls the run method of the App instance
    app.run()
