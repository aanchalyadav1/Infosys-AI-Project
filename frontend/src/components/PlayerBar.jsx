import React, {useState, useRef} from 'react';

export default function PlayerBar({ tracks }){
  const [index, setIndex] = useState(0);
  const audioRef = useRef();

  const playAt = (i)=>{
    if(!tracks || tracks.length===0) return;
    const idx = Math.max(0, Math.min(i, tracks.length-1));
    setIndex(idx);
    if(audioRef.current){
      audioRef.current.src = tracks[idx]?.preview || '';
      audioRef.current.play().catch(()=>{});
    }
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-[#07121a] p-3 border-t border-gray-800">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-4">
          {tracks && tracks[index] ? (
            <>
              <img src={tracks[index].album || tracks[index].image || ''} alt="" className="w-14 h-14 rounded" />
              <div>
                <div className="font-semibold">{tracks[index].name}</div>
                <div className="text-sm text-gray-400">{tracks[index].artist}</div>
              </div>
            </>
          ) : <div className="text-gray-400">No track loaded</div>}
        </div>

        <div className="flex items-center gap-4">
          <button onClick={()=> playAt(Math.max(0,index-1))} className="px-3 py-2 rounded bg-white/5">Prev</button>
          <button onClick={()=> playAt(index)} className="px-4 py-2 rounded bg-[#1DB954] text-black font-semibold">Play</button>
          <button onClick={()=> playAt(Math.min(tracks.length-1, index+1))} className="px-3 py-2 rounded bg-white/5">Next</button>
        </div>

        <audio ref={audioRef} />
        <div className="text-sm text-gray-400">Preview player</div>
      </div>
    </div>
  );
}