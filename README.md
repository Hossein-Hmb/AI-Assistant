# AI-Assistant

Voice-Interactive Chatbot: Features
1. Voice Transcription with OpenAI:
The application integrates with OpenAI's Whisper ASR system.
Audio inputs from users are transcribed into text in real-time, allowing the system to understand and process user queries.
2. Conversational AI with GPT-4:
After transcription, the text is used as a prompt for the GPT-4 model.
GPT-4, being one of the most advanced language models, generates human-like text responses based on the user's input.
3. Real-time Text-to-Speech Conversion:
The generated text response is then converted back to audio for a seamless user experience.
Utilizes Google Cloud Text-to-Speech service, ensuring high-quality audio output with natural intonation and clarity.
4. Wake Word Detection with Porcupine:
The system continuously listens for a specific wake word using the Porcupine library.
Upon detecting the wake word, the system becomes ready to accept voice commands or queries from the user, allowing hands-free operation.
5. Interactive Web Interface:
Provides a user-friendly web interface designed for voice interactions.
Users can initiate voice chats, listen to AI responses, and also view transcriptions on the platform.
6. Multilanguage Support:
The system can detect the language of the user input and generate responses accordingly.
Text-to-Speech conversion is tailored to the detected language, ensuring accurate pronunciation and intonation.
