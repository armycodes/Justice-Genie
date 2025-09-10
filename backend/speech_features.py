import threading
import pyttsx3
import speech_recognition as sr

# 🔹 Global pyttsx3 engine instance
engine = pyttsx3.init()

def speak_text(text):
    """Convert text to speech using pyttsx3"""
    try:
        engine.endLoop()  # Stop any previous loop if running
    except:
        pass
    
    engine.say(text)
    engine.runAndWait()

def text_to_speech_handler(data):
    """Handler function (to be called in app.py route)"""
    text = data.get('text', '')
    if not text:
        return {"error": "No text provided"}, 400
    try:
        speak_text(text)
        return {"message": "Speech playing"}, 200
    except Exception as e:
        return {"error": f"Error: {str(e)}"}, 500

def stop_speech_handler():
    """Handler to stop speech"""
    global engine
    try:
        engine.stop()
        engine.endLoop()
        engine = pyttsx3.init()
        return {"message": "Speech stopped successfully"}, 200
    except Exception as e:
        return {"error": f"Error stopping speech: {str(e)}"}, 500

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Speech recognition service unavailable."

def speech_to_text_handler():
    """Handler to convert speech to text"""
    response = {"text": ""}

    def process_speech():
        text = recognize_speech()
        response["text"] = text

    thread = threading.Thread(target=process_speech)
    thread.start()
    thread.join()
    return response, 200
