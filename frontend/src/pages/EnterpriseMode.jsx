import React, { useState } from 'react';
import axios from 'axios';
import { 
  Building2, UploadCloud, BarChart3, FileText, AlertTriangle, 
  Download, CheckCircle2, ChevronRight, Activity, User, DollarSign, Database
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  PieChart, Pie, Cell, Legend
} from 'recharts';

const API_URL = "http://127.0.0.1:8000";

const RISK_COLORS = {
  'High Risk': '#ef4444',
  'Medium Risk': '#f59e0b',
  'Low Risk': '#10b981'
};

const SCHEMA_DATA = [
  { order: 1, name: "customerID", type: "String" },
  { order: 2, name: "customerName", type: "String" },
  { order: 3, name: "gender", type: "Category" },
  { order: 4, name: "SeniorCitizen", type: "Integer" },
  { order: 5, name: "Partner", type: "Category" },
  { order: 6, name: "Dependents", type: "Category" },
  { order: 7, name: "tenure", type: "Integer" },
  { order: 8, name: "PhoneService", type: "Category" },
  { order: 9, name: "MultipleLines", type: "Category" },
  { order: 10, name: "InternetService", type: "Category" },
  { order: 11, name: "OnlineSecurity", type: "Category" },
  { order: 12, name: "OnlineBackup", type: "Category" },
  { order: 13, name: "DeviceProtection", type: "Category" },
  { order: 14, name: "TechSupport", type: "Category" },
  { order: 15, name: "StreamingTV", type: "Category" },
  { order: 16, name: "StreamingMovies", type: "Category" },
  { order: 17, name: "Contract", type: "Category" },
  { order: 18, name: "PaperlessBilling", type: "Category" },
  { order: 19, name: "PaymentMethod", type: "Category" },
  { order: 20, name: "MonthlyCharges", type: "Float" },
  { order: 21, name: "TotalCharges", type: "Float" }
];

const SAMPLE_CSV = `customerID,customerName,gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges
CUST_001,John Doe,Male,0,Yes,No,12,Yes,No,DSL,Yes,Yes,No,Yes,No,No,One year,Yes,Credit card,75.5,906.0`;

