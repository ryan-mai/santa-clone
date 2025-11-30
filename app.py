from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, send_file, render_template, Response
import io

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

load_dotenv()

API_KEY = os.getenv('elevenLabsApiKey')
VOICE_ID = "uDsPstFWFBUXjIBimV7s"
INPUT_FILE = "./audio/Recording.m4a"
OUTPUT_FILE = "output.mp3"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(recipient_email, subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        print("Email text added")
        file = "output.mp3"
        with open(file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

            encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename"{file}"'
        )

        msg.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())

            print("Email sent to: ", recipient_email)
    except Exception as e:
        print(f"Error sending mail: {e}")
        return

if __name__ == '__main__':
    recipient = "inoober2008@gmail.com"
    subject = "Yo"
    body = "Yay"
    send_email(recipient, subject, body)
# elevenlabs = ElevenLabs(
#     api_key=API_KEY
# )

# app = Flask(__name__)

# def post_tts(txt: str):
#     try:
#         audio_gen = elevenlabs.text_to_speech.convert(
#             text=txt,
#             voice_id=VOICE_ID,
#             model_id="eleven_turbo_v2",
#             output_format="mp3_44100_128",
#         )

#         audio_bytes = b"".join(chunk for chunk in audio_gen)
#         return audio_bytes
    
#     except Exception as e:
#         print(f"Error: {e}")

# @app.route('/')
# def home():
#     print('Opening index.html')
#     return render_template("index.html")

# @app.route('/generate', methods=['POST'])
# def generate_audio():
#     text = request.form.get('text', 'Hello')

#     audio = post_tts(text)

#     audio_bytes = io.BytesIO(audio) #type: ignore
#     audio_bytes.seek(0)

#     return send_file(
#         audio_bytes,
#         as_attachment=True,
#         download_name="output.mp3",
#         mimetype="audio/mpeg"
#     )

# if __name__ == '__main__':
#     app.run(debug=True)

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