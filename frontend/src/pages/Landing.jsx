import { Link } from 'react-router-dom';
import { Bot, Users, Database } from 'lucide-react';

const Landing = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-5rem)] pt-10 pb-20 text-center">
      <div className="animate-fade-in max-w-4xl mx-auto px-4">
        <h1 className="text-5xl md:text-7xl font-bold mb-6">
          Your Private College
          <br />
          <span className="text-gradient">Placement Assistant</span>
        </h1>
        <p className="text-xl text-text-secondary mb-10 max-w-2xl mx-auto">
          Get real, grounded answers about company visits, eligibility, and selection processes. Powered by local AI and actual placement cell data.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-20">
          <Link to="/chat" className="btn btn-primary text-lg px-8 py-4 w-full sm:w-auto">
            Start Preparing
          </Link>
          <Link to="/contribute" className="btn btn-secondary text-lg px-8 py-4 w-full sm:w-auto">
            Share Experience
          </Link>
        </div>

        <div className="grid md:grid-cols-3 gap-8 text-left">
          <div className="card">
            <Bot className="text-accent-primary mb-4" size={32} />
            <h3 className="text-xl mb-2">Smart RAG Search</h3>
            <p className="text-text-secondary">Ask complex questions about placement history and get accurate answers backed by verified data.</p>
          </div>
          <div className="card">
            <Database className="text-accent-secondary mb-4" size={32} />
            <h3 className="text-xl mb-2">100% Private</h3>
            <p className="text-text-secondary">Your data never leaves the server. Using local Qwen3 LLM to guarantee complete privacy.</p>
          </div>
          <div className="card">
            <Users className="text-success mb-4" size={32} />
            <h3 className="text-xl mb-2">Alumni Network</h3>
            <p className="text-text-secondary">Connect directly with placed seniors who have consented to share their interview experiences.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
