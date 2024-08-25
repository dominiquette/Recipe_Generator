# ===== Importing Libraries ===========
import requests
from functools import wraps  # `wraps` is used to preserve the original function's metadata when decorating it
from .config import LOGGING_ENABLED  # Import a configuration setting to enable or disable logging


# Decorator for logging function calls
def log_function_call(func):
    """
        A decorator that logs the function calls and their return values.

        This decorator is used primarily for debugging purposes. When applied to a function,
        it will print a message before and after the function is called, showing the function's
        name and its return value.

        The logging behavior can be toggled on or off using the `LOGGING_ENABLED` setting in the
        config module by setting it to True or False. This allows you to enable detailed logging during development and
        debugging, but disable it during production or presentation to keep the console output clean.

        Args:
            func (function): The function to be decorated.

        Returns:
            function: The wrapped function with logging functionality.
        """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if LOGGING_ENABLED:
            print(f"Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        if LOGGING_ENABLED:
            print(f"Function {func.__name__} returned: {result}")
        return result

    return wrapper


def handle_errors(func):
    """
    A decorator that provides error handling for the decorated function.

    This decorator wraps the target function in a try-except block to handle exceptions that may
    occur during execution. It is particularly useful for handling user input errors in a
    console application, where the program should not crash due to invalid input.

    - If a `ValueError` is raised, and it's related to empty input, the decorator will prompt the user
      to re-enter the input by continuing the loop.
    - For `HTTPError` related to missing or invalid API keys, a specific error message will be shown.
    - For any other exceptions, the error is printed, and the function returns `None` to signal failure.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function with error handling functionality.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                print(f"Error!: {e}")
                # If the exception is related to empty input, prompt the user again
                if "Input cannot be empty" in str(e):
                    continue
                # For other ValueErrors, return None (or handle differently if desired)
                return None
            except requests.exceptions.HTTPError as e:
                # Handle HTTP errors, especially for missing or invalid API keys
                if e.response is not None and e.response.status_code == 401:
                    print("\nError!: No API key found or invalid API key. Check if API key is entered correctly")
                else:
                    print(f"HTTP Error: {e}")
                return None
            except Exception as e:
                # Catch any other unexpected exceptions and print an error message
                print(f"Error!: {e}")
                return None

    return wrapper
