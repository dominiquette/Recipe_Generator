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

## Unit testing first draft

+ General commments:
I used all I have to do it. sessions, code from the sessions, google, IA  
To summarize I used the file test_unit_test_example from Sophia's lesson about unit test  
However, we didn't cover in class how to unit test with classes So you we'll see comments about:
    + setUp: is like our class _init_ not the same but just to give you an idea
    + I tried to explain assert_called_with and patch inside the unit_test_app
    + useful links: 
https://docs.python.org/es/3.10/library/unittest.mock.html
https://docs.python.org/3/library/unittest.mock.html#patch
https://www.geeksforgeeks.org/python-unittest-assertin-function/

Furthermore, I think we need to ask how much is expected from us, because there are a million things to test.  
I don't know if it is necessary a unit test function for each function or only the app.py functions
I created to files regarding some functions in the app file and display file - 
We need to decide if it is better to divide them by classes depending on how many lines of code we will have.

+ unit_test_app: One function working and ideas
    + class TestSpoonacularAPI:
I wanted to test this class to check if the json response is a dict,
but I don't know how to do it without giving params and endpoint. 
I commented the code but I leave it first in case someone know how to do it
    + the function test_random_recipes_number:
we only test what happen test what happen if for some reason the response exceeded the params number: 2
I hope we could use the structure to test more things but I don't know what else test from this function
  
+ unit_test_display: This file only have ideas, I wish I have more time
    + I did a test that one only compares the input from the get_user_ingredients with some expected,
I don't think we can add this is not testing the function, only the input
That's why I wanted to test the ValueError
    +  I wanted to add something related to this ValueError, but I can't.
Also, I couldn't find a way for the app to give me this error. 
Hafsa I don't know what I'm doing wrong or maybe we need a redo
It jumps to a ValueError("API response is empty or invalid.") 
Here's an example 
![img.png](img.png)
    + Last, I want to add something related to assertIn to check if the ingredient was in the app response to combine
display and app test, but it was too hard for me



