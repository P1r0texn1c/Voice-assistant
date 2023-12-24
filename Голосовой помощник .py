import os
import random
import speech_recognition
import wikipedia
import requests
from datetime import datetime
from playsound import playsound

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'greeting_reply': ['привет', 'приветствую', 'добрый день', 'доброе утро', 'добрый вечер'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка', 'новая заметка', 'добавить заметку'],
        'play_music': ['включи музыку', 'музыка'],
        'time': ['сколько сейчас время', 'время', 'сколько времени'],
        'date': ['какое сегодня число', 'дата'],
        'wiki': ['поиск', 'узнай'],
        'weather':['погода', 'какая сейчас погода', 'температура за бортом']
    }
}


def listen_command():
    """The function will return the recognized command"""
    
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
            
        return query
    except speech_recognition.UnknownValueError:
        return 'Извините, не понял что вы сказали'


def greeting_reply(query):
    """Greeting function"""

    if query == 'добрый вечер':
        return 'Добрый вечер'
    elif query == 'добрый день':
        return 'Добрый день'
    elif query == 'доброе утро':
        return 'Доброе утро'
    else:
        greeting = random.choice(['Привет', 'Приветствую!'])
        return greeting
    


def create_task(query):
    """Create a todo task"""
    
    print('Что добавим в список дел?' or 'Что добавим?')
    
    query = listen_command()
        
    with open('/home/bunny_hop/Рабочий стол/Программы/Голосовой помощник/todo_list.txt', 'a') as file:
        file.write(f'❗️ {query}\n')
        
    return f'Задача {query} добавлена в todo-list!'


def play_music():
    """Play a random mp3 file"""
    
    files = os.listdir('/home/bunny_hop/Рабочий стол/Программы/Голосовой помощник/music')
    random_file = f'/home/bunny_hop/Рабочий стол/Программы/Голосовой помощник/music/{random.choice(files)}'
    playsound(random_file)
    

def time():

    return datetime.now().time()

def date():
    
    return datetime.now().date()

def wiki():

    print('Что нужно найти?')

    query = listen_command()
    wikipedia.set_lang("ru")

    print(wikipedia.summary(query))

def weather(query):

    print('В каком городе?')

    query = listen_command()
    query = query.title()
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+query+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])

    print('Сейчас в городе', query, str(temperature), '°C')
    print('Ощущается как', str(temperature_feels), '°C')


def main():
    query = listen_command()
    
    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k](query))
            break
       

if __name__ == '__main__':
    main()