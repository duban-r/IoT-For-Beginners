import re

NUMBER_WORDS = {
    # українською
    'один': 1, 'одна': 1, 'одну': 1,
    'два': 2, 'дві': 2,
    'три': 3,
    'чотири': 4,
    "п'ять": 5,
    'шість': 6,
    'сім': 7,
    'вісім': 8,
    "дев'ять": 9,
    'десять': 10,
    'одинадцять': 11,
    'дванадцять': 12,
    'тринадцять': 13,
    'чотирнадцять': 14,
    "п'ятнадцять": 15,
    'шістнадцять': 16,
    'сімнадцять': 17,
    'вісімнадцять': 18,
    "дев'ятнадцять": 19,
    'двадцять': 20,
    'тридцять': 30,
    'сорок': 40,
    "п'ятдесят": 50,
    # англійською
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
}

TIME_UNITS = {
    'minute': ['minute', 'minutes', 'min', 'mins',
               'хвилина', 'хвилину', 'хвилини', 'хвилин', 'хв'],
    'second': ['second', 'seconds', 'sec', 'secs',
               'секунда', 'секунду', 'секунди', 'секунд', 'сек'],
}


def find_time_unit(word):
    for time_unit, synonyms in TIME_UNITS.items():
        if word in synonyms:
            return time_unit
    return None


def understand(text):
    text = text.lower().replace('’', "'").replace('ʼ', "'")
    words = re.findall(r"[\w']+", text)

    numbers = []
    time_units = []
    number = None

    for word in words:
        time_unit = find_time_unit(word)

        if word.isdigit():
            number = int(word)
        elif word in NUMBER_WORDS:
            value = NUMBER_WORDS[word]
            if number is not None and number >= 20 and number % 10 == 0 and value < 10:
                number += value
            else:
                number = value
        elif time_unit is not None and number is not None:
            numbers.append(number)
            time_units.append(time_unit)
            number = None
        else:
            number = None

    intent = None
    if len(numbers) > 0:
        intent = 'set timer'

    return {
        'intent': intent,
        'entities': {
            'number': numbers,
            'time unit': time_units
        }
    }


def text_to_timer(text):
    prediction = understand(text)

    if prediction['intent'] == 'set timer':
        numbers = prediction['entities']['number']
        time_units = prediction['entities']['time unit']
        total_seconds = 0

        for i in range(0, len(numbers)):
            number = numbers[i]
            time_unit = time_units[i]

            if time_unit == 'minute':
                total_seconds += number * 60
            else:
                total_seconds += number

        return total_seconds

    return 0


if __name__ == '__main__':
    while True:
        text = input('> ')
        print(understand(text))
        print('Секунд для таймера:', text_to_timer(text))
