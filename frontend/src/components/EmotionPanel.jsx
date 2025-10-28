import React, { useRef, useState } from "react";
import axios from "axios";

export default function EmotionPanel({ onSetTracks }) {
  const fileRef = useRef(null);
  const videoRef = useRef(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [emotion, setEmotion] = useState(null);

  // 🌍 Use environment variable from Render (or fallback to a default for local)
  const backendURL =
    process.env.REACT_APP_BACKEND_URL ||
    "https://infosys-ai-project-0.onrender.com";

  console.log("🌍 Using backend URL:", backendURL);

  // 🎥 Start camera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    } catch (e) {
      alert("Camera access failed. Please allow camera permissions.");
    }
  };

  // 📸 Capture image from live video
  const capture = () => {
    const v = videoRef.current;
    const c = document.createElement("canvas");
    c.width = v.videoWidth;
    c.height = v.videoHeight;
    c.getContext("2d").drawImage(v, 0, 0);
    c.toBlob(
      (blob) => {
        const f = new File([blob], "capture.png", { type: "image/png" });
        handleFile(f);
      },
      "image/png",
      1
    );
  };

  // 📂 Handle file upload (manual upload)
  const handleFile = (file) => {
    fileRef.current = file;
    setPreview(URL.createObjectURL(file));
  };

  // 🧠 Detect emotion + Get recommendations
  const handleDetect = async () => {
    if (!fileRef.current) return alert("Upload or capture an image first.");
    setLoading(true);

    try {
      const form = new FormData();
      form.append("image", fileRef.current);

      // 🔹 Step 1 — Detect emotion
      const detectRes = await axios.post(`${backendURL}/detect`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const detectedEmotion =
        detectRes.data?.emotion || "Neutral";
      setEmotion(detectedEmotion);
      console.log("🎭 Detected Emotion:", detectedEmotion);

      // 🔹 Step 2 — Get recommendations
      const recRes = await axios.post(`${backendURL}/recommend`, {
        emotion: detectedEmotion,
      });

      const songs = recRes.data?.songs || [];
      onSetTracks(songs);
    } catch (err) {
      console.error("❌ Error during detection:", err);
      alert("Failed to detect emotion or get recommendations. Please try again.");
    }

    setLoading(false);
  };

  return (
    <div className="round-card p-8 text-white">
      <h1 className="text-2xl font-bold mb-4">Upload or Capture Your Photo</h1>

      <div className="grid md:grid-cols-2 gap-6">
        {/* 📸 Left panel: Upload or Camera */}
        <div>
          <div className="border-2 border-dashed rounded-2xl p-6 flex flex-col items-center bg-gray-900/40">
            {preview ? (
              <img
                src={preview}
                alt="preview"
                className="w-64 h-64 object-cover rounded-xl shadow-lg"
              />
            ) : (
              <div className="text-gray-400 py-24 text-center">
                Drag or upload an image
              </div>
            )}

            <input
              type="file"
              accept="image/*"
              className="mt-4"
              onChange={(e) => handleFile(e.target.files[0])}
            />
          </div>

          <div className="flex flex-wrap gap-4 mt-4">
            <button
              onClick={startCamera}
              className="px-4 py-2 rounded bg-emerald-500 hover:bg-emerald-600 transition"
            >
              Open Camera
            </button>
            <button
              onClick={capture}
              className="px-4 py-2 rounded bg-cyan-500 hover:bg-cyan-600 transition"
            >
              Capture
            </button>
            <button
              onClick={handleDetect}
              disabled={loading}
              className="px-6 py-2 rounded bg-amber-500 hover:bg-amber-600 transition"
            >
              {loading ? "Detecting..." : "Detect & Recommend"}
            </button>
          </div>

          {/* Hidden video element for camera */}
          <video ref={videoRef} style={{ display: "none" }} />
        </div>

        {/* 💬 Right panel: Detected Emotion */}
        <div className="p-4">
          <h3 className="text-xl font-semibold mb-3">Detection</h3>
          <div className="min-h-[120px] flex items-center justify-center text-gray-300">
            {emotion ? (
              <div className="text-2xl font-bold text-yellow-300 animate-pulse">
                {emotion}
              </div>
            ) : (
              "No detection yet"
            )}
          </div>

          <div className="mt-6">
            <h4 className="font-semibold mb-2">Tips</h4>
            <ul className="text-sm text-gray-300 list-disc ml-5 space-y-1">
              <li>Good lighting helps detect emotion better.</li>
              <li>Keep your face centered in the frame.</li>
              <li>Show a clear expression for best accuracy.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
