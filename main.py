import os
import argparse

from adapter import OpenAIAdapter, HTTPOpenAI, BuiltinOpenAI, NaiveOpenAI



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='openai')
    parser.add_argument('--config', type=str, default=None, help='Config file')
    parser.add_argument('--action', type=str, default='Ask', help='action (one of: Ask, Chat, Edit)')
    parser.add_argument('--source', type=str, default='builtin', help='action (one of: builtin, http, naive)')
    parser.add_argument('--chat-model', type=str, default='gpt-3.5-turbo', help='model for chat api')
    parser.add_argument('--edit-model', type=str, default='text-davinci-edit-001', help='model for edit api')
    parser.add_argument('--completion-model', type=str, default='text-davinci-003', help='model for completion api')

    FLAGS = parser.parse_args()

    oa: OpenAIAdapter
    api_key = os.getenv('OPENAI_API_KEY')
    models = {
        'chat': FLAGS.chat_model,
        'edit': FLAGS.edit_model,
        'completion': FLAGS.completion_model
    }

    match FLAGS.source:
        case 'builtin':
            oa = BuiltinOpenAI(api_key=api_key, models=models)
        case 'http':
            oa = HTTPOpenAI(api_key=api_key, models=models)
        case default:
            oa = NaiveOpenAI(api_key)


    prompt = 'Say this is a test'
    ans = oa.Completion(prompt)
    print(f'Promt: {prompt}')
    print(f'Answer: {ans}')
    print('------------------------------')
    instruction = "Correct this math operation"
    input = "1 plus 1 is 2, minus 1 is 3"
    ans = oa.Edit(input=input, instruction=instruction)
    print(f'{instruction}: {input}')
    print(f'Answer: {ans}')

    print('------------------------------')
    question = 'What is neural rendering?'
    print(f'Ask: {question}')
    ans = oa.Chat(question)
    print(f'Answer: {ans}')

    print('------------------------------')
