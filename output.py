# ===== Importing Libraries ===========
import xlsxwriter
# ===== Importing data from files ===========
from decorators import log_function_call, handle_errors

class RecipeDetails:
    def __init__(self, get_recipe):
        self.get_recipe = get_recipe
    @log_function_call
    @handle_errors
    def get_recipe_details(self, recipe_title):
        # Get the recipe ID from the recipe title
        recipe_id = self.get_recipe.find_recipe_id(recipe_title)
        if not recipe_id:
            print(f'No ID found for {recipe_title}')
            return None

        # Get the detailed information of the recipe
        api_response = self.get_recipe.find_recipe_details(recipe_id)
        return api_response

class RecipeProcessor:
    @staticmethod
    def get_ingredients(api_response):
        # Check if 'extendedIngredients' key exists in the API response
        if 'extendedIngredients' in api_response:
            # Extract ingredient details and format them
            ingredients_list = []
            for ingredient in api_response['extendedIngredients']:
                name = ingredient.get('name', 'Unknown')
                amount = ingredient.get('amount', '')
                unit = ingredient.get('measures', {}).get('us', {}).get('unitShort', '')
                ingredients_list.append(f"{amount} {unit} {name}")

            # Join all ingredients into a comma-separated string
            ingredients = ", ".join(ingredients_list)
            return ingredients
        else:
            print("No ingredients found in the API response.")
            return None

    @staticmethod
    def get_instructions(api_response):
        # Check if 'analyzedInstructions' key exists in the API response
        if 'analyzedInstructions' in api_response and api_response['analyzedInstructions']:
            # Extract the first set of instructions (if there are multiple sets)
            instructions_steps = api_response['analyzedInstructions'][0]['steps']
            instructions = "\n".join([f"Step {step['number']}: {step['step']}" for step in instructions_steps])
            return instructions
        else:
            print("No instructions found in the API response.")
            return None

class RecipeExporter:
    def __init__(self, recipe_details, recipe_processor, saved_recipes):
        self.recipe_details = recipe_details
        self.recipe_processor = recipe_processor
        self.saved_recipes = saved_recipes

    @log_function_call
    @handle_errors
    def find_instructions_ingredients(self, recipe_title):
        api_response = self.recipe_details.get_recipe_details(recipe_title)
        if not api_response:
            print(f'Unexpected API response: {api_response}')

        ingredients = self.recipe_processor.get_ingredients(api_response)
        instructions = self.recipe_processor.get_instructions(api_response)

        return ingredients, instructions

    @log_function_call
    @handle_errors
    def export_to_excel(self, filename):
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Recipes')

        # Define cell formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 18,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#f6eee1',
            'font_color': '#67595e',
            'text_wrap': True})

        header_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'left',
            'valign': 'vcenter',
            'bg_color': '#f6eee1',
            'font_color': '#67595e'})

        text_format = workbook.add_format({
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter',
            'bg_color': '#f6eee1',
            'font_color': '#67595e',
            'text_wrap': True})

        blank_format = workbook.add_format({
            'bg_color': '#f6eee1'})

        # Set column A width to 38
        worksheet.set_column(0, 0, 55)

        # Start writing the recipes
        saved_recipes = self.saved_recipes.get_saved_recipes()
        row = 0
        for category, recipes in saved_recipes.items():
            for recipe in recipes:
                ingredients, instructions = self.find_instructions_ingredients(recipe)

                # Write the recipe name in cell A1
                worksheet.write(row, 0, recipe, title_format)

                # Write blank row
                row += 1
                worksheet.write(row, 0, '', blank_format)

                # Write 'Ingredients' in cell A3
                row += 1  # Move to row 3 (which is index 2)
                worksheet.write(row, 0, 'Ingredients', header_format)

                # Write the actual ingredients starting from cell A4
                row += 1  # Move to row 4 (which is index 3)
                if ingredients:
                    worksheet.write(row, 0, ingredients, text_format)
                else:
                    worksheet.write(row, 0, 'No Ingredients', text_format)

                # Write blank row
                row += 1
                worksheet.write(row, 0, '', blank_format)

                # Write 'Instructions' in cell A6
                row += 1  # Move to row 6 (which is index 5)
                worksheet.write(row, 0, 'Instructions', header_format)

                # Write the actual instructions starting from cell A7
                row += 1  # Move to row 7 (which is index 6)
                if instructions:
                    worksheet.write(row, 0, instructions, text_format)
                else:
                    worksheet.write(row, 0, 'No Instructions', text_format)

                # Move to the next recipe, add some space before the next block
                row += 2  # Move to the next block of rows for the next recipe

        workbook.close()
        print(f"\nYour recipes have been exported to {filename}")