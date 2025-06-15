import streamlit as st
import pickle
from deep_translator import GoogleTranslator

# 🚨 Must be first Streamlit command!
st.set_page_config(page_title="Polyglot AI", page_icon="🌐", layout="centered")

# Load the trained ML model and vectorizer
@st.cache_resource
def load_model():
    try:
        with open("language_model.pkl", "rb") as f:
            model, vectorizer = pickle.load(f)
        return model, vectorizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

model, vectorizer = load_model()

# Supported languages and ISO codes for translation
language_codes = {
    "English": "en", "Portuguese": "pt", "French": "fr", "Spanish": "es",
    "German": "de", "Danish": "da", "Italian": "it", "Turkish": "tr",
    "Arabic": "ar", "Russian": "ru"
}

# Streamlit App UI
st.title("🌐 Polyglot AI – Language Detection & Translation")
st.markdown("This app detects the language of your input and translates it to English.")

user_input = st.text_area("Enter text to analyze", height=150)

if st.button("🧠 Detect Language"):
    if not user_input.strip():
        st.warning("Please enter some text!")
    elif not model or not vectorizer:
        st.error("Model not loaded!")
    else:
        vectorized = vectorizer.transform([user_input])
        language = model.predict(vectorized)[0]
        st.success(f"📝 Detected Language: **{language}**")

if st.button("🌍 Detect & Translate"):
    if not user_input.strip():
        st.warning("Please enter some text!")
    elif not model or not vectorizer:
        st.error("Model not loaded!")
    else:
        vectorized = vectorizer.transform([user_input])
        language = model.predict(vectorized)[0]

        if language not in language_codes:
            st.error(f"Unsupported language detected: {language}")
        else:
            try:
                translated = GoogleTranslator(source=language_codes[language], target="en").translate(user_input)
                st.markdown(f"📝 **Detected:** {language}")
                st.markdown(f"🌍 **Translated:** {translated}")
            except Exception as e:
                st.error(f"Translation error: {e}")
