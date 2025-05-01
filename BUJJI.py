import requests
import speech_recognition as sr
import pyttsx3
import os
import time
import pywhatkit as kit
import cv2
import ollama
from skimage.metrics import structural_similarity as ssim
from datetime import datetime
import pytz

# Initialize recognizer and text-to-speech
recog = sr.Recognizer()
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(text):
    """JARVIS speaks"""
    engine.say(text)
    engine.runAndWait()

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = "You are JARVIS, Tony Stark's AI assistant. Speak formally, efficiently, and with a touch of wit."

def ask_jarvis(prompt):
    """Send prompt to Ollama AI and get response"""
    data = {
        "model": "llama3",
        "prompt": f"System: {SYSTEM_PROMPT}\nUser: {prompt}\nJARVIS:",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=data)
    return response.json().get("response", "I'm unable to process that request, sir.")

def system_commands(command):
    """Execute system-level commands"""
    if "close window" in command:
        os.system("taskkill /f /im explorer.exe")
        speak("Window closed, sir.")

    elif "open notepad" in command:
        os.system("notepad")
        speak("Notepad opened, sir.")

    elif "open google" in command:
        speak("Opening Google, sir.")
        kit.search("")

    elif "game on" in command:
        speak("HOPPING ON FORTNITE SIGMA")
        os.startfile(r"C:\Users\vishw\OneDrive\Desktop\Fortnite.url")

    elif "shutdown" in command:
        speak("Shutting down your system in 5 seconds.")
        time.sleep(5)
        os.system("shutdown /s /t 1")

    else:
        speak("Sorry sir, I can't do that yet.")

