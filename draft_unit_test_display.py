# import unittest
# from unittest.mock import patch, Mock
# from io import StringIO
# from display import RecipeDisplay, MenuDisplay
# from user_input import UserInput
#
# class TestRecipeDisplay(unittest.TestCase):  # PASSED 1 out of 3 tests
#
#     @patch('builtins.input', return_value='rice')
#     def test_get_user_ingredients_successfully_parses_input(self, mock_input):  # PASSED
#         recipe_display = RecipeDisplay(get=None)
#         result = recipe_display.get_user_ingredients()
#         self.assertEqual(result, ['rice'])  # Check if the input is correctly parsed
#
#     # @patch('builtins.input', side_effect=['', 'rice'])
#     # def test_get_user_ingredients_empty_input(self, mock_input):
#     #     recipe_display = RecipeDisplay(get=None)
#     #     result = recipe_display.get_user_ingredients()
#     #     self.assertEqual(result, ['rice'])  # Ensure it returns the valid input after retry
#
#     # I wanted to add something related to this ValueError, but I can't.
#     # Also, I couldn't find a way for the app to give me this error, maybe we need a redo
#     # It jumps to a ValueError("API response is empty or invalid.") Check the readme, maybe Hafsa try it differently
#     # with self.assertRaises(ValueError):
#     #     recipe.get_user_ingredients(expected)
#     # I want to add something related to assertIn to check if the ingredient was in the app response to combine
#     # display and app test, but it was too hard for me
#     # Try to use this example with a for loop of the response, but I can't
#     # def test_positive(self):
#     #     key = "geeks"
#     #     container = "geeksforgeeks"
#     #     # error message in case if test case got failed
#     #     message = "key is not in container."
#     #     # assertIn() to check if key is in container
#     #     self.assertIn(key, container, message)
#
#     @patch('app.RecipeFinder.find_recipes_by_ingredients')
#     def test_display_recipes(self, mock_find_recipes):
#         mock_find_recipes.return_value = [
#             {'title': 'Pasta', 'usedIngredients': [{'name': 'Tomato'}], 'id': 1}
#         ]
#
#         recipe_display = RecipeDisplay(get=Mock())
#
#         with patch('sys.stdout', new=StringIO()) as fake_out:
#             recipe_display.display_recipes(mock_find_recipes())
#             output = fake_out.getvalue()
#
#         # Check if the output matches expected content
#         self.assertIn("Recipe 1: Pasta", output)
#         self.assertIn("Ingredients used:", output)
#
#         # Checking that the output matches expected format
#         # You might need to use a StringIO object to capture the printed output if required.
#
#
# class TestMenuDisplay(unittest.TestCase):  # PASSED 1 out of 2 tests
#
#     def setUp(self):
#         self.menu = MenuDisplay()
#
#     def test_display_menu(self):  # PASSED
#         with patch('sys.stdout', new=StringIO()) as fake_out:
#             self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
#             output = fake_out.getvalue()
#
#         # Ensure the menu title and items are correctly displayed
#         self.assertIn("Main Menu", output)
#         for item in self.menu.main_menu_items:
#             self.assertIn(item, output)
#
#     # @patch('builtins.input', return_value='1')
#     # def test_get_choice_success(self, mock_input):
#     #     choice = self.menu.get_choice("Please choose:")
#     #     self.assertEqual(choice, '1')
#
#     # @patch('builtins.input', side_effect=['', '1'])
#     # def test_get_choice_empty_input(self, mock_input):
#     #     choice = self.menu.get_choice("Please choose:")
#     #     self.assertEqual(choice, '1')  # Ensure it returns the valid input after retry
#
#
# if __name__ == '__main__':
#     unittest.main()

