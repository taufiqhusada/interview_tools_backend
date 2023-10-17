
from flask import Flask, request
from flask_cors import CORS
import os
from routes.interview_annotations import annotations_bp
from routes.interviews import interviews_bp
from routes.feedbacks import feedbacks_bp

from database.db import initialize_db
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
initialize_db(app)

@app.route("/")
def hello_world():
    return  "hello world"

app.register_blueprint(interviews_bp)
app.register_blueprint(annotations_bp)
app.register_blueprint(feedbacks_bp)


