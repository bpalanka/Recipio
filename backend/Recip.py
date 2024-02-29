# Imports
import pandas as pd
import taipy
import csv
from taipy.gui import Gui, Html
import taipy.gui.builder as tgb
import taipy as tp

import ast # converting to list

# Read csv file into data frame
csv_file_path = "./Ingredients2.csv"

# Attributes
#ingredientInput = ""
#allergyInput = ""
#finalRecommendations = []

# init state
#state=State()
ingredientInput = ""
allergyInput = ""
finalRecommendations = []



try:
    df = pd.read_csv(csv_file_path)
except pd.errors.EmptyDataError:
    print("The CSV file is empty.")
except FileNotFoundError:
    print(f"File not found: {csv_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

# Function to handle GUI actions
def on_action(state, id): # method MUST be named as "on_action" format (bc of Taipy)
    if id == "submitIngredients": # when you press the submit button for ingredients, this happens
        # Accessing state variables
        userIngredient = ""
        userAllergy = ""

        # putting the inputs into respective lists.
        if("," not in state.ingredientInput):
            userIngredient = [state.ingredientInput]
            print(userIngredient)
        else:
            userIngredient = state.ingredientInput.split(", ")
        
        if("," not in state.allergyInput):
            userAllergy = [state.allergyInput]
        else:
            userAllergy = state.allergyInput.split(", ")
    
        #print(userIngredient) #tests
        #print(userAllergy)
            
        #look for inputs in the recipes
        final_rec = findRecipes(userIngredient, userAllergy)
        print(final_rec[0][2])

        page = Html("""
                    <taipy:text>Name: {final_rec[0][0]} </taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Match: {final_rec[0][3]} </taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Ingredients: {final_rec[0][2]} </taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Instructions: {final_rec[0][1]} </taipy:text>
                    <br></br>
                    <br></br>
                    
                    <taipy:text> {final_rec[1][0]} </taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Match: {final_rec[1][3]} </taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Ingredients: {final_rec[1][2]} </taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Instructions: {final_rec[1][1]}</taipy:text>
                    <br></br>
                    <br></br>

                    <taipy:text>Name: {final_rec[2][0]}</taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Match: {final_rec[2][3]}</taipy:text>
                    <br></br>al
                    <br></br>
                    <taipy:text>Ingredients: {final_rec[2][2]}</taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Instructions: {final_rec[2][1]}</taipy:text>
                    <br></br>
                    <br></br>

                    
                    <taipy:text>Name: {final_rec[3][0]} </taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Match: {final_rec[3][3]} </taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Ingredients: {final_rec[3][2]}</taipy:text>
                    <br></br>
                    <br></br>
                    <taipy:text>Instructions: {final_rec[3][1]}</taipy:text>
                    <br></br>
                    <br></br>
                    
                    """)
        Gui(page).run(port=5006)


# Function to process user's ingredients and allergies, and then find recipes
def findRecipes(userIngredient, userAllergy):
    count = 0 # keep track of matches
    counts = [] # keep track of the amt of matches between the recipes and the user's ingredients
    countsMax = [] # max matches of ingredients (total amt of their ingredients)

    matchRatio = []
    
    recommendations = []

    # Convert string rep of lists in 'Ingredients' to actual lists
    ingredientsToSearch = [ast.literal_eval(ingredients) for ingredients in df["Ingredients"]] # do NOT ask me how this works. -Arman

    for i in range(0, len(ingredientsToSearch)) :
        countsMax.append([len(ingredientsToSearch[i]), i]) # creates list of all the max matches of ingredients. and also the indeces
    #print(countsMax) # TESTING

    for i in range(0, len(ingredientsToSearch)): # cycle through the recipes
        count = 0 # ingredient match count reset to 0
        for j in range(len(ingredientsToSearch[i])): # cycle through each ingredient in the recipe
            for k in range(len(userIngredient)): # cycle through the ingredients which the user has
                if(userIngredient[k] in ingredientsToSearch[i][j]): # if the user has the ingredient that is specified
                    print(userIngredient[k])
                    #print(ingredientsToSearch[i][j])
                    count += 1
                    #print("User ingredient:", userIngredient[k]) #TEST
                    #print("Recipe ingredient:", ingredientsToSearch[i][j]) #TEST
            for a in range(len(userAllergy)):
                if(userAllergy[a] in ingredientsToSearch[i][j]):
                    count = 0
        counts.append(count)

    #print(counts) # TESTING

    print(counts)
    print(countsMax)
    for i in range(0, len(ingredientsToSearch)) :
        matchRatio.append([round(counts[i]/countsMax[i][0], 3), countsMax[i][1]]) # finds the percentage match between the ingredients and the recipes. the closer it is to 1, the better the match.
    #print(matchRatio) #TESTING

    matchRatio.sort(reverse=True) # sorts greatest to least.
    #print(matchRatio) #TESTING

    #for i in range(0, len(matchRatio)) :
    for i in range(min(4, len(matchRatio))) :
        #recs.append[[df["Title"].iloc[matchRatio[i][1]]], [df["Instructions"].iloc[matchRatio[i][1]]], [df["Ingredients"].iloc[matchRatio[i][1]]] ]
        if(matchRatio[i][0] == 0):
            break
        
        title = (df["Title"].iloc[matchRatio[i][1]])
        instructions = (df["Instructions"].iloc[matchRatio[i][1]])
        ingredients = ""
        for j in range(len(ingredientsToSearch[matchRatio[i][1]])): # printing the list of ingredients properly
            if(j != len(ingredientsToSearch[matchRatio[i][1]]) - 1):
                ingredients = ingredients + ingredientsToSearch[matchRatio[i][1]][j] + ", "
            else:
                ingredients = ingredients + ingredientsToSearch[matchRatio[i][1]][j]
        ingredientMatch = str(round((matchRatio[i][0] * 100), 3)) + "%"

        recommendations.append([title, instructions, ingredients, ingredientMatch])
    
    finalRecommendations = recommendations 
    #print(finalRecommendations)
    #print(finalRecommendations[0][1])
    return finalRecommendations

# Set up GUI
with tgb.Page() as page:
    with tgb.layout("1"):
        with tgb.part():
            tgb.html("h1", "Welcome to Recip.io!")
            tgb.input("{ingredientInput}", label="List your ingredients...")
            tgb.input("{allergyInput}", "Any ingredients to avoid?", label="List your allergies and avoidances...")
            tgb.button("Submit", id="submitIngredients")



        #recommendation_elements = create_recommendation_elements(finalRecommendations)
        #for element in recommendation_elements:
        #    with tgb.part():
        #        element



# Run the GUI
Gui(page).run(port=5005)


#for recipes: if the user has all ingredients let them know
#if user is missing some ingredients, let them know
    
# cooking filters: allergies, dietary restrictions (halal, vegetarian, etc.)
