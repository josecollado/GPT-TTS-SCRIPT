import openai
from dotenv import load_dotenv
import os
from pathlib import Path
import re
from elevenlabs import set_api_key, save, generate

# Load environment variables from .env file for API keys
load_dotenv()
set_api_key(os.getenv('ELABS_API_KEY'))

# Title for the audio file
title = 'siberian cat'
# Text to be converted to speech
text = "Insert your script or text here"

def title_declutter(title):
    """Clean and truncate the title to be used as a valid filename."""
    # Remove invalid filename characters
    clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
    # Truncate if the title is too long, reserving space for the file extension
    max_length = 255 - len(".mp3")
    return clean_title[:max_length]

def openAiModel(text, title):
    """Converts text to speech using OpenAI's text-to-speech API and saves the audio."""
    clean_title = title_declutter(title)
    try:
        # Initialize OpenAI client with API key
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        speech_file_path = Path(__file__).parent / f"{clean_title}.OAI.mp3"

        # Converting text to speech
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text
        )

        # Saving the response audio to a file
        response.stream_to_file(speech_file_path)

        print(f"======Run successful! Audio saved as {clean_title}.OAI.mp3=====")
    except Exception as err:
        print(f"An Error occurred: {err}")

def elevenLabsModel(text, title):
    """Converts text to speech using ElevenLabs API and saves the audio file."""
    clean_title = title_declutter(title)
    try:
        # Generate audio from text using ElevenLabs
        audio = generate(
            text=text,
            voice='James',
            model="eleven_monolingual_v1"
        )
        # Save the audio file
        save(audio, f"{clean_title}.EL.mp3")
        print(f"======Run successful! Audio saved as {clean_title}.EL.mp3=====")
    except Exception as err:
        print(f"An Error occurred: {err}")

def main():
    # Generate and save audio file using ElevenLabsModel and OpenAiModel
    elevenLabsModel(text, title)
    openAiModel(text, title) 

if __name__ == "__main__":
    main()
