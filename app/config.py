# ===== Spoonacular API Configuration ==========

# Replace 'your-api-key-here' with your actual Spoonacular API key
api_key = 'your-api-key-here'

# ===== Logging Configuration ==========

# Toggle logging behavior for the application.
# This setting is used by the @log_function_call decorator to control logging.
LOGGING_ENABLED = False  # Set to True for debugging & development, False for presentation

"""
Team Notes:

- Set LOGGING_ENABLED = True during development to enable detailed logs of function calls and returns.
  This is useful for debugging and understanding the flow of the program.

- Set LOGGING_ENABLED = False when presenting or deploying your application. This prevents users from seeing internal
  logging details, keeping the console output clean and user-friendly.
"""


def self():
    return None
