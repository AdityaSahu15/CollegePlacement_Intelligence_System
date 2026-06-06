// Basic fetch wrapper for API calls
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Required to bypass ngrok browser interstitial page when using ngrok tunnel
const BASE_HEADERS = {
  'Content-Type': 'application/json',
  'ngrok-skip-browser-warning': 'true'
};

export const api = {
  chat: async (question, college = null) => {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: BASE_HEADERS,
      body: JSON.stringify({ question, college })
    });
    if (!response.ok) throw new Error('Failed to get answer');
    return response.json();
  },
  
  getCompanies: async () => {
    const response = await fetch(`${API_BASE_URL}/companies/`, { headers: BASE_HEADERS });
    if (!response.ok) throw new Error('Failed to fetch companies');
    return response.json();
  },
  
  getCompanyDetails: async (name) => {
    const response = await fetch(`${API_BASE_URL}/companies/${encodeURIComponent(name)}`, { headers: BASE_HEADERS });
    if (!response.ok) throw new Error('Failed to fetch company details');
    return response.json();
  },
  
  getSeniors: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.company) params.append('company', filters.company);
    if (filters.batch) params.append('batch', filters.batch);
    if (filters.consent !== undefined) params.append('consent', filters.consent);
    
    const response = await fetch(`${API_BASE_URL}/seniors/?${params.toString()}`, { headers: BASE_HEADERS });
    if (!response.ok) throw new Error('Failed to fetch seniors');
    return response.json();
  },
  
  contributeExperience: async (data) => {
    const response = await fetch(`${API_BASE_URL}/seniors/contribute`, {
      method: 'POST',
      headers: BASE_HEADERS,
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to submit experience');
    return response.json();
  },
  
  adminUpload: async (file, password) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('password', password);
    
    const response = await fetch(`${API_BASE_URL}/admin/upload`, {
      method: 'POST',
      headers: { 'ngrok-skip-browser-warning': 'true' },
      body: formData
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to upload document');
    }
    return response.json();
  },
  
  getAdminStats: async () => {
    const response = await fetch(`${API_BASE_URL}/admin/stats`, { headers: BASE_HEADERS });
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }
};
