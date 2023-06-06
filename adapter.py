import openai
import requests
from abc import ABC, abstractmethod

class OpenAIAdapter(ABC):
    chatModels = {'gpt-4', 'gpt-4-0314', 'gpt-4-32k', 'gpt-4-32k-0314', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0301'}
    completionModels = {'text-davinci-003', 'text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001'}
    editModels = {'text-davinci-edit-001', 'code-davinci-edit-001'}
    
    @abstractmethod
    def ListModel(self):
        print(openai.Model.list())

    @abstractmethod
    def Chat(self, message: str):
        pass
    # @abstractmethod
    # def Ask(self, message: str, temperature: float, top_p: float, n: int, stream: bool, stop: str, max_tokens: int, presence_penalty: float, frequency_penalty: float, bias: dict):
    #     pass
    @abstractmethod
    def Completion(self, promt: str):
        pass

    @abstractmethod
    def Edit(self, input: str):
        pass

    
class HTTPOpenAI(OpenAIAdapter):
    api_key: str
    models: dict

    def __init__(self, api_key, models):
        self.api_key = api_key
        self.models = models
        super().__init__()
    
    def ListModel(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        r = requests.get('https://api.openai.com/v1/models', headers=headers)
        return super().ListModel()
    
    def Completion(self, prompt: str):
        model = self.models['completion']
        if not model in self.completionModels:
            return f'model {model} does not support Completion'
        
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        body = {
            'model': model,
            'prompt': prompt,
        }

        res = requests.post('https://api.openai.com/v1/completions', headers=headers, json=body)
        if res.status_code != 200:
            return f'call completion got error: {res.content}'
    
        choices = res.json()["choices"]
        return choices[0]["text"]
    
    def Edit(self, input: str, instruction):
        model = self.models['edit']
        if not model in self.editModels:
            return f'model {model} does not support Edit'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        body = {
            'model': model,
            'input': input,
            'instruction': instruction,
        }

        res = requests.post('https://api.openai.com/v1/edits', headers=headers, json=body)
        if res.status_code != 200:
            return f'call edit got error: {res.content}'
        
        ans = res.json()["choices"]
        if len(ans) == 0:
            return "I have no idea for your question"

        return ans[0]['text']
    
    def Chat(self, message: str):
        model = self.models['chat']
        if not model in self.chatModels:
            return f'model {model} does not support Ask'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        body = {
            'model': model,
            'messages': [{'role': "user", 'content': message}],
        }

        res = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=body)

        if res.status_code != 200:
            return f'call chat got error: {res.content}'
        
        choices = res.json()["choices"]
        if len(choices) == 0:
            return "I have no idea for your question"

        return choices[0]['message']['content']

class BuiltinOpenAI(OpenAIAdapter):
    models: dict

    def __init__(self, api_key, models: dict):
        self.api_key = api_key
        self.models = models
        super().__init__()
    
    def ListModel(self):
        return super().ListModel()
    
    def Completion(self, prompt: str):
        model = self.models['completion']
        if not model in self.completionModels:
            return f'model {model} does not support Completion'
        res = openai.Completion.create(
            model=model,
            prompt = prompt,
            temperature=0,
        )
        return res['choices'][0]['text']
    
    def Edit(self, input: str, instruction: str):
        model = self.models['edit']
        if not model in self.editModels:
            return f'model {self.model} does not support Edit'
    
        res = openai.Edit.create(
            model=model,
            input=input,
            instruction=instruction
        )
        return res['choices'][0]['text']
    
    def Chat(self, message: str):
        model = self.models['chat']
        if not model in self.chatModels:
            return f'model {model} does not support Chat'
        
        res = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return res['choices'][0]['message']['content']
    
class NaiveOpenAI(OpenAIAdapter):
    def __init__(self, api_key):
        self.api_key = api_key
        super().__init__()
    
    def ListModel(self):
        return 'I dont know any models'
    
    def Completion(self, promt: str):
        return "I don't know anything, please don't tell me to chat"
    
    def Edit(self, input: str):
        return "I don't know anything, please don't tell me to edit"
    
    def Chat(self, message: str):
        return "I don't know anything, please don't ask me"