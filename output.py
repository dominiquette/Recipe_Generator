# ===== Importing Libraries ===========
import xlsxwriter
# ===== Importing data from files ===========
from decorators import log_function_call, handle_errors


class RecipeExporter:
    def __init__(self, recipe_details, saved_recipes):
        self.recipe_details = recipe_details
        self.saved_recipes = saved_recipes

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
                ingredients, instructions = self.recipe_details.find_instructions_ingredients(recipe)

                # Write the recipe name in cell A1
                worksheet.write(row, 0, recipe, title_format)

                # Write blank row
                row += 1
                worksheet.write(row, 0, '', blank_format)

                # Write 'Ingredients' in cell A3
                row += 1  # Move to row 3
                worksheet.write(row, 0, 'Ingredients', header_format)

                # Write the ingredients starting from cell A4
                row += 1
                if ingredients:
                    worksheet.write(row, 0, ingredients, text_format)
                else:
                    worksheet.write(row, 0, 'No Ingredients', text_format)

                # Write blank row
                row += 1
                worksheet.write(row, 0, '', blank_format)

                # Write 'Instructions' in cell A6
                row += 1  # Move to row 6
                worksheet.write(row, 0, 'Instructions', header_format)

                # Write the actual instructions starting from cell A7
                row += 1  # Move to row 7
                if instructions:
                    worksheet.write(row, 0, instructions, text_format)
                else:
                    worksheet.write(row, 0, 'No Instructions', text_format)

                # Move to the next recipe, add some space before the next block
                row += 2

        workbook.close()
        print(f"\nYour recipes have been exported to {filename}")