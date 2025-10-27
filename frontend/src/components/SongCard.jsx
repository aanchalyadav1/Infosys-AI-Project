import React from 'react';
export default function SongCard({ track, index, onPlay }){
  return (
    <div className="round-card p-3">
      <img src={track.album || track.image || ''} alt={track.name} className="w-full h-36 object-cover rounded" />
      <h3 className="mt-2 font-semibold">{track.name}</h3>
      <p className="text-sm text-gray-300">{track.artist}</p>
      {track.preview ? <audio controls className="w-full mt-2" src={track.preview}></audio> : <div className="text-sm text-gray-500 mt-2">No preview available</div>}
      {onPlay && <button onClick={onPlay} className="big-btn w-full mt-3">Play</button>}
    </div>
  );
}