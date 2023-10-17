from database.models import InterviewAnnotation
from flask import request, Blueprint
from util.response import  convert_to_json_resp

annotations_bp = Blueprint('annotations', __name__)

# Routes for CRUD operations on InterviewAnnotation
@annotations_bp.route('/interviews/<sessionID>/annotations', methods=['GET'])
def get_annotations(sessionID):
    annotations = InterviewAnnotation.objects(sessionID=sessionID)
    return convert_to_json_resp({'annotations': [annotation.to_json() for annotation in annotations]})

@annotations_bp.route('/interviews/<sessionID>/annotations', methods=['POST'])
def create_annotation(sessionID):
    data = request.json
    data['sessionID'] = sessionID
    annotation = InterviewAnnotation(**data)
    annotation.save()
    return convert_to_json_resp({'message': 'Annotation created', 'id': str(annotation.id)})

@annotations_bp.route('/interviews/<sessionID>/annotations/<annotation_id>', methods=['GET'])
def get_annotation(sessionID, annotation_id):
    annotation = InterviewAnnotation.objects.get_or_404(id=annotation_id, sessionID=sessionID)
    return convert_to_json_resp({'annotation': annotation})

@annotations_bp.route('/interviews/<sessionID>/annotations/<annotation_id>', methods=['PUT'])
def update_annotation(sessionID, annotation_id):
    annotation = InterviewAnnotation.objects.get_or_404(id=annotation_id, sessionID=sessionID)
    data = request.json
    annotation.update(**data)
    return convert_to_json_resp({'message': 'Annotation updated'})

@annotations_bp.route('/interviews/<sessionID>/annotations/<annotation_id>', methods=['DELETE'])
def delete_annotation(sessionID, annotation_id):
    annotation = InterviewAnnotation.objects.get_or_404(id=annotation_id, sessionID=sessionID)
    annotation.delete()
    return convert_to_json_resp({'message': 'Annotation deleted'})