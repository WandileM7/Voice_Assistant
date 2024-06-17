import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import google.generativeai as genai


class GenAIException(Exception):
    """GEN AI EXCEPTION CLASS"""


class Chatbot:
    CHATBOT_NAME = "Wednesday"

    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []
        self.preload_conversation()

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])

    def _generative_config(self, temperature):
        return GenerationConfig(temperature=temperature)

    def send_prompt(self, prompt, temperature=0.5):
        if not 0 <= temperature <= 1:
            raise GenAIException('Temperature must be between 0 and 1')

        if not prompt:
            raise GenAIException('Prompt cannot be empty')

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self._generative_config(temperature)
            )
            response.resolve()
            return f'{response.text}\n' + '---' * 20
        except Exception as e:
            raise GenAIException(str(e))

    @property
    def history(self):
        conversational_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversational_history

    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)

    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': [text]
        }

    def preload_conversation(self, conversation_history=None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._construct_message(
                    'From now on, return the output as a JSON object that can be loaded in Python with the key as \'text\'. For example, {"text": "<output goes here>"}'),
                self._construct_message(
                    '{"text": "Sure, I can return the output as a regular JSON object with the key as `text`. Here is an example: {"text": "Your Output"}.',
                    'model')
            ]
