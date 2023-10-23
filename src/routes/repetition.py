from database.models import InterviewAnnotation
from flask import request, Blueprint
from util.response import  convert_to_json_resp
from config.openai_connector import init_openai_config

repetition_bp = Blueprint('repetitions', __name__)


@repetition_bp.route('/repetition/feedbacks', methods=['POST'])
def get_():
    data = request.json

    sessionIDs = data['sessionIDs']
    question = data['question']

    concatenated_interview_data = ""
    for i, session_id in enumerate(sessionIDs):
        concatenated_interview_data += f"Interview {i+1}: ```"
        annotations = InterviewAnnotation.objects(sessionID=session_id)
        for annotation in annotations:
            concatenated_interview_data += f"- user annotation: {annotation.annotation}; generated feedback: {annotation.feedback}\n"
        concatenated_interview_data += "```\n"

    
    prompt = f"""Your task is to answer a question based on a these past interviews data. Each interview data is numbered and separated by ```. Each interview data consisted of series of user annotations and generated feedbacks.  
                Question: ```{question}```
                Interview Data: ```{concatenated_interview_data}```"""

    print(prompt)

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