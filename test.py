# pip install vosk
# pip install pyaudio
from answer import answer
import os
import vosk
import pyaudio
import json
import pyttsx3

# Проверьте, существует ли модель
if not os.path.exists("model"):
    print("Пожалуйста, скачайте модель с https://alphacephei.com/vosk/models и распакуйте её в текущий каталог. Нужно скачать vosk-model-small-ru-0.22 и распаковать в папку model содержимое vosk-model-small-ru-0.22")
    exit()

# Загрузка модели
model = vosk.Model("model")

# Настройка аудиопотока
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

rec = vosk.KaldiRecognizer(model, 16000)

print("Начало распознавания... Говорите в микрофон.")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print(f"Распознанный текст: {result['text']}")

            # text = result['text']
            tts = pyttsx3.init()

            tts.getProperty('voice')


            if result['text'] in answer.keys():
                # print("Робот ответил: Hello user!")

                text = answer[result['text']]

                tts.say(text)
                tts.runAndWait()

                

except KeyboardInterrupt:
    print("Распознавание завершено.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
