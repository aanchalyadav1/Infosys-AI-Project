# ==========================
# app.py — AI Music Backend (Render Final v3 — CORS Fixed)
# ==========================
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import tensorflow as tf
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import firebase_admin
from firebase_admin import credentials, firestore
import os, json, traceback
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# -----------------------------
# 1️⃣ App Configuration
# -----------------------------
load_dotenv()
app = Flask(__name__)

# ✅ Fix CORS — allow both frontend + localhost
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://infosys-ai-project-1-id29.onrender.com",  # your frontend
            "https://infosys-ai-project-0.onrender.com",        # your backend (for testing)
            "http://localhost:3000"                            # local dev
        ]
    }
})

# -----------------------------
# 2️⃣ Environment Variables
# -----------------------------
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
MODEL_PATH = os.getenv("MODEL_PATH", "emotion_model.keras")
FIREBASE_CONFIG = os.getenv("FIREBASE_CONFIG")

# -----------------------------
# 3️⃣ Load Emotion Model
# -----------------------------
model = None
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Emotion model loaded successfully.")
    else:
        print(f"⚠️ Model not found at {MODEL_PATH}; using random fallback.")
except Exception as e:
    print("❌ Model load failed:", e)
    traceback.print_exc()

# -----------------------------
# 4️⃣ Firebase Initialization
# -----------------------------
db = None
try:
    if FIREBASE_CONFIG:
        firebase_json = json.loads(FIREBASE_CONFIG)
        cred = credentials.Certificate(firebase_json)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully.")
    elif os.path.exists("firebase_config.json"):
        cred = credentials.Certificate("firebase_config.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized from file.")
    else:
        print("⚠️ No Firebase config found; skipping initialization.")
except Exception as e:
    print("🔥 Firebase initialization failed:", e)
    traceback.print_exc()

# -----------------------------
# 5️⃣ Spotify Setup
# -----------------------------
sp = None
try:
    if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
            )
        )
        print("✅ Spotify client initialized.")
    else:
        print("⚠️ Spotify credentials missing.")
except Exception as e:
    print("❌ Spotify setup failed:", e)
    traceback.print_exc()

# -----------------------------
# Utils
# -----------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "bmp"}

# -----------------------------
# 6️⃣ Routes
# -----------------------------
@app.route("/")
def home():
    return jsonify({"message": "🎶 AI Music Recommendation Backend Running!"})

@app.route("/detect", methods=["GET", "POST", "OPTIONS"])
def detect_emotion():
    try:
        if request.method == "OPTIONS":
            return jsonify({"message": "Preflight OK"}), 200

        if request.method == "GET":
            return jsonify({"message": "✅ Use POST method to send an image for emotion detection."}), 200

        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"success": False, "error": "Empty filename"}), 400
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        temp_dir = "/tmp/uploads"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)

        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return jsonify({"success": False, "error": "Corrupted image"}), 400

        img = cv2.resize(img, (48, 48)) / 255.0
        img = np.expand_dims(img.reshape(48, 48, 1), axis=0).astype(np.float32)

        if model:
            preds = model.predict(img)
            emotion = emotion_labels[int(np.argmax(preds))]
        else:
            import random
            emotion = random.choice(emotion_labels)

        print(f"🎭 Emotion detected: {emotion}")
        return jsonify({"success": True, "emotion": emotion})

    except Exception as e:
        print("🔥 /detect error:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/recommend", methods=["POST"])
def recommend_music():
    try:
        data = request.get_json(force=True)
        emotion = data.get("emotion", "")
        if not emotion:
            return jsonify({"success": False, "error": "Emotion missing"}), 400

        if not sp:
            mock = [{"name": f"{emotion} Song {i+1}", "artist": "Various"} for i in range(5)]
            return jsonify({"success": True, "songs": mock})

        query = f"{emotion} mood songs"
        res = sp.search(q=query, type="track", limit=5)
        tracks = [
            {
                "name": t["name"],
                "artist": t["artists"][0]["name"],
                "url": t["external_urls"]["spotify"],
                "album": t["album"]["images"][0]["url"] if t["album"]["images"] else None,
                "preview": t.get("preview_url"),
            }
            for t in res["tracks"]["items"]
        ]
        return jsonify({"success": True, "songs": tracks})
    except Exception as e:
        print("🔥 /recommend error:", e)
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# 7️⃣ Run the App
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
