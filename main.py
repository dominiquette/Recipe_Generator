# ===== Importing Libraries ===========
# Import the necessary functions and variables from the app module.
# These functions handle API requests and menu display, while the variables define menu items and mappings.
from app import fetch_recipe_instructions, fetch_recipes_by_ingredients, fetch_random_recipes, fetch_recipes_by_category
from app import main_menu_items, category_menu_items, display_menu, category_mapping

# ===== Welcome to the app ===========
# A Welcome message to greet user when they start the application.
welcome_message = """
·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
    🧄🍲🍎 Welcome to Group 5 Recipe generator 🍉🍰🥕
·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚ ‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
"""

# Print the welcome message to the console
print(welcome_message)

# Prompt the user to input their name and store it in the variable `nickname`
nickname = input("What's your name? ")
print(f"Welcome to my console app, {nickname}! Do you want help choosing what to cook? ")


# ===== Functions ===========

# Function to prompt the user to enter ingredients they have on hand.
# This function reads user input, splits it by commas, and returns a list of ingredients.
def get_user_ingredients():
    # Ask the user to input their ingredients as a comma-separated string
    ingredients = input("\nEnter the ingredients you have, separated by commas: ")
    # Split the input string by commas and strip any extra whitespace from each ingredient
    return [ingredient.strip() for ingredient in ingredients.split(',')]


# Function to display a list of recipes to the user.
# It formats and prints the recipe details including used and missing ingredients, and cooking instructions.
def display_recipes(recipes, by_ingredients=True):
    # Check if the recipes list is empty
    if not recipes:
        print("No recipes found.")
        return

    # Loop through each recipe in the list
    for recipe in recipes:
        # Print the recipe title with styling for emphasis
        print(f"\n\33[33m\33[40m\33[1mRECIPE: {recipe['title']} \33[0m\n")  # Black background, yellow font.

        if by_ingredients:
            # Extract and print used ingredients
            used_ingredients = [ingredient['name'] for ingredient in recipe.get('usedIngredients', [])]
            missed_ingredients = [ingredient['name'] for ingredient in recipe.get('missedIngredients', [])]
            print(f"\33[1mUsed ingredients:\33[0m")
            for ingredient in used_ingredients:
                print(f" - {ingredient}")   # prints in line points. Example: - Chicken
            print(f"\n\33[1mMissing ingredients:\33[0m")
            for ingredient in missed_ingredients:
                print(f" - {ingredient}")

        # Fetch and display recipe instructions and ingredients
        recipe_info = fetch_recipe_instructions(recipe['id'])
        extended_ingredients = recipe_info.get('extendedIngredients', [])
        if extended_ingredients:
            # Print the list of all ingredients needed for the recipe
            print(f"\n\33[1mIngredients:\33[0m")
            for ingredient in extended_ingredients:
                print(f" - {ingredient['original']}")
        else:
            print("No ingredients available.")

        # Extract and print step-by-step cooking instructions
        instructions = recipe_info.get('analyzedInstructions', [])
        if instructions:
            print("\n\33[4m\33[1mInstructions:\33[0m")
            for step in instructions[0]['steps']:
                print(f"Step {step['number']}: {step['step']}")
        else:
            print("No instructions available.")

        # Print a separator line for readability
        print('-' * 100)


# ===== Main Application ===========
# Main loop that repeatedly displays the menu and processes user choices
while True:
    # Display the main menu options to the user
    display_menu(main_menu_items, "Main Menu")
    # Get the user's selection choice from the menu.
    choice = input("\nPlease enter your choice: ")

    if choice == '1':
        # Option 1: Fetch recipes based on user-provided ingredients
        ingredients = get_user_ingredients()   # Get ingredients from user
        recipes = fetch_recipes_by_ingredients(ingredients)   # Fetch recipes using those ingredients
        display_recipes(recipes, by_ingredients=True)   # Display the recipes with ingredient details
    elif choice == '2':
        # Option 2: Fetch random recipes
        recipes = fetch_random_recipes()   # Fetch random recipes
        display_recipes(recipes, by_ingredients=False)   # Display the recipes without ingredient details
    elif choice == '3':
        # Option 3: View recipes by category
        while True:
            # Display the recipe category menu to the user
            display_menu(category_menu_items, "Recipe Categories")
            # Get the user's choice of recipe category
            category_choice = input("\nPlease select a category: ")

            if category_choice in category_mapping:
                # If a valid category choice is made, fetch recipes for that category
                category = category_mapping[category_choice]
                recipes = fetch_recipes_by_category(category)
                display_recipes(recipes, by_ingredients=False)   # Display the recipes without ingredient details
            elif category_choice == '13':
                # Option '13' is to go back to the main menu
                break
            else:

                print("Invalid choice. Please try again.")    # Handle invalid category choice
    elif choice == '4':
        # Option 4: Exit the application
        print(f"Thank you {nickname} for using the app. Goodbye!")
        break   # Exit the main loop and end the program
    else:
        # Handle invalid main menu choice
        print("Invalid choice. Please try again.")