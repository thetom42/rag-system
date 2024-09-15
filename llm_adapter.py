from config import LLM_PROVIDER, OPENAI_API_KEY
from openai_chat_completion import send_openai_request

class LLMAdapter:
    def __init__(self):
        self.provider = LLM_PROVIDER

    def generate_response(self, prompt):
        if self.provider == 'openai':
            return self._generate_openai_response(prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _generate_openai_response(self, prompt):
        return send_openai_request(prompt)
