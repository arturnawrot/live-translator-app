from django.conf import settings
import requests
import json

class TonguesAPI:

    BASE_URL = 'https://api.tonguesservices.com/prod'

    def __init__(self):
        self.API_KEY = settings.TONGUES_API_KEY

        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.API_KEY
        }
    
    def translate_speech_to_speech(self, base64: str, source_lang: str, target_lang: str) -> dict:
        """
        Translates speech from one language to speech in another language.

        List of supported languages: https://tongues.services/stt-asr-dialects-supported-by-tongues-api-series/
        
        Parameters:
            text (str): Base64 encoded speech to be translated.
            source_lang (str): The code of the source language (e.g., 'en-US' for American English).
            target_lang (str): The code of the target language (e.g., 'es-ES' for Spanish).

        Returns:
            str: Audio encoded as a base64 string.
        """
        payload = {
            "TonguesVoiceCode": target_lang,
            "SourceLangCode": source_lang,
            "SourceAudioContent": base64
        }

        data = json.dumps(payload)

        response = requests.post(self.BASE_URL + '/realtime/v1/SpeechToSpeechTextTranslation', data=data, headers=self.headers)

        if response.status_code != 200 or not response.json()['translatedAudio']:
            print(response.text)
            raise Exception('Something went wrong...')
        
        data = response.json()

        return {
            'translatedAudio': data['translatedAudio'],
            'translatedText': data['translatedText']
        }
    
    def get_health_status(self) -> bool:
        """
        https://api.tonguesservices.com/prod/swagger/index.html

        If the response status code is 200 everything is ok, otherwise it's not.
        """
        try:
            return requests.get(self.BASE_URL + '/realtime/Health').status_code == 200
        except Exception as e:
            print(f"Error connecting to Tongues API: {e}")
            return False