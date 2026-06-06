import { Link, useLocation } from 'react-router-dom';
import { GraduationCap, MessageSquare, FilePlus, Shield } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 right-0 h-20 bg-bg-primary/80 backdrop-blur-md border-b border-bg-tertiary z-50 flex items-center ">
      <div className="container mx-auto px-8 flex justify-between items-center w-full">
        <Link to="/" className="flex items-center gap-3 text-2xl font-bold font-heading text-text-primary">
          <GraduationCap className="text-accent-primary" size={28} />
          <span className="text-gradient">PlacementAI</span>
        </Link>
        
        <div className="hidden md:flex gap-4">
          <Link to="/chat" className={`flex items-center gap-2 font-medium transition-all duration-200 px-4 py-2 rounded-lg ${isActive('/chat') ? 'text-accent-primary bg-accent-primary/10' : 'text-text-secondary hover:text-text-primary hover:bg-white/5'}`}>
            <MessageSquare size={18} />
            <span>Chat</span>
          </Link>
          <Link to="/contribute" className={`flex items-center gap-2 font-medium transition-all duration-200 px-4 py-2 rounded-lg ${isActive('/contribute') ? 'text-accent-primary bg-accent-primary/10' : 'text-text-secondary hover:text-text-primary hover:bg-white/5'}`}>
            <FilePlus size={18} />
            <span>Contribute</span>
          </Link>
          <Link to="/admin" className={`flex items-center gap-2 font-medium transition-all duration-200 px-4 py-2 rounded-lg ${isActive('/admin') ? 'text-accent-primary bg-accent-primary/10' : 'text-text-secondary hover:text-text-primary hover:bg-white/5'}`}>
            <Shield size={18} />
            <span>Admin</span>
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
