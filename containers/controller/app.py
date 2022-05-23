#!/usr/bin/env python
from typing import List
from google.cloud.speech import (
    SpeechClient,
    RecognitionConfig,
    RecognitionAudio,
    RecognizeResponse,
)
from pymediainfo import MediaInfo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.constants import MAX_MESSAGE_LENGTH
from handler import Controller
import os
import io
import re
from DateFilter import DateFilter


SUPPORTED_SAMPLE_RATES = [8000, 12000, 16000, 24000, 48000]
RESAMPLE_RATE = 48000
UPLOAD_LIMIT = 20
MY_NERVES_LIMIT = 20
POLITE_RESPONSE = "Sorry, but no messages longer than 20 seconds"

speech_client = SpeechClient.from_service_account_file("datastore/creds.json")

handlers = Controller()


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Welcome Pentester \U0001F601\nRegister OpenAI model with /register"
    )


def register(update, context):
    """Send a message when the command /register is issued."""
    handlers.register_commands(update.message.text, update)


def voice_to_text(update, context) -> None:
    """Convert voice commands to text"""
    message = update.effective_message
    if message.voice.duration > MY_NERVES_LIMIT:
        message.reply_text(POLITE_RESPONSE, quote=True)
        return

    chat_id = update.effective_message.chat.id
    file_name = "%s_%s%s.ogg" % (
        chat_id,
        update.message.from_user.id,
        update.message.message_id,
    )
    download_and_prep(file_name, message)

    transcriptions = transcribe(file_name, update.message)

    if len(transcriptions) == 0 or transcriptions[0] == "":
        message.reply_text(
            "Transcription results are empty. Try Again", quote=True
        )
        return

    # Format incorrect ip address transcriptions
    for transcription in transcriptions:
        re_search = re.search(
            r"(\d{1,3}\s?\..*\s?\d{1,3}\s?\..*\s?\d{1,3}\s?\..*\s?\d{1,3})",
            transcription,
        )

        if re_search is not None:
            ip_index = re_search.span()
            ip_address = transcription[ip_index[0]: ip_index[1]]
            ip_address = re.sub(
                r"(.)\1+", r"\1", ip_address.strip(". ").replace(" ", ".")
            )
            transcription = (
                transcription[: ip_index[0]]
                + ip_address
                + transcription[ip_index[1]:]
            )
        message.reply_text(
            "Interpreted message: " + str(transcription), quote=True
        )
        handlers.process_input(transcription, update)


def transcribe(
    file_name: str,
    message,
    lang_code: str = "en-US",
    alternatives: List[str] = ["uk-UA"],
) -> List[str]:
    """Transcribe received voice message"""
    media_info = MediaInfo.parse(file_name)
    if len(media_info.audio_tracks) != 1 or not hasattr(
        media_info.audio_tracks[0], "sampling_rate"
    ):
        os.remove(file_name)
        raise ValueError("Failed to detect sample rate")
    actual_duration = round(media_info.audio_tracks[0].duration / 1000)

    sample_rate = media_info.audio_tracks[0].sampling_rate
    encoding = RecognitionConfig.AudioEncoding.OGG_OPUS
    if sample_rate not in SUPPORTED_SAMPLE_RATES:
        message.reply_text(
            "Your voice message has a sample rate of {} Hz which is not in "
            "the supported sample rates ({}).\n\n".format(
                sample_rate,
                ", ".join(
                    str(int(rate / 1000)) + " kHz"
                    for rate in SUPPORTED_SAMPLE_RATES
                ),
            ),
            quote=True,
        )
    config = RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate,
        enable_automatic_punctuation=True,
        language_code=lang_code,
        alternative_language_codes=alternatives,
    )

    try:
        response = regular_upload(file_name, config)
    except Exception as e:
        print(e)
        os.remove(file_name)
        return ["Failed"]
    os.remove(file_name)

    message_text = ""
    for result in response.results:
        message_text += result.alternatives[0].transcript + "\n"

    return split_long_message(message_text)


def regular_upload(
    file_name: str, config: RecognitionConfig
) -> RecognizeResponse:
    """Upload Voice message for recognition"""
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
    audio = RecognitionAudio(content=content)
    return speech_client.recognize(config=config, audio=audio)


def split_long_message(text: str) -> List[str]:
    """Split long transcriptions to max supported length"""
    length = len(text)
    if length < MAX_MESSAGE_LENGTH:
        return [text]

    results = []
    for i in range(0, length, MAX_MESSAGE_LENGTH):
        results.append(text[i:MAX_MESSAGE_LENGTH])

    return results


def download_and_prep(file_name: str, message) -> None:
    """Get voice file from telegram chat"""
    message.voice.get_file().download(file_name)


def controller(update, context):
    """Relay user message to reconPal logic."""
    handlers.process_input(update.message.text, update)


def main():
    """Start the bot."""
    updater = Updater("TOKEN_API", use_context=True)
    dp = updater.dispatcher

    voice_handler = MessageHandler(
        Filters.voice & DateFilter(), voice_to_text, run_async=True
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, controller))
    dp.add_handler(voice_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
