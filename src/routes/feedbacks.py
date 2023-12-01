
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

    prompt = f"""Your task is to answer the conversation based on video transcript of an interview, and comment. Ensure the response is concise and give bullet points. 
                If the interview transcript pertains to behavioral questions, use the STAR method to organize your improvements. For other questions like the introduction please don’t use the STAR method. 
                Do not exceed 200 words. Format your answer in a HTML format
                Transcript: ```{transcript}```
                Comment: ```{comment}```"""

    messages = [{
        "role": "system",
        "content": prompt
        }]

    messages += data['messages'] # append user messages

    response = openai.ChatCompletion.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages,
        temperature=0,
    )

    response = response["choices"][0]["message"]["content"]
    print(response)
    return convert_to_json_resp(response)
