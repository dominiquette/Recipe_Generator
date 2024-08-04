# ===== Importing Libraries ===========

from app import fetch_recipe_instructions, fetch_recipes_by_ingredients, fetch_random_recipes, fetch_recipes_by_category
from app import main_menu_items, category_menu_items, display_menu, category_mapping

# ===== Welcome to the app ===========


welcome_message = """
·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
    🧄🍲🍎 Welcome to Group 5 Recipe generator 🍉🍰🥕
·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚·͙̩̩̥˚‧₊⁺⁺₊‧˚ ‧₊⁺⁺₊‧˚·͙ ‧₊⁺⁺
"""

print(welcome_message)
# I copied my code (China) but we could decide if we want to ask for the nickname or
# it isn't necessary - change it and improve the output
nickname = input("What's your name? ")
print(f"Welcome to my console app, {nickname}! Do you want help choosing what to cook? ")


# ===== Functions ===========

# === by ingredients ====
# mix with eve and my code..
def get_user_ingredients():
    ingredients = input("\nEnter the ingredients you have, separated by commas: ")
    return [ingredient.strip() for ingredient in ingredients.split(',')]


def display_recipes(recipes, by_ingredients=True):
    if not recipes:
        print("No recipes found.")
        return

    for recipe in recipes:
        print(f"\n\33[33m\33[40m\33[1mRECIPE: {recipe['title']} \33[0m\n")

        if by_ingredients:
            used_ingredients = [ingredient['name'] for ingredient in recipe.get('usedIngredients', [])]
            missed_ingredients = [ingredient['name'] for ingredient in recipe.get('missedIngredients', [])]
            print(f"\33[1mUsed ingredients:\33[0m {', '.join(used_ingredients)}")
            print(f"\33[1mMissing ingredients:\33[0m {', '.join(missed_ingredients)}")
        else:
            ingredients = [ingredient['name'] for ingredient in recipe.get('extendedIngredients', [])]
            print(f"Ingredients: {', '.join(ingredients)}")

        recipe_info = fetch_recipe_instructions(recipe['id'])
        instructions = recipe_info.get('analyzedInstructions', [])
        if instructions:
            print("\n\33[4m\33[1mInstructions:\33[0m")
            for step in instructions[0]['steps']:
                print(f"Step {step['number']}: {step['step']}")
        else:
            print("No instructions available.")

        print('-' * 100)


# ===== Displaying Functions ===========
while True:
    display_menu(main_menu_items, "Main Menu")
    choice = input("\nPlease enter your choice: ")

    if choice == '1':
        ingredients = get_user_ingredients()
        recipes = fetch_recipes_by_ingredients(ingredients)
        display_recipes(recipes, by_ingredients=True)
    elif choice == '2':
        recipes = fetch_random_recipes()
        display_recipes(recipes, by_ingredients=False)
    elif choice == '3':
        while True:
            display_menu(category_menu_items, "Recipe Categories")
            category_choice = input("\nPlease select a category: ")

            if category_choice in category_mapping:
                category = category_mapping[category_choice]
                recipes = fetch_recipes_by_category(category)
                display_recipes(recipes, by_ingredients=False)
            elif category_choice == '9':
                break  # Back to main menu
            else:
                print("Invalid choice. Please try again.")
    elif choice == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

