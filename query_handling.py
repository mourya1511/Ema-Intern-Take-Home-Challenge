from openai import OpenAI

class QueryHandler:
    def __init__(self, api_key):
        self.openai = OpenAI(api_key)

    def generate_response(self, query):
        response = self.openai.Completions.create(
            model="text-davinci-003",
            prompt=query,
            max_tokens=50
        )
        return response.choices[0].text.strip()
