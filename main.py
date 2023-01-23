import openai
import streamlit as st
import concurrent.futures

#set the GPT-3 api key
openai.api_key = st.secrets['pass']

st.header("Improvado chat")

call_text = st.text_area("Enter your text to process",max_chars=None)
question_text = st.text_area("Enter your question")
temp = st.slider("temperature", 0.0,1.0,0.2)

# Split the input text every 12000 characters
text_parts = [call_text[i:i+12000] for i in range(0, len(call_text), 12000)]

if (st.button("Submit")):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use the executor to submit all the requests at the same time
        future_responses = [executor.submit(openai.Completion.create,
            engine = "text-davinci-003",
            prompt = part + question_text,
            max_tokens = 500,
            temperature = temp) for part in text_parts]

        # wait for all the futures to complete
        responses = [future.result() for future in concurrent.futures.as_completed(future_responses)]
    response = "".join([r["choices"][0]["text"] for r in responses])
    # ask the same question to the final response
    final_response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = response + question_text,
        max_tokens = 500,
        temperature = temp
    )
    st.info(final_response["choices"][0]["text"])
