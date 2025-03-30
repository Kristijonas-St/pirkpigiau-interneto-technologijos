import unittest
from unittest.mock import patch
import whisper
from voice_recognition.voice_recognition import VoiceRecognizer

class TestVoiceRecognizer(unittest.TestCase):
    @patch.object(whisper.Whisper, 'transcribe')
    @patch('voice_recognition.voice_recognition.VoiceRecognizer.record_audio', return_value="test_audio.wav")
    def test_recognize_speech_whisper(self, mock_record_audio, mock_transcribe):
        mock_transcribe.return_value = {"text": "testas"}

        recognizer = VoiceRecognizer()
        result = recognizer.recognize_speech_whisper()

        self.assertEqual(result, "testas")
        mock_record_audio.assert_called_once()
        mock_transcribe.assert_called_once_with("test_audio.wav", language="lt")

if __name__ == "__main__":
    unittest.main()