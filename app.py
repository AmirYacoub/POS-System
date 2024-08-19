from flask import Flask
from google.cloud import firestore

app = Flask(__name__)

# Initialize Firestore DB
db = firestore.Client()

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
