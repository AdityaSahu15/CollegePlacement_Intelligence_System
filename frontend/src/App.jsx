import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Landing from './pages/Landing';
import Chat from './pages/Chat';
import Companies from './pages/Companies';
import Seniors from './pages/Seniors';
import Contribute from './pages/Contribute';
import Admin from './pages/Admin';
import './index.css';

function App() {
  // Lifted chat state here so messages persist across navigation
  const [chatMessages, setChatMessages] = useState([]);

  return (
    <Router>
      <Navbar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/chat" element={<Chat messages={chatMessages} setMessages={setChatMessages} />} />
          <Route path="/companies" element={<Companies />} />
          <Route path="/seniors" element={<Seniors />} />
          <Route path="/contribute" element={<Contribute />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
