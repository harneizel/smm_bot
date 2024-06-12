import os
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from bot.utils.config import DG_API_KEY
from bot.texts import TEXT_28

load_dotenv()



API_KEY = os.getenv(DG_API_KEY)


def speech_convert(tg_id):
    try:
        # STEP 1 Create a Deepgram client using the API key
        AUDIO_FILE = f"{tg_id}.mp3"
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # STEP 4: Print the response
        return response.to_json(indent=4)

    except Exception as e:
        print(f"Exception: {e}")
        return TEXT_28

