import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
# from openai import OpenAI
# from gtts import gTTS 
import pygame
import os

# pip install pocketsphinx

# Initialize pygame mixer
pygame.mixer.init()

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
engine.setProperty('rate', 180)
newsapi = "f2a49ada6c114a1b8a8675831b42bf00"

def speak(text):
    engine.say(text)
    engine.runAndWait()

'''
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 
'''

# def aiProcess(command):
#     client = OpenAI(api_key="<Your Key Here>",
#     )

#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
#         {"role": "user", "content": command}
#     ]
#     )

#     return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("search"):
        l = c.split()
        I = '+'.join(l[1:len(l)])
        webbrowser.open(f"https://www.bing.com/search?q={I}&cvid=7658d7d456174c12a4c58b733740349a&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg80gEJMTE3MjRqMGo3qAIAsAIA&FORM=ANNTA0&PC=HCTS")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        # webbrowser.open(link)
        # Function to play music
        def play_music(file_path):
            # Load the music file
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            # Keep playing until the music is finished
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        # Specify the path to your music file
        music_file = f"{link}"  # Update with your file path

        if os.path.exists(music_file):
            play_music(music_file)
        else:
            print("Music file not found!")
    elif "bahra" in c.lower():
        speak(" tu hoga bahra")

    elif "abey" in c.lower():
        speak("abey mat kahiye")

    elif "kya" in c.lower():
        speak("nahi. achhaa chal poochh poochh")
        
    elif "beta" in c.lower():
        speak("mai aapka betaa nahi hu !")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            try:
                # Parse the JSON response
                data = r.json()
                
                # Extract the articles
                articles = data.get('articles', [])
                
                # Print the headlines
                for article in articles:
                    speak(article['title'])
            except ValueError:
                speak("Failed to parse news data.")
        else:
            speak(f"Failed to retrieve news: {r.status_code}")

    # else:
    #     speak(" bkwas mt kar yaar ")
    else:
        print(c.lower())
        # else:
        #     # Let OpenAI handle the request
        #     output = aiProcess(c)
        #     speak(output) 


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        recognizer = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            word = recognizer.recognize_google(audio)
            print(f"Recognized: {word}")
            
            if word.lower() == "jarvis":
                speak("Haa bol naa")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                command = recognizer.recognize_google(audio)
                print(f"Command: {command}")
                processCommand(command)

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
