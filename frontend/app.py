import streamlit as st
import requests
import json
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="CV Extractor", layout="centered")

# Init session state
if "page" not in st.session_state:
    st.session_state.page = "upload"

if "cv" not in st.session_state:
    st.session_state.cv = None



# UPLOAD
def upload_page():
    st.title("📄 CV Extractor")
    st.write("Upload a PDF or DOCX CV to extract information")

    uploaded_file = st.file_uploader(
        "Upload your CV",
        type=["pdf", "docx"]
    )

    if uploaded_file:
        if st.button("🔍 Analyser le CV"):
            with st.spinner("Analyse du CV en cours..."):
                try:
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue())
                    }
                    response = requests.post(f"{BACKEND_URL}/api/v1/upload-cv", files=files)

                    if response.status_code != 200:
                        st.error("Erreur lors de l'analyse du CV")
                        return

                    st.session_state.cv = response.json()
                    st.session_state.page = "result"
                    st.rerun()

                except Exception as e:
                    st.error(f"Erreur : {e}")


# result
def result_page():
    st.title("📊 Résultat de l'extraction")

    cv = st.session_state.cv

    if not cv:
        st.warning("Aucun CV analysé")
        if st.button("⬅ Retour"):
            st.session_state.page = "upload"
            st.rerun()
        return

    # remplir les champs
    cv["first_name"] = st.text_input("Prénom", value=cv.get("first_name", ""))
    cv["last_name"] = st.text_input("Nom", value=cv.get("last_name", ""))
    cv["email"] = st.text_input("Email", value=cv.get("email", ""))
    cv["phone"] = st.text_input("Téléphone", value=cv.get("phone", ""))
    cv["degree"] = st.text_input("Diplôme", value=cv.get("degree", ""))

    st.session_state.cv = cv

    st.download_button(
        label="📥 Télécharger JSON",
        data=json.dumps(cv, ensure_ascii=False, indent=2),
        file_name="cv.json",
        mime="application/json"
    )

    if st.button("⬅ Analyser un autre CV"):
        st.session_state.page = "upload"
        st.session_state.cv = None
        st.rerun()


# ROUTER
if st.session_state.page == "upload":
    upload_page()
else:
    result_page()
