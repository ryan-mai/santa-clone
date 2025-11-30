from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, send_file, render_template, Response
import io

from email.message import EmailMessage
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

elevenlabs = ElevenLabs(
    api_key=API_KEY
)

app = Flask(__name__)

def post_tts(txt: str):
    try:
        audio_gen = elevenlabs.text_to_speech.convert(
            text=txt,
            voice_id=VOICE_ID,
            model_id="eleven_turbo_v2",
            output_format="mp3_44100_128",
        )

        audio_bytes = b"".join(chunk for chunk in audio_gen)
        return audio_bytes
    
    except Exception as e:
        print(f"Error: {e}")

def send_email(recipient_email, subject, body, bytes, filename="santas_memo.mp3"):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return
    try:
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.set_content(body)
        
        msg.add_attachment(
            bytes,
            maintype="audio",
            subtype="mpeg",
            filename=filename
        )

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

            print("Email sent to: ", recipient_email)
            return True
    except Exception as e:
        print(f"Error sending mail: {e}")
        return False

@app.route('/')
def home():
    print('Opening tts.html')
    return render_template("tts.html")

@app.route('/generate', methods=['POST'])
def generate_audio():
    child = request.form.get('name', 'Your Child')
    subject = request.form.get('context', '')
    text = request.form.get('text', '')
    parent_email = request.form.get('parent_email', '').strip()

    if not subject or not text or not parent_email:
        return ("Incomplete form!", 400)

    audio = post_tts(text)
    if not audio:
        return ("Santa is unable to speak to your child :( at this time", 500)
    audio_bytes = io.BytesIO(audio) #type: ignore
    audio_bytes.seek(0)

    email_subject = f"Santa's message for {child}"
    email_body = f'Ho ho ho! I hope you are doing well, {child}. I have recieved your note: "{subject}." Because I am so busy preparing my toys, I can\'t speak with you directly. So {child}, I have sent you a voice recording. Please listen and I hope you have a wonderful christmas!'

    sent = send_email(parent_email, email_subject, email_body, audio, filename="santas_memo.mp3")
    if sent:
        return ("Email sent", 200)
    else:
        return ("Failed", 500)

if __name__ == '__main__':
    app.run(debug=True)