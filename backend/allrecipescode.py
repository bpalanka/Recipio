import requests  # Required to make HTTP requests to the Spoonacular API

def getIngredientList(prompt, include_measurement=True):
    print(prompt)
    user_dict = {}
    
    while True:
        ingredient = input("Enter ingredient (or press Enter to stop): ").strip()
        if not ingredient:
            print("Ending list...\n")
            break

        if include_measurement:
            measurement = input("Enter measurement for " + ingredient + " (include units): ").strip()
            user_dict[ingredient.lower()] = measurement  # Store ingredients in lowercase for consistency
        else:
            user_dict[ingredient.lower()] = None
    
    return user_dict

def search_recipes(api_key, include_ingredients, exclude_ingredients):
    include = ','.join(include_ingredients.keys())  # Ingredients to include
    exclude = ','.join(exclude_ingredients.keys())  # Ingredients to exclude
    
    # Prepare the API request
    url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={include}&ignorePantry=true&number=5"
    if exclude:
        url += f"&excludeIngredients={exclude}"
    
    print(f"Searching for recipes with URL: {url}")

    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching data from Spoonacular:", response.json())
        return []
    
    return response.json()

def get_recipe_details(api_key, recipe_id):
    # Get detailed information about a specific recipe by its ID
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching details for recipe ID {recipe_id}: {response.json()}")
        return None
    
    return response.json()

def display_recipes(api_key, recipes):
    if not recipes:
        print("No recipes found matching your ingredients.")
        return

    print("\nAvailable Recipes:\n" + "=" * 20 + "\n")
    for idx, recipe in enumerate(recipes, 1):
        recipe_id = recipe.get('id')
        print(f"## Recipe {idx}: {recipe.get('title', 'Unknown Title')}")
        print(f"ID: {recipe_id}")
        print(f"Link: https://spoonacular.com/recipes/{recipe.get('title').replace(' ', '-')}-{recipe_id}")
        
        # Get detailed recipe information
        detailed_recipe = get_recipe_details(api_key, recipe_id)
        if detailed_recipe:
            # Display ingredients used in the recipe
            print("\nIngredients used in this recipe:")
            for ingredient in detailed_recipe.get('extendedIngredients', []):
                # Safely access ingredient information
                ingredient_name = ingredient.get('name', 'Unknown Ingredient')
                ingredient_amount = ingredient.get('amount', 'N/A')
                ingredient_unit = ingredient.get('unit', '')
                print(f"  - {ingredient_amount} {ingredient_unit} {ingredient_name}")

            # Display cooking steps
            print("\nCooking Steps:")
            instructions = detailed_recipe.get('analyzedInstructions', [])
            if instructions:
                for step in instructions[0].get('steps', []):
                    print(f"  - {step.get('step', 'Unknown step')}")
            else:
                print("  - No cooking steps found.")

        print("\n" + "-" * 40 + "\n")

def main():
    print("Welcome to Recip.io!\n")
    
    # Your actual API key
    api_key = ''

    # Get included ingredients from user
    ingredients_incl = getIngredientList("Enter ingredients to include (with measurements):", include_measurement=True)
    print("Ingredients to include:", ingredients_incl)

    # Get excluded ingredients from user
    ingredients_excl = getIngredientList("Enter ingredients to exclude:", include_measurement=False)
    print("Ingredients to exclude:", ingredients_excl)

    if not ingredients_incl:
        print("No ingredients to include were entered. Exiting...")
        return

    # Search for recipes using Spoonacular API
    recipes = search_recipes(api_key, ingredients_incl, ingredients_excl)

    # Display the found recipes with detailed ingredients and steps
    display_recipes(api_key, recipes)

# Ensure that the main function is called only when this script is executed directly
if __name__ == "__main__":
    main()
