from allrecipes import AllRecipes
import pandas as pd
import Recipio as rec
import sys
def getIngredientList(prompt, image,include_measurement=True):
    """Ask user for ingredients repeatedly to construct a list.
    param: prompt String that will ask user if they want to include or exclude ingredients.
    param: include_measurement Boolean to determine if measurements are needed.
    """
    print(prompt)
    user_dict = {}
    #if image recognition was not used
    if(not image):
        while True:
            ingredient = input("Enter ingredient (or press Enter to stop): ")
            if not ingredient:  # Stop if ingredient is empty
                print("Ending list...")
                break

        # Ask for measurement if including ingredients
            if include_measurement:
                while True:
                    measurement = input("Enter measurement for {ingredient} (include units): ")
                    if measurement:  # Only accept non-empty measurement
                        break
                    print("Measurement cannot be empty. Please provide a value.")
            else:
                measurement = None  # No measurement for excluded ingredients
        
        # Add to the dictionary
            user_dict[ingredient] = measurement
    #if image recognition was used
    else:
        i=0
        #while loop that loops through every other index starting with 0
        while(i<len(image)-1):
            user_dict[image[i]]=image[i+1]
            i+=2
    return user_dict
def main():
    print("Welcome to Recip.io!")
    '''image=True
    if(image):
        arr=rec.imager(THE_IMAGE_HERE)'''
    #run the below code if there's an image passed
    image=rec.preload()
    # Get ingredients to include
    ingredients_incl = getIngredientList("Please start typing your ingredients and measurements below (hit enter twice to end your list)",image, include_measurement=True)
    print("Ingredients entered:", ingredients_incl)

    # Get ingredients to exclude
    ingredients_excl = getIngredientList("Please start typing the ingredients you want to exclude (hit enter twice to end your list)",False, include_measurement=False)
    print("Ingredients excluded:", ingredients_excl)

    # If the ingredient list is empty, ask again
    if not ingredients_incl: 
        print("No ingredients were entered. Exiting...\n")
        return

    # Collect the ingredients for searching recipes
    query = ', '.join(ingredients_incl.keys())  # Form a query string from included ingredients
    
    # Search for recipes
    query_result = AllRecipes.search(query)

    # Check if results were returned
    if not query_result:
        print("No recipes found matching your ingredients.")
        return

    # Get the most relevant recipe
    main_recipe_url = query_result[0]['url']
    detailed_recipe = AllRecipes.get(main_recipe_url)  # Get the details of the first returned recipe

    # Convert the query result to a DataFrame
    df = pd.DataFrame(query_result)

    # Display relevant data
    print("Available Recipes:")
    print(df)
    # Filter and sort the DataFrame
    filtered_data = df[['name', 'rate']].sort_values(by='rate', ascending=False)
    filtered_data = df['name']
    print(filtered_data)
    #print("Filtered and Sorted Recipes:")
    #print(filtered_data)

# Run the main function
main()
