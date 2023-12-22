
from flask import Flask, request
from flask_cors import CORS
import os
from routes.interview_annotations import annotations_bp
from routes.interviews import interviews_bp
from routes.feedbacks import feedbacks_bp
from routes.repetition import repetition_bp
from routes.videoProcessor import video_processor_bp
from routes.simulation import simulation_bp

from database.db import initialize_db
from dotenv import load_dotenv


import firebase_admin
from firebase_admin import credentials, storage

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
app.register_blueprint(repetition_bp)
app.register_blueprint(video_processor_bp)
app.register_blueprint(simulation_bp)

cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred, {"storageBucket": os.getenv('FIREBASE_BUCKET')})


