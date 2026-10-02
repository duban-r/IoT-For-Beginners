import threading
from text_to_timer import text_to_timer

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
    print('Ви сказали:', text)

    seconds = get_timer_time(text)
    if seconds > 0:
        create_timer(seconds)

while True:
    text = input('> ')
    process_text(text)
