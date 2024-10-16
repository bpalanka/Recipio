from allrecipes import AllRecipes
import pandas as pd

# Ask for ingredients
def getIngredientList(prompt):
    """Ask user for ingredient repeatedly to construct list.
    .param: prompt String that will ask user if they want to include or exclude ingredients
    in this list.
    """
    print(prompt)

    counter = 1
    ingredients = []
    while True:
        user_input = input("Enter ingredient {}: ".format(counter))
        if not user_input.strip():
            ans = input("Would you like to add more ingredients? (Yes/No): ")
            if ans in ["yes", "y"]:
                continue
            else:
                break
        ingredients.append(user_input)
        counter += 1
    print("Ingredients entered:", ingredients)
    return ingredients

def main():
    # User input
    print("Welcome to Recip.io! To get started, please choose \nwhether you would like to type or take a picture of your ingredients ")
    user_input = input("Please enter \"TYPE\" or \"PICTURE\": ")

    if user_input.upper() == "TYPE":
        # Empty ingredients list

        while True:
            ingredients = getIngredientList("Please enter the ingredients you have: (hit Enter twice to end)")
            
            #if ingredients list is still empty, ask again
            if ingredients == []:
                print("No ingredients were entered. \n")
            else:
                break

        exclIngred = getIngredientList("Please enter the ingredients you do not want in your recipe: (hit Enter twice to end)")

        print("Searching for recipes with ingredients:", ingredients)
        # Perform search based on the concatenated query
        recipe_result = AllRecipes.search(ingredients)
        # exit()

        if recipe_result:
            #Search:
            comboList = ingredients + exclIngred                #list of all ingredients
            query_result = AllRecipes.search(ingredients)       #get recipes with desired ingredients, long array of links + data
            eclquery_result = AllRecipes.search(comboList)      #get recipes with desired and undesired ingredients
            
            #filters out undesired recipes, adjusted to improve performance
            for recipe in query_result:
                # for excl in eclquery_result:
                if recipe in eclquery_result:
                    query_result.remove(recipe)

            main_recipe_url = recipe_result[0]['url']
            # Get the detailed information about the first recipe
            detailed_recipe = AllRecipes.get(main_recipe_url)

            # Calling DataFrame constructor on list
            df = pd.DataFrame(query_result)
            filtered_data = df[['name', 'rate']]    #Gets a filtered DatatFrame with only the name and rating of all results.
            #descending
            filtered_data = filtered_data.sort_values(by='rate', ascending=False)
            print(filtered_data)
            

            # Display result:
            #print("## %s:" % detailed_recipe['name'])  # Name of the recipe
            # Print other details of the recipe (like ingredients and steps) as needed
        else:
            print("No recipes found for the provided ingredients.")

    elif user_input.upper() == "PICTURE":
        print("I am sorry, we do not have that feature right now!")
    else:
        print("Invalid input. Please enter \"TYPE\" or \"PICTURE\".")

main()