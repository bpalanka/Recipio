#Working Recipio File
import pandas as pd
from allrecipes import AllRecipes

def getIngredientList(prompt, include_measurement=True):
    print(prompt)
    user_dict = {}
    
    while True:
        ingredient = input("Enter ingredient (or press Enter to stop): ")  
        if not ingredient:
            print("Ending list...")
            break

        if include_measurement:
            measurement = input(f"Enter measurement for {ingredient} (include units): ").strip()
            user_dict[ingredient] = measurement
        else:
            user_dict[ingredient] = None
    
    return user_dict

def main():
    print("Welcome to Recip.io!")

    # Get included ingredients from user
    ingredients_incl = getIngredientList("Enter ingredients to include (with measurements):", include_measurement=True)
    print("Ingredients to include:", ingredients_incl)

    # Get excluded ingredients from user
    ingredients_excl = getIngredientList("Enter ingredients to exclude:", include_measurement=False)
    print("Ingredients to exclude:", ingredients_excl)

    if not ingredients_incl:
        print("No ingredients to include were entered. Exiting...")
        return

    # Normalize the ingredient names for the query
    query = ', '.join(ingredients_incl.keys()).lower()

    # Search recipes using AllRecipes API
    try:
        query_result = AllRecipes.search(query)  # Search for recipes
    except Exception as e:
        print("An error occurred while searching for recipes:", e)
        return

    if not query_result:
        print("No recipes found matching your ingredients.")
        return

    # Filter out recipes containing excluded ingredients
    filtered_recipes = []
    excluded_set = {excl.lower() for excl in ingredients_excl}  # Upper -> lowercase for case matching

    for recipe in query_result:
        recipe_ingredients = {ing.lower() for ing in recipe.get('ingredients', [])}  # Normalize recipe ingredients
        print(recipe_ingredients)
        # Check if the recipe contains any excluded ingredients
        if excluded_set.intersection(recipe_ingredients):
            continue

        # If the recipe passes the filter, add it to the list
        filtered_recipes.append(recipe)

    # Display the filtered recipes with ingredients and steps
    print("\nAvailable Recipes:")
    for recipe in filtered_recipes:
        print("Title:", recipe.get('name', 'Unknown Title'))
        print("URL:", recipe.get('url', 'No URL Available'), "\n")

        # Display ingredients
        print("Ingredients:")
        #NEED to display Ingredients
        # Display steps
        print("\nSteps:")
        #NEED to display steps

# Call the main function
main()
