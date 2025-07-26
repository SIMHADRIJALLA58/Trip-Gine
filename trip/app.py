import os
from flask import Flask, render_template, request, redirect, session, abort
# render_template for displaying HTML pages
# request for form data
# redirect for redirecting
# session for session handling
# abort for handling 404 errors

from pymongo import MongoClient

# ✅ Local MongoDB connection (Campus)
# muri = 'mongodb://localhost:27017'
muri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(muri)
print("DB connected")

# ✅ Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session handling

# ✅ Home route (landing page)
@app.route('/')
def home():
    return render_template('landing.html')

# ✅ Login page
@app.route('/login.html')
def login():
    return render_template('login.html')

# ✅ Main dashboard page
@app.route('/main.html')
def main():
    return render_template('main.html')

# ✅ Signup page
@app.route('/signup.html')
def signup():
    return render_template('signup.html')

# ✅ Handle Signup Form submission
@app.route('/signupForm', methods=["POST"])
def signupForm():
    username = request.form["username"]
    password = request.form["password"]
    data = {"username": username, "password": password}

    # ✅ Use your DB and collection
    db = client["admin"]
    collection = db["trip"]

    existing_user = collection.find_one({"username": username})
    print(data)

    if existing_user is None:
        collection.insert_one(data)
        return render_template('login.html', msg="Registration successful")
    else:
        return render_template('signup.html', msg="Username already exists")

# ✅ Handle Login Form submission
@app.route('/loginForm', methods=["POST"])
def loginForm():
    username = request.form["username"]
    password = request.form["password"]
    db = client["admin"]
    collection = db["trip"]

    user = collection.find_one({"username": username, "password": password})

    if user:
        session["username"] = username
        return render_template('main.html')
    else:
        return render_template("login.html", err="Invalid credentials")

# ✅ Start the server
# if __name__ == "__main__":
#     app.run(
#         host="0.0.0.0",  # Use 127.0.0.1 for local only
#         port=8000,
#         debug=True
#     )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
