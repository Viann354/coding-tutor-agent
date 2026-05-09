from google import genai
from google.genai import types
import os
import json
import datetime

class CodingTutorAgent:
    def __init__(self):
        api_key = "AIzaSyByZCBpLFxuapuqlMEC-5J7kOr3JeXlJTE"
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash-lite"
        self.system_prompt = (
            "You are CodeSensei, a friendly and motivational coding tutor for students. "
            "Always be encouraging and helpful. Format all code in ```language``` blocks. "
            "Explain concepts clearly and provide step-by-step solutions."
        )
        self.history_file = "data/chat_history.json"
        self.history = self._load_history()
        self.conversation = []

    def _load_history(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_history(self, role, message):
        entry = {
            "role": role,
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.history.append(entry)
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Warning: Could not save history: {e}")

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
        self.conversation = []
        if os.path.exists(self.history_file):
            try:
                os.remove(self.history_file)
            except OSError:
                pass

    def chat(self, message):
        self._save_history("user", message)
        self.conversation.append({"role": "user", "parts": [{"text": message}]})
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.conversation,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                )
            )
            reply = response.text
        except Exception as e:
            reply = f"Error: {str(e)}"
        self.conversation.append({"role": "model", "parts": [{"text": reply}]})
        self._save_history("assistant", reply)
        return reply

    def debug_code(self, code, error="", language="python"):
        prompt = f"Please debug this {language} code:\n\n```{language}\n{code}\n```\n"
        if error:
            prompt += f"Error: {error}\n\n"
        prompt += "Explain the problem and provide a working solution."
        return self.chat(prompt)

    def generate_quiz(self, topic, level="beginner", language="python"):
        prompt = (
            f"Create 3 practice questions about '{topic}' using {language} "
            f"(level: {level}). Include hints and expected output for each question."
        )
        return self.chat(prompt)

    def check_answer(self, question, user_answer, language="python"):
        prompt = f"Question: {question}\n\nUser's answer:\n```{language}\n{user_answer}\n```\nCheck if correct and give a score 0-100."
        return self.chat(prompt)

    def recommend_resources(self, topic, level="beginner", language="python"):
        prompt = (
            f"Recommend learning resources for '{topic}' using {language} "
            f"(level: {level}). Include roadmap and free online resources."
        )
        return self.chat(prompt)

    def auto_detect_and_respond(self, message):
        lower = message.lower()
        if any(k in lower for k in ["error", "bug", "not working", "fix", "debug"]):
            mode = "debug"
        elif any(k in lower for k in ["quiz", "exercise", "practice", "problem"]):
            mode = "quiz"
        elif any(k in lower for k in ["learn", "resource", "roadmap", "recommend"]):
            mode = "recommend"
        else:
            mode = "chat"
        return {"mode": mode, "response": self.chat(message)}