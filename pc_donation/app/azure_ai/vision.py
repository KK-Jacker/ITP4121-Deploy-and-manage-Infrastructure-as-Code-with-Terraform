import requests
from flask import current_app
from flask_babel import _

from config import AiAnalyzeConfig


# TODO: rewrite with SDK https://docs.microsoft.com/en-us/python/api/overview/azure/cognitiveservices-vision-computervision-readme?view=azure-python
def vision_analyze(photo_path, check_age_range=False, check_face=True):
    if AiAnalyzeConfig.KEY is not None and AiAnalyzeConfig.ENDPOINT is not None:
        analyze_url = AiAnalyzeConfig.ENDPOINT + "vision/v3.1/analyze"
        headers = {
            'Ocp-Apim-Subscription-Key': AiAnalyzeConfig.KEY,
            'Content-Type': 'application/json'
        }
        params = {'visualFeatures': 'Description,Faces,Adult'}
        data = {"url": photo_path}
        analysis = None
        try:
            response = requests.post(analyze_url,
                                     headers=headers,
                                     params=params,
                                     json=data)
            response.raise_for_status()
            analysis = response.json()
        except Exception as ex:
            current_app.logger.info(ex)
            return _(ex.__str__())
            # return _(ex)

        current_app.logger.info(analysis)
        if check_face and len(analysis['faces']) == 0:
            current_app.logger.info("No face")
            return _('Invalid Photo: Unable to recognize any faces!')
        elif analysis["adult"]["isAdultContent"]:
            current_app.logger.info("Adult Content")
            return _('Invalid Photo: Adult Content!')
        elif analysis["adult"]["isGoryContent"]:
            current_app.logger.info("Gory Content")
            return _('Invalid Photo: Gory Content!')
        elif analysis["adult"]["isRacyContent"]:
            current_app.logger.info("Racy Content")
            return _('Invalid Photo: Racy Content!')
        elif check_face and check_age_range:
            # Do some function in here (e.g.: upload photos)
            if analysis['faces'][0]['age'] < 6 or analysis['faces'][0]['age'] >= 30:
                return _(
                    'Invalid Photo: our AI infers you are under age 6 or over 30!'
                )
    return None
