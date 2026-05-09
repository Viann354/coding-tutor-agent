import google.generativeai as genai
import os
import json
import datetime

class CodingTutorAgent:
    def __init__(self):
        # WARNING: Never hardcode API keys in production! Use environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        self.system_prompt = (
            "You are CodeSensei, a friendly and motivational coding tutor for students. "
            "Always be encouraging and helpful. Format all code in ```language``` blocks. "
            "Explain concepts clearly and provide step-by-step solutions."
        )
        self.history_file = "data/chat_history.json"
        self.history = self._load_history()
        self.conversation = []

    def _load_history(self):
        """Load chat history from JSON file"""
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_history(self, role, message):
        """Save message to chat history"""
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
        """Get full chat history"""
        return self.history

    def clear_history(self):
        """Clear chat history and conversation"""
        self.history = []
        self.conversation = []
        if os.path.exists(self.history_file):
            try:
                os.remove(self.history_file)
            except OSError:
                pass
        print("Chat history cleared!")

    def chat(self, message):
        """Send message to AI and get response"""
        self._save_history("user", message)
        self.conversation.append({"role": "user", "parts": [message]})
        
        try:
            response = self.model.generate_content(
                contents=self.conversation,
                generation_config={
                    "system_instruction": self.system_prompt
                }
            )
            reply = response.text
        except Exception as e:
            reply = f"Error: {str(e)}. Please check your API key and internet connection."
        
        self.conversation.append({"role": "model", "parts": [reply]})
        self._save_history("assistant", reply)
        return reply

    def debug_code(self, code, error="", language="python"):
        """Debug code with optional error message"""
        prompt = f"Please debug this {language} code:\n\n```{language}\n{code}\n```\n"
        if error:
            prompt += f"Error: {error}\n\n"
        prompt += "Explain the problem and provide a working solution."
        return self.chat(prompt)

    def generate_quiz(self, topic, level="beginner", language="python"):
        """Generate practice quiz questions"""
        prompt = (
            f"Create 3 practice questions about '{topic}' using {language} "
            f"(level: {level}). Include hints and expected output for each question. "
            "Format nicely with numbered questions."
        )
        return self.chat(prompt)

    def check_answer(self, question, user_answer, language="python"):
        """Check user's answer against question"""
        prompt = f"""Question: {question}

User's answer:
```{language}
{user_answer}