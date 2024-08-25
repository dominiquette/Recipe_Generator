# Recipe Generator Console App 🍲

🍴 Welcome to the Recipe Generator Console App! 🍽️

This Python-based application is designed to simplify meal planning by allowing users to search for recipes based on the ingredients they have on hand. Whether you're looking to utilize what’s in your pantry or discover exciting new dishes, this tool offers a seamless way to find and view recipes tailored to your needs.

The application harnesses the power of the Spoonacular API to fetch a diverse range of recipes. Additionally, it features functionality to save your favorite recipes to an Excel file, named [saved_recipes.xlsx](saved_recipes.xlsx), for easy reference and future use.

This guide will walk you through the setup process, from configuring your environment and API key to installing necessary packages and running the application. You will also find detailed information on the application's key features and functionalities.

Discover a range of delicious recipes effortlessly and conveniently! 🍲


## Features 🌟

- **Search Recipes by Ingredients**: Enter a list of ingredients, and the app will find recipes that include those ingredients.
- **Search Recipes by Categories**: View recipes categorised by different themes.
 - **Get random recipes**: The app will generate random recipes for you.
- **View Recipe Details**: For each recipe, you can view the title, ingredients, and preparation instructions.
- **Save Recipes**: Display and save selected recipes to an Excel file [saved_recipes.xlsx](saved_recipes.xlsx) for later reference.




## Installation ⚙️

Clone the repository or download the files in the correct folders. 📂

### Prerequisites

Before running the API, ensure you have the following installed on your system:
- Python 3.8 or higher  🐍
- pip (Python package installer) 📦


### Install Required Packages

Before running the application, ensure you have all the required packages installed. You can install them using `pip` with the `requirements.txt` file provided.

To install the required packages, open your terminal and run the following commands:

```bash
pip install -r requirements.txt
```


This will install the following packages:

- **requests**: For making HTTP requests to the Spoonacular API. 

- **XlsxWriter**: For writing data to the [saved_recipes.xlsx](saved_recipes.xlsx) file.

Alternatively, you can individually install the packages by running:

```bash
pip install requests
```
```bash
pip install XlsxWriter
```


## Set Up API Key 🔑

You need to obtain an API key from **Spoonacular** to use the Recipe Finder Application. 

