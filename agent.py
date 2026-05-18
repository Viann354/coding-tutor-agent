import os
import json
import datetime
import urllib.request

class CodingTutorAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "openrouter/auto"
        self.system_prompt = (
            "You are CodeSensei, a friendly and motivational coding tutor for students. "
            "Always be encouraging and helpful. Format all code in ```language``` blocks. "
            "Explain concepts clearly and provide step-by-step solutions."
        )
        self.history_file = "data/chat_history.json"
        self.history = self._load_history()
        self.conversation = [{"role": "system", "content": self.system_prompt}]

    def _load_history(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_history(self, role, message):
        entry = {"role": role, "message": message, "timestamp": datetime.datetime.now().isoformat()}
        self.history.append(entry)
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
        self.conversation = [{"role": "system", "content": self.system_prompt}]
        if os.path.exists(self.history_file):
            try:
                os.remove(self.history_file)
            except:
                pass

    def chat(self, message):
        self._save_history("user", message)
        self.conversation.append({"role": "user", "content": message})
        try:
            data = json.dumps({
                "model": self.model,
                "messages": self.conversation
            }).encode("utf-8")
            req = urllib.request.Request(
                self.api_url,
                data=data,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://coding-tutor-agent-production.up.railway.app",
                    "X-Title": "CodeSensei"
                }
            )
            with urllib.request.urlopen(req) as res:
                result = json.loads(res.read().decode("utf-8"))
                reply = result["choices"][0]["message"]["content"]
        except Exception as e:
            reply = f"Error: {str(e)}"
        self.conversation.append({"role": "assistant", "content": reply})
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
        prompt = f"Question: {question}\n\nUser answer:\n```{language}\n{user_answer}\n```\nCheck if correct and give a score 0-100."
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
