# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "0e7f4fef0c264e569363fb4993f62b18"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)

0e7f4fef0c264e569363fb4993f62b18

gemini = AIzaSyB2rrGuPKXfyQHvATyyH67LJsyWcPTcUig