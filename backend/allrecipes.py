# Import necessary libraries
from allrecipes import AllRecipes

# Function to prompt user for ingredients and exclude ingredients
def ingredientInput():
    ingredients = []
    ingredExcl = []

    # Function to input ingredients
    def inputIngredients(prompt):
        ingredients_list = []
        counter = 1
        while True:
            user_input = input(prompt.format(counter))
            if not user_input.strip():
                break
            ingredients_list.append(user_input)
            counter += 1
        return ingredients_list

    print("Please enter the ingredients you have: (hit Enter twice to end)")
    ingredients = inputIngredients("Enter ingredient {}: ")

    print("Please enter the ingredients you would like to exclude: (hit Enter twice to end)")
    ingredExcl = inputIngredients("Enter excluded ingredient {}: ")

    return ingredients, ingredExcl

# User input
print("Welcome to Recip.io! To get started, please choose whether you would like to type or take a picture of your ingredients")
user_input = input("Please enter \"TYPE\" or \"PICTURE\": ")

if user_input.upper() == "TYPE":
    ingredients, ingredExcl = ingredientInput()
    query = " ".join(ingredients)
    print("Searching for recipes with ingredients:", query)
    
    # Search for recipes
    recipe_results = AllRecipes.search(query)
    
    # Filter out recipes containing excluded ingredients
    if recipe_results:
        filtered_recipes = []
        for recipe in recipe_results:
            excluded = False
            if 'name' in recipe and 'ingredients' in recipe:
                for excl in ingredExcl:
                    if excl.lower() in recipe['name'].lower() or any(excl.lower() in ing.lower() for ing in recipe['ingredients']):
                        excluded = True
                        break
            if not excluded:
                filtered_recipes.append(recipe)
        
        if filtered_recipes:
            for idx, filtered_recipe in enumerate(filtered_recipes):
                print(f"Recipe {idx+1}: {filtered_recipe['name']}")
                main_recipe_url = filtered_recipe['url']
                detailed_recipe = AllRecipes.get(main_recipe_url)
                print("## %s:" % detailed_recipe['name'])
                for ingredient in detailed_recipe['ingredients']:
                    print(" %s" % ingredient)
                print()  # Print an empty line for separation
        else:
            print("No recipes found without the excluded ingredients.")
    else:
        print("No recipes found for the provided ingredients.")
else:
    print("Invalid input. Please enter \"TYPE\" or \"PICTURE\".")
