
from flask import Blueprint, request, jsonify
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config
import os
import asyncio

identification_bp = Blueprint('identification', __name__)

@identification_bp.route('/identification', methods=['POST'])
async def get_moments():
    data = request.json
    transcript = data['transcript']

    res = await process_get_moments(transcript)
    return res

async def process_get_moments(transcript):
    openai = init_openai_config()

    prompt = f"""Your task is to decide whether the way user answer the interview is 'very good', 'good', or 'need improvement' baesed on the Transcript delimited by triple backticks. 
                Format your answer as a string of 'very good', 'good', or 'need improvement'. 
                Answer is defined as 'need improvement' if the answer lack of some of these points
                - Lack of details
                - If the interview can be answered using the STAR method but user does not do it. For other questions like the introduction it is not required to use the STAR method. 
                - Also consider the interview answer in terms of Effectiveness, Appropriateness, Efficiency, Verisimilitude (Clarity), Task-Achievement (Competence on answering the interview correctly).
        
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