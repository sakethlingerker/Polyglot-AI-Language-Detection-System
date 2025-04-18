# Polyglot AI - Language Detection & Translation

A web application that uses machine learning to detect the language of input text and translate it to English.

## Features

- **Language Detection**: Identifies the language of the input text
- **Translation**: Translates detected text to English
- **Supported Languages**: English, Spanish, French, German, Italian, Portuguese, Danish, Turkish, Russian, and Arabic

## Live Demo

Visit the [GitHub Pages site](https://vishalvoweldas.github.io/Polyglot-AI---Language-Detection-and-Translation-System/) for a project overview.

## Local Setup

### Prerequisites

- Python 3.6+
- pip

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/vishalvoweldas/Polyglot-AI---Language-Detection-and-Translation-System.git
   cd Polyglot-AI---Language-Detection-and-Translation-System
   ```

2. Install required dependencies:
   ```
   pip install flask flask-cors deep-translator scikit-learn
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## How It Works

The application uses a machine learning model trained on multiple languages to classify text. Once the language is detected, it uses the deep-translator library to translate the text to English.

## Project Structure

- `app.py` - Flask web application
- `language_model.pkl` - Trained language detection model
- `templates/` - HTML templates for the web interface
- `Language_Detection.csv` - Training dataset

## Deployment

The project is deployed using GitHub Pages. The static site provides information about the project and instructions for local deployment, as the full functionality requires a Flask backend.

## License

This project is open source and available under the [MIT License](LICENSE).