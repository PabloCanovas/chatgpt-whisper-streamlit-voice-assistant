import openai
import myapikeys
from text_speech_utils import *

openai.api_key = myapikeys.OPENAI_KEY
input_audio_filename = 'input.wav'

messages = [{"role": "system", "content": "You are a helpful assistant."}]

def main():
    while True:
        record_audio_manual(input_audio_filename)
        transcription = transcribe_audio(input_audio_filename)             # if we want to speak in another language  we would use 'translate_audio' function

        messages.append({"role": "user", "content": transcription['text']})
        print(f"\n- Me: {transcription['text']}")

        bot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        
        response = bot.choices[0].message.content
        print(f"- ChatGPT: {response}")
        print("\n***   Press enter to interrupt assistant and ask a new question   ***\n")
        say(response)


if __name__ == '__main__':
    main()

