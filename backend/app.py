from flask import Flask, request, jsonify
import subprocess
from prompts import CLINICAL_PROMPT, PATIENT_PROMPT

app = Flask(__name__)

MODEL_NAME = "llama3.1:8b"  # your installed Ollama model

def call_ollama(prompt):
    """Run Ollama model via CLI and return output text."""
    try:
        # Pass the prompt directly as an argument
        cmd = ["ollama", "run", MODEL_NAME, prompt]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr)
        return result.stdout.strip()
    except Exception as e:
        raise Exception(f"Ollama CLI call failed: {e}")

@app.route("/api/clinical-summary", methods=["POST"])
def clinical_summary():
    data = request.get_json() or {}
    notes = data.get("notes", "").strip()
    if not notes:
        return jsonify({"error": "notes is required"}), 400

    prompt = CLINICAL_PROMPT.format(notes=notes)
    try:
        summary = call_ollama(prompt)
        return jsonify({"summary": summary})
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
        summary = call_ollama(prompt)
        return jsonify({"patient_summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
