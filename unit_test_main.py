import unittest
from unittest.mock import patch
from main import App  # Import the App class from the main module


class TestMain(unittest.TestCase):  # passed 1 out of 2

    @patch('app.SpoonacularAPI.make_request')
    @patch('builtins.input', side_effect=['1', 'tomato,cheese', 'N', '5'])
    @patch('builtins.exit')  # Mocks the exit function to prevent SystemExit
    def test_main_flow_ingredients_search(self, _mock_exit, _mock_input, mock_make_request):
        # Mocks the response from the Spoonacular API
        mock_make_request.return_value = [
            {"id": 1, "title": "Tomato Basil Pasta", "usedIngredients": [{"name": "tomato"}],
             "missedIngredients": [{"name": "pasta"}]},
            {"id": 2, "title": "Cheese Pizza", "usedIngredients": [{"name": "cheese"}],
             "missedIngredients": [{"name": "dough"}]}
        ]

        # Patch the RecipeDisplay's display_recipes method
        with patch('display.RecipeDisplay.display_recipes') as mock_display_recipes:
            app_instance = App()  # Creates an instance of the App class
            app_instance.run()  # Calls the run method to execute the main application flow

            # Confirms display_recipes was called once with the correct arguments
            mock_display_recipes.assert_called_once()
            mock_display_recipes.assert_called_with([
                {"id": 1, "title": "Tomato Basil Pasta", "usedIngredients": [{"name": "tomato"}],
                 "missedIngredients": [{"name": "pasta"}]},
                {"id": 2, "title": "Cheese Pizza", "usedIngredients": [{"name": "cheese"}],
                 "missedIngredients": [{"name": "dough"}]}
            ], by_ingredients=True)


    @patch('app.SpoonacularAPI.make_request')
    @patch('builtins.input', side_effect=['2', 'N', '5'])
    @patch('builtins.exit')  # Mocks the exit function to prevent SystemExit
    def test_main_flow_random_recipes(self, _mock_exit, _mock_input, mock_make_request):
        # Mocks the response for random recipes
        mock_make_request.return_value = {
            "recipes": [
                {"id": 1, "title": "Random Recipe 1"},
                {"id": 2, "title": "Random Recipe 2"}
            ]
        }

        # Patch the RecipeDisplay's display_recipes method
        with patch('display.RecipeDisplay.display_recipes') as mock_display_recipes:
            app_instance = App()  # Creates an instance of the App class
            app_instance.run()  # Calls the run method to execute the main application flow

            # Ensure display_recipes was called once with the correct arguments
            mock_display_recipes.assert_called_once()
            mock_display_recipes.assert_called_with([
                {"id": 1, "title": "Random Recipe 1"},
                {"id": 2, "title": "Random Recipe 2"}
            ], by_ingredients=False)


if __name__ == '__main__':
    unittest.main()
