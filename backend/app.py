from flask import Flask, request, jsonify
import os
import requests
from prompts import CLINICAL_PROMPT, PATIENT_PROMPT

app = Flask(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:8b")

def call_ollama(prompt, timeout=120):
    payload = {"model": MODEL_NAME, "prompt": prompt, "temperature": 0.0}
    resp = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

@app.route("/api/clinical-summary", methods=["POST"])
def clinical_summary():
    data = request.get_json() or {}
    notes = data.get("notes", "").strip()
    if not notes:
        return jsonify({"error": "notes is required"}), 400

    prompt = CLINICAL_PROMPT.format(notes=notes)
    try:
        model_out = call_ollama(prompt)
        # Attempt to extract text safely from different Ollama responses
        text = model_out.get("text") if isinstance(model_out, dict) else str(model_out)
        if not text:
            text = model_out.get("output", "")
        return jsonify({"summary": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/patient-summary", methods=["POST"])
def patient_summary():
    data = request.get_json() or {}
    notes = data.get("notes", "").strip()
    if not notes:
        return jsonify({"error": "notes is required"}), 400

    prompt = PATIENT_PROMPT.format(notes=notes)
    try:
        model_out = call_ollama(prompt)
        text = model_out.get("text") if isinstance(model_out, dict) else str(model_out)
        if not text:
            text = model_out.get("output", "")
        return jsonify({"patient_summary": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
