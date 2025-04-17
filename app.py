import streamlit as st
import openai
import logging

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Web App Title
st.set_page_config(page_title="Multi-Agent AI Assistant")
st.title("🤖 Article Writer AI Assistant")

# User query input
user_input = st.text_area("💬 Enter your topic:")

# Style selection
style = st.selectbox(
    "Style:",
    ["Formal", "Dry", "Witty", "Dark", "Romantic", "Effervescent", "Cartoonish", "Shy", "Camp", "Brash", "Rap", "Afrikaans", "German", "Ace Ventura"]
)

# Button to trigger AI agents
logging.info("App started.")

if st.button("🚀 Write It"):

    # Validate input
    if not user_input:
        st.warning("Please enter a topic.")
    else:
        logging.info("Generating article with topic: %s and style: %s", user_input, style)
        client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

        # Define agents and their unique instructions
        agents = [
            {
                "name": "Article Writer",
                "prompt": f"You are a skilled article and blog writer. Write an informative, well reasoned piece suitable for a linkedin-length article on the given topic. Write in a {style} style."
            }
        ]

        # Loop through agents and get responses
        for agent in agents:
            with st.spinner(f"{agent['name']} is creating content..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": agent["prompt"]},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    logging.info("OpenAI API response received.")
                    reply = response.choices[0].message.content
                    logging.info("Article generated successfully.")
                    st.session_state["reply"] = reply
                    st.subheader(f"{agent['name']} says:")
                    st.write(reply)
                except Exception as e:
                    logging.error(f"{agent['name']} encountered an error: {str(e)}")
                    st.error(f"{agent['name']} encountered an error: {str(e)}")

# Always show the AI reply and Read Aloud button if a reply exists
if "reply" in st.session_state and st.session_state["reply"]:
    st.subheader("Article Writer says:")
    st.write(st.session_state["reply"])
    if st.button("🔊 Read Aloud"):
        import requests
        with st.spinner("Waiting for ElevenLabs audio..."):
            logging.info("Sending text to ElevenLabs for TTS.")
            # ElevenLabs API endpoint and headers
            api_key = st.secrets["elevenlabs_api_key"]
            voice_id = "pqHfZKP75CvOlQylNhV4"  # Bill
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": st.session_state["reply"],
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                audio_bytes = response.content
                logging.info("Audio received from ElevenLabs and played in app.")
                st.audio(audio_bytes, format="audio/mp3")
            else:
                logging.error("Text-to-speech failed: " + response.text)
                st.error("Text-to-speech failed: " + response.text)
