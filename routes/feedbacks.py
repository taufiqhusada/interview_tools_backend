
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config


feedbacks_bp = Blueprint('feedbacks', __name__)

@feedbacks_bp.route('/feedbacks', methods=['POST'])
def get_interviews():
    data = request.json

    question = data['question']
    transcript = data['transcript']
    comment = data['comment']

    prompt = f"""Your task is to answer a question based on a question, video transcript, and comment  
                Question: ```{question}```
                Transcript: ```{transcript}```
                Comment: ```{comment}```"""


    openai = init_openai_config()

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "user",
        "content": prompt
        },
    ],
    )

    response = response["choices"][0]["message"]["content"]
    return convert_to_json_resp(response)
