"""
Comic Strip Generator - backend.

    pip install -U sarvamai flask
    export SARVAM_API_KEY="your-key"     (Windows: set SARVAM_API_KEY=your-key)
    python server.py     ->  open http://localhost:5000
"""
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from sarvamai import SarvamAI

load_dotenv()

api_key = os.environ.get("SARVAM_API_KEY")
if not api_key:
    raise ValueError("SARVAM_API_KEY environment variable not found. Please set it in .env or as an environment variable.")

client = SarvamAI(api_subscription_key=api_key)
app = Flask(__name__)


@app.get("/")
def home():
    return send_from_directory(os.path.dirname(__file__), "index.html")


@app.post("/api/comic")
def comic():
    d = request.get_json()
    prompt = f"""Write a funny, kid-friendly 4-panel comic strip in {d['language']} about: {d['idea']}

Return ONLY valid JSON, no explanation, in exactly this shape:
{{"title": "...", "panels": [
  {{"bg": "day|night|sunset|indoor|rain|forest",
    "scene": "2-4 emoji showing the setting",
    "who": "1 emoji for the speaking character",
    "caption": "short narration, or empty string",
    "text": "what the character says, max 15 words"}}
]}}
Exactly 4 panels. Write title, caption and text in {d['language']}."""

    r = client.chat.completions(
        model="sarvam-105b-conversations",
        messages=[{"role": "user", "content": prompt}],
    )
    raw = r.choices[0].message.content or ""
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.S)  # drop any visible reasoning
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.M)
    match = re.search(r"\{.*\}", raw, re.S)
    try:
        return jsonify(json.loads(match.group(0)))
    except Exception:
        print("Could not parse model output:\n", raw)
        return jsonify({"error": "The AI's answer wasn't valid JSON. Try again."}), 500


@app.post("/api/speak")
def speak():
    d = request.get_json()
    tts = client.text_to_speech.convert(
        text=d["text"][:500],
        language_code=d["lang"],
        model="bulbul:v3",
        speaker="simran",
    )
    return jsonify({"audio": tts.audios[0]})  # base64 audio


@app.post("/api/stt")
def stt():
    """Speech -> text, so the plot idea can be spoken in any Indian language."""
    f = request.files["audio"]
    r = client.speech_to_text.transcribe(
        file=(f.filename or "idea.webm", f.read(), f.mimetype),
        model="saaras:v3",
    )
    return jsonify({"text": r.transcript})


def translate_one(text, source, target):
    if not text.strip():
        return ""
    try:
        r = client.text.translate(
            input=text,
            source_language_code=source,
            target_language_code=target,
            model="sarvam-translate:v1",
        )
        return r.translated_text
    except Exception as e:
        print("translate failed:", e)
        return text  # fall back to the original text


@app.post("/api/translate")
def translate():
    """Translate the whole comic (title, captions, dialogue) into another language."""
    d = request.get_json()
    with ThreadPoolExecutor(max_workers=8) as pool:
        out = list(pool.map(lambda t: translate_one(t, d["source"], d["target"]), d["texts"]))
    return jsonify({"texts": out})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
