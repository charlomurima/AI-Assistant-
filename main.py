import os
import time
import sounddevice as sd
import soundfile as sf
import requests
import json
from gtts import gTTS
import openai

api_key = "YOUR_API_KEY"
lang = 'en'

openai.api_key = api_key


def record_audio(filename, duration):
    # Record audio for the specified duration
    print("Recording...")
    audio_data = sd.rec(int(duration * 44100), samplerate=44100, channels=2)
    sd.wait()
    # Save the recorded audio to a WAV file
    sf.write(filename, audio_data, samplerate=44100)


def recognize_speech(filename):
    try:
        # Make a POST request to the Google Web Speech API with the recorded audio
        url = "https://speech.googleapis.com/v1/speech:recognize?key=YOUR_API_KEY"
        headers = {"Content-Type": "audio/wav"}
        with open(filename, "rb") as f:
            audio_data = f.read()
        response = requests.post(url, headers=headers, data=audio_data)
        response_data = json.loads(response.text)

        # Parse the response and extract the recognized text
        if "results" in response_data and response_data["results"]:
            recognized_text = response_data["results"][0]["alternatives"][0]["transcript"]
            print("You said:", recognized_text)
            return recognized_text
        else:
            print("Sorry, no speech was recognized.")
            return ""
    except Exception as e:
        print("Error:", e)
        return ""


def generate_response(input_text):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": input_text}])
    response = completion.choices[0].message.content
    print("Response:", response)
    speak(response)


def speak(text):
    speech = gTTS(text=text, lang=lang, slow=False)
    speech.save("response.mp3")
    os.system("start response.mp3")


def main():
    while True:
        record_audio("audio.wav", 5)  # Record audio for 5 seconds and save it to "audio.wav"
        command = recognize_speech("audio.wav")
        if "stop" in command:
            break
        if command:
            generate_response(command)
        time.sleep(1)


if __name__ == "__main__":
    main()
