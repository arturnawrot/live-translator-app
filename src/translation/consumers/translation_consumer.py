from translation.models import Usage, ShareCode, TranscriptRecord
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
from tongues_api.tongues_api import TonguesAPI
from pydub import AudioSegment
from datetime import datetime
import json
import io
import base64

class TranslationConsumer(AsyncWebsocketConsumer):
    
    # result in seconds
    def get_audio_length(self, base64audio: str) -> float:
        audio_bytes = base64.b64decode(base64audio)

        audio_stream = io.BytesIO(audio_bytes)
        audio = AudioSegment.from_file(audio_stream)

        duration_milliseconds = len(audio)
        duration_seconds = duration_milliseconds / 1000.0

        return duration_seconds

    async def connect(self):
        self.user = self.scope["user"]
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def __save_usage(self, base64, user):
        duration_seconds = self.get_audio_length(base64)

        usage = Usage(user=user, duration=duration_seconds)
        usage.save()

    @database_sync_to_async
    def __get_user_to_bill(self, share_code=None):
        if share_code is not None and share_code is not '':
            share_code = ShareCode.objects.filter(code=share_code).first()
            
            if share_code is None:
                return None
            
            return share_code.user
        elif isinstance(self.user, User):
            return self.user
        
        return None
    
    @database_sync_to_async
    def __save_transcript_record(self, text, uuid=None):
        if len(text) == 0 or text == None:
            return
        
        new_record = TranscriptRecord(
            uuid=uuid,
            datetime=datetime.now(),
            content=text
        )

        new_record.save()

    @database_sync_to_async
    def __is_authorized(self, user):
        if user.is_superuser:
            return True
        
        if user is None or user is AnonymousUser:
            return False
        
        if user.payment_profile.is_subscription_active():
            return True
        
        return False
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        base64 = text_data_json['base64']
        source_lang = text_data_json['source_lang']
        target_lang = text_data_json['target_lang']
        share_code = text_data_json['share_code'] if 'share_code' in text_data_json else None
        uuid = text_data_json['uuid'] if 'uuid' in text_data_json else None

        tongues_api = TonguesAPI()

        translation_result = None

        try:
            status = "success"

            user = await self.__get_user_to_bill(share_code)

            if await self.__is_authorized(user) == False:
                translation_result = 'Unauthorized. Make sure the administrator has an active subscription.'
                raise Exception('Unauthorized')

            await self.__save_usage(base64, user)

            translation_result = tongues_api.translate_speech_to_speech(base64, source_lang, target_lang)

            await self.__save_transcript_record(translation_result['translatedText'], uuid)
        except Exception as e:
            status = "error"
            if translation_result is None:
                translation_result = 'Something went wrong. If the issue persists please try again later or contact the administrator.'


        await self.send(text_data=json.dumps({
            'status': status,
            'translation_result': translation_result
        }))
