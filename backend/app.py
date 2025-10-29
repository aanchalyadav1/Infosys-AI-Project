# ==========================
# app.py — AI Music Backend (Final Render Version)
# ==========================

from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, traceback
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import tensorflow as tf
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import firebase_admin
from firebase_admin import credentials, firestore

# -----------------------------
# 1️⃣ App Configuration (Fixed for Render)
# -----------------------------
load_dotenv()
app = Flask(__name__)

# ✅ CORS Fix — Allow frontend from anywhere (Render safe)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# -----------------------------
# 2️⃣ Helper Configurations
# -----------------------------
UPLOAD_FOLDER = "/tmp/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -----------------------------
# 3️⃣ Firebase Initialization
# -----------------------------
firebase_config = os.getenv("FIREBASE_CONFIG")
if firebase_config:
    try:
        firebase_json = json.loads(firebase_config)
        cred = credentials.Certificate(firebase_json)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully")
    except Exception as e:
        print("⚠️ Firebase init failed:", e)
else:
    db = None
    print("⚠️ Firebase config not found")

# -----------------------------
# 4️⃣ Spotify Setup
# -----------------------------
try:
    spotify = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
        )
    )
    print("✅ Spotify connection established")
except Exception as e:
    print("⚠️ Spotify connection failed:", e)
    spotify = None

# -----------------------------
# 5️⃣ Load ML Model (optional)
# -----------------------------
emotion_labels = ["happy", "sad", "angry", "neutral", "fear", "disgust", "surprise"]
model = None
try:
    if os.path.exists("model.h5"):
        model = tf.keras.models.load_model("model.h5")
        print("✅ Model loaded successfully")
    else:
        print("⚠️ model.h5 not found, using random emotion")
except Exception as e:
    print("⚠️ Model loading failed:", e)

# -----------------------------
# 6️⃣ Routes
# -----------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🎶 AI Music Recommendation Backend Running!"})

# ✅ Emotion Detection Route
@app.route("/detect", methods=["POST"])
def detect_emotion():
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"success": False, "error": "Empty filename"}), 400
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
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

# -----------------------------
# 7️⃣ Run App
# -----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
