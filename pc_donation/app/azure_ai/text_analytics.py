import io
from enum import Enum

from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics._generated.v3_1.models import PiiCategory
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.core.credentials import AzureKeyCredential
from flask import current_app
from msrest.authentication import CognitiveServicesCredentials

from app.azure_ai.result_base import ResultBase
from config import AiTextAnalyticsConfig, ContentModeratorConfig


def _get_text_analytics_client():
    ta_credential = AzureKeyCredential(AiTextAnalyticsConfig.KEY)
    text_analytics_client = TextAnalyticsClient(
        endpoint=AiTextAnalyticsConfig.ENDPOINT,
        credential=ta_credential)
    return text_analytics_client


class SentimentResult(ResultBase):
    class Sentiment(Enum):
        POSITIVE = 1
        # TODO: NEUTRAL may be no longer used at all and need to delete it once Azure released documents.
        NEUTRAL = 2
        NEGATIVE = 3
        MIXED = 4

    def __init__(self, result: Sentiment, positive_score, neutral_score, negative_score):
        self.result = result
        self.positive_score = positive_score
        self.neutral_score = neutral_score
        self.negative_score = negative_score


def sentiment_analysis(text):
    client = _get_text_analytics_client()
    response = client.analyze_sentiment(documents=[text])[0]
    return SentimentResult(SentimentResult.Sentiment[response.sentiment.upper()],
                           response.confidence_scores.positive, response.confidence_scores.neutral,
                           response.confidence_scores.negative)


def get_urgency_point(text):
    sentiment = sentiment_analysis(text)
    details = min(len(text.replace(" ", "")), 100)
    current_app.logger.info(text)
    current_app.logger.info(sentiment)
    current_app.logger.info(details)
    urgency = 0
    if sentiment.result == SentimentResult.Sentiment.POSITIVE:
        urgency = details - sentiment.positive_score * 50
    elif sentiment.result == SentimentResult.Sentiment.NEUTRAL or sentiment.result == SentimentResult.Sentiment.MIXED:
        urgency = details + sentiment.negative_score * 50 - sentiment.positive_score * 50
    elif sentiment.result == SentimentResult.Sentiment.NEGATIVE:
        urgency = details + sentiment.negative_score * 100
    current_app.logger.info("urgency: " + str(urgency))
    return urgency


def get_thankful_point(text):
    sentiment = sentiment_analysis(text)
    details = min(len(text.replace(" ", "")), 100)
    current_app.logger.info(text)
    current_app.logger.info(sentiment)
    current_app.logger.info(details)
    thankful = 0
    if sentiment.result == SentimentResult.Sentiment.NEGATIVE:
        thankful = details - sentiment.positive_score * 50
    elif sentiment.result == SentimentResult.Sentiment.NEUTRAL or sentiment.result == SentimentResult.Sentiment.MIXED:
        thankful = details + sentiment.negative_score * 50 - sentiment.positive_score * 50
    elif sentiment.result == SentimentResult.Sentiment.POSITIVE:
        thankful = details + sentiment.negative_score * 100
    current_app.logger.info("thankful: " + str(thankful))
    return thankful


def key_phrase_extraction(text):
    client = _get_text_analytics_client()
    try:
        response = client.extract_key_phrases(documents=[text])[0]
        if not response.is_error:
            return response.key_phrases
        else:
            return []

    except Exception as err:
        current_app.logger.info("Encountered exception. {}".format(err))
        return []


def redact_pii(text):
    client = _get_text_analytics_client()
    categories_filter = [PiiCategory.EMAIL, PiiCategory.CREDIT_CARD_NUMBER, PiiCategory.PHONE_NUMBER]
    response = client.recognize_pii_entities([text], categories_filter=categories_filter)
    result = [doc for doc in response if not doc.is_error]
    return result[0].redacted_text


def is_content_ok(text, check_pii=True):
    current_app.logger.info("is_content_ok: " + text)
    ta_credential = CognitiveServicesCredentials(ContentModeratorConfig.KEY)
    client = ContentModeratorClient(
        endpoint=ContentModeratorConfig.ENDPOINT,
        credentials=ta_credential
    )

    f = io.BytesIO(text.encode())
    screen = client.text_moderation.screen_text(
        text_content_type="text/plain",
        text_content=f,
        language="eng",
        autocorrect=True,
        pii=check_pii
    )
    current_app.logger.info(screen.pii)
    if check_pii:
        if screen.pii is not None:
            current_app.logger.info("Found PII")
            return False
    return screen.terms is None


if __name__ == '__main__':
    test = '''
    my family is poor and my mother is in sick.
    
    '''
    print(is_content_ok(test))
