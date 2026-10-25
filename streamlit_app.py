import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="TOST Asistan", page_icon="🤖")

st.title("🤖 TOST - Gemini Asistanı")
st.write("Google Gemini gücüyle çalışan arkadaş canlısı yapay zeka uygulamanız!")

# Kullanıcıdan Gemini API anahtarı isteme
api_key = st.text_input("Google AI Studio API Anahtarınızı Girin:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Gemini modelini ve özel sistem talimatını ayarlama
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="Sen arkadaş canlısı, yardımsever ve sempatik bir asistansın."
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Geçmiş mesajları ekranda gösterme
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Kullanıcıdan girdi alma
        if prompt := st.chat_input("TOST'a bir şeyler sorun..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Gemini sohbet oturumu başlatma
                chat_history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
else:
    st.warning("🔑 Devam etmek için lütfen Google AI Studio API anahtarınızı girin.")