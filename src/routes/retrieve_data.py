from flask import Blueprint, request, jsonify
from database.models import Interview, InterviewTranscript, InterviewAnnotation
from util.response import  convert_to_json_resp
from util.jwt import verify_and_extract_payload

retrieve_data_bp = Blueprint('retrieve_data_bp', __name__)

@retrieve_data_bp.route('/retrieve', methods=['GET'])
def get_all_data():
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Authorization header is missing'}), 401
    
    # Extract the token from the Authorization header
    token_parts = auth_header.split()
    if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
        return jsonify({'error': 'Invalid authorization header format'}), 401
    
    token = token_parts[1]
    
    # Verify the token and extract the payload
    payload = verify_and_extract_payload(token)
    if not payload:
        return jsonify({'error': 'Not authorized'}), 401
    
    sessionID = payload.get('sessionID')
    if not sessionID:
        return jsonify({'error': 'SessionID not found in payload'}), 401
    
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
            'transcript': transcript.transcript,
            'identifiedMoments': transcript.identifiedMoments,
        }), 200
    else:
        return jsonify({'error': 'Data not found'}), 404