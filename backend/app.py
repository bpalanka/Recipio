# Import necessary libraries and functions
from flask import Flask, jsonify, request
import requests

# Creating a Flask app
app = Flask(__name__)

# Replace this with your actual Spoonacular API key
API_KEY = '34639591c01a4fe28a8a42da2678fa33'

# Function to search for recipes based on ingredients
def search_recipes(api_key, include_ingredients, exclude_ingredients):
    include = ','.join(include_ingredients)  # Ingredients to include
    exclude = ','.join(exclude_ingredients)  # Ingredients to exclude

    # Prepare the API request URL
    url = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=" + api_key + "&ingredients=" + include + "&ignorePantry=true&number=5"
    if exclude:
        url += "&excludeIngredients=" + exclude

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Error fetching data from Spoonacular", "details": response.json()}, response.status_code

    return response.json(), 200

# Function to get detailed recipe information
def get_recipe_details(api_key, recipe_id):
    url = "https://api.spoonacular.com/recipes/" + str(recipe_id) + "/information?apiKey=" + api_key
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Error fetching details for recipe ID " + str(recipe_id), "details": response.json()}, response.status_code

    return response.json(), 200

# Route to search for recipes
@app.route('/search_recipes', methods=['POST'])
def api_search_recipes():
    # Get JSON data from request
    data = request.json
    include_ingredients = data.get("include_ingredients", [])
    exclude_ingredients = data.get("exclude_ingredients", [])

    if not include_ingredients:
        return jsonify({"error": "No ingredients provided to include"}), 400

    recipes, status_code = search_recipes(API_KEY, include_ingredients, exclude_ingredients)
    return jsonify(recipes), status_code

# Route to get detailed recipe information
@app.route('/recipe_details/<int:recipe_id>', methods=['GET'])
def api_get_recipe_details(recipe_id):
    recipe_details, status_code = get_recipe_details(API_KEY, recipe_id)
    return jsonify(recipe_details), status_code

# Root route providing API instructions
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "endpoints": {
            "POST /search_recipes": "Search recipes by including and excluding ingredients. Provide 'include_ingredients' and 'exclude_ingredients' in the JSON body.",
            "GET /recipe_details/<recipe_id>": "Get detailed information about a recipe by providing its recipe ID."
        }
    })

# Main function
if __name__ == '__main__':
    app.run(debug=True)

