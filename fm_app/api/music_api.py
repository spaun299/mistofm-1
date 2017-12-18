from ..blueprints import api_music_bp
from ..models import Music
from flask import Response, current_app
import logging


@api_music_bp.route('/stream/<string:song_name>')
def stream(song_name):
    def generate():
        try:
            with open(Music.get_song_path(song_name), "rb") as mp3:
                data = mp3.read(1024)
                while data:
                    yield data
                    data = mp3.read(1024)
        except FileNotFoundError:
            logging.error('Requested song not found: %s' % song_name)

    return Response(generate(), mimetype="audio/mpeg")
