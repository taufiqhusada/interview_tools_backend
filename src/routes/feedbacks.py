
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

                - If the user seeks to enhance a segment of their interview response that is already satisfactory in terms of detail, effectiveness, appropriateness, efficiency, clarity, and task achievement, using the STAR method (Situation, Task, Action, Result) when applicable, affirm its adequacy and advise against further revisions.
                - When improvement is necessary, offer constructive feedback.
                - Provide an objective evaluation of the interview performance, kindly but honestly pointing out areas of weakness.
                - Employ the STAR method for feedback on performance-based questions, excluding it for introductory responses.
                - Instead of suggesting the use of the STAR method, demonstrate it by breaking it down step by step.
                - Start with the positives in the user's response before offering areas for improvement.
                - Limit your response to 200 words and format it in HTML.

                Transcript: ```{transcript}```
                Comment: ```{comment}```
                """

    messages = [{
        "role": "system",
        "content": prompt
        }]
    
    reminder_prompt = "- If the user seeks to enhance a segment of their interview response that is already satisfactory in terms of detail, effectiveness, appropriateness, efficiency, clarity, and task achievement, using the STAR method (Situation, Task, Action, Result) when applicable, affirm its adequacy and advise against further revisions."

    messages += data['messages'] # append user messages

    messages += [{
        "role": "system",
        "content": reminder_prompt,
    }]

    response = openai.chat.completions.create(
        model=os.getenv('OPENAI_GPT_MODEL'),
        messages=messages,
        temperature=0,
    )

    response = response.choices[0].message.content
    return convert_to_json_resp(response)
