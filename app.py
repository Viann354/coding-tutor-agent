from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from agent import CodingTutorAgent
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

agent = CodingTutorAgent()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Pesan kosong"}), 400
    result = agent.auto_detect_and_respond(message)
    return jsonify(result)

@app.route("/api/debug", methods=["POST"])
def debug():
    data = request.json
    code = data.get("code", "")
    error = data.get("error", "")
    language = data.get("language", "python")
    response = agent.debug_code(code, error, language)
    return jsonify({"mode": "debug", "response": response})

@app.route("/api/quiz", methods=["POST"])
def quiz():
    data = request.json
    topic = data.get("topic", "python dasar")
    level = data.get("level", "pemula")
    language = data.get("language", "python")
    response = agent.generate_quiz(topic, level, language)
    return jsonify({"mode": "quiz", "response": response})

@app.route("/api/check-answer", methods=["POST"])
def check_answer():
    data = request.json
    question = data.get("question", "")
    answer = data.get("answer", "")
    response = agent.check_answer(question, answer)
    return jsonify({"mode": "check", "response": response})

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.json
    topic = data.get("topic", "python")
    level = data.get("level", "pemula")
    language = data.get("language", "python")
    response = agent.recommend_resources(topic, level, language)
    return jsonify({"mode": "recommend", "response": response})

@app.route("/api/history", methods=["GET"])
def history():
    return jsonify({"history": agent.get_history()})

@app.route("/api/history/clear", methods=["POST"])
def clear_history():
    agent.clear_history()
    return jsonify({"status": "ok", "message": "Riwayat chat dihapus"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)