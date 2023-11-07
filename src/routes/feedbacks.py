
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config
import os

feedbacks_bp = Blueprint('feedbacks', __name__)

@feedbacks_bp.route('/feedbacks/conversation', methods=['POST'])
def do_conversation():
    data = request.json
    print(data)

    openai = init_openai_config()

    transcript = data['transcript']
    comment = data['comment']

    prompt = f"""Your task is to answer the conversation based on video transcript of an interview, and comment. Make sure your answer is concise and providing key points. 
                Transcript: ```{transcript}```
                Comment: ```{comment}```"""

    messages = [
        {
        "role": "system",
        "content": prompt
        },
    ]

    messages += data['messages'] # append user messages

    response = openai.ChatCompletion.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages
    )

    response = response["choices"][0]["message"]["content"]
    return convert_to_json_resp(response)
