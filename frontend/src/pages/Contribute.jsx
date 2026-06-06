import { useState } from 'react';
import { api } from '../api';
import { FileEdit, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';

const Contribute = () => {
  const [formData, setFormData] = useState({
    name: '',
    batch: '2024',
    company: '',
    role: '',
    rounds_detail: '',
    questions_asked: '',
    tech_stack: '',
    tips: '',
    linkedin_url: '',
    consent: false,
    selected: true
  });
  
  const [status, setStatus] = useState('idle'); // idle, submitting, success, error
  const [errorMsg, setErrorMsg] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('submitting');
    try {
      await api.contributeExperience(formData);
      setStatus('success');
      // Reset form
      setFormData({
        name: '', batch: '2024', company: '', role: '',
        rounds_detail: '', questions_asked: '', tech_stack: '',
        tips: '', linkedin_url: '', consent: false, selected: true
      });
    } catch (error) {
      setStatus('error');
      setErrorMsg(error.message || "Failed to submit experience");
    }
  };

  if (status === 'success') {
    return (
      <div className="container pt-24 pb-20 md:pt-32 flex justify-center">
        <div className="card max-w-lg w-full text-center py-16 animate-fade-in">
          <div className="w-20 h-20 bg-success/20 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 size={40} className="text-success" />
          </div>
          <h2 className="text-3xl mb-4 font-semibold">Thank You!</h2>
          <p className="text-text-secondary mb-8">
            Your experience has been successfully added to our knowledge base. You're helping future batches succeed!
          </p>
          <button onClick={() => setStatus('idle')} className="btn btn-primary px-8">
            Submit Another
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container pt-24 pb-8 md:pt-32 max-w-4xl mx-auto">
      <div className="mb-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-accent-primary/20 text-accent-primary rounded-full mb-4">
          <FileEdit size={32} />
        </div>
        <h1 className="text-4xl mb-4 text-gradient">Share Your Experience</h1>
        <p className="text-text-secondary max-w-2xl mx-auto">
          Help your juniors by sharing your interview experience. This information will be ingested by our AI to provide targeted guidance.
        </p>
      </div>

      <div className="card animate-fade-in">
        {status === 'error' && (
          <div className="mb-6 p-4 bg-danger/10 border border-danger/30 rounded-lg flex items-start gap-3">
            <AlertCircle className="text-danger shrink-0 mt-0.5" size={20} />
            <p className="text-danger">{errorMsg}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Full Name</label>
              <input required type="text" name="name" value={formData.name} onChange={handleChange} className="input-field" placeholder="John Doe" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Batch</label>
              <select name="batch" value={formData.batch} onChange={handleChange} className="input-field bg-[rgba(15,23,42,0.6)]">
                <option value="2025">2025</option>
                <option value="2024">2024</option>
                <option value="2023">2023</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Company</label>
              <input required type="text" name="company" value={formData.company} onChange={handleChange} className="input-field" placeholder="e.g. Amazon" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Role</label>
              <input required type="text" name="role" value={formData.role} onChange={handleChange} className="input-field" placeholder="e.g. SDE-1" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-secondary mb-2">Rounds Detail</label>
            <textarea required name="rounds_detail" value={formData.rounds_detail} onChange={handleChange} rows="3" className="input-field resize-none" placeholder="Describe the number of rounds and what each entailed..." />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-secondary mb-2">Questions Asked</label>
            <textarea required name="questions_asked" value={formData.questions_asked} onChange={handleChange} rows="3" className="input-field resize-none" placeholder="Specific DSA, System Design, or Core CS questions..." />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Tech Stack Used/Asked</label>
              <input required type="text" name="tech_stack" value={formData.tech_stack} onChange={handleChange} className="input-field" placeholder="e.g. React, Node.js, Python" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">LinkedIn URL (Optional)</label>
              <input type="url" name="linkedin_url" value={formData.linkedin_url} onChange={handleChange} className="input-field" placeholder="https://linkedin.com/in/..." />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-secondary mb-2">Advice / Tips</label>
            <textarea required name="tips" value={formData.tips} onChange={handleChange} rows="2" className="input-field resize-none" placeholder="What should juniors focus on?" />
          </div>

          <div className="bg-bg-primary/50 p-4 rounded-lg border border-bg-tertiary">
            <div className="flex items-center gap-3 mb-4">
              <input type="checkbox" id="selected" name="selected" checked={formData.selected} onChange={handleChange} className="w-5 h-5 rounded border-bg-tertiary bg-bg-secondary text-accent-primary focus:ring-accent-primary" />
              <label htmlFor="selected" className="font-medium">I was selected for this role</label>
            </div>
            <div className="flex items-start gap-3">
              <input type="checkbox" id="consent" name="consent" checked={formData.consent} onChange={handleChange} className="w-5 h-5 mt-1 rounded border-bg-tertiary bg-bg-secondary text-accent-primary focus:ring-accent-primary" />
              <label htmlFor="consent" className="text-sm text-text-secondary leading-relaxed">
                <span className="text-text-primary font-medium block mb-1">Make my profile public</span>
                By checking this, you agree to let your name and LinkedIn URL be visible in the Alumni Network page so students can contact you. (Your experience data will be used by the AI regardless).
              </label>
            </div>
          </div>

          <button type="submit" disabled={status === 'submitting'} className="btn btn-primary w-full py-4 text-lg">
            {status === 'submitting' ? (
              <><Loader2 className="animate-spin" size={20} /> Submitting to Knowledge Base...</>
            ) : (
              'Submit Experience'
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Contribute;
