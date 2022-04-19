from uuid import uuid4

from flask import current_app
from requests import post

from app.azure_ai.result_base import ResultBase
from config import AiTranslateConfig


class TranslateResult(ResultBase):

    def __init__(self, original_texts, translated_texts,
                 translated_language):
        self.original_texts = original_texts
        self.translated_texts = translated_texts
        self.translated_language = translated_language


def translate_to(text_inputs, to='zh-Hant'):
    params = {
        'api-version': '3.0',
        'to': [to],
        'includeSentenceLength': True
    }

    headers = {
        'Ocp-Apim-Subscription-Key': AiTranslateConfig.KEY,
        'Ocp-Apim-Subscription-Region': AiTranslateConfig.LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid4())
    }

    # You can pass more than one object in body.
    body = list(map(lambda s: {"text": s}, text_inputs))

    request = post(AiTranslateConfig.CONSTRUCTED_URL, params=params, headers=headers, json=body)
    response = request.json()
    translated_texts = list(map(lambda s: s["translations"][0]["text"], response))

    return TranslateResult(text_inputs, translated_texts, to)


if __name__ == '__main__':
    test1 = '''
    1. Invest in your learning by participating in some fun and friendly competition. 
    '''
    test2 = '''
    2. Track your progress using the leaderboard as you navigate the Cloud Skill Challenge on Microsoft’s digital learn platform, 
    Microsoft Learn Compete between February 24, 2021 to March 24, 2021. Winners will be awarded on April 1, 2021.
    '''
    current_app.logger.info(translate_to([test1, test2]), 'zh-Hant')
