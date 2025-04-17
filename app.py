import streamlit as st
import openai

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
if st.button("🚀 Write It"):

    # Validate input
    if not user_input:
        st.warning("Please enter a topic.")
    else:
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
                    reply = response.choices[0].message.content
                    st.subheader(f"{agent['name']} says:")
                    st.write(reply)
                    # Add Read Aloud button after displaying the reply
                    if st.button("🔊 Read Aloud"):
                        import requests
                        import base64
                        # ElevenLabs API endpoint and headers
                        api_key = st.secrets["elevenlabs_api_key"]
                        voice_id = "EXAVITQu4vr4xnSDxMaL"  # Default voice, can be customized
                        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                        headers = {
                            "xi-api-key": api_key,
                            "Content-Type": "application/json"
                        }
                        data = {
                            "text": reply,
                            "voice_settings": {
                                "stability": 0.5,
                                "similarity_boost": 0.75
                            }
                        }
                        response = requests.post(url, headers=headers, json=data)
                        if response.status_code == 200:
                            audio_bytes = response.content
                            st.audio(audio_bytes, format="audio/mp3")
                        else:
                            st.error("Text-to-speech failed: " + response.text)
                except Exception as e:
                    st.error(f"{agent['name']} encountered an error: {str(e)}")
