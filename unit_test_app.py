import unittest
from unittest import TestCase
from unittest.mock import patch, Mock
from app import SpoonacularAPI, RecipeFinder

# I tried to test this class but I don't know how to do it without giving params and endpoint.
# I searched online and with IA tried to adapted but even though is "working" is not doing what I want to.
# class TestSpoonacularAPI(TestCase):
#
#     def setUp(self):
#         # Initialize the SpoonacularAPI instance correctly
#         self.api = SpoonacularAPI(base_url="https://examplespoonacularapi.com", api_key="anykey")
#
#     @patch('app.requests.get')
#     def test_make_request_success(self, mock_get):
#         # Mock the response with a JSON dictionary
#         mock_response = Mock()
#         mock_response.json.return_value = {}
#         mock_get.return_value = mock_response
#
#         # Call the make_request method to compare the result
#         result = self.api.make_request(endpoint="recipes/findByIngredients", params={"param1": "value1"})
#         # Assert that the result matches the mock response
#         self.assertEqual(result, {})
#
#         # Assert that requests.get was called with the correct URL and parameters
#         mock_get.assert_called_once_with(
#             "https://examplespoonacularapi.com/recipes/findByIngredients",
#             params={"param1": "value1"}
#         )

class Test_RecipeFinder(TestCase):

    def setUp(self):
        # testing values to run the mock, not need real values
        self.api = SpoonacularAPI(base_url="https://examplespoonacularapi.com", api_key="anykey")
        self.recipe_finder = RecipeFinder(api=self.api)

    # Explanation of @patch:
    # check the classes example from the unit test session  ('nano.unit_test_examples.get_file_content')
    # It's a decorator, and it mocks that the make_request function is working
    @patch('app.SpoonacularAPI.make_request')
    def test_random_recipes_number(self, mock_make_request): # First, I named it Test_Random_Recipes and wouldn't run
        # mock a response with a number of recipes,
        # to test what happen if for some reason the response exceeded the params number: 2
        mock_make_request.return_value = {"recipes": [{1},{2}]} # This will pass
        # mock_make_request.return_value = {"recipes": [{1},{2},{3}]} # This will fail
        # call our app code to check
        result = self.recipe_finder.find_random_recipes()
        self.assertEqual(len(result), 2)


        # Below is the code to check the endpoint AND params
        # I search online to reduce it in one check
        # There are called_once and called_once_with https://docs.python.org/3/library/unittest.mock.html
        mock_make_request.assert_called_once_with(
                "recipes/random", # this should be the real one and not like in the setUp
                params={"number": 2, "apiKey": "anykey"})

if __name__ == '__main__':
    unittest.main()
