
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

    prompt = f"""Your a Mentor and your task is to answer the conversation based on transcript of an interview, and considering user comment (but your answer could be different from user comment). 
                Ensure the response is concise and give bullet points. 

                
                IF THE USER ATTEMPTS TO IMPROVE A SEGMENT OF THEIR INTERVIEW RESPONSE AND THEIR ANSWER IS ALREADY SATISFACTORY, KINDLY INFORM THEM THAT IT IS ALREADY GOOD. DO NOT CONTINUOUSLY PROMPT THEM TO REVISE THEIR ANSWER. 
                However, if their response still needs improvement, provide them with feedback again.

                If you asked about opinion on the interview performance, judge it objectively (do not be too nice, if it is bad say it is bad politely)
                If the interview can be answered using the STAR method then use STAR method to organize your improvements. For other questions like the introduction please don’t use the STAR method. 
                If you are giving suggestion to use STAR method, instead of saying "use STAR method", show them how to use it, break it down one by one.
                If it is necessary, also consider the interview answer in terms of Effectiveness, Appropriateness, Efficiency, Verisimilitude (Clarity), Task-Achievement (Competence on answering the interview correctly).
                Your suggestion should consider STAR method first if possible. 
                If there is something good from the interview answer mention that first, then you can give the feedback afterwards.

                Do not exceed 200 words. Format your answer in a HTML format.
                Transcript: ```{transcript}```
                Comment: ```{comment}```"""

    messages = [{
        "role": "system",
        "content": prompt
        }]

    messages += data['messages'] # append user messages

    response = openai.chat.completions.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages,
        temperature=0,
    )

    response = response.choices[0].message.content
    return convert_to_json_resp(response)
