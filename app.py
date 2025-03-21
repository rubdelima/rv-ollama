import streamlit as st
import lib.ollama as ol
import requests
import base64
from io import BytesIO

def image_url_to_base64(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            img = BytesIO(response.content)
            img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
            return img_base64
        else:
            print(f"Falha ao carregar a imagem. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        return None

modelos_disponiveis = ol.avaliable_models()

selected_model: str = st.selectbox(label="Selecione um modelo", options=modelos_disponiveis)

image_url = st.text_input("Cole o link da imagem")
image_name = image_url.split("/")[-1] 
st.text(f"Nome do arquivo: {image_name}")

if image_url:
    image = image_url_to_base64(image_url) 
    if image:
        st.image(image_url, use_container_width=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}

    if (selected_model, image_name) not in st.session_state.chat_history.keys():
        st.session_state.chat_history[(selected_model, image_name)] = [{'role': 'user', 'images': [image],}]

    for message in st.session_state.chat_history[(selected_model, image_name)][1:]:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(message['content'])
        else:
            with st.chat_message("assistant"):
                st.markdown(message['content'])

    if prompt := st.chat_input("Pergunte algo sobre a imagem: "):
        response, messages = ol.new_message(selected_model, prompt, st.session_state.chat_history[(selected_model, image_name)])

        st.session_state.chat_history[(selected_model, image_name)] = messages
        
        with st.chat_message("user"):
                st.markdown(prompt)
        
        response_text = ''
        with st.chat_message(name='assistant'):
            message_placeholder = st.empty()

            for chunk in response:
                response_text += chunk['message']['content']
                message_placeholder.markdown(response_text + "▌")

            message_placeholder.markdown(response_text)

        st.session_state.chat_history[(selected_model, image_name)].append({
            'role': 'assistant',
            'content': response_text
        })