#
#  ############################### UNIT_TEST_APP.PY#########################
#
# import unittest
# from unittest.mock import patch, Mock
# import requests
#
# from app import SpoonacularAPI, RecipeFinder
#
#
# # I tried to test this class, but I don't know how to do it without giving params and endpoint.
# # I searched online and with IA tried to adapt this but even though is "working" is not doing what I want to.
#
# class TestSpoonacularAPI(unittest.TestCase):  # PASSED 1 OUT OF 3
#
#     def setUp(self):  # Initialize the SpoonacularAPI instance correctly
#         self.api = SpoonacularAPI(base_url="https://api.spoonacular.com", api_key="test_api_key")
#
#     @patch('app.requests.get')
#     def test_make_request_success(self, mock_get):  # PASSED
#         mock_response = Mock()  # Mock the API response with a JSON dictionary
#         mock_response.json.return_value = {"key": "value"}
#         mock_get.return_value = mock_response
#
#         # Call the make_request method to compare the result
#         result = self.api.make_request(endpoint="recipes/findByIngredients", params={"param1": "value1"})
#         self.assertEqual(result, {"key": "value"})  # Ensures that the result matches the mock response
#
#         # Assert that requests.get was called with the correct URL and parameters
#         mock_get.assert_called_once_with(
#             "https://examplespoonacularapi.com/recipes/findByIngredients",
#             params={"param1": "value1"}
#         )
#
#     @patch('app.requests.get')
#     def test_make_request_http_error(self, mock_get):
#         mock_response = Mock()
#         mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP Error")
#         mock_get.return_value = mock_response
#
#         with self.assertRaises(requests.HTTPError):
#             self.api.make_request(endpoint="recipes/findByIngredients")
#
#     @patch('app.requests.get')
#     def test_make_request_request_exception(self, mock_get):
#         mock_get.side_effect = requests.RequestException("Request Error")  # Mocks a RequestException
#
#         with self.assertRaises(requests.RequestException):
#             self.api.make_request(endpoint="recipes/findByIngredients")
#
#
# class TestRecipeFinder(unittest.TestCase):  # failed 2 out of 2
#
#     def setUp(self):
#         # Mock API for testing
#         self.api = SpoonacularAPI(base_url="https://examplespoonacularapi.com", api_key="anykey")
#         self.recipe_finder = RecipeFinder(api=self.api)
#
#     # Explanation of @patch:
#     # check the classes example from the unit test session  ('nano.unit_test_examples.get_file_content')
#     # It's a decorator, and it mocks that the make_request function is working
#     @patch('app.SpoonacularAPI.make_request')
#     def test_find_recipes_by_category(self, mock_make_request):
#         # Mocks the API response
#         mock_make_request.return_value = {"results": [{"title": "Recipe A"}, {"title": "Recipe B"}]}
#         # mock_make_request.return_value = {"recipes": [{1},{2},{3}]} # This will fail
#         # Calls our app code and checks the results
#         result = self.recipe_finder.find_recipes_by_category("vegan")
#         self.assertEqual(len(result), 2)
#         self.assertEqual(result[0]['title'], "Recipe A")
#
#         # Ensure the API was called with the correct parameters
#         mock_make_request.assert_called_once_with(
#             "recipes/complexSearch",
#             params={"number": 3, "apiKey": "anykey", "sort": "random", "ignorePantry": "true", "diet":
#                     "vegan|vegetarian"}
#         )
#
#     @patch('app.SpoonacularAPI.make_request')
#     def test_find_random_recipes(self, mock_make_request):
#         # Mocks the API response for random recipes
#         mock_make_request.return_value = {"recipes": [{"title": "Recipe X"}, {"title": "Recipe Y"}]}
#
#         # Call the method and check the results
#         result = self.recipe_finder.find_random_recipes()
#         self.assertEqual(len(result), 2)
#         self.assertEqual(result[0]['title'], "Recipe X")
#
#         # Below is the code to check the endpoint AND params
#         # Researched online to reduce it in one check
#         # There are called_once and called_once_with https://docs.python.org/3/library/unittest.mock.html
#         mock_make_request.assert_called_once_with(
#             "recipes/random",
#             params={"number": 3, "apiKey": "anykey"}
#         )
#
#
# if __name__ == '__main__':
#     unittest.main()



