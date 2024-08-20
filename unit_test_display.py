import unittest
from unittest.mock import patch, Mock
from io import StringIO
from display import RecipeDisplay, MenuDisplay
from user_input import UserInput


class TestRecipeDisplay(unittest.TestCase):  # PASSED 3 OUT OF 4

    def setUp(self):
        self.get_mock = Mock()  # Mocking the get object that would normally fetch recipe instructions
        self.recipe_display = RecipeDisplay(get=self.get_mock)

    #     @patch('builtins.input', return_value='rice')
    #     def test_get_user_ingredients_successfully_parses_input(self, mock_input):  # PASSED
    #         recipe_display = RecipeDisplay(get=None)
    #         result = recipe_display.get_user_ingredients()
    #         self.assertEqual(result, ['rice'])  # Check if the input is correctly parsed
    #

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_recipes_with_ingredients(self, mock_stdout):
        # Mocking the response of find_recipe_instructions method
        self.get_mock.find_recipe_instructions.return_value = {
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

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_recipes_without_ingredients(self, mock_stdout):
        # Mocking the response of find_recipe_instructions method
        self.get_mock.find_recipe_instructions.return_value = {
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

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_saved_recipes(self, mock_stdout): # FAILED
        saved_recipes = {
            'dessert': ['Chocolate Cake', 'Ice Cream'],
            'snacks': ['Nachos', 'Popcorn']
        }

        # Calling the display_saved_recipes method to test its output
        self.recipe_display.display_saved_recipes(saved_recipes)

        # Getting the printed output
        output = mock_stdout.getvalue()

        # Check if the output contains the expected strings
        self.assertIn("Here are your saved recipes:", output)
        self.assertIn(" - Saved Recipes by dessert: Chocolate Cake, Ice Cream", output)
        self.assertIn(" - Saved Recipes by snacks: Nachos, Popcorn", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_saved_recipes_empty(self, mock_stdout):
        saved_recipes = {}

        # Calling the display_saved_recipes method to test its output
        self.recipe_display.display_saved_recipes(saved_recipes)

        # Getting the printed output
        output = mock_stdout.getvalue()

        # Check if the output correctly indicates no saved recipes
        self.assertIn("No saved recipes.", output)


class TestMenuDisplay(unittest.TestCase):  # PASSED 1 out of 1 test

    def setUp(self):
        self.menu = MenuDisplay()

    def test_display_menu(self):  # PASSED
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
            output = fake_out.getvalue()

        # Ensure the menu title and items are correctly displayed
        self.assertIn("Main Menu", output)
        for item in self.menu.main_menu_items:
            self.assertIn(item, output)

    # @patch('builtins.input', return_value='1')
    # def test_get_choice_success(self, mock_input):
    #     choice = self.menu.get_choice("Please choose:")
    #     self.assertEqual(choice, '1')

    # @patch('builtins.input', side_effect=['', '1'])
    # def test_get_choice_empty_input(self, mock_input):
    #     choice = self.menu.get_choice("Please choose:")
    #     self.assertEqual(choice, '1')  # Ensure it returns the valid input after retry


if __name__ == '__main__':
    unittest.main()