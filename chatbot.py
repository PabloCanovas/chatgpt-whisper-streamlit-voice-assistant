import openai
import config
from text_speech_utils import *

openai.api_key = config.OPENAI_KEY
input_audio_filename = 'audio/input.wav'
output_audio_filename = 'audio/chatgpt_response.wav'

messages = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    record_audio_manual(input_audio_filename)

    # transcription = translate_audio(input_audio_filename)            # if we want to use another language for the input message
    transcription = transcribe_audio(input_audio_filename)
    messages.append({"role": "user", "content": transcription['text']})

    bot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response = bot.choices[0].message.content
    print(f"ChatGPT: {response}")

    save_text_as_audio(response, output_audio_filename)
    play_audio(output_audio_filename)

    messages.append({"role": "assistant", "content": response})



