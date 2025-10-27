import React, {useEffect, useState} from 'react';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { auth } from '../firebase';
import EmotionPanel from './EmotionPanel';
import Recommendations from './Recommendations';
import PlayerBar from './PlayerBar';
import Sidebar from './Sidebar';
import { useNavigate } from 'react-router-dom';

export default function Dashboard(){
  const [tracks,setTracks] = useState([]);
  const [user,setUser] = useState(null);
  const nav = useNavigate();

  useEffect(()=> {
    const unsub = onAuthStateChanged(auth, (u)=>{
      if(u) setUser(u);
      else nav('/login');
    });
    return ()=> unsub();
  },[nav]);

  const handleLogout = async ()=>{ await signOut(auth); nav('/login'); };

  return (
    <div className="app-bg min-h-screen">
      <div className="max-w-7xl mx-auto grid grid-cols-12 gap-6 p-6">
        <div className="col-span-3"><Sidebar user={user} onLogout={handleLogout} /></div>
        <div className="col-span-9 space-y-6">
          <EmotionPanel onSetTracks={setTracks} />
          <Recommendations tracks={tracks} onPlayIndex={(i)=>{ /* optional */ }} />
        </div>
      </div>
      <PlayerBar tracks={tracks} />
    </div>
  );
}