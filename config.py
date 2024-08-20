# ===== Spoonacular API Configuration ==========

# spoonacular API key
api_key = 'a169b338e10a401aabd737b59bfa78c9'

# ===== Logging Configuration ==========

# Control the logging behavior of the application
# This is for the @log_function_call decorator
LOGGING_ENABLED = False  # Set to True for debugging & development, False for presentation

"""
Team Notes

Set LOGGING_ENABLED = 'True' during development to see detailed logs of function calls and returns. 
This helps with debugging and understanding the flow of the program.

Set LOGGING_ENABLED = False when presenting or deploying your application to users, so they don't see the internal 
logging details. This keeps the console output clean and user-friendly.

"""


def self():
    return None
