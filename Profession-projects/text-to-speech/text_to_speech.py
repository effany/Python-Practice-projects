import os
from dotenv import load_dotenv
import httpx
from pathlib import Path
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

class TextToSpeech:
    def __init__(self, input, instructions, voice):
        http_client = httpx.Client(verify=False)
        client = OpenAI(api_key=api_key, http_client=http_client)
        self.speech_file_path = Path(__file__).parent / "speech.mp3"

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=input,
            instructions=instructions,
        ) as response:
            response.stream_to_file(self.speech_file_path)

