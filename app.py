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
    ["Formal", "Dry", "Witty", "Dark", "Romantic", "Effervcescent", "Cartoonish", "Shy"]
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
                except Exception as e:
                    st.error(f"{agent['name']} encountered an error: {str(e)}")
