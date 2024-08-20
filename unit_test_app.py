import unittest
from unittest.mock import patch, Mock
import requests
from app import SpoonacularAPI, RecipeFinder


# I tried to test this class, but I don't know how to do it without giving params and endpoint.
# I searched online and with IA tried to adapt this but even though is "working" is not doing what I want to.

class TestSpoonacularAPI(unittest.TestCase):  # passed 2 OUT OF 3

    def setUp(self):  # Initialize the SpoonacularAPI instance correctly
        self.api = SpoonacularAPI(base_url="https://api.spoonacular.com", api_key="test_api_key")

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
            "https://examplespoonacularapi.com/recipes/findByIngredients",
            params={"param1": "value1"}
        )

    @patch('app.requests.get')
    def test_make_request_http_error(self, mock_get):
        # Mock the response object to simulate an HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.make_request("test_endpoint")

        mock_get.assert_called_once_with("https://api.spoonacular.com/test_endpoint", params=None)
        self.assertIsNone(result)

    @patch('app.requests.get')
    def test_make_request_request_exception(self, mock_get):
        # Mock the requests.get to raise a RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = self.api.make_request("test_endpoint")

        mock_get.assert_called_once_with("https://api.spoonacular.com/test_endpoint", params=None)
        self.assertIsNone(result)


class TestRecipeFinder(unittest.TestCase):  # passed 6 out of 8
    def setUp(self):
        self.api = SpoonacularAPI(base_url="https://api.spoonacular.com", api_key="test_api_key")
        self.recipe_finder = RecipeFinder(self.api)

    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipes_by_ingredients_success(self, mock_make_request):
        mock_make_request.return_value = [{"id": 1, "title": "Test Recipe"}]

        result = self.recipe_finder.find_recipes_by_ingredients("tomato, cheese")

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
        self.assertEqual(result, [{"id": 1, "title": "Test Recipe"}])

    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipes_by_ingredients_empty_response(self, mock_make_request):
        mock_make_request.return_value = []

        result = self.recipe_finder.find_recipes_by_ingredients("tomato, cheese")

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
        self.assertIsNone(result)

    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipes_by_category_success(self, mock_make_request):
        mock_make_request.return_value = {"results": [{"id": 1, "title": "Test Recipe"}]}

        result = self.recipe_finder.find_recipes_by_category("chicken")

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
        self.assertEqual(result, [{"id": 1, "title": "Test Recipe"}])

    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipes_by_category_empty_response(self, mock_make_request):
        mock_make_request.return_value = {}

        result = self.recipe_finder.find_recipes_by_category("chicken")

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
        self.assertEqual(result, [])

    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipe_instructions_success(self, mock_make_request):
        mock_make_request.return_value = {"id": 1, "instructions": "Test instructions"}

        result = self.recipe_finder.find_recipe_instructions(1)

        mock_make_request.assert_called_once_with(
            "recipes/1/information",
            params={
                "apiKey": "test_api_key"
            }
        )
        self.assertEqual(result, {"id": 1, "instructions": "Test instructions"})

    @patch('app.SpoonacularAPI.make_request')
    def test_find_recipe_instructions_empty_response(self, mock_make_request):
        mock_make_request.return_value = None

        result = self.recipe_finder.find_recipe_instructions(1)

        mock_make_request.assert_called_once_with(
            "recipes/1/information",
            params={
                "apiKey": "test_api_key"
            }
        )
        self.assertIsNone(result)

    @patch('app.SpoonacularAPI.make_request')
    def test_find_random_recipes_success(self, mock_make_request):
        mock_make_request.return_value = {"recipes": [{"id": 1, "title": "Test Recipe"}]}

        result = self.recipe_finder.find_random_recipes()

        mock_make_request.assert_called_once_with(
            "recipes/random",
            params={
                "number": 3,
                "apiKey": "test_api_key"
            }
        )
        self.assertEqual(result, [{"id": 1, "title": "Test Recipe"}])

    @patch('app.SpoonacularAPI.make_request')
    def test_find_random_recipes_empty_response(self, mock_make_request):
        mock_make_request.return_value = {}

        # Call the method and check the results
        result = self.recipe_finder.find_random_recipes()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], "Recipe X")

        # Below is the code to check the endpoint AND params
        # Researched online to reduce it in one check
        # There are called_once and called_once_with https://docs.python.org/3/library/unittest.mock.html
        mock_make_request.assert_called_once_with(
            "recipes/random",
            params={
                "number": 3,
                "apiKey": "test_api_key"
            }
        )
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
