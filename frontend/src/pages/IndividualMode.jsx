import React, { useState } from 'react';
import axios from 'axios';
import { User, Shield, CreditCard, AlertTriangle, CheckCircle2, Search, DollarSign, Activity } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || "https://real-time-churn-prediction-system.onrender.com";

const IndividualMode = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Form State
  const [formData, setFormData] = useState({
    gender: 'Male',
    SeniorCitizen: 'No',
    Partner: 'No',
    Dependents: 'No',
    tenure: 12,
    InternetService: 'Fiber optic',
    OnlineSecurity: 'No',
    TechSupport: 'No',
    StreamingTV: 'No',
    Contract: 'Month-to-month',
    MonthlyCharges: 70.0,
    PaymentMethod: 'Electronic check',
    TotalCharges: 2000.0,
    // Streamlit app hardcoded defaults:
    PhoneService: 'Yes',
    MultipleLines: 'No',
    OnlineBackup: 'No',
    DeviceProtection: 'No',
    StreamingMovies: 'No',
    PaperlessBilling: 'Yes'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      ...formData,
      SeniorCitizen: formData.SeniorCitizen === "Yes" ? 1 : 0,
      tenure: Number(formData.tenure),
      MonthlyCharges: Number(formData.MonthlyCharges),
      TotalCharges: Number(formData.TotalCharges),
    };

    try {
      const response = await axios.post(`${API_URL}/predict`, payload);
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderTabs = () => (
    <div className="flex bg-white/5 p-1 rounded-xl mb-6 border border-white/10 w-fit">
      <button 
        onClick={() => setActiveTab('profile')}
        className={`px-6 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${activeTab === 'profile' ? 'bg-blue-600 text-white shadow-lg' : 'text-gray-400 hover:text-white'}`}
      >
        <User className="w-4 h-4" /> Profile
      </button>
      <button 
        onClick={() => setActiveTab('services')}
        className={`px-6 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${activeTab === 'services' ? 'bg-blue-600 text-white shadow-lg' : 'text-gray-400 hover:text-white'}`}
      >
        <Shield className="w-4 h-4" /> Services
      </button>
      <button 
        onClick={() => setActiveTab('billing')}
        className={`px-6 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${activeTab === 'billing' ? 'bg-blue-600 text-white shadow-lg' : 'text-gray-400 hover:text-white'}`}
      >
        <CreditCard className="w-4 h-4" /> Billing
      </button>
    </div>
  );

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out">
      {renderTabs()}

      <div className="glass space-y-6">
        {activeTab === 'profile' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Gender</label>
              <select name="gender" value={formData.gender} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>Male</option>
                <option>Female</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Senior Citizen</label>
              <select name="SeniorCitizen" value={formData.SeniorCitizen} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>No</option>
                <option>Yes</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Partner</label>
              <select name="Partner" value={formData.Partner} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>No</option>
                <option>Yes</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Dependents</label>
              <select name="Dependents" value={formData.Dependents} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>No</option>
                <option>Yes</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Tenure (Months)</label>
              <input type="number" name="tenure" value={formData.tenure} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white outline-none focus:border-blue-500 transition-colors" min="0" max="72" />
            </div>
          </div>
        )}

        {activeTab === 'services' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Internet Service</label>
              <select name="InternetService" value={formData.InternetService} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>Fiber optic</option>
                <option>DSL</option>
                <option>No</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Online Security</label>
              <select name="OnlineSecurity" value={formData.OnlineSecurity} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>No</option>
                <option>Yes</option>
                <option>No internet service</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Tech Support</label>
              <select name="TechSupport" value={formData.TechSupport} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>No</option>
                <option>Yes</option>
                <option>No internet service</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Streaming TV</label>
              <select name="StreamingTV" value={formData.StreamingTV} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>No</option>
                <option>Yes</option>
                <option>No internet service</option>
              </select>
            </div>
          </div>
        )}

        {activeTab === 'billing' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Contract</label>
              <select name="Contract" value={formData.Contract} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>Month-to-month</option>
                <option>One year</option>
                <option>Two year</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Payment Method</label>
              <select name="PaymentMethod" value={formData.PaymentMethod} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white appearance-none outline-none focus:border-blue-500 transition-colors">
                <option>Electronic check</option>
                <option>Mailed check</option>
                <option>Bank transfer</option>
                <option>Credit card</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Monthly Charges ($)</label>
              <input type="number" name="MonthlyCharges" value={formData.MonthlyCharges} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white outline-none focus:border-blue-500 transition-colors" step="0.1" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Total Charges ($)</label>
              <input type="number" name="TotalCharges" value={formData.TotalCharges} onChange={handleChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white outline-none focus:border-blue-500 transition-colors" step="0.1" />
            </div>
          </div>
        )}
      </div>

      <button 
        onClick={handlePredict} 
        disabled={loading}
        className="w-full py-4 mt-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl font-bold uppercase tracking-wider flex items-center justify-center gap-3 transition-transform hover:scale-[1.01] active:scale-100 disabled:opacity-50 disabled:pointer-events-none shadow-[0_0_20px_rgba(59,130,246,0.5)]"
      >
        {loading ? (
          <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
        ) : (
          <><Search className="w-5 h-5" /> RUN INTELLIGENCE ENGINE</>
        )}
      </button>

      {error && (
        <div className="mt-8 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 flex items-center gap-3">
          <AlertTriangle className="w-5 h-5" />
          {error}
        </div>
      )}

      {result && (
        <div className="mt-8 glass animate-in fade-in zoom-in duration-500">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Activity className="text-blue-400" /> Intelligence Results
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-black/20 p-6 rounded-xl border border-white/5">
              <div className="text-sm text-gray-400 mb-1">Churn Probability</div>
              <div className="text-3xl font-black">{(result.churn_probability * 100).toFixed(1)}%</div>
            </div>
            
            <div className={`p-6 rounded-xl border flex items-center justify-between ${
              result.risk_level === 'High Risk' ? 'bg-red-500/10 border-red-500/30 text-red-400' :
              result.risk_level === 'Medium Risk' ? 'bg-orange-500/10 border-orange-500/30 text-orange-400' :
              'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
            }`}>
              <div>
                <div className="text-sm opacity-80 mb-1">Risk Level</div>
                <div className="text-2xl font-black">{result.risk_level}</div>
              </div>
              {result.risk_level === 'High Risk' ? <AlertTriangle className="w-8 h-8" /> : <CheckCircle2 className="w-8 h-8" />}
            </div>
            
            <div className="bg-black/20 p-6 rounded-xl border border-white/5">
              <div className="text-sm text-gray-400 mb-1 flex items-center gap-2">
                <DollarSign className="w-4 h-4" /> Annual Revenue Risk
              </div>
              <div className="text-3xl font-black text-rose-400">
                ${(result.churn_probability * formData.MonthlyCharges * 12).toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </div>
            </div>
          </div>
          
          <div className="bg-blue-900/20 border border-blue-500/30 p-6 rounded-xl">
            <div className="text-blue-400 font-semibold mb-2 text-sm uppercase tracking-wider">🎯 Recommended Action</div>
            <div className="text-xl">{result.recommended_action}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IndividualMode;
