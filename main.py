import streamlit as st
from tts import TTS
from assistant import call , download_file
ttos = TTS()

st.title("PsychGenGPT")
st.markdown('PsychGenGPT - Psychological Counseling | Text to voice psychotherapy generator At any time, to generate a psychotherapy session, say, "Generate psychotherapy session now.')
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "🌟 Welcome to PsychGenGPT! 🌟 \n Hello and thank you for choosing PsychGenGPT for your psychological counseling needs and to generate psychotherapy script and audio. How can I assist you today?"})


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input

if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    output = call(prompt)

    response = f'PsychGenGPT: {output["data"][0]["content"][0]["text"]["value"]}'
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    if "psychotherapy session" in prompt.lower() or "psychotherapy script" in prompt.lower():
        # if output["data"][0]["content"][0]["text"]["annotations"] == []:
        # print(output["data"][0]["content"][0]["text"]["annotations"])
        audio_output = ttos.generate_tts(output["data"][0]["content"][0]["text"]["value"])
        # st.session_state.messages.append(st.audio(audio_output))
        st.audio(audio_output)
    
    if output["data"][0]["content"][0]["text"]["annotations"] != []:
        file_id = output["data"][0]["content"][0]["text"]["annotations"][0]["file_path"]["file_id"]
        file_type = output["data"][0]["content"][0]["text"]["annotations"][0]["text"].split(".")[1]
        print(file_id)
        PDFbyte = download_file(file_id,file_type)
        # st.download_button("Download PDF",f"script.{file_type}")
        st.download_button(label="Download PDF",
                    data=PDFbyte,
                    file_name="test.pdf",
                    mime='application/octet-stream')
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})