def listen_command():
    """Listen for a command and return the recognized text"""
    with sr.Microphone() as mic:
        recog.adjust_for_ambient_noise(mic, duration=1)  # Better background noise handling
        recog.pause_threshold = 2  # Increase pause time
        print("Listening...")
        try:
            audio = recog.listen(mic, timeout=5, phrase_time_limit=8)  # Longer listening duration
            command = recog.recognize_google(audio).lower()
            print(f"Recognized: {command}")  # Debugging print
            return command
        except sr.UnknownValueError:
            print("JARVIS: Sorry, I couldn't understand that.")
            speak("Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError:
            print("JARVIS: Error connecting to speech recognition service.")
            speak("Error connecting to speech recognition service.")
            return ""

# Load reference image
reference = cv2.imread(r"C:\Users\vishw\OneDrive\Pictures\Camera Roll\WIN_20250427_13_01_37_Pro.jpg")
reference = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
reference = cv2.resize(reference, (100, 100))

# Function to calculate SSIM
def calculate_ssim(img1, img2):
    score, _ = ssim(img1, img2, full=True)
    return score

# Open camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
speak("Are you my BOSS ?")
owner_found = False  # 👈 New flag

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))

        similarity = calculate_ssim(reference, face)

        if similarity >= 0.22:
            owner_found = True
            color = (0, 255, 0)
            label = f"OWNER ({similarity:.2f})"
        else:
            color = (0, 0, 255)
            label = f"NOT OWNER ({similarity:.2f})"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow('Frame Comparison', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if owner_found:
        speak("BOSS detected")
        speak("POWERING UP")
        break

# Start-up message
speak("Hello sir, hope you're doing well.")
speak("What mode do you want to operate in, sir? System level, general level, or WhatsApp mode?")
print("Listening for mode selection...")

sleep_mode = False  # Variable to track sleep mode

while True:
    try:
        if sleep_mode:
            print("JARVIS is sleeping... Say 'Jarvis, wake up' to activate.")
            while True:
                wake_up = listen_command()
                if "jarvis wake up" in wake_up:
                    speak("I am back, sir.")
                    sleep_mode = False
                    break  # Exit sleep mode and continue operations

        mode = listen_command()
        print(f"You: {mode}")

        if "jarvis sleep" in mode:
            speak("Going into sleep mode, sir. Call me when you need me.")
            sleep_mode = True
            continue  # Restart loop to enter sleep mode

        if "exit" in mode or "quit" in mode:
            speak("Very well, sir. I shall now power down. Goodbye.")
            print("JARVIS: Powering down.")
            break

        if "system level" in mode:
            speak("System level mode activated, sir.")
            print("JARVIS: System level mode activated.")

            while True:
                speak("Awaiting your system command, sir.")
                command = listen_command()
                print(f"You: {command}")

                if "jarvis sleep" in command:
                    speak("Going into sleep mode, sir.")
                    sleep_mode = True
                    break  # Go back to sleep mode

                if "exit" in command:
                    speak("Exiting system level mode, sir.")
                    break

                system_commands(command)

        elif "general level" in mode:
            speak("General mode activated, sir.")
            print("JARVIS: General mode activated.")

            while True:
                speak("How may I assist you, sir?")
                user_input = listen_command()
                print(f"You: {user_input}")

                if "jarvis sleep" in user_input:
                    speak("Going into sleep mode, sir.")
                    sleep_mode = True
                    break

                if "exit" in user_input:
                    speak("Exiting general level mode, sir.")
                    break

                response = ask_jarvis(user_input)
                print("JARVIS:", response)
                speak(response)


        elif "whatsapp" in mode:

            speak("WhatsApp mode activated, sir.")

            print("JARVIS: WhatsApp mode activated.")

            while True:

                speak("Do you want to send a normal message or need my help drafting one?")

                whatsapp_choice = listen_command()

                print(f"You: {whatsapp_choice}")

                if "jarvis sleep" in whatsapp_choice:
                    speak("Going into sleep mode, sir.")

                    sleep_mode = True

                    break

                if "exit" in whatsapp_choice:
                    speak("Exiting WhatsApp mode, sir.")

                    break

                if "help" in whatsapp_choice:

                    speak("How can I help you draft your message, sir?")

                    user_message = listen_command()

                    print(f"You: {user_message}")

                    ai_response = ask_jarvis(user_message)

                    print("JARVIS:", ai_response)

                    speak(ai_response)

                    kit.sendwhatmsg_instantly("+919952326686", ai_response, 60, True, 2)

                    speak("Message sent, sir.") 


                else:

                    speak("What message would you like to send?")

                    user_message = listen_command()

                    print(f"You: {user_message}")

                    kit.sendwhatmsg_instantly("+918248454249", user_message, 5, True, 2)

                    speak("Message sent, sir.")
        elif "lock in" in mode:
            speak("Lock in mode activated, sir.")
            speak("Enjoy your task, sir.")
            print("JARVIS: Lock in mode activated.")
        elif "image check" in mode:


            # 1. Open the webcam
            cam = cv2.VideoCapture(0)

            if not cam.isOpened():
                print("Could not open webcam")
                exit()

            print("Press SPACE to capture the image, or ESC to exit.")

            while True:
                ret, frame = cam.read()
                if not ret:
                    print("Failed to grab frame!")
                    break

                cv2.imshow("Live Camera - Press SPACE to Capture", frame)

                k = cv2.waitKey(1)

                if k % 256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k % 256 == 32:
                    # SPACE pressed
                    image_path = 'live_capture.jpg'
                    cv2.imwrite(image_path, frame)
                    print(f"Image saved as {image_path}")
                    break

            cam.release()
            cv2.destroyAllWindows()

            # 2. Send the captured image to ollama
            res = ollama.chat(
                model='llava:13b',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful assistant who clearly looks at the image and analyzes it in a simple and easy way.'
                    },
                    {
                        'role': 'user',
                        'content': 'Describe the live captured image properly.',
                        'images': [image_path]
                    }
                ]
            )

            # 3. Print the description
            print("\n🧠 LLaVA Analysis:")
            print(res['message']['content'])
            speak(res['message']['content'])

        elif "what is the weather" in mode:
            timezone = pytz.timezone('Asia/Kolkata')
            api_key = '30d4741c779ba94c470ca1f63045390a'
            user_input = "Pune"

            # Fetching the weather data from OpenWeatherMap
            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")

            # Check if city is found
            if weather_data.json()['cod'] == '404':
                print("No City Found")
            else:
                # Extracting weather details
                weather = weather_data.json()['weather'][0]['main']
                description = weather_data.json()['weather'][0]['description']
                temp = round(weather_data.json()['main']['temp'])
                temp = int((temp - 32) * 5 / 9)
                country = weather_data.json()['sys']['country']
                time = datetime.now(timezone)
                print("Local time in India:", time.strftime('%Y-%m-%d %H:%M:%S'))
                speak ("Local time in India:", time.strftime('%Y-%m-%d %H:%M:%S'))
                print(f"The weather in {user_input}, {country} is: {weather}")
                speak(f"The weather in {user_input}, {country} is: {weather}")
                print(f"Description: {description.capitalize()}")
                speak(f"Description: {description.capitalize()}")
                print(f"The temperature in Celsius is: {temp}°C")
                speak(f"The temperature in Celsius is: {temp}°C")
                print(f"The temperature in Fahrenheit is: {round(weather_data.json()['main']['temp'])}°F")
                speak(f"The temperature in Fahrenheit is: {round(weather_data.json()['main']['temp'])}°F")

        else:
            print("Sorry, I don't know that yet.")
            speak("Sorry, I don't know that yet.")
    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()
