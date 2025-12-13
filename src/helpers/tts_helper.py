import pyttsx3
from threading import Thread

class TTS:
    def speak(self, text: str):
        def task():
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 170)
                engine.setProperty("volume", 1.0)

                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as e:
                print("Erro no TTS:", e)

        Thread(target=task, daemon=True).start()

tts = TTS()
