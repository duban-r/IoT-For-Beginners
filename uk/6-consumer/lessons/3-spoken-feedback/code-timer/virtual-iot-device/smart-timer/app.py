import threading
import time
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer
from text_to_timer import text_to_timer

speech_api_key = '<key>'
location = '<location>'
language = '<language>'

recognizer_config = SpeechConfig(subscription=speech_api_key,
                                 region=location,
                                 speech_recognition_language=language)

recognizer = SpeechRecognizer(speech_config=recognizer_config)

def get_timer_time(text):
    seconds = text_to_timer(text)
    return seconds

def say(text):
    print(text)

def announce_timer(minutes, seconds):
    announcement = 'Час вийшов! Таймер на '
    if minutes > 0:
        announcement += f'{minutes} хв '
    if seconds > 0:
        announcement += f'{seconds} с '
    announcement += 'завершено.'
    say(announcement)

def create_timer(total_seconds):
    minutes, seconds = divmod(total_seconds, 60)
    threading.Timer(total_seconds, announce_timer, args=[minutes, seconds]).start()

    announcement = 'Таймер на '
    if minutes > 0:
        announcement += f'{minutes} хв '
    if seconds > 0:
        announcement += f'{seconds} с '
    announcement += 'запущено.'
    say(announcement)

def process_text(text):
    print(text)

    seconds = get_timer_time(text)
    if seconds > 0:
        create_timer(seconds)

def recognized(args):
    process_text(args.result.text)

recognizer.recognized.connect(recognized)

recognizer.start_continuous_recognition()

while True:
    time.sleep(1)
