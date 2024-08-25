# ===== Importing Libraries ===========
# Used for creating Excel files
import xlsxwriter
# ===== Importing methods from files ===========
from .decorators import log_function_call, handle_errors


# RecipeExporter class handles exporting recipes to an Excel file
class RecipeExporter:
    # Initialises the class with recipe details and saved recipes
    def __init__(self, recipe_details, saved_recipes):
        self.recipe_details = recipe_details
        self.saved_recipes = saved_recipes

    # Method to export recipes to an Excel file, decorated with logging and error handling
    @log_function_call
    @handle_errors
    def export_to_excel(self, filename):
        # Create a new Excel workbook with the given filename
        workbook = xlsxwriter.Workbook(filename)
        # Add a worksheet named 'Recipes' to the workbook
        worksheet = workbook.add_worksheet('Recipes')

        # Define cell formatting styles for title, headers, and text
        title_format = workbook.add_format({
            'bold': True,  # Bold text
            'font_size': 18,  # Large font size for titles
            'align': 'center',  # Center alignment
            'valign': 'vcenter',  # Vertical center alignment
            'bg_color': '#f6eee1',  # Background color for the title cells
            'font_color': '#67595e',  # Font color for the title
            'text_wrap': True})  # Wraps text in the cell if it's too long

        header_format = workbook.add_format({
            'bold': True,  # Bold text for headers
            'font_size': 14,  # Header font size
            'align': 'left',  # Align text to the left
            'valign': 'vcenter',  # Vertical center alignment
            'bg_color': '#f6eee1',  # Header background color
            'font_color': '#67595e'})  # Header font color

        text_format = workbook.add_format({
            'font_size': 12,  # Regular font size for body text
            'align': 'left',  # Align text to the left
            'valign': 'vcenter',  # Vertical center alignment
            'bg_color': '#f6eee1',  # Background color for body text
            'font_color': '#67595e',  # Font color for body text
            'text_wrap': True})  # Wraps text in the cell if it's too long

        blank_format = workbook.add_format({
            'bg_color': '#f6eee1'})  # Format for blank rows with background color

        # Set the width of column A to 55
        worksheet.set_column(0, 0, 55)

        # Retrieve the saved recipes from the saved_recipes object
        saved_recipes = self.saved_recipes.get_saved_recipes()

        # Initialise row counter for Excel writing
        row = 0

        # Iterate over the saved recipes, by category name
        for category, recipes in saved_recipes.items():
            # Loop through each recipe in the category
            for recipe in recipes:
                # Get the ingredients and instructions for the current recipe
                ingredients, instructions = self.recipe_details.find_instructions_ingredients(recipe)

                # Write the recipe title in the current row with title formatting
                worksheet.write(row, 0, recipe, title_format)

                # Increment row
                row += 1
                # Add a blank row with formatting
                worksheet.write(row, 0, '', blank_format)

                # Move to the next row
                row += 1
                # Write 'Ingredients' header in the next row with header formatting
                worksheet.write(row, 0, 'Ingredients', header_format)

                # Move to the next row
                row += 1
                # If ingredients found, write the ingredients list in the following row with text formatting
                if ingredients:
                    worksheet.write(row, 0, ingredients, text_format)
                # Placeholder if no ingredients found
                else:
                    worksheet.write(row, 0, 'No Ingredients', text_format)

                # Increment row
                row += 1
                # Add a blank row with formatting
                worksheet.write(row, 0, '', blank_format)

                # Move to the next row
                row += 1
                # Write 'Instructions' header in the next row with header formatting
                worksheet.write(row, 0, 'Instructions', header_format)

                # Move to the next row
                row += 1
                # If instructions found, write the instructions in the following row with text formatting
                if instructions:
                    worksheet.write(row, 0, instructions, text_format)
                # Placeholder if no instructions found
                else:
                    worksheet.write(row, 0, 'No Instructions', text_format)

                # Leave space before writing the next recipe
                row += 2

        # Close the workbook, saving the file
        workbook.close()

        # Print a confirmation message to the user
        print(f"\nYour recipes have been exported to {filename}")