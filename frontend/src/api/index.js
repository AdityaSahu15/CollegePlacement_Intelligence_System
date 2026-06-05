// Basic fetch wrapper for API calls
const API_BASE_URL = 'http://localhost:8000/api'; // Update to backend URL if different

export const api = {
  chat: async (question, college = null) => {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, college })
    });
    if (!response.ok) throw new Error('Failed to get answer');
    return response.json();
  },
  
  getCompanies: async () => {
    const response = await fetch(`${API_BASE_URL}/companies/`);
    if (!response.ok) throw new Error('Failed to fetch companies');
    return response.json();
  },
  
  getCompanyDetails: async (name) => {
    const response = await fetch(`${API_BASE_URL}/companies/${encodeURIComponent(name)}`);
    if (!response.ok) throw new Error('Failed to fetch company details');
    return response.json();
  },
  
  getSeniors: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.company) params.append('company', filters.company);
    if (filters.batch) params.append('batch', filters.batch);
    if (filters.consent !== undefined) params.append('consent', filters.consent);
    
    const response = await fetch(`${API_BASE_URL}/seniors/?${params.toString()}`);
    if (!response.ok) throw new Error('Failed to fetch seniors');
    return response.json();
  },
  
  contributeExperience: async (data) => {
    const response = await fetch(`${API_BASE_URL}/seniors/contribute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
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
      body: formData
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to upload document');
    }
    return response.json();
  },
  
  getAdminStats: async () => {
    const response = await fetch(`${API_BASE_URL}/admin/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }
};
