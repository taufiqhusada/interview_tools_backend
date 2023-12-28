
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config
import os

identification_bp = Blueprint('identification', __name__)

@identification_bp.route('/identification', methods=['POST'])
def get_moments():
    data = request.json
    transcript = data['transcript']

    return convert_to_json_resp(process_get_moments(transcript))

async def process_get_moments(transcript):
    openai = init_openai_config()

    prompt = f"""Your task is to decide whether the way user answer the interview is 'very good', 'good', or 'need improvement' baesed on the Transcript delimited by triple backticks. 
                Format your answer as a string of 'very good', 'good', or 'need improvement'. 
                Answer is defined as 'need improvement' if the answer lack of detail of specific experience, or not concise answer, or not relevant answer, or does not give enough explanation, or if it is possible to be answered using STAR method but user does not do it.
                Transcript: ```{transcript}```
                `"""

    messages = [{
        "role": "system",
        "content": prompt
        }]

    response = openai.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=messages,
        temperature=0,
    )

    response = response.choices[0].message.content
    return response