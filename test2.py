import openai
import config
import sounddevice as sd
import numpy as np

openai.api_key = config.OPENAI_API_KEY


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


"""GPT part of the code"""
# use transcribeAudio() to transcribe audio, then use the text as a prompt for gpt-4 to generate a text response


def gptPrompt():
    messages = []
    while True:
        prompt = voiceRecorder()
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", "content": "You are Donna, an AI friend for people to talk with.",
                    "role": "user", "content": prompt
                }
            ],
            temperature=0.9,
            max_tokens=4096,
        )
        gptResponse = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": gptResponse})
        print("User: " + prompt[0] + "\n\n" + "Donna: " + gptResponse + "\n")


"""Voice Recording part of the code"""
# Parameters
duration = 5  # Record for x seconds
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


print(gptPrompt())