Sign up at [spoonacular.com/food-api](https://spoonacular.com/food-api/console#Dashboard) to get your API key.

Once you have the API key, open the **[config.py](config.py)** file and replace **api_key** with your actual API key:


`api_key = "your-api-key-here"`

Replace "**your_spoonacular_api_key**" with your actual API key.
 

## Run the Application 🚀

1. Open and run the [main.py](main.py) file.
2. You will be prompted to enter your name for a personalised welcome message.
3. After entering your name, you will be taken to the main menu:

   <img width="379" alt="Screenshot of the main menu" src="https://github.com/user-attachments/assets/80e3108e-18b1-4391-a64f-8c7081e65dc9">

4. From the main menu, you can:
   - **Get recipes based on ingredients**: Enter a list of ingredients to find matching recipes.
   - **Get random recipes**: Receive a selection of random recipes.
   - **View recipe categories**: Browse recipes by different categories.
   - **View your saved recipes**: Access recipes you have previously saved.
   - **Export saved recipes to Excel**: Save your favorite recipes to an Excel file.
   - **Exit**: Close the application.


## Saving Recipes 💾

After retrieving recipes, you can choose to save any of them by selecting the corresponding option.

<img width="605" alt="Screenshot of saving recipe option" src="https://github.com/user-attachments/assets/238765e4-3301-470c-b548-ebfccdfa93a1">

You can then view your saved recipes.

<img width="456" alt="Screenshot of saved recipes list" src="https://github.com/user-attachments/assets/cc6ced47-ec32-4d50-a940-27f82989a3c4">

You can then export your recipes to an Excel file to print or save on your device.

<img width="463" alt="Screenshot of export options" src="https://github.com/user-attachments/assets/cc5ed9fc-59b5-4dfa-9bd5-6941294f20e5">

The recipes will be saved to an Excel file named [saved_recipes.xlsx](saved_recipes.xlsx) in the same directory.

## Excel File  📊

The [saved_recipes.xlsx](saved_recipes.xlsx) file is automatically generated when you save recipes. It contains the recipe titles, ingredients, and instructions in a structured format.

<img width="373" alt="Screenshot of Excel file content" src="https://github.com/user-attachments/assets/488c1900-f288-412a-8dfc-65e2292224d4">


## API Endpoints 🔗

Although the Recipe Finder Application primarily runs as a command-line interface, the following endpoints are used internally:

#### Find Recipes by Ingredients

```http
    GET /recipes/findByIngredients

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `ingredients`    | `string` | Comma-separated list of ingredients. |
| `number`    | `int` | Number of recipes to return. |
| `ranking`    | `int` | Ranking of recipes by the number of ingredients matched. |
| `ignorePantry`    | `string` | Whether to ignore common pantry items.|




#### Find Recipes by Category

```http
    GET /recipes/complexSearch

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `number`    | `int` | Number of recipes to return.  |
| `apiKey`    | `string` | Your Spoonacular API key. |
| `sort`    | `string` | Sorting method. Default is "random". |
| `ignorePantry`    | `string` | Whether to ignore common pantry items.  |
| `type`    | `string` | Type of recipe (e.g., "snack", "dessert").  |




#### Get Random Recipe

```http
    GET /recipes/random

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `number`    | `int` | Number of random recipes to retrieve.|
| `apiKey`    | `string` | Your Spoonacular API key |



#### Find Recipe Details

```http
    GET /recipes/{recipe_id}/information

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `recipe_id`    | `string` | The ID of the recipe to retrieve details for.|
| `apiKey`    | `string` | Your Spoonacular API key |



# Unit Test 🧪

We conducted tests on the core classes of the application to ensure they meet the functional requirements. Additionally, we created another file to test the display-related classes.

## Unit test app file

In the unit test app file, we use `unittest` for the testing framework and `unittest.mock` for mocking objects during tests. The `mock` module is utilized to simulate objects and modify their behavior, while `requests` is imported for HTTP requests, though it's primarily used for mocking.

**Code explanation:**

We created two classes to test the corresponding class methods on the app file. Using mock and assert to make the testing classes work.
We added setUp to initialise the SpoonacularAPI in the TestSpoonacularAPI class and the SpoonacularAPI and RecipeFinder instances in the TestRecipeFinder class.

- **TestSpoonacularAPI**
  - `test_make_request_success`: Tests if the `make_request` method correctly handles a successful API call.
  - `test_make_request_http_error`: Tests how the `make_request` method manages HTTP error responses.
  - `test_make_request_request_exception`: Tests how the `make_request` method handles general request exceptions, such as connection errors.

- **TestRecipeFinder**
  - `test_find_recipes_by_ingredients_success`: Tests if the `find_recipes_by_ingredients` method successfully retrieves recipes when given valid ingredients.
  - `test_find_recipes_by_ingredients_empty_response`: Tests how the `find_recipes_by_ingredients` method handles an empty response.
  - `test_find_recipes_by_category_success`: Tests if `find_recipes_by_category` correctly retrieves recipes for a given category.
  - `test_find_recipes_by_category_empty_response`: Tests the method’s response to an empty API result.
  - `test_find_recipe_instructions_success`: Tests if `find_recipe_details` retrieves recipe instructions successfully.
  - `test_find_recipe_instructions_empty_response`: Tests how `find_recipe_details` handles an empty response.
  - `test_find_random_recipes_success`: Tests if `find_random_recipes` successfully retrieves random recipes.
  - `test_find_random_recipes_one_response`: Tests if the method handles a response with a single recipe correctly.

### Unit Test Display File

In the unit test display file, we use `unittest` and `unittest.mock`, including `mock` and `patch`, for simulating objects and modifying their behavior. Additionally, `StringIO` from the `io` module is used to capture printed output for assertions.

**Code Explanation:**

We created two classes to test the corresponding class methods on the app file. Each class has its setUp explained below:

- **TestRecipeDisplay**
  - `setUp`: Initializes a `Mock` object to simulate fetching recipe details and creates an instance of `RecipeDisplay` with this mock.
  - `test_display_recipes_with_ingredients`: Tests the `display_recipes` method when recipe details include both used and missed ingredients, as well as instructions.
  - `test_display_recipes_without_ingredients`: Tests the `display_recipes` method when recipe details are empty.
  - `test_display_saved_recipes`: Tests the `display_saved_recipes` method with a dictionary of saved recipes categorized by type.
  - `test_display_saved_recipes_empty`: Tests the `display_saved_recipes` method with an empty dictionary of saved recipes.

- **TestMenuDisplay**
  - `setUp`: Initializes an instance of `MenuDisplay`.
  - `test_display_menu`: Tests the `display_menu` method to ensure it correctly formats and displays the menu items with a title.

## Credits 🏅

This project was developed by:

- [Anto](https://github.com/chinatortora)
- [Eve](https://github.com/evelinakald)
- [Hafsa](https://github.com/hafsaarale)
- [Dominique](https://github.com/dominiquette)
