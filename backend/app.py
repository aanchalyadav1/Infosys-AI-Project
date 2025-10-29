# app.py — AI Music Backend (Render-ready, CORS fixed)
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import tensorflow as tf
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import traceback

# -----------------------------
# 1️⃣ App Configuration
# -----------------------------
load_dotenv()
app = Flask(__name__)

# Allowed origins (add any frontend/backends you use)
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://infosys-ai-project-1-id29.onrender.com")
BACKEND_HOSTNAME = os.getenv("BACKEND_HOSTNAME", "https://infosys-ai-project-0.onrender.com")
LOCALHOST = "http://localhost:3000"

ALLOWED_ORIGINS = [FRONTEND_URL, BACKEND_HOSTNAME, LOCALHOST]

# Configure Flask-CORS to allow multiple origins and credentials
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}}, supports_credentials=True)

# -----------------------------
# 2️⃣ Environment Variables
# -----------------------------
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
FIREBASE_CONFIG_JSON = os.getenv("FIREBASE_CONFIG_JSON")
MODEL_PATH = os.getenv("MODEL_PATH", "emotion_model.keras")

# -----------------------------
# 3️⃣ Load Emotion Detection Model
# -----------------------------
model = None
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Emotion detection model loaded successfully.")
    else:
        # If model not present, keep None and use random fallback for development
        print(f"⚠️ Model not found at '{MODEL_PATH}'. Running with random fallback.")
        model = None
except Exception as e:
    print("⚠️ Failed to load emotion model:", e)
    traceback.print_exc()
    model = None

# -----------------------------
# 4️⃣ Firebase Initialization (optional)
# -----------------------------
db = None
try:
    if FIREBASE_CONFIG_JSON:
        firebase_config_dict = json.loads(FIREBASE_CONFIG_JSON)
        cred = credentials.Certificate(firebase_config_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully.")
    else:
        print("⚠️ FIREBASE_CONFIG_JSON not provided; skipping Firebase init.")
except Exception as e:
    print("🔥 Firebase initialization failed:", e)
    traceback.print_exc()
    db = None

# -----------------------------
# 5️⃣ Spotify Configuration (optional)
# -----------------------------
sp = None
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
            )
        )
        print("✅ Spotify client initialized.")
    except Exception as e:
        print("⚠️ Spotify initialization failed:", e)
        traceback.print_exc()
        sp = None
else:
    print("⚠️ Spotify credentials missing — recommendations will use a fallback if necessary.")

# -----------------------------
# Utilities
# -----------------------------
def allowed_file(filename):
    allowed_ext = {"png", "jpg", "jpeg", "bmp"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_ext

# -----------------------------
# 6️⃣ Routes
# -----------------------------
@app.route("/")
def home():
    return jsonify({"message": "🎶 AI Music Recommendation Backend Running!"})

@app.route("/health")
def health():
    return "OK", 200

# Emotion detection
@app.route("/detect", methods=["POST", "OPTIONS"])
def detect_emotion():
    try:
        # OPTIONS preflight handled by Flask-CORS; return quick OK if OPTIONS
        if request.method == "OPTIONS":
            return jsonify({"message": "preflight ok"}), 200

        # Check file
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded (form field 'image' missing)"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"success": False, "error": "Empty filename"}), 400

        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Unsupported file type"}), 400

        filename = secure_filename(file.filename)
        os.makedirs("/tmp/uploads", exist_ok=True)
        temp_path = os.path.join("/tmp/uploads", filename)
        file.save(temp_path)

        # Read image in grayscale (48x48 expected by model)
        img = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return jsonify({"success": False, "error": "Invalid image format or corrupted file"}), 400

        # Preprocess
        img = cv2.resize(img, (48, 48)) / 255.0
        img = np.expand_dims(img.reshape(48, 48, 1), axis=0).astype(np.float32)

        if model is not None:
            preds = model.predict(img)
            emotion = emotion_labels[int(np.argmax(preds))]
        else:
            # fallback for development / no model deployed
            import random
            emotion = random.choice(emotion_labels)

        print(f"🎭 Detected Emotion: {emotion}")
        return jsonify({"success": True, "emotion": emotion})

    except Exception as e:
        print("🔥 Error in /detect:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# Music recommendation
@app.route("/recommend", methods=["POST"])
def recommend_music():
    try:
        data = request.get_json(force=True, silent=True) or {}
        emotion = data.get("emotion")
        language = data.get("language", "english")
        artist = data.get("artist", "")

        if not emotion:
            return jsonify({"success": False, "error": "Emotion not provided"}), 400

        # If Spotify not configured, return mocked recommendations (safe fallback)
        if sp is None:
            print("⚠️ Spotify client not configured; returning mock recommendations.")
            mock_songs = [
                {"name": f"{emotion} Song {i+1}", "artist": "Various", "preview": None, "url": None, "album": None}
                for i in range(5)
            ]
            return jsonify({"success": True, "songs": mock_songs})

        # Build query and search
        query = f"{emotion} mood {language} songs {artist}".strip()
        results = sp.search(q=query, type="track", limit=5)

        tracks = []
        for t in results.get("tracks", {}).get("items", []):
            tracks.append({
                "name": t.get("name"),
                "artist": t.get("artists", [{}])[0].get("name"),
                "preview": t.get("preview_url"),
                "url": t.get("external_urls", {}).get("spotify"),
                "album": t.get("album", {}).get("images", [{}])[0].get("url") if t.get("album", {}).get("images") else None
            })

        return jsonify({"success": True, "songs": tracks})

    except Exception as e:
        print("🔥 Error in /recommend:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# Signup (requires Firebase)
@app.route("/signup", methods=["POST"])
def signup():
    if db is None:
        return jsonify({"success": False, "error": "Firebase not configured"}), 503

    try:
        data = request.get_json(force=True)
        email = data["email"]
        password = data["password"]

        user = auth.create_user(email=email, password=password)
        db.collection("users").document(user.uid).set(
            {"email": email, "created": firestore.SERVER_TIMESTAMP}
        )

        return jsonify({"success": True, "uid": user.uid, "message": "Signup successful"})
    except Exception as e:
        print("🔥 Error in /signup:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# Forgot password (requires Firebase)
@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    if db is None:
        return jsonify({"success": False, "error": "Firebase not configured"}), 503

    try:
        data = request.get_json(force=True)
        email = data["email"]

        link = auth.generate_password_reset_link(email)
        return jsonify({"success": True, "link": link})
    except Exception as e:
        print("🔥 Error in /forgot-password:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# Run the App
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug_flag = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug_flag)
