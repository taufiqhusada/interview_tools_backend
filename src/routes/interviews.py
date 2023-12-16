
from flask import Blueprint, request, jsonify
from database.models import Interview, InterviewTranscript
from util.response import  convert_to_json_resp

interviews_bp = Blueprint('interviews', __name__)

@interviews_bp.route('/interviews', methods=['GET'])
def get_interviews():
    interviews = Interview.objects.all()
    return convert_to_json_resp({'interviews': interviews})

@interviews_bp.route('/interviews/<id>', methods=['GET'])
def get_interview(id):
    interview = Interview.objects.get_or_404(id=id)
    return convert_to_json_resp({'interview': interview})

@interviews_bp.route('/interviews', methods=['POST'])
def create_interview():
    data = request.json
    interview = Interview(**data)
    interview.save()
    return convert_to_json_resp({'message': 'Interview created', 'id': str(interview.id), 'sessionID': interview.sessionID})
    
@interviews_bp.route('/interviews/<id>', methods=['PUT'])
def update_interview(id):
    data = request.json
    interview = Interview.objects.get_or_404(id=id)
    interview.update(**data)
    return convert_to_json_resp({'message': 'Interview updated'})

@interviews_bp.route('/interviews/<id>', methods=['DELETE'])
def delete_interview(id):
    interview = Interview.objects.get_or_404(id=id)
    interview.delete()
    return convert_to_json_resp({'message': 'Interview deleted'})

@interviews_bp.route('/interviews/transcript', methods=['POST'])
def create_interview_transcript():
    data = request.json
    interview = InterviewTranscript(**data)
    interview.save()
    return convert_to_json_resp({'message': 'Interview trasncript created', 'id': str(interview.id), 'sessionID': interview.sessionID})