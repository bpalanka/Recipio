#Recipio with Gemini
from allrecipes import AllRecipes
import pandas as pd
import Recipio as rec

def getIngredientList(prompt, image=None, include_measurement=True):
    """Collects ingredients from user input or image recognition output."""
    print(prompt)
    user_dict = {}

    if not image:  # Manual input
        while True:
            ingredient = input("Enter ingredient (or press Enter to stop): ")
            if not ingredient:  # Stop if ingredient is empty
                print("Ending list...")
                break

            if include_measurement:
                while True:
                    measurement = input(f"Enter measurement for {ingredient} (include units): ").strip()
                    if measurement:  # Only accept non-empty measurement
                        break
                    print("Measurement cannot be empty. Please provide a value.")
            else:
                measurement = None  # No measurement for excluded ingredients
            
            user_dict[ingredient] = measurement
    else:  # Use recognized ingredients from image
        i = 0
        while i < len(image) - 1:
            user_dict[image[i]] = image[i + 1]
            i += 2

    return user_dict

def main():
    print("Welcome to Recip.io!")

    # If image recognition is used, preprocess the image
    '''image=True
    if(image):
        arr = rec.imager(THE_IMAGE_HERE)'''  # Uncomment if you have an image recognition function
    image = rec.preload()

    # Get ingredients to include
    ingredients_incl = getIngredientList(
        "Please start typing your ingredients and measurements below (hit enter twice to end your list)", 
        image=image, 
        include_measurement=True
    )
    print("Ingredients to include:", ingredients_incl)

    # Get ingredients to exclude
    ingredients_excl = getIngredientList(
        "Please start typing the ingredients you want to exclude (hit enter twice to end your list)",
        include_measurement=False
    )
    print("Ingredients to exclude:", ingredients_excl)

    if not ingredients_incl:
        print("No ingredients were entered. Exiting...\n")
        return

    # Create query string from included ingredients
    query = ', '.join(ingredients_incl.keys()).lower()

    # Search for recipes
    try:
        query_result = AllRecipes.search(query)
    except Exception as e:
        print("An error occurred while searching for recipes:", e)
        return

    if not query_result:
        print("No recipes found matching your ingredients.")
        return

    # Filter recipes to exclude certain ingredients
    excluded_set = {excl.lower() for excl in ingredients_excl}
    filtered_recipes = []

    for recipe in query_result:
        recipe_ingredients = {ing.lower() for ing in recipe.get('ingredients', [])}

        if excluded_set.intersection(recipe_ingredients):
            continue  # Skip if any excluded ingredient is found

        # If the recipe passes the filter, add it to the list
        filtered_recipes.append(recipe)

    # Convert to DataFrame and sort by rating
    df = pd.DataFrame(filtered_recipes)
    filtered_data = df[['name', 'rate']].sort_values(by='rate', ascending=False)

    # Display available recipes and sorted list
    print("\nAvailable Recipes:")
    print(df)
    print("\nFiltered and Sorted Recipes by Rating:")
    print(filtered_data['name'])

    # Display ingredients and steps for each filtered recipe
    print("\nDetailed Recipe Information:")
    for recipe in filtered_recipes:
        print("Title:", recipe.get('name', 'Unknown Title'))
        print("URL:", recipe.get('url', 'No URL Available'))

        # Retrieve full recipe details
        detailed_recipe = AllRecipes.get(recipe.get('url'))

        # Display ingredients
        print("\nIngredients:")
        if 'ingredients' in detailed_recipe:
            for ingredient in detailed_recipe['ingredients']:
                print(ingredient)
        else:
            print("No ingredients found.")

        # Display steps
        print("\nSteps:")
        if 'steps' in detailed_recipe:
            for step in detailed_recipe['steps']:
                print(step)
        else:
            print("No steps found.")
        print("\n" + "-"*40 + "\n")

# Run the main function
main()
