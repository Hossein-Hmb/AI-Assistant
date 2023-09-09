import os
from flask import Flask, render_template, request, jsonify, send_file
import openai
import config
import sounddevice as sd
import numpy as np
import io
from pydub import AudioSegment
import requests
import base64

openai.api_key = config.OPENAI_API_KEY
ELEVENLABS_API_KEY = config.ELEVENLABS_API_KEY

messages = []
app = Flask(__name__, static_folder="static", template_folder="templates")

# Function that converts text to speech using Eleven Labs' API


def tts_eleven_labs(text):
    url = "https://tts.api.elevenlabs.com/v1/speak"
    headers = {
        "Authorization": f"Bearer {ELEVENLABS_API_KEY}"
    }
    data = {
        "text": text,
        "voice": "elevenlabs/en-US-WaveNet-A",  # You can change the voice as needed
        "outputFormat": "mp3"
    }
    response = requests.post(url, json=data, headers=headers)
    audio_mp3_base64 = base64.b64encode(response.content).decode('utf-8')
    return audio_mp3_base64


# ... (Your existing code, such as "import openai" and "transcribeAudio()" should be here.) ...
"""Transcription part of the code"""
# Function that transcribes audio using OpenAI's API


def transcribeAudio(audio):
    global model_id
    media_file_path = audio
    media_file = open(media_file_path, "rb")

    response = openai.Audio.transcribe(
        model="whisper-1",
        file=media_file,
        response_format="json"
    )

    prompt = response["text"]
    return prompt


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/record", methods=["POST"])
def record_voice():
    audio_data = request.files["audio_data"]
    audio_data.save("voice_recording.webm")

    # Convert webm to wav
    webm_audio = AudioSegment.from_file("voice_recording.webm", format="webm")
    webm_audio.export("voice_recording.wav", format="wav")

    prompt = transcribeAudio("voice_recording.wav")

    response = gptPrompt(prompt)

    # Generate the AI response audio
    response_audio_base64 = tts_eleven_labs(response)

    return jsonify({"response": response, "user_prompt": prompt, "response_audio": response_audio_base64})

# ... (The rest of your existing code, such as "gptPrompt()" and "voiceRecorder()" should be here.) ...


"""GPT part of the code"""
# use transcribeAudio() to transcribe audio, then use the text as a prompt for gpt-4 to generate a text response


def gptPrompt(prompt):
    global messages

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are Donna, an AI friend for people to talk with.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
        max_tokens=4096,
    )
    gptResponse = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": gptResponse})

    return gptResponse


"""Voice Recording part of the code"""
# Parameters
duration = 10  # Record for x seconds
fs = 44100  # Sample rate (44.1 kHz)
channels = 1  # Use mono
output_filename = "voice_recording.wav"

# Function to create wav file


def write_wav(data, filename, fs):
    with open(filename, 'wb') as file:
        file.write(b'RIFF')
        file.write((36 + len(data)).to_bytes(4, 'little'))
        file.write(b'WAVEfmt ')
        file.write((16).to_bytes(4, 'little'))
        file.write((1).to_bytes(2, 'little'))
        file.write((channels).to_bytes(2, 'little'))
        file.write((fs).to_bytes(4, 'little'))
        file.write((fs * channels * 2).to_bytes(4, 'little'))
        file.write((4).to_bytes(2, 'little'))
        file.write((16).to_bytes(2, 'little'))
        file.write(b'data')
        file.write((len(data)).to_bytes(4, 'little'))
        file.write(data)


def voiceRecorder():
    # Recording
    print("Recording started...")
    recorded_data = sd.rec(
        int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()  # Wait for the recording to finish
    print("Recording finished.")

    # Convert data to PCM format and save as WAV file
    pcm_data = (recorded_data *
                np.iinfo(np.int16).max).astype(np.int16).tobytes()
    write_wav(pcm_data, output_filename, fs)
    print(f"Voice recording saved as {output_filename}.")
    # transcribe audio file
    fileText = transcribeAudio(output_filename)
    return fileText


if __name__ == "__main__":
    app.run(debug=True)
