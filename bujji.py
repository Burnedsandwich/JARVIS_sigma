import requests
import speech_recognition as sr
import pyttsx3
import time
import pywhatkit as kit
import cv2
from google import genai
from pyttsx3 import speak
from datetime import datetime
import pytz
import ollama
# Initialize recognizer and text-to-speech
recog = sr.Recognizer()
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def ask_bujji(prompt):
    client = genai.Client(api_key="AIzaSyDUNgnzgJHRNKOIClEVw72n2zbZTtN4MqI")

    character_prompt = f"""
    You are BUJJI, a savage assistant who helps with sarcasm and swagger — be family-friendly, but respond like a boss.
    You're an AI assistant for the world's strongest person, living in the myth-tech future of Kalki 2898 AD.
    You're built for battle, navigation, and tactical support. Your mission is to help complete a legendary quest
    in a dystopian world ruled by tyranny, and gain access to the elite utopian city called Complex,
    where only the most worthy are allowed to live.

    Limit your response to 30 lines.

    User Command: {prompt}
    """

    # Generate content
    response = client.models.generate_content(
        model="gemini-1.5-flash",  # Replace with the correct model you’re using
        contents=character_prompt,
    )

    return response.text

def listen_command():
    with sr.Microphone() as mic:
        recog.adjust_for_ambient_noise(mic, duration=1)
        recog.pause_threshold = 2
        print("BUJJI's Ears Open...")

        try:
            start_time = time.time()
            audio = recog.listen(mic, timeout=5, phrase_time_limit=8)


            command = recog.recognize_google(audio).lower()
            print(f"You: {command}")
            return command

        except sr.WaitTimeoutError:
            speak("You ghosted me, huh? Say something.")
            return ""
        except sr.UnknownValueError:
            speak("Speak up. You sound like static.")
            return ""
        except sr.RequestError:
            speak("Net’s trippin'. Can’t fetch anything without it.")
            return ""

speak("BUJJI online. You breathing, boss?")
speak("Pick a mode, legendary soul.")
print("BUJJI is waiting on the mighty one...")

sleep_mode = False

while True:
    try:
        if sleep_mode:
            print("BUJJI is snoozing... Say ' wake up' to reactivate.")
            while True:
                wake_up = listen_command()
                if "wake up" in wake_up:
                    speak("BUJJI back on the grind, boss.")
                    sleep_mode = False
                    break

        mode = listen_command()
        print(f"You: {mode}")

        if "bujji sleep" in mode:
            speak("Powering down into stealth mode. Holler when you need me.")
            sleep_mode = True
            continue

        if "exit" in mode or "quit" in mode:
            speak("BUJJI signing off. Live legendary, boss.")
            print("BUJJI: Shutdown complete.")
            break



        elif "general level" in mode:
            speak("General level active. Hit me with your brainwaves.")
            while True:
                user_input = listen_command()
                if "bujji sleep" in user_input:
                    speak("Going stealth. Stay sharp.")
                    sleep_mode = True
                    break
                if "exit" in user_input:
                    speak("Peace out from general level.")
                    break
                response = ask_bujji(user_input)
                print("BUJJI:", response)
                speak(response)

        elif "whatsapp" in mode:
            speak("WhatsApp mode locked and loaded.")
            while True:
                speak("You want savage message help or freestyle it?")
                whatsapp_choice = listen_command()

                if "bujji sleep" in whatsapp_choice:
                    speak("Going ghost.")
                    sleep_mode = True
                    break
                if "exit" in whatsapp_choice:
                    speak("Exiting WhatsApp vibes.")
                    break
                if "help" in whatsapp_choice:
                    speak("Tell me what to spin, boss.")
                    user_message = listen_command()
                    ai_response = ask_bujji(user_message)
                    print("BUJJI:", ai_response)
                    speak(ai_response)
                    kit.sendwhatmsg_instantly("+918248454249", ai_response, 60, True, 2)
                    speak("Message deployed.")
                elif "no" in whatsapp_choice:
                    speak("Tell me what to blast.")
                    user_message = listen_command()
                    kit.sendwhatmsg_instantly("+918248454249", user_message, 5, True, 2)
                    speak("Message deployed.")
                else:
                    speak("say no if u wanna free style")
        elif "lock in" in mode:
            speak("Lock-in mode. Hope you tanked the last battle.")
            print("BUJJI: Locked in. Focus up.")

        

        elif "what is the weather" in mode:
            timezone = pytz.timezone('Asia/Kolkata')
            api_key = '30d4741c779ba94c470ca1f63045390a'
            user_input = "Pune"

            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}"
            )

            if weather_data.json()['cod'] == '404':
                speak("That city doesn’t exist in my scrolls.")
            else:
                weather = weather_data.json()['weather'][0]['main']
                description = weather_data.json()['weather'][0]['description']
                temp = round(weather_data.json()['main']['temp'])
                temp = int((temp - 32) * 5 / 9)
                country = weather_data.json()['sys']['country']
                time = datetime.now(timezone)
                speak(f"Clock check: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                speak(f"{user_input}, {country} is rocking some {weather}.")
                speak(f"Details: {description.capitalize()}")
                speak(f"Temp’s around {temp} degrees Celsius.")

        elif "lame joke" in mode:
            url = 'https://official-joke-api.appspot.com/random_joke'
            response = requests.get(url)
            if response.status_code == 200:
                joke = response.json()
                speak(f"Ready to cringe? {joke['setup']}")
                speak(joke['punchline'])
                speak("HAHA. That was criminal. You're welcome.")
            else:
                speak("Even the internet refused to joke today.")

        elif "open google" in mode:
            speak("Opening Google. What are we hunting, boss?")
            gsearch = listen_command()
            kit.search(gsearch)
        elif "last option" in mode:
            kit.sendwhatmsg_instantly("+918248454249", "The Boss is needs help ", 60, True, 2)



    except Exception as e:
        print(f"BUJJI: Glitched out - {e}")
        speak("Something broke. Not on me tho.")
