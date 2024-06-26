import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
cred_dict = {
  "type": os.environ.get("type"),
  "project_id": os.environ.get("project_id"),
  "private_key_id": os.environ.get("private_key_id"),
  "private_key": os.environ.get("private_key").replace("\\n", "\n"),
  "client_email": os.environ.get("client_email"),
  "client_id": os.environ.get("client_id"),
  "auth_uri": os.environ.get("auth_uri"),
  "token_uri": os.environ.get("token_uri"),
  "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
  "client_x509_cert_url": os.environ.get("client_x509_cert_url"),
  "universe_domain": os.environ.get("universe_domain")
}

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Fetch emoji from Firestore
def fetch_emoji():
    doc_ref = db.collection('emojis').document('current')
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('emoji', '🙂')
    else:
        return '🙂'

# Update emoji in Firestore
def update_emoji(new_emoji):
    doc_ref = db.collection('emojis').document('current')
    doc_ref.set({'emoji': new_emoji})

# Streamlit app
st.title('AYEMOOD')

# Get current emoji
current_emoji = fetch_emoji()
st.markdown(f"<div style='text-align: center; font-size: 100px;'>{current_emoji}</div>", unsafe_allow_html=True)

# Input for new emoji
emoji = st.text_input("Introduce un emoji:", value=current_emoji)
if st.button('ACTUALIZAR'):
    update_emoji(emoji)
    st.experimental_rerun()

# Ocultar el menú y la marca de agua de Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)