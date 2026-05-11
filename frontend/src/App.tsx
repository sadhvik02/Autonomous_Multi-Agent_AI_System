import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LayoutDashboard, 
  Search, 
  BarChart3, 
  FileText, 
  Rocket, 
  PlusCircle, 
  CheckCircle2, 
  AlertCircle,
  Loader2,
  Globe,
  Mail,
  MapPin
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedBusiness, setSelectedBusiness] = useState(null);
  
  // Form state
  const [formData, setFormData] = useState({ name: '', category: '', location: '' });

  const fetchDashboard = async () => {
    try {
      const res = await axios.get('/api/dashboard-summary');
      setBusinesses(res.data);
    } catch (err) {
      console.error("Error fetching dashboard", err);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post('/api/analyze-business', formData);
      setFormData({ name: '', category: '', location: '' });
      await fetchDashboard();
      setActiveTab('dashboard');
    } catch (err) {
      alert("Analysis failed. Make sure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const viewDetails = async (id) => {
    setLoading(true);
    try {
      const res = await axios.get(`/api/business/${id}`);
      setSelectedBusiness(res.data);
      setActiveTab('details');
    } catch (err) {
      alert("Failed to load details");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <div className="w-72 glass border-r border-white/10 p-6 flex flex-col gap-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
            <Rocket className="text-white" size={24} />
          </div>
          <h1 className="text-xl font-bold gradient-text">Antigravity AI</h1>
        </div>
        
        <nav className="flex flex-col gap-2">
          <SidebarItem 
            icon={<LayoutDashboard size={20} />} 
            label="Dashboard" 
            active={activeTab === 'dashboard'} 
            onClick={() => setActiveTab('dashboard')} 
          />
          <SidebarItem 
            icon={<PlusCircle size={20} />} 
            label="New Analysis" 
            active={activeTab === 'new'} 
            onClick={() => setActiveTab('new')} 
          />
        </nav>

        <div className="mt-auto p-4 glass bg-primary/10 rounded-xl border-primary/20">
          <p className="text-xs text-primary font-bold uppercase tracking-wider mb-2">Agent Status</p>
          <div className="flex flex-col gap-2">
            <StatusIndicator label="Discovery Agent" active />
            <StatusIndicator label="Analysis Agent" active />
            <StatusIndicator label="Strategy Agent" active />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">
        <AnimatePresence mode="wait">
          {activeTab === 'dashboard' && (
            <motion.div 
              key="dashboard"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <div className="flex justify-between items-center mb-8">
                <div>
                  <h2 className="text-3xl font-bold">Business Intelligence Dashboard</h2>
                  <p className="text-gray-400">Overview of all analyzed businesses and acquisition targets.</p>
                </div>
                <button 
                  onClick={() => setActiveTab('new')}
                  className="btn-primary flex items-center gap-2"
                >
                  <PlusCircle size={20} />
                  Run New Pipeline
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {businesses.map((biz) => (
                  <BusinessCard key={biz.id} biz={biz} onClick={() => viewDetails(biz.id)} />
                ))}
              </div>
            </motion.div>
          )}

          {activeTab === 'new' && (
            <motion.div 
              key="new"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="max-w-2xl mx-auto"
            >
              <div className="glass p-8">
                <h2 className="text-2xl font-bold mb-6">Initialize Multi-Agent Workflow</h2>
                <form onSubmit={handleAnalyze} className="space-y-6">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-400">Business Name</label>
                    <input 
                      required
                      className="w-full bg-white/5 border border-white/10 rounded-xl p-3 focus:outline-none focus:border-primary transition-colors"
                      placeholder="e.g. Sparkle Cleaners"
                      value={formData.name}
                      onChange={e => setFormData({...formData, name: e.target.value})}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-gray-400">Industry Category</label>
                      <input 
                        required
                        className="w-full bg-white/5 border border-white/10 rounded-xl p-3 focus:outline-none focus:border-primary transition-colors"
                        placeholder="e.g. Retail"
                        value={formData.category}
                        onChange={e => setFormData({...formData, category: e.target.value})}
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-gray-400">Location</label>
                      <input 
                        required
                        className="w-full bg-white/5 border border-white/10 rounded-xl p-3 focus:outline-none focus:border-primary transition-colors"
                        placeholder="e.g. New York, NY"
                        value={formData.location}
                        onChange={e => setFormData({...formData, location: e.target.value})}
                      />
                    </div>
                  </div>
                  <button 
                    disabled={loading}
                    className="w-full btn-primary flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    {loading ? <Loader2 className="animate-spin" /> : <Rocket size={20} />}
                    {loading ? "Orchestrating Agents..." : "Start Autonomous Pipeline"}
                  </button>
                </form>
              </div>
            </motion.div>
          )}

          {activeTab === 'details' && selectedBusiness && (
            <motion.div 
              key="details"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-8"
            >
              <button onClick={() => setActiveTab('dashboard')} className="text-primary hover:underline">← Back to Dashboard</button>
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left: Analysis & Profile */}
                <div className="lg:col-span-1 space-y-6">
                  <div className="glass p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-bold">{selectedBusiness.business.name}</h3>
                        <p className="text-gray-400">{selectedBusiness.business.category}</p>
                      </div>
                      <div className="bg-primary/20 text-primary px-3 py-1 rounded-full text-xs font-bold">
                        SCORE: {selectedBusiness.analysis.score}
                      </div>
                    </div>
                    <div className="space-y-3 text-sm text-gray-300">
                      <div className="flex items-center gap-2"><Globe size={14} /> {selectedBusiness.business.website || "No Website"}</div>
                      <div className="flex items-center gap-2"><MapPin size={14} /> {selectedBusiness.business.location}</div>
                      <div className="flex items-center gap-2"><Mail size={14} /> {selectedBusiness.business.contact_info}</div>
                    </div>
                  </div>

                  <div className="glass p-6">
                    <h4 className="font-bold mb-4 flex items-center gap-2"><BarChart3 size={18} className="text-primary" /> Digital Audit</h4>
                    <div className="space-y-4">
                      <div>
                        <p className="text-xs text-green-400 font-bold uppercase mb-1">Strengths</p>
                        <p className="text-sm">{selectedBusiness.analysis.strengths}</p>
                      </div>
                      <div>
                        <p className="text-xs text-red-400 font-bold uppercase mb-1">Weaknesses</p>
                        <p className="text-sm">{selectedBusiness.analysis.weaknesses}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Right: Strategy & Proposal */}
                <div className="lg:col-span-2 space-y-6">
                  <div className="glass p-6 border-l-4 border-primary">
                    <h4 className="font-bold mb-4 flex items-center gap-2"><Rocket size={18} className="text-primary" /> Growth Strategy</h4>
                    <p className="text-lg mb-4">{selectedBusiness.strategy.recommended}</p>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-white/5 p-4 rounded-xl">
                        <p className="text-xs text-gray-400 uppercase mb-1">Actions</p>
                        <p className="text-sm">{selectedBusiness.strategy.actions}</p>
                      </div>
                      <div className="bg-white/5 p-4 rounded-xl">
                        <p className="text-xs text-gray-400 uppercase mb-1">Impact</p>
                        <p className="text-sm">{selectedBusiness.strategy.impact}</p>
                      </div>
                    </div>
                  </div>

                  <div className="glass p-8 bg-gradient-to-br from-white/5 to-primary/5">
                    <h4 className="font-bold mb-6 flex items-center gap-2"><FileText size={18} className="text-primary" /> Generated Proposal</h4>
                    <div className="prose prose-invert max-w-none mb-8">
                      <pre className="whitespace-pre-wrap font-sans text-gray-300 bg-black/20 p-6 rounded-xl border border-white/5">
                        {selectedBusiness.proposal.text}
                      </pre>
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                      <MetricCard label="Timeline" value={selectedBusiness.proposal.timeline} />
                      <MetricCard label="Cost" value={selectedBusiness.proposal.cost} />
                      <MetricCard label="Expected ROI" value={selectedBusiness.proposal.roi} />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
};

const SidebarItem = ({ icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
      active ? 'bg-primary text-white shadow-lg shadow-primary/20' : 'text-gray-400 hover:bg-white/5 hover:text-white'
    }`}
  >
    {icon}
    <span className="font-medium">{label}</span>
  </button>
);

const StatusIndicator = ({ label, active }) => (
  <div className="flex items-center justify-between text-[10px]">
    <span className="text-gray-400">{label}</span>
    <div className="flex items-center gap-1">
      <div className={`w-1.5 h-1.5 rounded-full ${active ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-gray-600'}`} />
      <span className={active ? 'text-green-500' : 'text-gray-600'}>{active ? 'ONLINE' : 'OFFLINE'}</span>
    </div>
  </div>
);

const BusinessCard = ({ biz, onClick }) => (
  <div 
    onClick={onClick}
    className="glass p-6 glass-hover cursor-pointer group"
  >
    <div className="flex justify-between items-start mb-4">
      <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center group-hover:bg-primary/20 transition-colors">
        <Globe size={24} className="text-gray-400 group-hover:text-primary transition-colors" />
      </div>
      <div className="text-right">
        <p className="text-[10px] text-gray-500 font-bold uppercase">Maturity Score</p>
        <p className={`text-xl font-bold ${biz.maturity_score > 70 ? 'text-green-400' : biz.maturity_score > 40 ? 'text-yellow-400' : 'text-red-400'}`}>
          {biz.maturity_score}
        </p>
      </div>
    </div>
    <h3 className="text-lg font-bold mb-1 truncate">{biz.name}</h3>
    <p className="text-xs text-gray-500 mb-4">{biz.category} • {biz.location}</p>
    <div className="flex items-center justify-between">
      <span className="text-[10px] bg-white/5 px-2 py-1 rounded text-gray-400 uppercase tracking-tighter">
        {biz.website ? 'Website Detected' : 'Missing Website'}
      </span>
      <span className="text-primary text-xs font-bold group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
        View Intelligence →
      </span>
    </div>
  </div>
);

const MetricCard = ({ label, value }) => (
  <div className="bg-black/20 p-4 rounded-xl border border-white/5">
    <p className="text-[10px] text-gray-500 font-bold uppercase mb-1">{label}</p>
    <p className="text-sm font-bold text-white">{value}</p>
  </div>
);

export default App;
