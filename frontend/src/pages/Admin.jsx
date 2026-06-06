import { useState, useEffect } from 'react';
import { api } from '../api';
import { ShieldAlert, UploadCloud, FileText, Loader2, Database, Users, Building2, CheckCircle2 } from 'lucide-react';

const Admin = () => {
  const [password, setPassword] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  const [stats, setStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(false);
  
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('idle'); // idle, uploading, success, error
  const [uploadMsg, setUploadMsg] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    if (password.trim()) {
      setIsAuthenticated(true);
      fetchStats();
    }
  };

  const fetchStats = async () => {
    setLoadingStats(true);
    try {
      const data = await api.getAdminStats();
      setStats(data);
    } catch (error) {
      console.error("Failed to fetch stats", error);
    } finally {
      setLoadingStats(false);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type !== 'application/pdf') {
        setUploadStatus('error');
        setUploadMsg('Only PDF files are supported.');
        return;
      }
      setFile(selectedFile);
      setUploadStatus('idle');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    setUploadStatus('uploading');
    try {
      const result = await api.adminUpload(file, password);
      setUploadStatus('success');
      setUploadMsg(`Successfully ingested ${file.name} into ${result.chunks_added} chunks.`);
      setFile(null);
      // Refresh stats
      fetchStats();
      
      // Reset success message after 3 seconds
      setTimeout(() => setUploadStatus('idle'), 3000);
    } catch (error) {
      setUploadStatus('error');
      setUploadMsg(error.message || "Failed to upload document");
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto min-h-[calc(100vh-6rem)] flex items-center justify-center">
        <div className="card max-w-md w-full text-center py-12 animate-fade-in">
          <div className="w-16 h-16 bg-danger/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <ShieldAlert size={32} className="text-danger" />
          </div>
          <h2 className="text-2xl font-semibold mb-2">Admin Access Required</h2>
          <p className="text-text-secondary mb-8">Please enter the placement cell password to access the dashboard.</p>
          
          <form onSubmit={handleLogin} className="space-y-4">
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password..."
              className="input-field text-center"
              required
            />
            <button type="submit" className="btn btn-primary w-full">
              Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="container pt-24 pb-8 md:pt-32 max-w-5xl mx-auto">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-4xl mb-2 text-gradient inline-block">Admin Dashboard</h1>
          <p className="text-text-secondary">Manage knowledge base and view platform statistics.</p>
        </div>
        <button 
          onClick={() => { setIsAuthenticated(false); setPassword(''); }}
          className="btn btn-secondary text-sm px-4 py-2"
        >
          Logout
        </button>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="card animate-fade-in relative overflow-hidden" style={{ animationDelay: '0ms' }}>
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <Database size={64} />
          </div>
          <h3 className="text-text-secondary font-medium mb-2">Total Document Chunks</h3>
          {loadingStats ? (
            <Loader2 className="animate-spin text-accent-primary" size={24} />
          ) : (
            <p className="text-4xl font-bold text-text-primary">{stats?.total_docs || 0}</p>
          )}
        </div>
        
        <div className="card animate-fade-in relative overflow-hidden" style={{ animationDelay: '100ms' }}>
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <Building2 size={64} />
          </div>
          <h3 className="text-text-secondary font-medium mb-2">Companies Tracked</h3>
          {loadingStats ? (
            <Loader2 className="animate-spin text-accent-primary" size={24} />
          ) : (
            <p className="text-4xl font-bold text-accent-primary">{stats?.companies_count || 0}</p>
          )}
        </div>
        
        <div className="card animate-fade-in relative overflow-hidden" style={{ animationDelay: '200ms' }}>
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <Users size={64} />
          </div>
          <h3 className="text-text-secondary font-medium mb-2">Senior Experiences</h3>
          {loadingStats ? (
            <Loader2 className="animate-spin text-accent-primary" size={24} />
          ) : (
            <p className="text-4xl font-bold text-accent-secondary">{stats?.seniors_count || 0}</p>
          )}
        </div>
      </div>

      <div className="card animate-fade-in" style={{ animationDelay: '300ms' }}>
        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-bg-tertiary">
          <FileText className="text-accent-primary" size={24} />
          <h2 className="text-xl font-semibold">Upload Knowledge Document</h2>
        </div>
        
        <p className="text-text-secondary mb-6 max-w-2xl">
          Upload PDF documents such as placement policies, company eligibility criteria, or past placement statistics. The AI will chunk and embed these automatically for the RAG pipeline.
        </p>

        {uploadStatus === 'error' && (
          <div className="mb-6 p-4 bg-danger/10 border border-danger/30 rounded-lg text-danger text-sm">
            {uploadMsg}
          </div>
        )}
        
        {uploadStatus === 'success' && (
          <div className="mb-6 p-4 bg-success/10 border border-success/30 rounded-lg text-success text-sm flex items-center gap-2">
            <CheckCircle2 size={18} />
            {uploadMsg}
          </div>
        )}

        <form onSubmit={handleUpload} className="flex flex-col md:flex-row gap-4 items-start">
          <div className="flex-1 w-full relative">
            <input 
              type="file" 
              accept=".pdf"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              disabled={uploadStatus === 'uploading'}
            />
            <div className={`w-full border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
              file ? 'border-accent-primary bg-accent-primary/5' : 'border-bg-tertiary bg-bg-secondary hover:border-text-secondary'
            }`}>
              <UploadCloud size={40} className={`mx-auto mb-4 ${file ? 'text-accent-primary' : 'text-text-secondary'}`} />
              {file ? (
                <div>
                  <p className="font-medium text-text-primary mb-1">{file.name}</p>
                  <p className="text-sm text-text-secondary">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              ) : (
                <div>
                  <p className="font-medium text-text-primary mb-1">Click or drag PDF to upload</p>
                  <p className="text-sm text-text-secondary">Maximum file size: 10MB</p>
                </div>
              )}
            </div>
          </div>
          
          <button 
            type="submit" 
            disabled={!file || uploadStatus === 'uploading'}
            className="btn btn-primary h-full min-h-[140px] md:w-48 flex-col gap-3"
          >
            {uploadStatus === 'uploading' ? (
              <><Loader2 className="animate-spin" size={24} /> Ingesting...</>
            ) : (
              <>Ingest to DB</>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Admin;
