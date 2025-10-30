from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import tensorflow as tf
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import firebase_admin
from firebase_admin import credentials, firestore
import os, json, traceback, random
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile

# -----------------------------
# 1️⃣ App Initialization
# -----------------------------
load_dotenv()
app = FastAPI(title="🎵 AI Music Recommender")

FRONTEND_URL = "https://infosys-ai-project-2-b7l7.onrender.com"
BACKEND_URL = "https://infosys-ai-project-7.onrender.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, BACKEND_URL, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        print("✅ Emotion model loaded successfully")
    else:
        print("⚠️ Model not found; using fallback.")
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
        print("✅ Firebase initialized.")
except Exception as e:
    print("⚠️ Firebase initialization failed:", e)

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
        print("✅ Spotify client ready.")
except Exception as e:
    print("⚠️ Spotify setup failed:", e)

# -----------------------------
# 6️⃣ Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "🎶 AI Music Recommendation Backend (FastAPI) Running!"}


@app.post("/detect")
async def detect_emotion(image: UploadFile = File(...)):
    try:
        # Save image temporarily
        with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await image.read())
            temp_path = tmp.name

        img = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return JSONResponse(content={"success": False, "error": "Invalid image"}, status_code=400)

        img = cv2.resize(img, (48, 48)) / 255.0
        img = np.expand_dims(img.reshape(48, 48, 1), axis=0).astype(np.float32)

        if model:
            preds = model.predict(img)
            emotion = emotion_labels[int(np.argmax(preds))]
        else:
            emotion = random.choice(emotion_labels)

        print(f"🎭 Emotion detected: {emotion}")
        return {"success": True, "emotion": emotion}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/recommend")
async def recommend_music(payload: dict):
    try:
        emotion = payload.get("emotion", "")
        if not emotion:
            return JSONResponse(content={"success": False, "error": "Emotion missing"}, status_code=400)

        if not sp:
            mock = [{"name": f"{emotion} Song {i+1}", "artist": "Various"} for i in range(5)]
            return {"success": True, "songs": mock}

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
        return {"success": True, "songs": tracks}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
