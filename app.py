import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Cargar credenciales desde el archivo secrets.toml
cred_path = st.secrets["firebase"]
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Obtener el emoji guardado
doc_ref = db.collection("emojis").document("current_emoji")
doc = doc_ref.get()
if doc.exists:
    current_emoji = doc.to_dict().get("emoji", "😊")
else:
    current_emoji = "😊"

st.title("AYEMOOD")

emoji = st.text_input("Introduce un emoji:", value=current_emoji)

if st.button("ACTUALIZAR"):
    doc_ref.set({"emoji": emoji})

st.markdown(f"<div style='text-align: center; font-size: 100px;'>{emoji}</div>", unsafe_allow_html=True)

# Ocultar la marca de agua y el menú de Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)