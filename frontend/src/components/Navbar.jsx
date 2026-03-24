import React from 'react';
import { NavLink } from 'react-router-dom';
import { User, Building2, Activity, ShieldCheck, Zap } from 'lucide-react';

const Navbar = () => {
  return (
    <div className="w-full glass-nav px-8 py-5 flex items-center justify-between z-30 sticky top-0 border-b border-white/10 shadow-[0_4px_30px_rgba(0,0,0,0.5)] bg-black/40 backdrop-blur-xl">
      <div className="flex items-center gap-4">
        <div className="bg-gradient-to-br from-blue-500 to-indigo-600 p-2.5 rounded-xl shadow-[0_0_20px_rgba(59,130,246,0.6)]">
          <Activity className="w-6 h-6 text-white animate-pulse" />
        </div>
        <span className="text-2xl font-black tracking-widest bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 drop-shadow-md">
          CHURNAI
        </span>
      </div>
      
      <nav className="flex items-center gap-2 bg-black/20 p-1.5 rounded-2xl border border-white/5">
        <NavLink 
          to="/individual" 
          className={({isActive}) => `flex items-center gap-2 px-6 py-2.5 rounded-xl transition-all font-semibold ${isActive ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg' : 'hover:bg-white/10 text-gray-300'}`}
        >
          <User className="w-4 h-4" />
          <span>Individual Prediction</span>
        </NavLink>
        
        <NavLink 
          to="/enterprise" 
          className={({isActive}) => `flex items-center gap-2 px-6 py-2.5 rounded-xl transition-all font-semibold ${isActive ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg' : 'hover:bg-white/10 text-gray-300'}`}
        >
          <Building2 className="w-4 h-4" />
          <span>Enterprise Dashboard</span>
        </NavLink>
      </nav>
    </div>
  );
};

export default Navbar;
