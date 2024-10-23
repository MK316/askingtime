import streamlit as st
from datetime import datetime
import pytz
from gtts import gTTS
import random
import io

# Title of the app
st.title("🌍 What Time is it in Different Cities?")
st.write("Choose a city, and get the current time in the selected city along with a speech synthesis.")

# Step 1: City selection
citylist = ["Asia/Seoul", "Asia/Shanghai", "Asia/Dubai", "Australia/Sydney", "America/New_York", "Canada/Montreal", 
            "Europe/London", "Europe/Barcelona", "Africa/Cairo"]

city = st.selectbox("Choose a city", citylist)

# Step 2: Display current time in the selected city
if city:
    tz_loc = pytz.timezone(city)
    datetime_loc = datetime.now(tz_loc)
    current_time24 = datetime_loc.strftime("%H:%M")
    current_time12 = datetime_loc.strftime("%I:%M %p")

    st.write(f"**Current time in {city.split('/')[1]}:**")
    st.write(f"24-hour format: {current_time24}")
    st.write(f"12-hour format: {current_time12}")

# Step 3: Choose a language and dialect for TTS
languages = {
    "🇺🇸 English (US)": ["en", "us"],
    "🇬🇧 English (UK)": ["en", "co.uk"],
    "🇦🇺 English (Australia)": ["en", "com.au"],
    "🇨🇦 English (Canada)": ["en", "ca"],
    "🇮🇳 English (India)": ["en", "co.in"],
    "🇫🇷 French": ["fr", None],
    "🇪🇸 Spanish": ["es", None],
    "🇰🇷 Korean": ["ko", None],
    "🇨🇳 Chinese": ["zh-CN", None],
    "🇯🇵 Japanese": ["ja", None]
}

language_select = st.selectbox("Choose the language for speech", list(languages.keys()))
lang_code, tld = languages[language_select]

# Step 4: Text input and TTS generation
user_text = st.text_input("Type a sentence to say")

if st.button("Generate Speech"):
    if city and user_text:
        # Replace _ with space in the text
        txtnew = user_text.replace("_", " ")
        city_name = city.split('/')[1]
        mytext = f"{txtnew}... What time is it in {city_name} now?"

        # Generate TTS
        if tld:  # If there is a TLD for the language (e.g., UK English)
            tts = gTTS(text=mytext, lang=lang_code, tld=tld, slow=False)
        else:  # If no TLD, just use the language code
            tts = gTTS(text=mytext, lang=lang_code, slow=False)

        # Save to a buffer and play the audio
        audio_buffer = io.BytesIO()
        tts.save(audio_buffer, format="mp3")
        audio_buffer.seek(0)

        st.audio(audio_buffer, format="audio/mp3")
    else:
        st.warning("Please select a city and type a sentence.")