################ new APP.PY UNIT TEST ###############
#
# import unittest
# from unittest.mock import patch, Mock
# from io import StringIO
# from display import RecipeDisplay, MenuDisplay
# from user_input import UserInput
#
#
# class TestRecipeDisplay(unittest.TestCase):  # PASSED 3 OUT OF 4
#
#     def setUp(self):
#         self.get_mock = Mock()  # Mocking the get object that would normally fetch recipe instructions
#         self.recipe_display = RecipeDisplay(get=self.get_mock)
#
#     @patch('sys.stdout', new_callable=StringIO)
#     def test_display_recipes_with_ingredients(self, mock_stdout):
#         # Mocking the response of find_recipe_instructions method
#         self.get_mock.find_recipe_instructions.return_value = {
#             'extendedIngredients': [{'original': '1 Tomato'}, {'original': '2 Basil leaves'}],
#             'analyzedInstructions': [
#                 {'steps': [{'number': 1, 'step': 'Chop tomatoes.'}, {'number': 2, 'step': 'Mix with basil.'}]}]
#         }
#
#         recipes = [
#             {'id': 1, 'title': 'Tomato Basil Pasta', 'usedIngredients': [{'name': 'Tomato'}],
#              'missedIngredients': [{'name': 'Basil'}]}
#         ]
#
#         # Calling the display_recipes method to test its output
#         self.recipe_display.display_recipes(recipes)
#
#         # Getting the printed output
#         output = mock_stdout.getvalue()
#
#         # Check if the output contains the expected strings
#         self.assertIn("RECIPE 1: Tomato Basil Pasta", output)
#         self.assertIn("Used ingredients:", output)
#         self.assertIn(" - Tomato", output)
#         self.assertIn("Missing ingredients:", output)
#         self.assertIn(" - Basil", output)
#         self.assertIn("Ingredients:", output)
#         self.assertIn(" - 1 Tomato", output)
#         self.assertIn("Instructions:", output)
#         self.assertIn("Step 1: Chop tomatoes.", output)
#         self.assertIn("Step 2: Mix with basil.", output)
#
#     @patch('sys.stdout', new_callable=StringIO)
#     def test_display_recipes_without_ingredients(self, mock_stdout):
#         # Mocking the response of find_recipe_instructions method
#         self.get_mock.find_recipe_instructions.return_value = {
#             'extendedIngredients': [],
#             'analyzedInstructions': []
#         }
#
#         recipes = [
#             {'id': 1, 'title': 'Mysterious Dish', 'usedIngredients': [], 'missedIngredients': []}
#         ]
#
#         # Calling the display_recipes method to test its output
#         self.recipe_display.display_recipes(recipes)
#
#         # Getting the printed output
#         output = mock_stdout.getvalue()
#
#         # Check if the output contains the expected strings
#         self.assertIn("RECIPE 1: Mysterious Dish", output)
#         self.assertIn("No ingredients available.", output)
#         self.assertIn("No instructions available.", output)
#
#     @patch('sys.stdout', new_callable=StringIO)
#     def test_display_saved_recipes(self, mock_stdout): # FAILED
#         saved_recipes = {
#             'dessert': ['Chocolate Cake', 'Ice Cream'],
#             'snacks': ['Nachos', 'Popcorn']
#         }
#
#         # Calling the display_saved_recipes method to test its output
#         self.recipe_display.display_saved_recipes(saved_recipes)
#
#         # Getting the printed output
#         output = mock_stdout.getvalue()
#
#         # Check if the output contains the expected strings
#         self.assertIn("Here are your saved recipes:", output)
#         self.assertIn(" - Saved Recipes by dessert: Chocolate Cake, Ice Cream", output)
#         self.assertIn(" - Saved Recipes by snacks: Nachos, Popcorn", output)
#
#     @patch('sys.stdout', new_callable=StringIO)
#     def test_display_saved_recipes_empty(self, mock_stdout):
#         saved_recipes = {}
#
#         # Calling the display_saved_recipes method to test its output
#         self.recipe_display.display_saved_recipes(saved_recipes)
#
#         # Getting the printed output
#         output = mock_stdout.getvalue()
#
#         # Check if the output correctly indicates no saved recipes
#         self.assertIn("No saved recipes.", output)
#
#
# class TestMenuDisplay(unittest.TestCase):  # PASSED 1 out of 1 test
#
#     def setUp(self):
#         self.menu = MenuDisplay()
#
#     def test_display_menu(self):  # PASSED
#         with patch('sys.stdout', new=StringIO()) as fake_out:
#             self.menu.display_menu(self.menu.main_menu_items, "Main Menu")
#             output = fake_out.getvalue()
#
#         # Ensure the menu title and items are correctly displayed
#         self.assertIn("Main Menu", output)
#         for item in self.menu.main_menu_items:
#             self.assertIn(item, output)
#
#     # @patch('builtins.input', return_value='1')
#     # def test_get_choice_success(self, mock_input):
#     #     choice = self.menu.get_choice("Please choose:")
#     #     self.assertEqual(choice, '1')
#
#     # @patch('builtins.input', side_effect=['', '1'])
#     # def test_get_choice_empty_input(self, mock_input):
#     #     choice = self.menu.get_choice("Please choose:")
#     #     self.assertEqual(choice, '1')  # Ensure it returns the valid input after retry
#
#
# if __name__ == '__main__':
#     unittest.main()
