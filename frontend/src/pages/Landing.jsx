import { Link } from 'react-router-dom';
import { Bot, Lock, Zap } from 'lucide-react';

const Landing = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-5rem)] pt-24 md:pt-32 pb-20 text-center">
      <div className="animate-fade-in max-w-4xl mx-auto px-4">
        <h1 className="text-5xl md:text-7xl font-bold mb-6">
          Your Private College
          <br />
          <span className="text-gradient">Placement Assistant</span>
        </h1>
        <p className="text-xl text-text-secondary mb-10 max-w-2xl mx-auto">
          Ask any placement-related question and get grounded, specific answers — backed by real college data, not generic internet advice.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-20">
          <Link to="/chat" className="btn btn-primary text-lg px-10 py-4 w-full sm:w-auto">
            Start Preparing →
          </Link>
        </div>

        <div className="grid md:grid-cols-3 gap-8 text-left">
          <div className="card">
            <Bot className="text-accent-primary mb-4" size={32} />
            <h3 className="text-xl mb-2">Ask Anything</h3>
            <p className="text-text-secondary">Ask about company visits, eligibility, selection rounds, packages, and past experiences — all in plain English.</p>
          </div>
          <div className="card">
            <Lock className="text-accent-secondary mb-4" size={32} />
            <h3 className="text-xl mb-2">100% Private</h3>
            <p className="text-text-secondary">Powered by a local Qwen3-8B LLM. Your college's data never leaves the server — no OpenAI, no API calls.</p>
          </div>
          <div className="card">
            <Zap className="text-yellow-400 mb-4" size={32} />
            <h3 className="text-xl mb-2">Always Up-to-date</h3>
            <p className="text-text-secondary">Admins upload new PDFs and seniors submit experiences. The knowledge base improves every placement season.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
