from tongues_api.tongues_api import TonguesAPI
from django.test import SimpleTestCase
from pydub import AudioSegment
from io import BytesIO
import speech_recognition as sr

import base64
import string

class TestTranslateSpeechToSpeech(SimpleTestCase):

    # Contains numbers 1-10 in spanish as base64 string
    SAMPLE_BASE64_FILE_PATH = "tongues_api/tests/fixtures/base64_audio_es_1_10.txt"
    SOURCE_LANG = 'es-ES'
    TARGET_LANG = 'en-US_M_Neural_D_0028'
    EXPECTED_TRANSLATION = "1,2,3,4,5,6,7,8,9,10"
    EXPECTED_RECOGNIZED_TEXT = "one two three four five six seven eight nine ten."

    def setUp(self):
        with open(self.SAMPLE_BASE64_FILE_PATH, 'r') as file: self.base64_speech = file.read()

        self.speech_recognizer = sr.Recognizer()

        self.tongues_api = TonguesAPI()

    def _base64_audio_to_text(self, base64_str: str) -> str:
        # Decode Base64 string to bytes
        audio_bytes = base64.b64decode(base64_str)

        # Load audio data into an AudioSegment
        audio_segment = AudioSegment.from_file(BytesIO(audio_bytes))

        # Convert the audio to WAV format (if not already in WAV)
        if audio_segment.channels != 1 or audio_segment.frame_rate != 16000 or audio_segment.sample_width != 2:
            audio_segment = audio_segment.set_frame_rate(16000).set_channels(1).set_sample_width(2)

        # Export the audio to a BytesIO object in WAV format
        wav_file = BytesIO()
        audio_segment.export(wav_file, format="wav")

        # Reset the file pointer for reading
        wav_file.seek(0)

        # Recognize the speech from the WAV file
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)

    def test_translate_speech_to_speech(self):
        translation_result = self.tongues_api.translate_speech_to_speech(self.base64_speech, self.SOURCE_LANG, self.TARGET_LANG)

        translation_result_base64_str = translation_result['translatedAudio']
        translation_result_recognized_text = translation_result['translatedText'].lower()

        translation_result_readable_text = self._base64_audio_to_text(translation_result_base64_str)

        # translator variable has nothing to do with the actual linguistic translation.
        # it's a "translator" in the context of "string" library
        translator = str.maketrans('', '', string.punctuation)
        translation_result_readable_text = translation_result_readable_text.translate(translator).lower().replace(" ", "")
        expected_translation = self.EXPECTED_TRANSLATION.translate(translator).lower().replace(" ", "")

        
        self.assertEquals(translation_result_readable_text, expected_translation)

        self.assertEquals(translation_result_recognized_text, self.EXPECTED_RECOGNIZED_TEXT)