# CFG-Group-Project-5
## First Code
04-08 We create the first shared code from Dom's Code
## a lot of code later hah
10-08 comments from anto's work, explaining and a general suggestion
+ I had to create a new account. I suggested not showing 10 recipes every time we try and reduce them to 2 - we could 
decide when everything is working the right number to the users, but for us to try I think this is okay,
what do you think? I change it in this version
+ First I try to compare the codes and the classes but I was getting nowhere the classes seems right
So, I try the main code before the classes and Dominique Code before the classes: 
both of them didn't show the ingredients 
Thus, I confirm it wasn't a problem of classes it was on the original code
Gladly Dominique fixed that code on api-links So I compared Dominique's code with the new main code (Eve), 
after a while trying different parts I realized that the function display_recipes was different. 
I copy the new Dominique's display_recipes function from api-links and adapted to Eve code with classes and it work!
+ Some small thing: the welcome message is after the question about the name. I voted to remove that part
I've only added it to add error handling but we would have other parts to add this.
+ I try the code without the function get_headers and it works, so I erased it

## Adding deque

I modified main and display files

+ Display: I only edit adding a new category: "[4] View your Recipes names so far", please change the writing if you want

+ Main - I added:

from collections import deque at first

Only change the def run function:
    + I added a line to create a list using deque: total_titles = deque()
    + In each choice (1,2,3): 1. I added the titles of the recipes to the list 2. I leave the print mssg in case you  
want to try it. 3. I added in two different ways to decide which one is the best (like dictionary or with a msg)
    + I created a new category in the main menu with the code to show 

+ When we decided how we want it I could improve the way that the user see the results I don't know if we could do it   
with decorators or adding a display_recipes_names function in the display file

## Adjust the parameters based on the selected category

12/08
fixing the  def find_recipes_by_category(self, category) adding the if statements on 
def fetch_recipes_by_category(category) on api-links branch

18/08

Errors:
1) I found that we set as param "type": category
In category include things that the api has in other params, for ex. fish is not
2) The if statements categories didn't match with the category mapping in display

Changes:

+ display.py file
As we agreed in the meeting I changed the class MenuDisplay
The category_menu_items is change and accordingly the category_mapping to translate user input
+ app.py file
I created the abstract class CategoryParams and all the inherit classes according to each option.
To do so, I used the abc library
I changed  the find_recipe_instructions to use the abstract class
Also I edited the common params to erase type, add random sort and ignore pantry
