import ollama
import os 

class Chatbot():
    def __init__(self, model_name = "llama3.2:1b"):
        """Initializing the chatbot with llama"""
        self.model_name = model_name

    def checkForSQL(self, message):
        message = "Does this look like something you can create a SQL query from? If yes, say yes. If no, say no. Be strict but still considerate.:" + message

        response = ollama.chat(model=self.model_name, messages=[{"role":"user", "content":message}],         options={
            "num_predict": 1,   # Limits max tokens in response (default is too high)
            "temperature": 0.2,   # Lower = more deterministic, slightly faster
            "top_k": 40,          # Restrict next token choices
            "top_p": 0.9          # Reduce probability range
        })
        print(response["message"]["content"])
        return response["message"]["content"]

    def get_response(self, message):
        
        message = message + ". Extract the SQL query from this. No other text at all."
        
        response = ollama.chat(model=self.model_name, messages=[{"role":"user", "content":message}],         options={
            "num_predict": 1000,   # Limits max tokens in response (default is too high)
            "temperature": 0.2,   # Lower = more deterministic, slightly faster
            "top_k": 40,          # Restrict next token choices
            "top_p": 0.9          # Reduce probability range
        })
        print(response["message"]["content"])
        if response["message"]["content"] == "No":
            return "Please enter a valid question statement."
        else:
            return response["message"]["content"]
        # store_chat(query.user_id, query.message, response)



        