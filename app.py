from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, send_file, render_template, Response
import io
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

load_dotenv()

API_KEY = os.getenv('elevenLabsApiKey')
VOICE_ID = "uDsPstFWFBUXjIBimV7s"
INPUT_FILE = "./audio/Recording.m4a"
OUTPUT_FILE = "output.mp3"

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
GMAIL_SENDER = os.getenv("GMAIL_SENDER")

elevenlabs = ElevenLabs(
    api_key=API_KEY
)

app = Flask(__name__, static_folder='static', static_url_path='/static')

def get_gmail_service():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES
    )
    return build("gmail", "v1", credentials=creds)

def add_attachment(sender, to, subject, html, attachment, filename):
    msg = MIMEText(html, "html")
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject
    
    mixed = MIMEMultipart("mixed")
    mixed["To"] = msg["To"]
    mixed["From"] = msg["From"]
    mixed["Subject"] = msg["Subject"]

    mixed.attach(msg)

    audio = MIMEBase("audio", "mpeg")
    audio.set_payload(attachment)
    encoders.encode_base64(audio)
    audio.add_header("Content-Disposition", f'attachment; filename="{filename}"')

    mixed.attach(audio)

    raw = base64.urlsafe_b64encode(mixed.as_bytes()).decode()
    return {"raw": raw}

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
    try:
        service = get_gmail_service()
        msg = add_attachment(GMAIL_SENDER, recipient_email, subject, body, bytes, filename)
        sent = service.users().messages().send(userId="me", body=msg).execute()
        print("Santa sent it!", sent.get("id"))
        return True

    except Exception as e:
        print(f"Error sending mail: {e}")
        return False

@app.route('/')
def home():
    print('Opening index.html')
    return render_template("index.html")

@app.route('/tts')
def tts_page():
    return render_template('tts.html')

@app.route('/countdown')
def countdown_page():
    return render_template('countdown.html')


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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)