const EnterpriseMode = () => {
  const [activeTab, setActiveTab] = useState('company');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  
  // Results State
  const [summaryData, setSummaryData] = useState(null);
  const [sampleData, setSampleData] = useState(null);
  const [allPredictions, setAllPredictions] = useState(null);

  // Form State
  const [companyInfo, setCompanyInfo] = useState({
    name: '',
    email: '',
    location: '',
    website: ''
  });

  const handleCompanyChange = (e) => {
    setCompanyInfo({ ...companyInfo, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleBatchPredict = async () => {
    if (!file) {
      setError("Please upload a CSV or Excel file first.");
      return;
    }
    
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API_URL}/predict-batch`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setSummaryData(response.data.summary);
        setSampleData(response.data.sample_predictions);
        setAllPredictions(response.data.all_predictions);
        setActiveTab('dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    setLoading(true);
    setError(null);

    try {
      // Group customers by risk for the PDF
      const grouped = { 'High Risk': [], 'Medium Risk': [], 'Low Risk': [] };
      if (allPredictions) {
        allPredictions.forEach(p => {
          if (grouped[p.risk_segment]) {
            grouped[p.risk_segment].push(p);
          }
        });
      }

      const response = await axios.post(`${API_URL}/generate-report`, {
        company_name: companyInfo.name,
        company_email: companyInfo.email,
        company_location: companyInfo.location,
        company_website: companyInfo.website,
        summary_data: summaryData,
        customer_lists: grouped
      }, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'Churn_Decision_Intelligence_Report.pdf');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError("Failed to generate PDF. Make sure the backend endpoint is configured.");
    } finally {
      setLoading(false);
    }
  };

  const renderTabs = () => {
    const tabs = [
      { id: 'company', label: 'Company Details', icon: Building2 },
      { id: 'upload', label: 'Upload Dataset', icon: UploadCloud },
      { id: 'dashboard', label: 'Dashboard', icon: BarChart3, disabled: !summaryData },
      { id: 'report', label: 'PDF Report', icon: FileText, disabled: !summaryData }
    ];

    return (
      <div className="flex bg-white/5 p-1 rounded-xl mb-6 border border-white/10 w-fit overflow-x-auto">
        {tabs.map(tab => (
          <button 
            key={tab.id}
            onClick={() => !tab.disabled && setActiveTab(tab.id)}
            disabled={tab.disabled}
            className={`px-4 lg:px-6 py-2 rounded-lg font-medium transition-all flex items-center gap-2 whitespace-nowrap
              ${activeTab === tab.id ? 'bg-blue-600 text-white shadow-lg' : 
                tab.disabled ? 'text-gray-600 opacity-50 cursor-not-allowed' : 'text-gray-400 hover:text-white'}`}
          >
            <tab.icon className="w-4 h-4" /> {tab.label}
          </button>
        ))}
      </div>
    );
  };

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out">
      {renderTabs()}

      {error && (
        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 flex-shrink-0" />
          {error}
        </div>
      )}

      {/* COMPONENT: COMPANY DETAILS */}
      {activeTab === 'company' && (
        <div className="glass space-y-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Building2 className="text-blue-400" /> Company Information
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Company Name</label>
              <input type="text" name="name" value={companyInfo.name} onChange={handleCompanyChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white outline-none focus:border-blue-500 transition-colors" placeholder="Acme Corp" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Company Email</label>
              <input type="email" name="email" value={companyInfo.email} onChange={handleCompanyChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white outline-none focus:border-blue-500 transition-colors" placeholder="contact@acme.com" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Location</label>
              <input type="text" name="location" value={companyInfo.location} onChange={handleCompanyChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white outline-none focus:border-blue-500 transition-colors" placeholder="New York, NY" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Website</label>
              <input type="text" name="website" value={companyInfo.website} onChange={handleCompanyChange} className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white outline-none focus:border-blue-500 transition-colors" placeholder="https://acme.com" />
            </div>
          </div>
          <div className="mt-4 p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl flex items-center gap-3 text-sm text-blue-200">
            <AlertTriangle className="w-4 h-4 text-blue-400" />
            This information will be included in the executive PDF report.
          </div>
          <div className="flex justify-end mt-4">
            <button onClick={() => setActiveTab('upload')} className="px-6 py-2 bg-white/10 hover:bg-white/20 rounded-lg font-medium transition-colors flex items-center gap-2">
              Next Step <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* COMPONENT: UPLOAD */}
      {activeTab === 'upload' && (
        <div className="glass">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <UploadCloud className="text-blue-400" /> Upload Customer Dataset
          </h2>
          
          <div className="mb-6 p-4 bg-gray-900/50 rounded-xl border border-white/5 text-sm">
            <p className="font-semibold mb-2">📌 Important Requirements:</p>
            <ul className="list-disc list-inside text-gray-400 space-y-1 mb-4">
              <li>Must be CSV or Excel format.</li>
              <li>Columns must match the required schema exactly in order and naming.</li>
            </ul>

            <div className="overflow-x-auto rounded-lg border border-white/10 mb-4 max-h-[300px]">
              <table className="w-full text-left whitespace-nowrap">
                <thead className="bg-black/60 text-gray-300 sticky top-0">
                  <tr>
                    <th className="p-2 font-semibold border-b border-white/10">Order</th>
                    <th className="p-2 font-semibold border-b border-white/10">Column Name</th>
                    <th className="p-2 font-semibold border-b border-white/10">Type</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 bg-black/20">
                  {SCHEMA_DATA.map((row) => (
                    <tr key={row.name} className="hover:bg-white/5 transition-colors">
                      <td className="p-2 text-gray-500">{row.order}</td>
                      <td className="p-2 font-mono text-blue-300">{row.name}</td>
                      <td className="p-2 text-emerald-400">{row.type}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <a 
              href={`data:text/csv;charset=utf-8,${encodeURIComponent(SAMPLE_CSV)}`} 
              download="sample_enterprise_dataset.csv"
              className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white font-medium transition-colors border border-white/10"
            >
              <Database className="w-4 h-4" /> Download Sample Dataset
            </a>
          </div>

          <div className="border-2 border-dashed border-white/20 rounded-2xl p-10 text-center transition-colors hover:border-blue-500/50 group">
            <input 
              type="file" 
              accept=".csv,.xlsx" 
              onChange={handleFileChange}
              className="hidden" 
              id="file-upload" 
            />
            <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
              <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <UploadCloud className="w-8 h-8 text-blue-400" />
              </div>
              <span className="text-lg font-medium mb-1">{file ? file.name : 'Click to upload dataset'}</span>
              <span className="text-sm text-gray-500">{file ? 'File selected' : 'CSV or XLSX allowed'}</span>
            </label>
          </div>

          <button 
            onClick={handleBatchPredict} 
            disabled={loading || !file}
            className="w-full py-4 mt-6 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl font-bold uppercase tracking-wider flex items-center justify-center gap-3 transition-all disabled:opacity-50 disabled:pointer-events-none"
          >
            {loading ? (
              <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <><Activity className="w-5 h-5" /> Run Batch Analysis</>
            )}
          </button>
        </div>
      )}

      {/* COMPONENT: DASHBOARD */}
      {activeTab === 'dashboard' && summaryData && (
        <div className="space-y-6">
          <div className="glass">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <Building2 className="text-indigo-400" /> Company Intelligence Overview
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-indigo-900/40 to-black/40 p-6 rounded-2xl border border-indigo-500/20 shadow-[0_4px_20px_rgba(79,70,229,0.15)] hover:scale-105 transition-transform duration-300">
                <div className="text-sm text-indigo-300/80 uppercase font-semibold tracking-wider mb-2">Company</div>
                <div className="text-2xl font-bold text-white">{companyInfo.name || '—'}</div>
              </div>
              <div className="bg-gradient-to-br from-blue-900/40 to-black/40 p-6 rounded-2xl border border-blue-500/20 shadow-[0_4px_20px_rgba(59,130,246,0.15)] hover:scale-105 transition-transform duration-300">
                <div className="text-sm text-blue-300/80 uppercase font-semibold tracking-wider mb-2">Location</div>
                <div className="text-2xl font-bold text-white">{companyInfo.location || '—'}</div>
              </div>
              <div className="bg-gradient-to-br from-emerald-900/40 to-black/40 p-6 rounded-2xl border border-emerald-500/20 shadow-[0_4px_20px_rgba(16,185,129,0.15)] relative overflow-hidden hover:scale-105 transition-transform duration-300">
                <div className="text-sm text-emerald-300/80 uppercase font-semibold tracking-wider mb-2">Analyzed Profiles</div>
                <div className="text-4xl font-black text-emerald-400 drop-shadow-md">{allPredictions?.length || 0}</div>
                <User className="absolute -right-4 -bottom-4 w-24 h-24 text-emerald-500/10" />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="glass border-t-4 border-t-indigo-500/50">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                <BarChart3 className="text-indigo-400" /> Customer Risk Segments
              </h3>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={summaryData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                    <XAxis dataKey="risk_segment" stroke="#888" tick={{fill: '#888'}} axisLine={false} tickLine={false} />
                    <YAxis stroke="#888" tick={{fill: '#888'}} axisLine={false} tickLine={false} />
                    <Tooltip cursor={{fill: '#ffffff10'}} contentStyle={{backgroundColor: '#111827', borderColor: '#4f46e5', color: '#fff', borderRadius: '0.5rem'}} />
                    <Bar dataKey="customers" fill="#6366f1" radius={[6, 6, 0, 0]}>
                      {summaryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={RISK_COLORS[entry.risk_segment] || '#6366f1'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="glass border-t-4 border-t-rose-500/50">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                <DollarSign className="text-rose-400" /> Predicted Revenue at Risk
              </h3>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={summaryData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                    <XAxis dataKey="risk_segment" stroke="#888" tick={{fill: '#888'}} axisLine={false} tickLine={false} />
                    <YAxis stroke="#888" tick={{fill: '#888'}} axisLine={false} tickLine={false} tickFormatter={(val) => `$${val/1000}k`} />
                    <Tooltip cursor={{fill: '#ffffff10'}} contentStyle={{backgroundColor: '#111827', borderColor: '#f43f5e', color: '#fff', borderRadius: '0.5rem'}} formatter={(value) => `$${Number(value).toLocaleString()}`} />
                    <Bar dataKey="revenue_at_risk" fill="#fb7185" radius={[6, 6, 0, 0]}>
                      {summaryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={RISK_COLORS[entry.risk_segment] || '#fb7185'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="glass lg:col-span-2 border-t-4 border-t-purple-500/50 flex flex-col md:flex-row items-center gap-8">
              <div className="flex-1 w-full">
                <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
                  <Activity className="text-purple-400" /> Portfolio Risk Distribution
                </h3>
                <p className="text-gray-400 text-sm mb-6">Proportional view of customer volume matched to segmented distress levels across the company portfolio.</p>
                <div className="h-[350px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={summaryData}
                        dataKey="customers"
                        nameKey="risk_segment"
                        cx="50%"
                        cy="50%"
                        innerRadius={80}
                        outerRadius={120}
                        paddingAngle={5}
                        stroke="none"
                      >
                        {summaryData.map((entry, index) => (
                          <Cell key={`pie-cell-${index}`} fill={RISK_COLORS[entry.risk_segment] || '#8b5cf6'} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={{backgroundColor: '#111827', borderColor: '#8b5cf6', color: '#fff', borderRadius: '0.5rem'}} />
                      <Legend verticalAlign="bottom" height={36} iconType="circle" />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>

          <div className="glass overflow-hidden pb-4">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold flex items-center gap-2">
                <User className="text-blue-400" /> High-Confidence Top Predictions
              </h3>
            </div>
            <div className="overflow-x-auto rounded-xl border border-white/10 shadow-lg">
              <table className="w-full text-left text-sm whitespace-nowrap">
                <thead className="bg-[#111827] text-gray-300">
                  <tr>
                    <th className="p-5 font-bold uppercase tracking-wider text-xs border-b border-white/10">Customer ID</th>
                    <th className="p-5 font-bold uppercase tracking-wider text-xs border-b border-white/10">Customer Name</th>
                    <th className="p-5 font-bold uppercase tracking-wider text-xs border-b border-white/10">Risk Segment</th>
                    <th className="p-5 font-bold uppercase tracking-wider text-xs border-b border-white/10">Churn Prob</th>
                    <th className="p-5 font-bold uppercase tracking-wider text-xs border-b border-white/10 text-right">Risk Rev ($)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 bg-[#1f2937]/50">
                  {sampleData && sampleData.slice(0, 15).map((row, i) => (
                    <tr key={i} className="hover:bg-blue-500/10 transition-colors group">
                      <td className="p-4 font-mono text-gray-400 group-hover:text-blue-300 transition-colors">{row.customerID}</td>
                      <td className="p-4 text-gray-200 font-medium">{row.customerName || "—"}</td>
                      <td className="p-4">
                        <span className={`px-3 py-1.5 flex items-center gap-2 w-fit rounded-full text-xs font-bold tracking-wide shadow-sm ${
                          row.risk_segment === 'High Risk' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                          row.risk_segment === 'Medium Risk' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' :
                          'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        }`}>
                          {row.risk_segment === 'High Risk' && <AlertTriangle className="w-3.5 h-3.5" />}
                          {row.risk_segment === 'Medium Risk' && <AlertTriangle className="w-3.5 h-3.5" />}
                          {row.risk_segment === 'Low Risk' && <CheckCircle2 className="w-3.5 h-3.5" />}
                          {row.risk_segment}
                        </span>
                      </td>
                      <td className="p-4 font-mono text-gray-300">
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-2 bg-gray-700 rounded-full overflow-hidden">
                            <div 
                              className={`h-full ${row.churn_probability > 0.7 ? 'bg-red-500' : row.churn_probability > 0.4 ? 'bg-orange-500' : 'bg-emerald-500'}`} 
                              style={{width: `${row.churn_probability * 100}%`}}
                            />
                          </div>
                          {(row.churn_probability * 100).toFixed(1)}%
                        </div>
                      </td>
                      <td className="p-4 font-mono text-right text-rose-400 font-bold">${row.revenue_at_risk?.toFixed(2) || '0.00'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* COMPONENT: PDF REPORT */}
      {activeTab === 'report' && (
        <div className="glass flex flex-col items-center justify-center p-12 text-center">
          <div className="w-24 h-24 bg-blue-500/10 rounded-full flex items-center justify-center mb-6">
            <FileText className="w-12 h-12 text-blue-400" />
          </div>
          <h2 className="text-2xl font-bold mb-4">Executive Intelligence Report</h2>
          <p className="text-gray-400 max-w-lg mb-8">
            Generate a comprehensive PDF report including company details, risk segmentation analysis, revenue at risk, and actionable insights for stakeholders.
          </p>
          <button 
            onClick={handleGeneratePDF}
            disabled={loading}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg rounded-xl font-bold border border-blue-500/30 w-full max-w-sm flex items-center justify-center gap-3 transition-transform hover:scale-105 active:scale-100 disabled:opacity-50 disabled:pointer-events-none"
          >
            {loading ? (
              <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <><Download className="w-5 h-5" /> Download Executive PDF</>
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default EnterpriseMode;
