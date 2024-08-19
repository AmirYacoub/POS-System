from flask import Flask
from google.cloud import firestore
import os

# Path to the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "church-pos-554e25213dcd.json"

app = Flask(__name__)

# Initialize Firestore DB
db = firestore.Client()

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
