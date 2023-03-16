import streamlit as st
import pandas as pd
import openai
import myapikeys
from text_speech_utils import *

openai.api_key = myapikeys.OPENAI_KEY
input_audio_filename = 'input.wav'
output_audio_filename = 'chatgpt_response.wav'
output_conversation_filename = 'ChatGPT_conversation.txt'

# Initialize app
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]

st.title("My awesome personal assistant")
sec = st.slider("Select number of seconds of recording", min_value=2, max_value=8, value=5)

# Record audio + transcribe with Whisper + get GPT3 response
if st.button('Record audio'):
    st.write("Recording...")
    record_audio(input_audio_filename, sec)

    transcription = transcribe_audio(input_audio_filename)
    st.write(f"Me: {transcription['text']}")
    st.session_state['messages'].append({"role": "user", "content": transcription['text']})

    bot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state['messages'])
    response = bot.choices[0].message.content
    st.write(f"GPT: {response}")

    save_text_as_audio(response, output_audio_filename)
    play_audio(output_audio_filename)

    st.session_state['messages'].append({"role": "assistant", "content": response})


st.download_button(label="Download conversation", 
                   data = pd.DataFrame(st.session_state['messages']).to_csv(index=False).encode('utf-8'), 
                   file_name=output_conversation_filename)
