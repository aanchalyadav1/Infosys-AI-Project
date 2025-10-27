import React, {useState} from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';
import { useNavigate, Link } from 'react-router-dom';

export default function Login(){
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [err,setErr] = useState('');
  const nav = useNavigate();

  const handle = async (e) => {
    e.preventDefault();
    try{
      await signInWithEmailAndPassword(auth, email, password);
      nav('/dashboard');
    }catch(error){
      setErr(error.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center app-bg">
      <div className="w-full max-w-md p-8 round-card">
        <h1 className="text-3xl font-bold mb-4">Welcome back</h1>
        <p className="text-sm text-gray-300 mb-6">Log in to continue to AI Music</p>
        <form onSubmit={handle} className="flex flex-col gap-3">
          <input required value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" className="p-3 rounded bg-[#0f1724]"/>
          <input required type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" className="p-3 rounded bg-[#0f1724]"/>
          {err && <div className="text-red-400 text-sm">{err}</div>}
          <button type="submit" className="big-btn mt-2">Login</button>
        </form>
        <p className="mt-4 text-sm text-gray-300">New here? <Link to="/signup" className="text-green-400">Create an account</Link></p>
      </div>
    </div>
  );
}