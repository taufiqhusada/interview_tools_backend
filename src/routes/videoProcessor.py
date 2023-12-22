from flask import request, Blueprint, Response
from util.response import  convert_to_json_resp
import subprocess
import tempfile
import os
import json

import firebase_admin
from firebase_admin import credentials, storage
import datetime
import uuid


video_processor_bp = Blueprint('video_processor', __name__)

@video_processor_bp.route('/video/merge', methods=['POST'])
def merge_audio_video():
    try:
        # Get the uploaded video file from the request
        video_file = request.files['video']

        # Check if the video file is present
        if not video_file:
            return convert_to_json_resp({"error": "Video file is required."}), 400

        # Save the uploaded video file to the server
        video_filename = 'video.mp4'
        video_file.save(video_filename)

        # Define the output video filename
        output_filename = 'output.mp4'

        # Create a temporary directory to store the audio files
        temp_dir = tempfile.mkdtemp()

        # Get the start times from the JSON data
        start_times = json.loads(request.form.get('start_times'))

        # Merge audio with the video based on start times
        filter_complex_str = ''
        audio_inputs = ''
        for i, audio_file in enumerate(request.files.getlist('audio')):
            audio_filename = os.path.join(temp_dir, f'audio_{i}.m4a')
            audio_file.save(audio_filename)

            print(audio_filename)

            start_time = start_times[i]
            
            # Delay the audio based on start time
            filter_complex_str += f'[{i+1}:a]adelay={int(start_time*1000)}|{int(start_time*1000)}[a{i+1}];'

            audio_inputs += f'-i {audio_filename} '

        filter_complex_str += '[0:a]' + ''.join([f'[a{i+1}]' for i in range(len(request.files.getlist('audio')))])
        filter_complex = f'{filter_complex_str}amix=inputs={len(request.files.getlist("audio")) + 1}:duration=first[aout]'

        # Compress the video using H.264 codec and set a specific bitrate
        cmd_compress = [
            'ffmpeg',
            '-i', video_filename,
            '-c:v', 'libx264',          # Video codec
            '-b:v', '512K',             # Target video bitrate (adjust as needed)
            '-preset', 'ultrafast',     # Faster compression
            '-strict', 'experimental',  # Needed for AAC audio codec
            '-y',
            'compressed_video.mp4'     # Output compressed video
        ]

        subprocess.run(cmd_compress, check=True)

        cmd = [
            'ffmpeg',
            '-i', 'compressed_video.mp4',
            *audio_inputs.split(),
            '-filter_complex', filter_complex,
            '-map', '0:v:0',
            '-map', '[aout]',
            '-c:v', 'libx264',  # Re-encode the video using H.264 codec
            '-preset', 'medium',  
            '-y',
            output_filename
        ]

        print(cmd)
        subprocess.run(cmd, check=True)

        # Clean up temporary files and directory
        for i in range(len(request.files.getlist('audio'))):
            os.remove(os.path.join(temp_dir, f'audio_{i}.m4a'))
        os.rmdir(temp_dir)

        video_url = upload_to_firebase('output.mp4')
        print(video_url)

        os.remove('compressed_video.mp4')
        os.remove('output.mp4')
        os.remove('video.mp4')

        return convert_to_json_resp({'url': video_url})


    except Exception as e:
        print(e)
        return convert_to_json_resp({"error": str(e)}), 500
    

def upload_to_firebase(filename):
    # Initialize Firebase Admin SDK with your service account key
    bucket = storage.bucket()

    # Upload the merged video to Firebase Storage
    blob = bucket.blob(f'videos/interview/{str(uuid.uuid4())}')
    blob.upload_from_filename(filename)

    # Generate a signed URL for the uploaded video
    video_url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=60),  # Adjust the expiration as needed
        method="GET"
    )

    return video_url