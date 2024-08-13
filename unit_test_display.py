import unittest
from unittest import TestCase, main
from display import Recipe
# from main import RecipeFinder


class TestRecipeMethods(TestCase):
# A test that one only compares the input from the get_user_ingredients with some expected,
# I don't think we can add this is not testing the function, only the input
# That's why I wanted to test the ValueError

    def test_get_user_ingredients_successfully_parses_input(self):
        # Test one ingredient input
        expected = ['rice']
        recipe = Recipe(get=None)
        result = recipe.get_user_ingredients()
        self.assertEqual(result, expected)
    # I wanted to add something related to this ValueError, but I can't.
    # Also, I couldn't find a way for the app to give me this error, maybe we need a redo
    # It jumps to a ValueError("API response is empty or invalid.") Check the readme, maybe Hafsa try it differently
        # with self.assertRaises(ValueError):
        #     recipe.get_user_ingredients(expected)
    # I want to add something related to assertIn to check if the ingredient was in the app response to combine
    # display and app test, but it was too hard for me
    # Try to use this example with a for loop of the response, but I can't
    # def test_positive(self):
    #     key = "geeks"
    #     container = "geeksforgeeks"
    #     # error message in case if test case got failed
    #     message = "key is not in container."
    #     # assertIn() to check if key is in container
    #     self.assertIn(key, container, message)


if __name__ == '__main__':
    unittest.main()
