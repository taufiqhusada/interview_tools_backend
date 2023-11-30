from .db import db
import datetime

class Interview(db.Document):
    sessionID = db.StringField(required=True, unique=True)
    username_interviewer = db.StringField()
    username_interviewee = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.utcnow)
    transcript_link = db.StringField()
    video_link = db.StringField()

class ChatMessageEmbedded(db.EmbeddedDocument):
    content = db.StringField()
    role = db.StringField()
    isTyping = db.BooleanField()
    meta = {'strict': False}

class InterviewAnnotation(db.Document):
    sessionID = db.StringField(required=True)
    secondStart = db.FloatField()
    secondEnd = db.FloatField()
    transcript = db.StringField()
    annotation = db.StringField()
    feedback = db.StringField()
    question = db.StringField()
    chatMessages = db.ListField(db.EmbeddedDocumentField(ChatMessageEmbedded))