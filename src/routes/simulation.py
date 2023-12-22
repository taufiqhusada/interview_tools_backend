from flask import Flask, request, jsonify, Blueprint, Response
from config.openai_connector import init_openai_config
import base64
import os
from pathlib import Path

simulation_bp = Blueprint('simulation', __name__)

@simulation_bp.route('/simulation/transcript', methods=['POST'])
def get_transcript_from_whisper():
    try:
        # Get the audio blob from the request
        audio_blob = request.files['file']

        # Create a dictionary with the form data
        data = {
            'model': 'whisper-1',
            'language': 'en',
            'response_format': 'srt',
        }

        openai = init_openai_config()

        # Make an HTTP POST request to the Whisper API using the OpenAI SDK
        response = openai.audio.transcriptions.create(
            **data,
            file=(audio_blob.filename, audio_blob.read(), 'audio/webm' )
        )

        return jsonify({'data': extract_subtitles(response)})

    except Exception as e:
        return jsonify({'error': str(e)})

def extract_subtitles(str_subtitle):
    subtitle_blocks = str_subtitle.strip().split('\n\n')
    subtitles = []

    for block in subtitle_blocks:
        lines = block.strip().split('\n')

        subtitle_number = lines[0]

        timing = lines[1]

        text = '\n'.join(lines[2:])

        start_time, end_time = timing.split(' --> ')

        subtitle = {
            'number': subtitle_number,
            'startTime': srt_time_to_seconds(start_time),
            'endTime': srt_time_to_seconds(end_time),
            'text': text,
        }

        subtitles.append(subtitle)

    return subtitles

def srt_time_to_seconds(srt_time):
    parts = srt_time.replace(',', '.').split(':')

    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    milliseconds = float(parts[3]) if len(parts) > 3 else 0

    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000

    return total_seconds

@simulation_bp.route('/simulation/response', methods=['POST'])
def generate_gpt_response():
    try:
        # Get the transcript and instruction from the request
        transcript = request.json['transcript']
        instruction = request.json['instruction']

        messages = [{'role': item['speaker'].lower(), 'content': item['text']} for item in transcript]
        messages.append({'role': 'system', 'content': instruction})

        # Define the request payload
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': messages,
        }

        openai = init_openai_config()
        
        # Send the request to the OpenAI API using the OpenAI SDK
        response = openai.chat.completions.create(**data)

        if response.choices:
            gpt_response = response.choices[0].message.content
            tts_audio = generate_tts(gpt_response)
            audio_base64 = base64.b64encode(tts_audio).decode('utf-8')

            return jsonify({'audio_data': audio_base64,'text_response': gpt_response})
        else:
            return jsonify({'error': 'Failed to generate GPT response'})

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})

# Function to generate TTS audio from text
def generate_tts(text):
    try:
        openai = init_openai_config()

        # Send a request to the OpenAI TTS API to generate audio from text
        tts_response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
            response_format="opus"
        )
    
        return tts_response.content

    except Exception as error:
        print('Error generating TTS audio:', error)
        return None
