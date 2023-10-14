
from flask import Flask, request
from flask_cors import CORS
import os
from routes.interview_annotations import annotations_bp
from routes.interviews import interviews_bp

from database.db import initialize_db

app = Flask(__name__)
CORS(app)
initialize_db(app)

app.config["openai_api_key"] = os.getenv("openai_api_key")
app.config["openai_model"] = "gpt-4"

@app.route("/")
def hello_world():
    return  "hello world"

app.register_blueprint(interviews_bp)
app.register_blueprint(annotations_bp)


