import React, {useState} from 'react';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';
import { useNavigate, Link } from 'react-router-dom';

export default function Signup(){
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [confirm,setConfirm] = useState('');
  const [err,setErr] = useState('');
  const nav = useNavigate();

  const handle = async (e) => {
    e.preventDefault();
    if(password !== confirm){ setErr('Passwords do not match'); return; }
    try{
      await createUserWithEmailAndPassword(auth, email, password);
      nav('/dashboard');
    }catch(error){
      setErr(error.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center app-bg">
      <div className="w-full max-w-md p-8 round-card">
        <h1 className="text-3xl font-bold mb-4">Create account</h1>
        <form onSubmit={handle} className="flex flex-col gap-3">
          <input required value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" className="p-3 rounded bg-[#0f1724]"/>
          <input required type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" className="p-3 rounded bg-[#0f1724]"/>
          <input required type="password" value={confirm} onChange={e=>setConfirm(e.target.value)} placeholder="Confirm password" className="p-3 rounded bg-[#0f1724]"/>
          {err && <div className="text-red-400 text-sm">{err}</div>}
          <button type="submit" className="big-btn mt-2">Sign up</button>
        </form>
        <p className="mt-4 text-sm text-gray-300">Already have an account? <Link to="/login" className="text-green-400">Login</Link></p>
      </div>
    </div>
  );
}