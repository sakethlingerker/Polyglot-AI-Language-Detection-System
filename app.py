# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# import pickle
# from googletrans import Translator

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load the trained model and vectorizer
# try:
#     with open("language_model.pkl", "rb") as f:
#         model, vectorizer = pickle.load(f)
#     print("✅ Model loaded successfully!")
# except Exception as e:
#     print(f"❌ Error loading model: {e}")

# # List of supported languages
# all_languages = ['English', 'Portuguese', 'French', 'Spanish', 'German', 'Danish', 
#                  'Italian', 'Turkish', 'Arabic', 'Russian']
# language_codes = {
#     "English": "en", "Portuguese": "pt", "French": "fr", "Spanish": "es",
#     "German": "de", "Danish": "da", "Italian": "it", "Turkish": "tr",
#     "Arabic": "ar", "Russian": "ru"
# }

# # Initialize Google Translator
# translator = Translator()

# @app.route("/")
# def home():
#     return render_template("/index.html")

# # Language Detection API
# @app.route("/detect", methods=["POST"])
# def detect_language():
#     try:
#         data = request.json
#         text = data.get("text", "").strip()

#         if not text:
#             return jsonify({"error": "No text provided"}), 400

#         # Convert text to numerical form
#         text_vectorized = vectorizer.transform([text])
#         detected_language = model.predict(text_vectorized)[0]

#         return jsonify({"language": detected_language})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Language Detection + Translation API
# @app.route("/detect_translate", methods=["POST"])
# def detect_and_translate():
#     try:
#         data = request.json
#         text = data.get("text", "").strip()

#         if not text:
#             return jsonify({"error": "No text provided"}), 400

#         # Detect language
#         text_vectorized = vectorizer.transform([text])
#         detected_language = model.predict(text_vectorized)[0]

#         if detected_language not in language_codes:
#             return jsonify({"error": "Translation not available for this language"}), 400

#         # Ensure sync to prevent RuntimeWarning
#         translated = app.ensure_sync(translator.translate)(text, src=language_codes[detected_language], dest="en")
#         translated_text = translated.text.strip()

#         return jsonify({
#             "detected_language": detected_language,
#             "translated_text": translated_text
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run Flask app
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
from deep_translator import GoogleTranslator

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and vectorizer
try:
    with open("language_model.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model, vectorizer = None, None  # Prevent crashes if model fails

# Supported languages
language_codes = {
    "English": "en", "Portuguese": "pt", "French": "fr", "Spanish": "es",
    "German": "de", "Danish": "da", "Italian": "it", "Turkish": "tr",
    "Arabic": "ar", "Russian": "ru"
}

# ✅ **Fix: Pre-load GoogleTranslator**
translator = GoogleTranslator(source="auto", target="en")

@app.route("/")
def home():
    return render_template("index.html")

# Language Detection API
@app.route("/detect", methods=["POST"])
def detect_language():
    if not model or not vectorizer:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.json
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Detect language
        text_vectorized = vectorizer.transform([text])
        detected_language = model.predict(text_vectorized)[0]

        return jsonify({"language": detected_language})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Language Detection + Translation API
@app.route("/detect_translate", methods=["POST"])
def detect_and_translate():
    if not model or not vectorizer:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.json
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Detect language
        text_vectorized = vectorizer.transform([text])
        detected_language = model.predict(text_vectorized)[0]

        # ✅ **Fix: Ensure the detected language is supported**
        if detected_language not in language_codes:
            return jsonify({"error": f"Unsupported language detected: {detected_language}"}), 400

        # ✅ **Fix: Translate using deep-translator**
        translated_text = translator.translate(text, source=language_codes[detected_language], target="en")

        return jsonify({
            "detected_language": detected_language,
            "translated_text": translated_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
