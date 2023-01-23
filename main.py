import openai
import streamlit as st

#set the GPT-3 api key
openai.api_key = st.secrets['pass']

st.header("Improvado Chat")
call_text = st.text_area("Enter your text to process and your question")
temp = st.slider("temperature", 0.0,1.0,0.5)

if (st.button("Submit")):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = call_text,
        max_tokens = 500,
        temperature = temp
    )

    #print result
    res = response["choices"][0]["text"]
    st.info(res)
