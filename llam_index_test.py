import os

os.environ['OPENAI_API_KEY'] = "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"


import openai
import json
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex


class Chatbot:
    def __init__(self, api_key, index):
        self.index = index
        openai.api_key = api_key
        self.chat_history = []
        self.query_engine = index.as_query_engine()

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        response = self.query_engine.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message
    
    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)


data = SimpleDirectoryReader('./data').load_data()
index = GPTVectorStoreIndex(data)

bot = Chatbot("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", index=index)
bot.load_chat_history("chat_history.json")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "goodbye"]:
        print("Bot: Goodbye!")
        bot.save_chat_history("chat_history.json")
        break
    response = bot.generate_response(user_input)
    print(f"Bot: {response['content']}")