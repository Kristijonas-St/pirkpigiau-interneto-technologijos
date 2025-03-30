import streamlit as st
import sounddevice as sd
import numpy as np
import tempfile
import wave
import whisper

st.info("Įkeliama balso atpažinimo funkcija (gali užtrukti kelias sekundes)")
model = whisper.load_model("small")

class VoiceRecognizer:
    def __init__(self):
        self.model = model
    def record_audio(self, duration=3, samplerate=16000):
        st.info("🎙️ Kalbėkite dabar...")
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            with wave.open(temp_audio.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(samplerate)
                wf.writeframes(recording.tobytes())
            return temp_audio.name

    def recognize_speech_whisper(self):
        audio_file = self.record_audio()
        st.info("🔄 Apdorojama kalba...")

        result = model.transcribe(audio_file, language="lt")
        return result["text"].strip()

