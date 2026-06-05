import { useState, useEffect } from 'react';
import { api } from '../api';
import { Building2, Search, Loader2, ChevronRight, CheckCircle2 } from 'lucide-react';

const Companies = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCompany, setSelectedCompany] = useState(null);

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      const data = await api.getCompanies();
      setCompanies(data);
    } catch (error) {
      console.error("Failed to fetch companies", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredCompanies = companies.filter(c => 
    c.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-4xl mb-4 text-gradient inline-block">Company Profiles</h1>
        <p className="text-text-secondary">Explore companies that have visited the campus, their eligibility criteria, and selection rounds.</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Left Side: List */}
        <div className="w-full lg:w-1/3 flex flex-col gap-4">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-text-secondary" size={18} />
            <input 
              type="text" 
              placeholder="Search companies..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input-field pl-12"
            />
          </div>

          <div className="bg-bg-secondary border border-bg-tertiary rounded-xl overflow-hidden flex-1 min-h-[500px]">
            {loading ? (
              <div className="h-full flex items-center justify-center">
                <Loader2 className="animate-spin text-accent-primary" size={32} />
              </div>
            ) : filteredCompanies.length === 0 ? (
              <div className="h-full flex items-center justify-center text-text-secondary p-8 text-center">
                No companies found matching "{search}"
              </div>
            ) : (
              <div className="overflow-y-auto h-[500px] divide-y divide-bg-tertiary">
                {filteredCompanies.map((company, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedCompany(company)}
                    className={`w-full text-left p-4 hover:bg-bg-tertiary/50 transition-colors flex items-center justify-between ${selectedCompany?.name === company.name ? 'bg-bg-tertiary/50 border-l-4 border-accent-primary' : 'border-l-4 border-transparent'}`}
                  >
                    <div>
                      <h3 className="font-semibold text-lg">{company.name}</h3>
                      <p className="text-sm text-text-secondary">{company.visit_date}</p>
                    </div>
                    <ChevronRight size={18} className="text-text-secondary" />
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Side: Details */}
        <div className="w-full lg:w-2/3">
          {selectedCompany ? (
            <div className="card animate-fade-in h-full">
              <div className="flex items-center gap-4 mb-8 pb-6 border-b border-bg-tertiary">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center shrink-0">
                  <Building2 size={32} className="text-white" />
                </div>
                <div>
                  <h2 className="text-3xl mb-1">{selectedCompany.name}</h2>
                  <div className="flex gap-2">
                    <span className="tag">{selectedCompany.visit_date}</span>
                    <span className="tag">Offers: {selectedCompany.number_of_offers || 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div>
                  <h4 className="text-sm text-text-secondary uppercase tracking-wider mb-2 font-semibold">Eligibility</h4>
                  <div className="bg-bg-primary/50 p-4 rounded-lg border border-bg-tertiary">
                    <p className="text-2xl font-bold text-accent-primary mb-1">
                      {selectedCompany.eligibility_cgpa}+ CGPA
                    </p>
                    <p className="text-sm text-text-secondary">
                      Branches: {selectedCompany.branches_allowed || 'All Branches'}
                    </p>
                  </div>
                </div>
                
                <div>
                  <h4 className="text-sm text-text-secondary uppercase tracking-wider mb-2 font-semibold">Compensation</h4>
                  <div className="bg-bg-primary/50 p-4 rounded-lg border border-bg-tertiary">
                    <p className="text-2xl font-bold text-success mb-1">
                      {selectedCompany.package_range || 'TBD'}
                    </p>
                    <p className="text-sm text-text-secondary">Base + Bonus</p>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="text-sm text-text-secondary uppercase tracking-wider mb-4 font-semibold">Selection Process</h4>
                <div className="space-y-3">
                  {selectedCompany.rounds ? selectedCompany.rounds.split(',').map((round, idx) => (
                    <div key={idx} className="flex items-start gap-3 bg-bg-primary/30 p-4 rounded-lg border border-bg-tertiary">
                      <CheckCircle2 className="text-accent-primary shrink-0 mt-0.5" size={18} />
                      <span className="text-text-primary leading-tight">{round.trim()}</span>
                    </div>
                  )) : (
                    <p className="text-text-secondary">Round details not available.</p>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="card h-full flex flex-col items-center justify-center text-center p-12 min-h-[500px]">
              <Building2 size={64} className="text-bg-tertiary mb-6" />
              <h3 className="text-2xl font-semibold mb-2">Select a Company</h3>
              <p className="text-text-secondary max-w-md">
                Click on a company from the list to view their detailed eligibility criteria, package details, and selection process.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Companies;
