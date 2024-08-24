import unittest
from unittest.mock import patch, Mock
from io import StringIO
from display import RecipeDisplay, MenuDisplay

# Test display.py file

# Test RecipeDisplay class
class TestRecipeDisplay(unittest.TestCase):

    def setUp(self):
        self.get_mock = Mock()  # Mocking the get object that would normally fetch recipe instructions
        self.recipe_display = RecipeDisplay(get_recipe=self.get_mock)
        
    # Test the display_recipes method when recipe details include both used and missed ingredients, as well as instructions.
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_recipes_with_ingredients(self, mock_stdout):
        # Mocking the response of find_recipe_instructions method
        self.get_mock.find_recipe_details.return_value = {
            'extendedIngredients': [{'original': '1 Tomato'}, {'original': '2 Basil leaves'}],
            'analyzedInstructions': [
                {'steps': [{'number': 1, 'step': 'Chop tomatoes.'}, {'number': 2, 'step': 'Mix with basil.'}]}]
        }

        recipes = [
            {'id': 1, 'title': 'Tomato Basil Pasta', 'usedIngredients': [{'name': 'Tomato'}],
             'missedIngredients': [{'name': 'Basil'}]}
        ]

        # Calling the display_recipes method to test its output
        self.recipe_display.display_recipes(recipes)

        # Getting the printed output
        output = mock_stdout.getvalue()

        # Check if the output contains the expected strings
        self.assertIn("RECIPE 1: Tomato Basil Pasta", output)
        self.assertIn("Used ingredients:", output)
        self.assertIn(" - Tomato", output)
        self.assertIn("Missing ingredients:", output)
        self.assertIn(" - Basil", output)
        self.assertIn("Ingredients:", output)
        self.assertIn(" - 1 Tomato", output)
        self.assertIn("Instructions:", output)
        self.assertIn("Step 1: Chop tomatoes.", output)
        self.assertIn("Step 2: Mix with basil.", output)

    # Test the display_recipes method when recipe details are empty 
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_recipes_without_ingredients(self, mock_stdout):
        # Mocking the response of find_recipe_instructions method
        self.get_mock.find_recipe_details.return_value = {
            'extendedIngredients': [],
            'analyzedInstructions': []
        }

        recipes = [
            {'id': 1, 'title': 'Mysterious Dish', 'usedIngredients': [], 'missedIngredients': []}
        ]

        # Calling the display_recipes method to test its output
        self.recipe_display.display_recipes(recipes)

        # Getting the printed output
        output = mock_stdout.getvalue()

        # Check if the output contains the expected strings
        self.assertIn("RECIPE 1: Mysterious Dish", output)
        self.assertIn("No ingredients available.", output)
        self.assertIn("No instructions available.", output)
        
    # Test the display_saved_recipes method with a dictionary of saved recipes categorized by type.
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_saved_recipes(self, mock_stdout):
        saved_recipes = {
            'dessert': ['Chocolate Cake', 'Ice Cream'],
            'snacks': ['Nachos', 'Popcorn']
        }

        # Calling the display_saved_recipes method to test its output
        self.recipe_display.display_saved_recipes(saved_recipes)

        # Getting the printed output
        output = mock_stdout.getvalue()

        # Check if the output contains the expected strings
        self.assertIn("\n\33[33m\33[40m\33[1mHere are your saved recipes:\33[0m", output)
        self.assertIn("\33[1m - Saved Recipes by dessert:\33[0m Chocolate Cake, Ice Cream", output)
        self.assertIn("\33[1m - Saved Recipes by snacks:\33[0m Nachos, Popcorn", output)
        self.assertIn('-' * 100, output)

    # Test the display_saved_recipes method with an empty dictionary of saved recipes.
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_saved_recipes_empty(self, mock_stdout):
        saved_recipes = {}

        # Calling the display_saved_recipes method to test its output
        self.recipe_display.display_saved_recipes(saved_recipes)

        # Getting the printed output
        output = mock_stdout.getvalue()

        # Check if the output correctly indicates no saved recipes
        self.assertIn("No saved recipes.", output)

# Test Menu Display class
class TestMenuDisplay(unittest.TestCase):

    def setUp(self):
        self.menu = MenuDisplay()

    # Test the display_menu method to ensure it correctly formats and displays the menu items with a title.
    def test_display_menu(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
            output = fake_out.getvalue()

        # Ensure the menu title and items are correctly displayed
        self.assertIn("Main Menu", output)
        for item in self.menu.main_menu_items:
            self.assertIn(item, output)


if __name__ == '__main__':
    unittest.main()
