from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, send_file, render_template, Response
import io
load_dotenv()

API_KEY = os.getenv('elevenLabsApiKey')
VOICE_ID = "uDsPstFWFBUXjIBimV7s"
INPUT_FILE = "./audio/Recording.m4a"
OUTPUT_FILE = "output.mp3"

elevenlabs = ElevenLabs(
    api_key=API_KEY
)

app = Flask(__name__)

def post_tts(txt: str):
    audio_gen = elevenlabs.text_to_speech.convert(
        text=txt,
        voice_id=VOICE_ID,
        optimize_streaming_latency=4,
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
    )

    for chunk in audio_gen:
        if chunk:
            yield chunk

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_audio():
    text = request.form.get('text', 'Hi')
    if not text:
        return "Enter some text!", 400

    return Response(
        headers={
            "Content-Diposition": "inline; filename=santa_voice.mp3",
            "Cache-Control": "no-cache",
        },
        mimetype="audio/mpeg"
    )

if __name__ == '__main__':
    app.run(debug=True)

# url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

# headers = {
#     "xi-api-key": API_KEY
# }

# data = {
#     "model_id": "eleven_flash_v2_5"
# }

# files = {
#     "audio": open(INPUT_FILE, "rb")
# }

# response = requests.post(url, headers=headers, data=data, files=files, stream=True)

# if response.status_code == 200:
#     with open(OUTPUT_FILE, "wb") as f:
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 f.write(chunk)
# else:
#     print("error", response.status_code, response.text)