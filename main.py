from flask import Flask, render_template, url_for, request
from allrecipes import AllRecipes

app = Flask(__name__)

query_result = AllRecipes.search("rice tomato chicken")

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user_query = request.form["user_query"]
        global query_result
        query_result = AllRecipes.search(user_query)

    return render_template('home.html', recipes=query_result)


   

if __name__ == '__main__':
    app.run(debug=True)


