import requests
import speech_recognition as sr
import pyttsx3
import time
import pywhatkit as kit
import cv2
import ollama
from pyttsx3 import speak
from datetime import datetime
import pytz

# Initialize recognizer and text-to-speech
recog = sr.Recognizer()
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def ask_bujji(prompt):
    response = ollama.chat(
        model='llama3.2:1b',
        messages=[
            {"role": "system", "content": "You are BUJJI, a savage assistant with sarcasm and swagger, yet a little family-friendly. Respond like a myth-tech boss from Kalki 2898 AD. Your mission is to guide the user through the dystopian chaos and help them enter the elite city Complex."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']



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

        elif "image check" in mode:
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                print("Webcam’s hiding.")
                exit()
            print("Press SPACE to snap or ESC to flee.")

            while True:
                ret, frame = cam.read()
                if not ret:
                    print("No vibes in the frame.")
                    break

                cv2.imshow("Myth-Tech Cam - Hit SPACE", frame)
                k = cv2.waitKey(1)

                if k % 256 == 27:
                    print("Retreating from camera.")
                    break
                elif k % 256 == 32:
                    image_path = 'live_capture.jpg'
                    cv2.imwrite(image_path, frame)
                    print(f"Captured: {image_path}")
                    break

            cam.release()
            cv2.destroyAllWindows()

            res = ollama.chat(
                model='llava-phi3',

                messages=[
                    {'role': 'system', 'content': 'Describe the image clearly and easily.'},
                    {'role': 'user', 'content': 'Analyze this myth-tech snapshot.', 'images': [image_path]}
                ]
            )
            print("\n🔍 BUJJI’s Cam Insight:")
            print(res['message']['content'])
            speak(res['message']['content'])

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
