import streamlit as st
import openai

# Web App Title
st.set_page_config(page_title="Multi-Agent AI Assistant")
st.title("🤖 Article Writer AI Assistant")

# User API key and query input
api_key = st.text_input("🔐 OpenAI API Key", type="password")
user_input = st.text_area("💬 Enter your topic:")

# Button to trigger AI agents
if st.button("🚀 Run Agents"):

    # Validate inputs
    if not api_key:
        st.warning("Please enter your OpenAI API key.")
    elif not user_input:
        st.warning("Please enter a topic.")
    else:
        client = openai.OpenAI(api_key=api_key)

        # Define agents and their unique instructions
        agents = [
            {
                "name": "Article Writer",
                "prompt": "You are a skilled article and blog writer. Write an informative, well reasoned piece suitable for a linkedin-length article on the given topic."
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
