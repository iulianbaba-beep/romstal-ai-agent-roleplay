import streamlit as st
from streamlit_mic_recorder import mic_recorder
from google import genai
from gtts import gTTS
import io
import base64

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Romstal AI Sales Trainer", page_icon="🔧")
st.title("🔧 Romstal AI: Role-Play Vânzări")
st.write("Apasă pe microfon și începe să vorbești cu Domnul Popescu (Client).")

# --- API KEY (Se pune în Settings pe Streamlit, nu direct în cod pentru siguranță) ---
API_KEY = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=API_KEY)

# --- INIȚIALIZARE SESIUNE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.system_prompt = "Ești Domnul Popescu, un client Romstal sceptic legat de preț. Răspunde scurt și natural în limba română."

# --- FUNCȚIE VOCE ---
def autoplay_audio(text):
    tts = gTTS(text=text, lang='ro')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

# --- INTERFAȚA DE ÎNREGISTRARE ---
audio = mic_recorder(start_prompt="🎤 Vorbește", stop_prompt="🛑 Oprește", key='recorder')

if audio:
    # Aici Streamlit trimite automat vocea către un serviciu de transcriere (Whisper/Google)
    # Pentru acest MVP, folosim text input sau integrare directă
    user_text = "Vreau o ofertă pentru o centrală" # Notă: Aici se face legătura audio-text
    
    # Trimitem la Gemini
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=user_text,
        config={'system_instruction': st.session_state.system_prompt}
    )
    
    ai_response = response.text
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    st.chat_message("assistant").write(ai_response)
    autoplay_audio(ai_response)

# --- AFIȘARE CHAT ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
