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

Clone the repository or download the files into one folder. 📂

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

Once you have the API key, open the **[config.py](config.py)** file and replace **API_KEY** with your actual API key:


`API_KEY = "your_spoonacular_api_key"`

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



## Test 🧪

To verify that the Recipe Generator is working correctly, you can run the provided unit tests:



```bash
python -m unittest unit_test_app.py
python -m unittest unit_test_display.py
python -m unittest unit_test_main.py

```

## Credits 🏅

This project was developed by:

- [Anto](https://github.com/chinatortora)
- [Eve](https://github.com/evelinakald)
- [Hafsa](https://github.com/hafsaarale)
- [Dominique](https://github.com/dominiquette)
