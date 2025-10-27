import React, {useRef, useState} from 'react';
import axios from 'axios';

export default function EmotionPanel({ onSetTracks }){
  const fileRef = useRef(null);
  const videoRef = useRef(null);
  const [preview,setPreview] = useState(null);
  const [loading,setLoading] = useState(false);
  const [emotion,setEmotion] = useState(null);

  const startCamera = async ()=>{
    try{
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    }catch(e){ alert('Camera access failed'); }
  };

  const capture = ()=>{
    const v = videoRef.current;
    const c = document.createElement('canvas');
    c.width = v.videoWidth; c.height = v.videoHeight;
    c.getContext('2d').drawImage(v,0,0);
    c.toBlob(blob => {
      const f = new File([blob], 'capture.png', { type:'image/png' });
      handleFile(f);
    }, 'image/png');
  };

  const handleFile = (file)=>{
    fileRef.current = file;
    setPreview(URL.createObjectURL(file));
  };

  const handleDetect = async ()=>{
    if(!fileRef.current) return alert('Upload or capture an image first');
    setLoading(true);
    try{
      const form = new FormData(); form.append('image', fileRef.current);
      const r = await axios.post((process.env.REACT_APP_BACKEND_URL||'https://ai-music-backend-xrzo.onrender.com') + '/detect', form);
      const em = r.data.emotion || r.data?.emotion;
      setEmotion(em);
      // call backend recommend
      const rec = await axios.post((process.env.REACT_APP_BACKEND_URL||'https://ai-music-backend-xrzo.onrender.com') + '/recommend', { emotion: em });
      const songs = rec.data.songs || rec.data?.songs || [];
      onSetTracks(songs);
    }catch(e){ console.error(e); alert('Detection or recommendation failed'); }
    setLoading(false);
  };

  return (
    <div className="round-card p-8">
      <h1 className="text-2xl font-bold mb-4">Upload or capture your photo</h1>
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <div className="border-2 border-dashed rounded-2xl p-6 flex flex-col items-center">
            { preview ? (
              <img src={preview} alt="preview" className="w-64 h-64 object-cover rounded-xl shadow-lg" />
            ) : (
              <div className="text-gray-300 py-24">Drag or upload an image</div>
            )}
            <input type="file" accept="image/*" className="mt-4" onChange={e=>handleFile(e.target.files[0])} />
          </div>

          <div className="flex gap-4 mt-4">
            <button onClick={startCamera} className="px-4 py-2 rounded bg-[#1DB954]">Open Camera</button>
            <button onClick={capture} className="px-4 py-2 rounded bg-[#06b6d4]">Capture</button>
            <button onClick={handleDetect} className="px-6 py-2 rounded bg-[#f59e0b]">{loading ? 'Detecting...' : 'Detect & Recommend'}</button>
          </div>

          <video ref={videoRef} style={{display:'none'}} />
        </div>

        <div className="p-4">
          <h3 className="text-xl font-semibold mb-3">Detection</h3>
          <div className="min-h-[120px] flex items-center justify-center text-gray-300">
            {emotion ? <div className="text-2xl font-bold text-yellow-300">{emotion}</div> : "No detection yet"}
          </div>

          <div className="mt-6">
            <h4 className="font-semibold mb-2">Tips</h4>
            <ul className="text-sm text-gray-300 list-disc ml-5">
              <li>Good lighting</li>
              <li>Face centered</li>
              <li>Clear expression</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}