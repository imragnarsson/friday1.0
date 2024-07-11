import subprocess
import sys

# Vérifier si les packages requis sont installés
def verifier_dependences():
    with open('requirements.txt') as f:
        dependences = f.read().splitlines()
    
    for dependence in dependences:
        try:
            __import__(dependence)
        except ImportError:
            print(f"Installation de {dependence}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependence])

# Installer les dépendances
verifier_dependences()

# Maintenant, importer les modules nécessaires
import speech_recognition as sr
from gtts import gTTS
import os
from transformers import pipeline
import requests
from flask import Flask, render_template, request
from googlesearch import search

# Le reste de votre code reste inchangé...


import speech_recognition as sr
from gtts import gTTS
import os
from transformers import pipeline
import requests
from flask import Flask, render_template, request
from googlesearch import search

# Reconnaissance Vocale
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        audio = recognizer.listen(source)
    response = {"success": True, "error": None, "transcription": None}

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    
    return response

# Synthèse Vocale
def speak(text):
    tts = gTTS(text=text, lang='fr', tld='com.au')  # Utiliser un accent féminin (Australie)
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")

# Traitement du Langage Naturel (NLP)
nlp = pipeline("question-answering")
context = "Your context about the command or general knowledge base."

def handle_command(command):
    if "weather" in command:
        return get_weather()
    elif "light" in command:
        return control_smart_light("on")
    elif "reminder" in command:
        return "Reminder set for 3 PM."
    else:
        return search_web(command)

def get_weather():
    url = "http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=Paris"
    response = requests.get(url)
    weather_data = response.json()
    return f"The current temperature is {weather_data['current']['temp_c']} degrees Celsius."

def control_smart_light(action):
    url = "http://smart-light.local/api"
    data = {"action": action}
    response = requests.post(url, json=data)
    return response.json()

# Fonction de recherche web
def search_web(query):
    search_results = search(query, num_results=5)
    if search_results:
        first_result = search_results[0]
        return f"I found this information: {first_result}"
    else:
        return "I'm sorry, I couldn't find any information on that topic."

# Interface Web avec Flask (Python)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    user_command = request.form['command']
    response_text = handle_command(user_command)
    return response_text

if __name__ == '__main__':
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    print("Say something!")
    response = recognize_speech_from_mic(recognizer, mic)
    print("You said: {}".format(response["transcription"]))

    command = response["transcription"]
    response_text = handle_command(command)
    speak(response_text)

    app.run(debug=True)
