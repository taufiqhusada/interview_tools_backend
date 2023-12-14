from flask import request, Blueprint, Response
from util.response import  convert_to_json_resp
import subprocess


video_processor_bp = Blueprint('video_processor', __name__)

@video_processor_bp.route('/video/merge', methods=['POST'])
def merge_audio_video():
    try:
        # Get the uploaded audio and video files from the request
        audio_file = request.files['audio']
        video_file = request.files['video']

        # Check if the files are present
        if not audio_file or not video_file:
            return convert_to_json_resp({"error": "Both audio and video files are required."}), 400

        # Save the uploaded files to the server
        audio_filename = 'audio.mp3'
        video_filename = 'video.mp4'
        audio_file.save(audio_filename)
        video_file.save(video_filename)

        # Define the output video filename
        output_filename = 'output.mp4'

        # Use FFmpeg to merge audio and video
        cmd = [
            'ffmpeg',
            '-i', video_filename,
            '-i', audio_filename,
            '-filter_complex',
            f'[1:a]adelay=5s|5s[a1];[0:a][a1]amix=inputs=2:duration=first[aout]',
            '-map', '0:v:0',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-y',
            output_filename
        ]

        subprocess.run(cmd, check=True)

        
        # Return the merged video file as a response
        with open(output_filename, 'rb') as video_file:
            response = Response(video_file.read(), content_type='video/mp4')

        response.headers['Content-Disposition'] = 'inline; filename=output.mp4'

        return response

    except Exception as e:
        return convert_to_json_resp({"error": str(e)}), 500