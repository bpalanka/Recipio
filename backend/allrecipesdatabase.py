from allrecipes import AllRecipes
import pandas as pd

# Ask for ingredients
def getIngredientList(prompt):
    """Ask user for ingredients repeatedly to construct a list.
    param: prompt String that will ask user if they want to include or exclude ingredients.
    """
    print(prompt)
    # Dictionary to store ingredients and their measurements
    user_dict = {}
    while True:
        key = input("Enter ingredient (or press Enter to stop): ")
        if not key:  # Stop if key is empty
            print("Ending list...")
            break
        value = input(f"Enter measurement for {key} (include units): ")
        if not value:  # Stop if value is empty
            print("Measurement cannot be empty. Please provide a value.")
            continue  # Repeat the loop

        # Add to the dictionary
        user_dict[key] = value
    
    return user_dict


def main():
    # User input
    print("Welcome to Recip.io!")

    # Get ingredients from user
    ingredients_incl = getIngredientList("Please start typing your ingredients and measurements below (hit enter twice to end your list)")

    # Print ingredient list (for testing purposes)
    print("Ingredients entered:", ingredients_incl)

    #Get ingredients the user wants to exclude
    ingredients_excl = getIngredientList("Please start typing your ingredients and measurements below (hit enter twice to end your list)")

    # Get excluded ingredients
    

    # If the ingredient list is empty, ask again
    if not ingredients_incl: 
        print("No ingredients were entered. Exiting...\n")
        return

main()