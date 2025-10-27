import React from 'react';

export default function Sidebar({user,onLogout}){
  return (
    <aside className="round-card p-6 sticky top-6">
      <div className="mb-6">
        <h2 className="text-xl font-bold">AI Music</h2>
        <p className="text-sm text-gray-300">Welcome{user ? `, ${user.email}` : ''}</p>
      </div>
      <nav className="flex flex-col gap-3">
        <button className="sidebar-item">Home</button>
        <button className="sidebar-item">Discover</button>
        <button className="sidebar-item">Library</button>
      </nav>
      <div className="mt-6">
        <button onClick={onLogout} className="w-full px-3 py-2 rounded bg-red-600">Logout</button>
      </div>
    </aside>
  );
}