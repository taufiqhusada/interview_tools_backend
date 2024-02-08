from flask import Blueprint, request, jsonify
from database.models import Interview, InterviewTranscript, InterviewAnnotation
from util.response import  convert_to_json_resp

retrieve_data_bp = Blueprint('retrieve_data_bp', __name__)

@retrieve_data_bp.route('/retrieve/<sessionID>', methods=['GET'])
def get_all_data(sessionID):
    print(sessionID)
    interview = Interview.objects(sessionID=sessionID).first()
    annotation = InterviewAnnotation.objects(sessionID=sessionID)
    transcript = InterviewTranscript.objects(sessionID=sessionID).first()
    
    if not annotation:
        annotation = []

    print(annotation)

    if interview and transcript:
        return jsonify({
            'interview': interview,
            'annotation': annotation,
            'transcript': transcript.transcript
        }), 200
    else:
        return jsonify({'error': 'Data not found'}), 404
    