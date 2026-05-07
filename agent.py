from google import genai
import os
import json
import datetime

class CodingTutorAgent:
    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyCiUZmLxgpmWObohNM6Iy3WgTAZAujH8zQ")
        self.model = "gemini-2.0-flash-lite"
        self.system_prompt = "Kamu adalah CodeSensei, tutor coding AI untuk mahasiswa Indonesia. Selalu friendly dan motivatif. Format kode dalam blok ```bahasa```"
        self.history_file = "data/chat_history.json"
        self.history = self._load_history()
        self.conversation = []

    def _load_history(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_history(self, role, message):
        entry = {"role": role, "message": message, "timestamp": datetime.datetime.now().isoformat()}
        self.history.append(entry)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
        self.conversation = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

    def chat(self, message):
        self._save_history("user", message)
        self.conversation.append({"role": "user", "parts": [{"text": message}]})
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=self.conversation,
                config={"system_instruction": self.system_prompt}
            )
            reply = response.text
        except Exception as e:
            reply = f"Error: {str(e)}"
        self.conversation.append({"role": "model", "parts": [{"text": reply}]})
        self._save_history("assistant", reply)
        return reply

    def debug_code(self, code, error="", language="python"):
        prompt = f"Tolong debug kode {language} ini:\n{code}\n{'Error: ' + error if error else ''}\nJelaskan masalah dan berikan solusinya."
        return self.chat(prompt)

    def generate_quiz(self, topic, level="pemula", language="python"):
        prompt = f"Buat 3 soal latihan tentang {topic} menggunakan {language} level {level}. Sertakan hint dan expected output tiap soal."
        return self.chat(prompt)

    def check_answer(self, question, user_answer):
        prompt = f"Soal: {question}\nJawaban user: {user_answer}\nKoreksi jawaban ini dan beri nilai 0-100."
        return self.chat(prompt)

    def recommend_resources(self, topic, level="pemula", language="python"):
        prompt = f"Rekomendasikan materi belajar untuk {topic} menggunakan {language} level {level}. Sertakan roadmap dan resource gratis."
        return self.chat(prompt)

    def auto_detect_and_respond(self, message):
        lower = message.lower()
        if any(k in lower for k in ["error", "bug", "tidak jalan", "not working", "fix", "debug"]):
            mode = "debug"
        elif any(k in lower for k in ["soal", "latihan", "quiz", "exercise", "practice"]):
            mode = "quiz"
        elif any(k in lower for k in ["belajar", "learn", "resource", "materi", "rekomendasi", "recommend"]):
            mode = "recommend"
        else:
            mode = "chat"
        return {"mode": mode, "response": self.chat(message)}
