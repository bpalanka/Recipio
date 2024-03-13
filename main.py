from flask import Flask, render_template, url_for
from allrecipes import AllRecipes

app = Flask(__name__)

query_result = AllRecipes.search("rice tomato chicken")

@app.route("/")
def home():
    return render_template('home.html', recipes=query_result)

if __name__ == '__main__':
    app.run(debug=True)


