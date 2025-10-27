import React from 'react';
import SongCard from './SongCard';

export default function Recommendations({ tracks, onPlayIndex }){
  if(!tracks || tracks.length===0) return <div className="text-gray-400">No recommendations yet</div>;
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Recommended for you</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {tracks.map((t,i)=> <SongCard key={i} track={t} index={i} onPlay={()=> onPlayIndex && onPlayIndex(i)} />)}
      </div>
    </div>
  );
}