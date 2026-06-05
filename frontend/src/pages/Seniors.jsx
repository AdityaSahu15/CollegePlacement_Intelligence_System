import { useState, useEffect } from 'react';
import { api } from '../api';
import { UserCircle, Search, Linkedin, Loader2, Filter, Quote } from 'lucide-react';

const Seniors = () => {
  const [seniors, setSeniors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  
  // Filters
  const [companyFilter, setCompanyFilter] = useState('');
  const [batchFilter, setBatchFilter] = useState('');

  useEffect(() => {
    fetchSeniors();
  }, [companyFilter, batchFilter]);

  const fetchSeniors = async () => {
    setLoading(true);
    try {
      const filters = {};
      if (companyFilter) filters.company = companyFilter;
      if (batchFilter) filters.batch = batchFilter;
      filters.consent = true; // Only fetch seniors who consented
      
      const data = await api.getSeniors(filters);
      setSeniors(data);
    } catch (error) {
      console.error("Failed to fetch seniors", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredSeniors = seniors.filter(s => 
    s.name?.toLowerCase().includes(search.toLowerCase()) || 
    s.company?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container py-8">
      <div className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl mb-4 text-gradient inline-block">Alumni Network</h1>
          <p className="text-text-secondary max-w-2xl">Connect with seniors who have successfully cleared the placement process and learn from their experiences.</p>
        </div>
      </div>

      <div className="bg-bg-secondary p-4 rounded-xl border border-bg-tertiary mb-8 flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" size={18} />
          <input 
            type="text" 
            placeholder="Search by name or company..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field pl-10"
          />
        </div>
        
        <div className="flex gap-4">
          <div className="relative flex-1 md:w-48">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" size={18} />
            <select 
              className="input-field pl-10 appearance-none bg-[rgba(15,23,42,0.6)] cursor-pointer"
              value={companyFilter}
              onChange={(e) => setCompanyFilter(e.target.value)}
            >
              <option value="">All Companies</option>
              <option value="Amazon">Amazon</option>
              <option value="Microsoft">Microsoft</option>
              <option value="TCS">TCS</option>
              <option value="Deloitte">Deloitte</option>
            </select>
          </div>
          
          <select 
            className="input-field w-32 appearance-none bg-[rgba(15,23,42,0.6)] cursor-pointer"
            value={batchFilter}
            onChange={(e) => setBatchFilter(e.target.value)}
          >
            <option value="">All Batches</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center">
          <Loader2 className="animate-spin text-accent-primary mb-4" size={40} />
          <p className="text-text-secondary">Loading network...</p>
        </div>
      ) : filteredSeniors.length === 0 ? (
        <div className="card text-center py-16">
          <UserCircle size={64} className="text-bg-tertiary mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No seniors found</h3>
          <p className="text-text-secondary">Try adjusting your search or filters.</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSeniors.map((senior, idx) => (
            <div key={idx} className="card flex flex-col h-full animate-fade-in" style={{ animationDelay: `${idx * 100}ms` }}>
              <div className="flex justify-between items-start mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center">
                    <span className="text-white font-semibold text-lg">
                      {senior.name ? senior.name.charAt(0) : 'U'}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg leading-tight">{senior.name || 'Unknown'}</h3>
                    <p className="text-sm text-text-secondary">Batch {senior.batch || 'N/A'}</p>
                  </div>
                </div>
                {senior.linkedin_url && (
                  <a 
                    href={senior.linkedin_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="p-2 bg-[#0a66c2]/10 text-[#0a66c2] hover:bg-[#0a66c2] hover:text-white rounded-lg transition-colors"
                  >
                    <Linkedin size={20} />
                  </a>
                )}
              </div>

              <div className="mb-6">
                <div className="inline-flex flex-wrap gap-2 mb-4">
                  <span className="tag bg-bg-primary border-bg-tertiary text-text-primary">
                    <span className="text-text-secondary mr-1">At:</span> {senior.company || 'N/A'}
                  </span>
                  <span className="tag bg-bg-primary border-bg-tertiary text-text-primary">
                    <span className="text-text-secondary mr-1">Role:</span> {senior.role || 'N/A'}
                  </span>
                </div>
              </div>

              {senior.tips && (
                <div className="mt-auto bg-bg-primary/50 p-4 rounded-lg border border-bg-tertiary relative">
                  <Quote className="absolute -top-3 -left-2 text-bg-tertiary" size={24} />
                  <p className="text-sm text-text-secondary italic leading-relaxed pt-2 pl-2">
                    "{senior.tips}"
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Seniors;
