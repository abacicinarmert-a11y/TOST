import streamlit as st
import google.generativeai as genai

# Sayfa yapılandırması
st.set_page_config(page_title="TOST Asistan", page_icon="🤖")

st.title("🤖 TOST - Gemini Asistanı")
st.write("Google Gemini gücüyle çalışan arkadaş canlısı yapay zeka uygulamanız!")

# API anahtarını doğrudan koda yazmak yerine Streamlit'in güvenli alanından (secrets) alıyoruz
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    API_KEY = None

if not API_KEY:
    st.error("⚠️ API anahtarı bulunamadı! Lütfen Streamlit Cloud panelinden 'Secrets' bölümüne GOOGLE_API_KEY ekleyin.")
else:
    try:
        genai.configure(api_key=API_KEY)
        
        # Gemini modelini ayarlama (güncel model sürümü)
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