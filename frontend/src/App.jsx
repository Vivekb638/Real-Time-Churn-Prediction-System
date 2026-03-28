import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import IndividualMode from './pages/IndividualMode';
import EnterpriseMode from './pages/EnterpriseMode';

function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen text-white relative">
        <Navbar />
        
        <main className="flex-1 px-4 py-6 md:p-10 w-full max-w-7xl mx-auto mt-2 md:mt-8">
          <header className="mb-12 text-center lg:text-left">
            <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-3">
              Decision <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400">Intelligence</span> Engine
            </h1>
            <p className="text-gray-400 text-lg md:text-xl font-medium max-w-2xl">
              Predict customer churn, quantify revenue risk, and generate actionable retention strategies instantly.
            </p>
          </header>
          
          <Routes>
            <Route path="/" element={<Navigate to="/individual" replace />} />
            <Route path="/individual" element={<IndividualMode />} />
            <Route path="/enterprise" element={<EnterpriseMode />} />
          </Routes>
        </main>
        
        <footer className="mt-auto border-t border-white/10 bg-black/20 backdrop-blur-md py-6 z-20">
          <div className="max-w-7xl mx-auto px-6 md:px-10 flex justify-center items-center text-gray-400 text-sm">
            <p>© {new Date().getFullYear()} <span className="text-white font-semibold">ChurnAI Intelligence</span>. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
