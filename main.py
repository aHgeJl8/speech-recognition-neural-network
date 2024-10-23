# pip install vosk
# pip install pyaudio
from answer import answer_ru, answer_en
import os
import vosk
import pyaudio
import json
import pyttsx3

# Проверьте, существует ли модель
if not os.path.exists("model_ru"):
    print("Пожалуйста, скачайте модель с https://alphacephei.com/vosk/models и распакуйте её в текущий каталог. Нужно скачать vosk-model-small-ru-0.22 и распаковать в папку model содержимое vosk-model-small-ru-0.22")
    exit()
if not os.path.exists("model_en"):
    print("не скачал")
    exit()

# Загрузка модели
model_ru = vosk.Model("model_ru")
model_en = vosk.Model("model_en")

# Настройка аудиопотока
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

rec_ru = vosk.KaldiRecognizer(model_ru, 16000)
rec_en = vosk.KaldiRecognizer(model_en, 16000)

def ru():
    global qw
    
    if qw == 'ru':  
        try:
            print("Начало распознавания... Говорите в микрофон.")
            while True:
                    
                data = stream.read(4000, exception_on_overflow=False)
                if len(data) == 0:
                    break
                if rec_ru.AcceptWaveform(data):
                    result = json.loads(rec_ru.Result())
                    print(f"Распознанный текст: {result['text']}")

                    tts = pyttsx3.init()
                    tts.getProperty('voice')

                    if result['text'] in answer_ru.keys():
                        text = answer_ru[result['text']]
                        tts.say(text)
                        tts.runAndWait()

                    if result['text'] == 'пока':
                        print("Распознавание завершено.")
                        exit()

                    if result['text'] == 'смени на английский':
                        qw = 'en'
                        return qw

        except KeyboardInterrupt:
                print("Распознавание завершено.")
        finally:
                stream.stop_stream()
                stream.close()
                audio.terminate()

def en():
    global qw
    if qw == 'en':
        try:
            print("The beginning of recognition... Speak into the microphone.")
            while True:
                
                data = stream.read(4000, exception_on_overflow=False)
                if len(data) == 0:
                    break
                if rec_en.AcceptWaveform(data):
                    result = json.loads(rec_en.Result())
                    print(f"Recognized text: {result['text']}")

                    tts = pyttsx3.init()
                    tts.getProperty('voice')

                    if result['text'] in answer_en.keys():
                        text = answer_en[result['text']]
                        tts.say(text)
                        tts.runAndWait()
                            
                    if result['text'] == 'goodbye':
                        print("Recognition is complete.")
                        exit()
                    
                    if result['text'] == 'change to russian':
                        qw = 'ru'
                        return qw
                            
        except KeyboardInterrupt:
                print("Recognition is complete.")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

if __name__ == "__main__":
    qw = input("language/язык (en, ru): ")
    while True:
        if qw == 'ru':
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            stream.start_stream()
            print("\n")
            ru()
        elif qw == 'en':
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            stream.start_stream()
            print("\n")
            en()
        else:
            print("ERROR/ОШИБКА")

