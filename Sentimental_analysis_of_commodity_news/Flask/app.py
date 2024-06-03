
from flask import Flask, render_template, request, session, redirect, url_for
import pickle

model = pickle.load(open("ran_for.pkl", "rb"))
app = Flask(__name__)
app.secret_key = "hema"  # Set a secret key for session management

@app.route("/", methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        session['newsline'] = request.form["news-input"]
        return redirect(url_for('predictionpage'))  # Redirect to the prediction page

    return render_template("index.html")

@app.route("/prediction", methods=["POST", "GET"])
def predictionpage():
    if 'newsline' not in session:
        return redirect(url_for('homepage'))  # Redirect to the homepage if newsline is not in session

    newsline = session['newsline']
    pred = [newsline]
    output = model.predict(pred)

    if output == 0:
        sentiment = 'Positive'
    elif output == 1:
        sentiment = 'Negative'
    else:
        sentiment = ''

    session.pop('newsline')  # Remove newsline from session after prediction

    return render_template("result.html", sentiment=sentiment)

if __name__ == "__main__":
    app.run(debug=True)