import unittest
from unittest.mock import patch, Mock
import requests

from app import SpoonacularAPI, RecipeFinder


# Test class for the SpoonacularAPI class
class TestSpoonacularAPI(unittest.TestCase):

    def setUp(self):  # Initialise the SpoonacularAPI instance correctly
        self.api = SpoonacularAPI(base_url="https://api.spoonacular.com", api_key="test_api_key")

    # Test for successful API request
    @patch('app.requests.get')
    def test_make_request_success(self, mock_get):
        # Mock the response object to simulate a successful request with a JSON dictionary
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        # Call the make_request method to compare the result
        result = self.api.make_request(endpoint="recipes/findByIngredients", params={"param1": "value1"})
        self.assertEqual(result, {"key": "value"})  # Ensures that the result matches the mock response


        # Assert that requests.get was called with the correct URL and parameters
        mock_get.assert_called_once_with(
            "https://api.spoonacular.com/recipes/findByIngredients",
            params={"param1": "value1"}
        )

    # Test for handling HTTP error response
    @patch('app.requests.get')
    def test_make_request_http_error(self, mock_get):
        # Mock the response object to simulate an HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.make_request("test_endpoint")

        # This ensures that the correct endpoint was called
        mock_get.assert_called_once_with("https://api.spoonacular.com/test_endpoint", params=None)
        self.assertIsNone(result)

    # Test for handling general request exceptions such as connection errors
    @patch('app.requests.get')
    def test_make_request_request_exception(self, mock_get):
        # Mock the requests.get to raise a RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = self.api.make_request("test_endpoint")

        # Ensure that the correct endpoint was called
        mock_get.assert_called_once_with("https://api.spoonacular.com/test_endpoint", params=None)
        self.assertIsNone(result)


# Test class for the RecipeFinder class
class TestRecipeFinder(unittest.TestCase):
    def setUp(self):
        # Initialise the SpoonacularAPI and RecipeFinder instances
        self.api = SpoonacularAPI(base_url="https://api.spoonacular.com", api_key="test_api_key")
        self.recipe_finder = RecipeFinder(self.api)

    # Test for finding recipes by ingredients successfully
    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipes_by_ingredients_success(self, mock_make_request):
        # Mock the API response to return a list of recipes
        mock_make_request.return_value = [{"id": 1, "title": "Test Recipe"}]

        result = self.recipe_finder.find_recipes_by_ingredients("tomato, cheese")

        # Ensure that the API was called with the correct endpoint and parameters
        mock_make_request.assert_called_once_with(
            "recipes/findByIngredients",
            params={
                "ingredients": "tomato, cheese",
                "number": 3,
                "ranking": 2,
                "apiKey": "test_api_key",
                "ignorePantry": "true"
            }
        )
        self.assertEqual(result, [{"id": 1, "title": "Test Recipe"}])  # Confirm the correct recipe was returned

    # Test for handling an empty response when finding recipes by ingredients
    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipes_by_ingredients_empty_response(self, mock_make_request):
        # Mock the API response to return an empty list
        mock_make_request.return_value = []

        result = self.recipe_finder.find_recipes_by_ingredients("tomato, cheese")

        # Ensure that the API was called with the correct endpoint and parameters
        mock_make_request.assert_called_once_with(
            "recipes/findByIngredients",
            params={
                "ingredients": "tomato, cheese",
                "number": 3,
                "ranking": 2,
                "apiKey": "test_api_key",
                "ignorePantry": "true"
            }
        )
        self.assertIsNone(result)  # Confirm that None was returned due to the empty response

    # Test for successfully finding recipes by category
    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipes_by_category_success(self, mock_make_request):
        # Mock the API response to return a list of recipes
        mock_make_request.return_value = {"results": [{"id": 1, "title": "Test Recipe"}]}

        result = self.recipe_finder.find_recipes_by_category("chicken")

        # Ensure that the API was called with the correct endpoint and parameters
        mock_make_request.assert_called_once_with(
            "recipes/complexSearch",
            params={
                "number": 3,
                "apiKey": "test_api_key",
                "sort": "random",
                "ignorePantry": "true",
                "includeIngredients": "chicken"
            }
        )
        # Confirm that the correct recipe was returned
        self.assertEqual(result, [{"id": 1, "title": "Test Recipe"}])

    # Test for handling an empty response when finding recipes by category
    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipes_by_category_empty_response(self, mock_make_request):
        # Mock the API response to not returning a result
        mock_make_request.return_value = None

        result = self.recipe_finder.find_recipes_by_category("chicken")

        # Ensure that the API was called with the correct endpoint and parameters
        mock_make_request.assert_called_once_with(
            "recipes/complexSearch",
            params={
                "number": 3,
                "apiKey": "test_api_key",
                "sort": "random",
                "ignorePantry": "true",
                "includeIngredients": "chicken"
            }
        )
        self.assertIsNone(result)  # Confirm that we will have no response

    # Test for successfully retrieving recipe instructions
    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipe_instructions_success(self, mock_make_request):
        # Mock the API response to return a recipe's instructions
        mock_make_request.return_value = {"id": 1, "instructions": "Test instructions"}

        result = self.recipe_finder.find_recipe_details(1)

        # Ensure that the API was called with the correct endpoint and parameters
        mock_make_request.assert_called_once_with(
            "recipes/1/information",
            params={
                "apiKey": "test_api_key"
            }
        )
        # Confirm that the correct instructions were returned
        self.assertEqual(result, {"id": 1,
                                  "instructions": "Test instructions"})

    # Test for handling an empty response when retrieving recipe instructions
    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipe_instructions_empty_response(self, mock_make_request):
        # Mock the API response to return None
        mock_make_request.return_value = None

        result = self.recipe_finder.find_recipe_details(1)

        # Ensure that the API was called with the correct endpoint and parameters
        mock_make_request.assert_called_once_with(
            "recipes/1/information",
            params={
                "apiKey": "test_api_key"
            }
        )
        self.assertIsNone(result)  # Confirm that None was returned due to the empty response

    # Test for successfully finding random recipes
    @patch('app.SpoonacularAPI.make_request')
    def test_find_random_recipes_success(self, mock_make_request):
        # Mock the API response to return a list of random recipes
        mock_make_request.return_value = {"recipes": [{"id": 1, "title": "Test Recipe"}]}

        result = self.recipe_finder.find_random_recipes()

        # Ensure that the API was called with the correct endpoint and parameters
        mock_make_request.assert_called_once_with(
            "recipes/random",
            params={
                "number": 10,
                "apiKey": "test_api_key"
            }
        )
        # Confirm the correct random recipe was returned
        self.assertEqual(result, [{"id": 1, "title": "Test Recipe"}])

    # Test having one response when finding random recipes
    @patch('app.SpoonacularAPI.make_request')
    def test_find_random_recipes_one_response(self, mock_make_request):
        # Mock the API response to have one response
        mock_make_request.return_value = {"recipes": [{"id": 1, "title": "Test Recipe"}]}
        # the test will also pass is we mock this assert it: {"recipes": [{}]}
        # It is not checking the content of the list

        # Call the method and check the results
        result = self.recipe_finder.find_random_recipes()

        # Ensure that the API was called with the correct endpoint and parameters
        mock_make_request.assert_called_once_with(
            "recipes/random",
            params={
                "number": 10,
                "apiKey": "test_api_key"
            }
        )
        # check if the len of the result is one
        self.assertEqual(len(result), 1)
        # check the response
        self.assertEqual(result, [{"id": 1, "title": "Test Recipe"}])


if __name__ == "__main__":
    unittest.main()
